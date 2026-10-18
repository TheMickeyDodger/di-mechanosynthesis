# FIXTURE ONLY. A probe stand-in for the engine interpreter in the route-R2 tests. It is copied into a fake prefix
# inside a test temporary directory, with a shebang line naming the test's own Python, and launched exactly as the
# engine interpreter would be (through the R2 driver, or directly as an unsandboxed control). It imports no engine and
# ignores the payload and input it is given. It attempts writes and socket operations against targets owned by the
# test, in itself and in three descendants: a child, a grandchild in the same process group and a grandchild that
# leaves the session and process group with setsid. Each role records what happened in <attempt>/payload/probe-<role>.json.
# The only network destinations are an AF_UNIX socket owned by the test and the literal address 127.0.0.1 on ports
# owned by the test; no name is resolved. Configuration is read from <prefix>/FIXTURE-PROBE.json. Nothing it writes is
# a scientific value.
import json
import os
import socket
import subprocess
import sys

MARK = "FIXTURE - probe record, not engine output, not a scientific value"
PREFIX = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANDBOX_EXEC = "/usr/bin/sandbox-exec"


def attempt_op(fn):
    try:
        fn()
        return {"ok": True}
    except OSError as exc:
        return {"ok": False, "errno": exc.errno, "error": f"{exc.__class__.__name__}: {exc.strerror}"}


def create(path, text):
    with open(path, "x") as fh:
        fh.write(text)


def append(path, text):
    with open(path, "a") as fh:
        fh.write(text)


def probe(role, attempt, cfg):
    runs = os.path.dirname(attempt)
    token = f"FIXTURE-{role}"
    writes = {
        "prefix_existing_file": lambda: append(os.path.join(PREFIX, "include", "libint2", "shell.h"), token + "\n"),
        "prefix_new_file": lambda: create(os.path.join(PREFIX, "lib", f"fixture-{role}-new.txt"), token),
        "conda_meta_new_record": lambda: create(os.path.join(PREFIX, "conda-meta", f"fixture-{role}-0.0-0.json"), "{}"),
        "attempt_bundle": lambda: create(os.path.join(attempt, "bundle", f"fixture-{role}.txt"), token),
        "attempt_root": lambda: create(os.path.join(attempt, f"fixture-{role}.txt"), token),
        "runs_root": lambda: create(os.path.join(runs, f"fixture-{role}.txt"), token),
        "repository_tree": lambda: create(os.path.join(cfg["case_root"], "docs", f"fixture-{role}.txt"), token),
        "inside_payload": lambda: create(os.path.join(attempt, "payload", f"fixture-{role}-ok.txt"), token),
        "inside_scratch": lambda: create(os.path.join(attempt, "scratch", f"fixture-{role}-ok.txt"), token),
    }

    def unix_connect():
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect(os.path.relpath(cfg["unix_socket"], os.getcwd()))  # relative: AF_UNIX path length limit
            s.sendall((token + "-unix").encode())

    def unix_bind():
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.bind(f"fixture-{role}.sock")
        os.unlink(f"fixture-{role}.sock")

    def tcp_connect():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect(("127.0.0.1", cfg["tcp_port"]))
            s.sendall((token + "-tcp").encode())

    def udp_send():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto((token + "-udp").encode(), ("127.0.0.1", cfg["udp_port"]))

    net = {"unix_connect": unix_connect, "unix_bind": unix_bind, "tcp_connect_127": tcp_connect, "udp_send_127": udp_send}
    rec = {"fixture": MARK, "role": role, "pid": os.getpid(), "pgid": os.getpgid(0), "sid": os.getsid(0),
           "cwd": os.getcwd(), "environ_names": sorted(os.environ),
           "writes": {k: attempt_op(f) for k, f in writes.items()}, "network": {k: attempt_op(f) for k, f in net.items()}}
    print(f"FIXTURE-STDOUT-{role}", flush=True)
    print(f"FIXTURE-STDERR-{role}", file=sys.stderr, flush=True)
    return rec


def save(attempt, role, rec):
    with open(os.path.join(attempt, "payload", f"probe-{role}.json"), "x") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)


def spawn(role, attempt, new_session=False):
    return subprocess.Popen([sys.executable, "-I", "-B", os.path.abspath(__file__), "--role", role, "--attempt", attempt],
                            start_new_session=new_session)


def main(argv):
    with open(os.path.join(PREFIX, "FIXTURE-PROBE.json")) as fh:
        cfg = json.load(fh)
    if "--role" in argv:
        role, attempt = argv[argv.index("--role") + 1], argv[argv.index("--attempt") + 1]
    else:
        role, attempt = "process", argv[-1]  # argv: -I -B <payload> <input> <attempt>
    rec = probe(role, attempt, cfg)
    if role == "process":
        child = spawn("child", attempt)
        rec["child_exit"] = child.wait(timeout=120)
        if cfg.get("nested"):
            res = subprocess.run([SANDBOX_EXEC, "-p", "(version 1)(allow default)", sys.executable, "-I", "-B",
                                  os.path.abspath(__file__), "--role", "nested", "--attempt", attempt],
                                 capture_output=True, text=True, timeout=120)
            rec["nested_sandbox_exec"] = {"argv_head": [SANDBOX_EXEC, "-p", "(version 1)(allow default)"],
                                          "exit": res.returncode, "stdout": res.stdout[-500:], "stderr": res.stderr[-500:]}
            save(attempt, "process_after_nested", probe("process_after_nested", attempt, cfg))
    elif role == "child":
        kids = [spawn("grandchild", attempt), spawn("setsid_grandchild", attempt, new_session=True)]
        rec["grandchild_exits"] = [k.wait(timeout=120) for k in kids]
        rec["grandchild_pids"] = [k.pid for k in kids]
    save(attempt, role, rec)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
