#!/usr/bin/env python3
"""Feeds a SQL script into sqlplus through a pseudo-TTY so SQL*Plus echoes
the entered statements (like a real interactive session)."""
import os, pty, sys, time, select

def run(sql_file, out_file, rows=40, cols=180):
    pid, fd = pty.fork()
    if pid == 0:  # child
        os.environ["TERM"] = "xterm"
        os.execvp("docker", ["docker", "exec", "-i", "oraclexe",
                             "bash", "-lc", "stty rows %d cols %d; sqlplus -L system/Oracle_123@localhost/XEPDB1" % (rows, cols)])
    buf = b""
    script = open(sql_file).read().encode()
    # feed in chunks with small delays
    chunks = [script[i:i+400] for i in range(0, len(script), 400)]
    for c in chunks:
        os.write(fd, c)
        time.sleep(0.02)
    # drain
    end = time.time() + 60
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 1.0)
        if not r:
            break
        try:
            data = os.read(fd, 65536)
        except OSError:
            break
        if not data:
            break
        buf += data
    os.close(fd)
    open(out_file, "wb").write(buf)
    print(f"[pty] {out_file}: {len(buf)} bytes")

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
