# FIXTURE ONLY. Run by test_payload.py in a subprocess, with the test's own Python and -I. It fails closed unless the
# name "psi4" resolves to the fixture stand-in inside the test's temporary directory, then runs the payload's run()
# against a fake prefix that also lives in that temporary directory.
# usage: python -I -B fixture-ordering-harness.py <fixture-root> <payload.py> <input.json> <attempt-dir> <fake-prefix>
import importlib.util
import os
import sys


def main():
    fixture_root, payload, input_path, attempt, fake_prefix = sys.argv[1:6]
    if importlib.util.find_spec("psi4") is not None:
        return 97  # a real or other psi4 is importable here: abort before anything else
    sys.path.insert(0, fixture_root)
    spec = importlib.util.find_spec("psi4")
    root = os.path.realpath(fixture_root)
    if spec is None or not spec.origin or not os.path.realpath(spec.origin).startswith(root + os.sep):
        return 98  # psi4 does not resolve to the temporary fixture: abort
    sys.prefix = fake_prefix  # FIXTURE override so the payload's P0 compares against the fake prefix
    pspec = importlib.util.spec_from_file_location("h2_phase_a_payload_under_test", payload)
    mod = importlib.util.module_from_spec(pspec)
    pspec.loader.exec_module(mod)
    return mod.run([payload, input_path, attempt])


if __name__ == "__main__":
    sys.exit(main())
