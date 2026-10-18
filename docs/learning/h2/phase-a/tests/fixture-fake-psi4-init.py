# FIXTURE ONLY - NOT PSI4. Source of a stand-in module used by one ordering test. The file name is deliberately not
# importable; the test copies it to <temporary directory>/psi4/__init__.py, puts only that temporary directory on
# sys.path inside the test subprocess, and checks that "psi4" resolves there before the payload runs. Every value is
# fixture-marked, no numerical result is imitated, and every engine call the payload must not reach before its I1
# gate raises after logging itself.
import json
import os

MARK = "FIXTURE"
_LOG = os.environ["FIXTURE_CALL_LOG"]
_MODE = os.environ["FIXTURE_PSI4_MODE"]


def _log(event):
    with open(_LOG, "a") as fh:
        fh.write(json.dumps({"event": event, "fixture": MARK}) + "\n")


_log("import")
__version__ = "FIXTURE-0.0-mismatch" if _MODE == "version_mismatch" else "FIXTURE-1.11"


class FixtureViolation(Exception):
    pass


def _forbidden(name):
    def call(*args, **kwargs):
        _log("CALLED:" + name)
        raise FixtureViolation(f"FIXTURE: {name} reached")
    return call


set_output_file = _forbidden("set_output_file")
set_num_threads = _forbidden("set_num_threads")
set_memory = _forbidden("set_memory")
set_options = _forbidden("set_options")
energy = _forbidden("energy")


class _Molecule:
    from_dict = staticmethod(_forbidden("Molecule.from_dict"))


class _BasisSet:
    build = staticmethod(_forbidden("BasisSet.build"))


class _Core:
    __file__ = "FIXTURE-core-path-not-a-file"
    Molecule = _Molecule
    BasisSet = _BasisSet

    @staticmethod
    def get_datadir():
        _log("get_datadir")
        return "FIXTURE-datadir"

    get_option = staticmethod(_forbidden("core.get_option"))
    get_global_option = staticmethod(_forbidden("core.get_global_option"))


core = _Core()
