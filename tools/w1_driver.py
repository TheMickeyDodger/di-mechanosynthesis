# MS-001 W1 driver: the launcher and runner of the provenance wiring test, specification revision 01.
#
# Evidence label: SOFTWARE WIRING TEST ONLY. W1 runs no chemistry engine and evaluates no energy, force or
# gradient. A pass would be software wiring evidence only, never chemistry evidence, readiness, parity or
# physical validation. Governing specification: docs/ms-001/C3-WIRING-TEST-PROPOSAL.md, revision 01.
#
# Operator invocation, from the repository root, by the Stage 0 environment's interpreter at its exact path:
#     <environment>/bin/python -E -s -B tools/w1_driver.py launch
# The launcher starts the runner itself as `<environment>/bin/python -E -s -B tools/w1_driver.py run`, from an
# argument vector without a shell and with exactly the launcher record as its environment. `run` is never
# started by hand. One attempt only: the launcher refuses to start when the run area already exists.
#
# There is no module docstring on purpose. The first statement is `import os` and the second makes the
# interpreter record of Section 5, before any other import. Until the capture point of Section 4 nothing
# outside the standard library is imported; `w1_job`, AiiDA, ASE and NumPy are imported only after it.
import os
_INTERPRETER_RECORD_AT_START = dict(os.environ)

import ast  # noqa: E402
import base64  # noqa: E402
import copy  # noqa: E402
import csv  # noqa: E402
import hashlib  # noqa: E402
import importlib.machinery  # noqa: E402
import importlib.metadata  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import numbers  # noqa: E402
import platform  # noqa: E402
import plistlib  # noqa: E402
import pwd  # noqa: E402
import re  # noqa: E402
import signal  # noqa: E402
import stat  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import traceback  # noqa: E402
import types  # noqa: E402
import zipfile  # noqa: E402

# ---------------------------------------------------------------------------------------------------------------
# Locations. Everything private stays inside the repository, under the git-ignored `.herd/`.
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, 'tools')
DRIVER_REL = 'tools/w1_driver.py'
JOB_REL = 'tools/w1_job.py'
STAGE0_ENV = os.path.join(REPO, '.herd', 'work', 'ms001-stage0', 'env')
ENV = os.path.join(STAGE0_ENV, 'venv')
ENV_PY = os.path.join(ENV, 'bin', 'python')
SITE_PACKAGES = os.path.join(ENV, 'lib', 'python3.12', 'site-packages')
LOCK_PATH = os.path.join(STAGE0_ENV, 'requirements-lock.txt')
WHEELHOUSE = os.path.join(STAGE0_ENV, 'wheelhouse')
TASK = os.path.join(REPO, '.herd', 'work', 'ms001-w1-run-rev01')
RUN = os.path.join(TASK, 'run')
AIIDA_PATH = os.path.join(RUN, 'aiida')
CONFIG_DIR = os.path.join(AIIDA_PATH, '.aiida')  # A12 appends `.aiida`
STORAGE = os.path.join(CONFIG_DIR, 'repository', 'sqlite_dos_w1')
TMPDIR = os.path.join(RUN, 'tmp')
WORKDIR = os.path.join(RUN, 'work')
RECORDS = os.path.join(RUN, 'records')
CAPTURE = os.path.join(RUN, 'capture')
CAPTURE_UNTRACKED = os.path.join(CAPTURE, 'untracked')
CAPTURE_SITE_PACKAGES = os.path.join(CAPTURE, 'site-packages')
FROZEN_REL = 'structures/donor-activated-EAOGe-C2-radical.extxyz'
SYSTEM_VERSION_PLIST = '/System/Library/CoreServices/SystemVersion.plist'

# Brief 01, section 6: the wall-clock ceiling of the one attempt, enforced by the launcher, and the grace period after
# SIGTERM before SIGKILL. Reaching it is an operational stop, never a Section 8 condition.
CEILING_SECONDS = 4 * 3600
GRACE_SECONDS = 600

# The runner journal: every phase change, check, stop, not-reached reason and operational event, appended and
# forced to disk when it is recorded, so that a killed runner leaves its completed work behind (finalize).
JOURNAL = '80-runner-journal.jsonl'

# ---------------------------------------------------------------------------------------------------------------
# Declarations of the specification (Sections 2 to 6). These are the values every check is made against.
NA = 'not applicable: non-chemistry wiring test'
PROCESS_TYPE = 'w1_job.W1Job'
PROFILE_NAME = 'w1'
COMPUTER_LABEL = 'w1-local-nologin'
CODE_LABEL = 'w1-bash'
JOB_LABELS = ('w1-job1', 'w1-job2')
PYTHON_IMPLEMENTATION = 'CPython'
PYTHON_VERSION = '3.12.14'
LOCK_SHA256 = '813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8'
DECLARED_AIIDA_CORE = {'version': '2.9.2',
                       'wheel_sha256': '72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd'}
DECLARED_ASE = {'version': '3.29.0',
                'wheel_sha256': '7b9dd103f007810339c24acfee2f6b677c0c48443b21d3c98e52959246cf4ebf'}
DECLARED_NUMPY_VERSION = '2.5.3'
FROZEN_SHA256 = 'bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3'
FROZEN_PROPERTIES = 'species:S:1:pos:R:3:atom_id:S:1:map_num:I:1:radical_electrons:I:1'
FROZEN_ATOM_COUNT = 48
FIXTURE_ATOM_IDS = ['D-O1', 'D-O2', 'D-O3', 'D-O1-H1', 'D-O2-H1', 'D-O3-H1']
SIDECAR_FORMAT = 'w1-identity-sidecar-1'
SIDECAR_SITE_KEYS = ['index', 'atom_id', 'element', 'position', 'map_num', 'radical_electrons']
NATIVE_ARRAYS = ('atom_id', 'map_num', 'radical_electrons')
FIXTURE_DIFF_SHA256 = 'f3a3deb5cd0693c76b9bff397e811bff75eb253cb5f42265fe68e6582fdea609'
PROJECT_FILES = ['tools/w1_driver.py', 'tools/w1_job.py']
CAPTURE_POINT = ('after the interpreter record and the first F3 reading; before any import outside the '
                 'standard library')
USER_LEVEL_PATHS = ['', '.aiida', '.ase', '.cache', '.config', '.local', '.local/share', 'Library/Caches',
                    'Library/Application Support', 'Library/Preferences', 'Library/Logs']

# Section 5, item 1: the allow-list, in the order of Section 5, the declared platform-injected name and the names
# that must be absent. Section 3: the shell-maintained names that the payload record may also carry.
ALLOW_LIST = ['PATH', 'LC_ALL', 'AIIDA_PATH', 'TMPDIR', 'PYTHONNOUSERSITE']
PLATFORM_INJECTED = ['__CF_USER_TEXT_ENCODING']
ABSENT_NAMES = ['BASH_ENV', 'ENV', 'HOME']
SHELL_MAINTAINED = ['PWD', 'OLDPWD', 'SHLVL', '_']

# Section 4, "Git".
GIT = ['/usr/bin/git', '--no-optional-locks']
GIT_ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null',
           'GIT_OPTIONAL_LOCKS': '0'}
GIT_FORBIDDEN_KEYS = {'include.path', 'core.excludesfile', 'core.attributesfile', 'core.fsmonitor',
                      'core.untrackedcache', 'core.splitindex', 'core.worktree', 'core.hookspath'}
GIT_FORBIDDEN_PREFIXES = ('includeif.', 'filter.', 'diff.', 'index.', 'extensions.')

# Section 3, "Mandatory contents of the provenance inputs".
_CALCJOB = 'aiida/engine/processes/calcjobs/calcjob.py'
DEFAULTS = {
    'transport': {
        'value': {'transport_type': 'core.local', 'use_login_shell': False},
        'kind': 'explicit',
        'defined_by': 'aiida-core 2.9.2, aiida/transports/transport.py, lines 114-124 (A1): use_login_shell '
                      'defaults to true and selects `bash -l `; it is set false here'},
    'scheduler': {
        'value': {'scheduler_type': 'core.direct',
                  'submit_command': '(bash <script> > /dev/null 2>&1 & echo $!) &'},
        'kind': 'explicit',
        'defined_by': 'aiida-core 2.9.2, aiida/schedulers/plugins/direct.py, lines 126-174 and 192-206 (A3)'},
    'shebang': {
        'value': '#!/bin/bash',
        'kind': 'explicit',
        'defined_by': 'aiida-core 2.9.2, aiida/schedulers/scheduler.py, lines 205-244 (A5)'},
    'import_sys_environment': {
        'value': True,
        'kind': 'default relied upon',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 398-403 (A6); kept true for the reason in A4: '
                      'aiida-core 2.9.2, aiida/schedulers/plugins/direct.py, lines 160-174'},
    'environment_variables': {
        'value': {'OMP_NUM_THREADS': '1'},
        'kind': 'explicit',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 404-409 (A6); aiida/schedulers/scheduler.py, '
                      'lines 205-244 (A5)'},
    'resources': {
        'value': {'num_machines': 1, 'num_mpiprocs_per_machine': 1},
        'kind': 'explicit',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 338-345; aiida/schedulers/plugins/direct.py, '
                      'lines 126-174 (A3): no cores-per-process value, so the header adds no export'},
    'withmpi': {
        'value': False,
        'kind': 'explicit',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 385-390'},
    'prepend_text': {
        'value': '',
        'kind': 'explicit',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 426-432 (A6); aiida/schedulers/scheduler.py, '
                      'lines 205-244 (A5)'},
    'append_text': {
        'value': '',
        'kind': 'explicit',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 433-439; aiida/schedulers/scheduler.py, '
                      'lines 205-244 (A5)'},
    'custom_scheduler_commands': {
        'value': '',
        'kind': 'explicit',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 352-360; aiida/schedulers/plugins/direct.py, '
                      'lines 160-174 (A4)'},
    'submit_script_filename': {
        'value': '_aiidasubmit.sh',
        'kind': 'default relied upon',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 320-325 (A6)'},
    'scheduler_stdout': {
        'value': '_scheduler-stdout.txt',
        'kind': 'default relied upon',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 326-331 and 982-990 (A6)'},
    'scheduler_stderr': {
        'value': '_scheduler-stderr.txt',
        'kind': 'default relied upon',
        'defined_by': f'aiida-core 2.9.2, {_CALCJOB}, lines 332-337 and 982-990 (A6)'},
    'engine_defaults': NA,
}
DEFAULT_KINDS = ('explicit', 'default relied upon')
CALC_PERFORMED = {
    'method_and_levels': NA,
    'partition_embedding_and_links': NA,
    'charge': NA,
    'multiplicity': NA,
    'optimizer_and_settings': NA,
    'drive_branch': NA,
    'step_index': NA,
    'imposed_z': NA,
    'constraints': {'fixed_set_fixture': list(FIXTURE_ATOM_IDS),
                    'label': 'synthetic wiring fixture; not a scientific constraint'},
    'record_label': 'software wiring test; no model chemistry was executed',
}
SEED = 'none'
UNITS = {
    'positions': 'angstrom',
    'cell': 'angstrom; the structure is non-periodic',
    'extracted_quantities': {'atom_count': 'dimensionless count',
                             'digests': 'not applicable: identifiers, not quantities'},
    'energy': 'not applicable: none extracted',
    'forces': 'not applicable: none extracted',
    'gradient': 'not applicable: none extracted',
}
PER_CLAIM = {
    'units': 'see the units input of this job',
    'atom_identity': 'see the identity and fixed_set inputs of this job',
    'charge_and_spin': NA,
    'constraints': 'synthetic fixed-set fixture only; not a scientific constraint',
    'environment': 'see the env_policy, build_identity and host_record inputs of this job',
    'tool_state': "not applicable: the frozen donor file is carried only as an identity fixture; no claim about "
                  "the tool's state is made",
    'evidence_class': 'software wiring test; not chemistry evidence; no chemistry evidence class applies',
    'claim': 'none',
}
ENV_POLICY = {
    'allow_list': list(ALLOW_LIST),
    'platform_injected': list(PLATFORM_INJECTED),
    'platform_injected_scope': 'interpreter and payload records only; never the launcher record',
    'absent': list(ABSENT_NAMES),
    'use_login_shell': False,
    'import_sys_environment': True,
    'shell': '/bin/bash',
}
BUILD_IDENTITY_KEYS = ['python', 'distributions', 'aiida_core', 'ase', 'numpy', 'lock_sha256', 'bash',
                       'operating_system', 'engine', 'engine_banner', 'engine_build_identity']
PYTHON_KEYS = ['implementation', 'version', 'build', 'executable', 'interpreter_sha256']
DISTRIBUTION_KEYS = ['name', 'version', 'in_lock', 'status', 'lock_hashes', 'wheel_sha256', 'wheel_record_match',
                     'installed_record_sha256']
STATUSES = ('locked-verified', 'locked-wheel-unavailable', 'not-in-lock')
# The explicit third state of an F3 comparison that could not be completed (a file that could not be read). It is
# neither a success nor an observed failure, and it is not `not established` in the sense of
# `locked-wheel-unavailable`: the wheel exists. It appears in the record itself, and the reading holding it is
# incomplete (an operational inability, never a pass, never S10 or S11 on its own).
INCOMPLETE = 'incomplete: not every applicable comparison could be made'
OS_KEYS = ['sysname', 'release', 'version', 'machine', 'product_name', 'product_version', 'product_build',
           'plist_sha256']
HOST_SOURCES = {
    'host_name': 'os.uname().nodename',
    'cpu_model': '/usr/sbin/sysctl -n machdep.cpu.brand_string',
    'logical_cpu_count': 'os.cpu_count()',
    'memory_bytes': '/usr/sbin/sysctl -n hw.memsize',
}
CODE_IDENTITY_KEYS = ['commit', 'object_format', 'git_version', 'git_environment', 'git_config_sha256',
                      'info_exclude_sha256', 'index_state_sha256', 'raw_index_sha256', 'tracked_files',
                      'code_diff_sha256', 'untracked_files', 'project_files', 'environment_listing_sha256',
                      'pycache_listing_sha256', 'dont_write_bytecode', 'payload_sha256', 'fixture_diff_sha256',
                      'capture_point']

# Section 8. Every stop is recorded with the condition that fired and its observed values.
STOP_CONDITIONS = {
    'S01': 'a user-level AiiDA configuration directory appears, or the two user-level observations of Section 5 '
           'differ',
    'S02': 'the launcher record differs from the Section 5 allow-list or its declared values, or an interpreter '
           'record holds a name outside the allow-list and the declared platform-injected name, lacks an '
           'allow-list name or differs from the launcher record in an allow-list value',
    'S03': '`use_login_shell` reads back true',
    'S04': 'the `presubmit` validation raises, or the three copies of a submission file differ',
    'S05': 'the process type differs from `w1_job.W1Job`',
    'S06': 'a precondition of Section 4 fails, or a comparison of Section 4 between the capture point and the run '
           'end differs, a new, removed or changed bytecode file included',
    'S07': 'a required link is missing',
    'S08': 'a job returns 310, 311 or 312',
    'S09': 'a provenance input fails its Section 3 "Mandatory contents" declaration',
    'S10': 'a comparison that Section 3 declares, and that applies, fails: for the build identity, the host '
           'record, the payload record or a loaded module file',
    'S11': 'a `distributions` entry fits none of the three statuses',
    'S12': 'an F4 check fails',
    'S13': 'a negative case passes',
    'S14': 'a project module file, or a module file outside the classes of Section 3, is first listed at the run '
           'end',
    'S15': 'the fixture diff fails its check of Section 4',
}

# Section 7. A criterion is demonstrated only when every check named here was made before any Section 8 condition
# fired and passed (see `evaluate`). A check made after the first stop is evidence, never credit.
CRITERIA = {
    '1': ['job1.finished_ok', 'job2.finished_ok', 'job1.process_type', 'job2.process_type', 'job1.links',
          'job2.links', 'chain.calcjob_nodes', 'chain.job2_from_job1'],
    '2': ['capture.frozen_input', 'f4.sidecar_built', 'f4.T0', 'f4.S1', 'job1.f4', 'job2.f4', 'f4.sidecar_carriage',
          'negative_cases'],
    '3': ['interpreter.dont_write_bytecode', 'capture.preconditions', 'inputs.f1_equal_capture', 'f1.resolve_bytes',
          'f1.inputs_of_both_jobs', 'runend.section4'],
    '4': ['launcher.record', 'interpreter.record_start', 'interpreter.record_end', 'job1.payload_record',
          'job2.payload_record', 'computer.readback', 'computer.declared_configuration', 'job1.presubmit',
          'job2.presubmit', 'job1.binding', 'job2.binding', 'job1.submission_inventory', 'job2.submission_inventory',
          'job1.options_and_uuids', 'job2.options_and_uuids'],
    '5': ['inputs.mandatory_contents', 'job1.mandatory_contents', 'job2.mandatory_contents',
          'runend.mandatory_contents', 'job1.input_manifest', 'job2.input_manifest', 'f3.first_reading',
          'runend.build_identity', 'runend.host_record', 'modules.input_point', 'modules.run_end'],
    '6': ['repository_keys'],
    '7': ['user_level.aiida_dir_after_import', 'user_level.aiida_dir_at_run_end', 'user_level', 'fixture_diff'],
}

# The Section 8 condition that each check may fire. A check not listed here fires none: its failure leaves its
# criterion unmet (or not established) without a Section 8 condition. `Context.check` refuses any other pairing.
CHECK_CONDITIONS = {
    'launcher.record': 'S02', 'interpreter.record_start': 'S02', 'interpreter.record_end': 'S02',
    'computer.readback': 'S03',
    'job1.presubmit': 'S04', 'job2.presubmit': 'S04', 'job1.binding': 'S04', 'job2.binding': 'S04',
    'job1.finished_ok': ('S04', 'S08'), 'job2.finished_ok': ('S04', 'S08'),
    'job1.process_type': 'S05', 'job2.process_type': 'S05',
    'capture.preconditions': 'S06', 'inputs.f1_equal_capture': 'S06', 'runend.section4': 'S06',
    'job1.links': 'S07', 'job2.links': 'S07', 'chain.job2_from_job1': 'S07',
    'inputs.mandatory_contents': 'S09', 'job1.mandatory_contents': 'S09', 'job2.mandatory_contents': 'S09',
    'runend.mandatory_contents': 'S09',
    'f3.first_reading': ('S10', 'S11'), 'runend.build_identity': ('S10', 'S11'), 'runend.host_record': 'S10',
    'job1.payload_record': 'S10', 'job2.payload_record': 'S10', 'modules.input_point': 'S10',
    'modules.run_end': ('S10', 'S14'),
    'capture.frozen_input': 'S12', 'f4.sidecar_built': 'S12', 'f4.T0': 'S12', 'f4.S1': 'S12', 'job1.f4': 'S12',
    'job2.f4': 'S12', 'f4.sidecar_carriage': 'S12',
    'negative_cases': 'S13',
    'fixture_diff': 'S15',
    'user_level': 'S01', 'user_level.aiida_dir_after_import': 'S01', 'user_level.aiida_dir_at_run_end': 'S01',
}

INT_STRING = re.compile(r'[+-]?[0-9]+')
HEX64 = re.compile(r'[0-9a-f]{64}')


# ---------------------------------------------------------------------------------------------------------------
# Small helpers.
class W1Stop(Exception):
    """A Section 8 stop condition fired; it has been recorded already."""


class OperationalError(Exception):
    """A failure that is not a Section 8 condition: a command, a runtime or a checker defect."""


class JobSequenceEnded(Exception):
    """Job 1 did not finish cleanly without a Section 8 condition: job 2 is deliberately not started."""


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def hash_file(path, copy_to=None):
    """(size, SHA256) of a file read once; when `copy_to` is given, the same bytes are written there."""
    digest = hashlib.sha256()
    size = 0
    target = None
    if copy_to is not None:
        os.makedirs(os.path.dirname(copy_to), exist_ok=True)
        target = open(copy_to, 'xb')
    try:
        with open(path, 'rb') as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b''):
                digest.update(chunk)
                size += len(chunk)
                if target is not None:
                    target.write(chunk)
    finally:
        if target is not None:
            target.close()
    return size, digest.hexdigest()


def git_blob_id(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def path_bytes(path):
    return path.encode('utf-8', 'surrogateescape')


def under(path, root):
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def normalize_name(name):
    return re.sub(r'[-_.]+', '-', name).lower()


def is_bytecode_cache(rel):
    parts = rel.split('/')
    return rel.endswith('.pyc') and '__pycache__' in parts[:-1]


def launcher_record():
    """Section 5 item 1: the runner's environment, built as an explicit mapping, never from os.environ."""
    return {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'AIIDA_PATH': AIIDA_PATH, 'TMPDIR': TMPDIR,
            'PYTHONNOUSERSITE': '1'}


def run_child(argv, env, cwd=REPO):
    """A child process started from an argument vector without a shell, with an explicit environment."""
    proc = subprocess.run(argv, env=dict(env), cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True)
    return {'argv': list(argv), 'exit': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}


def child_summary(result):
    return {'argv': result['argv'], 'exit': result['exit'],
            'stdout': result['stdout'].decode('utf-8', 'replace'),
            'stderr': result['stderr'].decode('utf-8', 'replace')}


class Recorder:
    """Writes private records into one directory. Files are created once and never overwritten."""

    def __init__(self, directory):
        self.directory = directory
        self.progress_path = os.path.join(directory, 'progress.log')

    def progress(self, message):
        line = f'{time.strftime("%Y-%m-%dT%H:%M:%S%z")} {message}\n'
        with open(self.progress_path, 'a', encoding='utf-8') as handle:
            handle.write(line)
        print(line, end='', flush=True)

    def write_bytes(self, name, data):
        with open(os.path.join(self.directory, name), 'xb') as handle:
            handle.write(data)
        return sha256_bytes(data)

    def write_json(self, name, value):
        data = (json.dumps(value, indent=1, sort_keys=True, ensure_ascii=True, default=repr) + '\n').encode('ascii')
        return self.write_bytes(name, data)

    def journal(self, entry):
        """Append one entry to the runner journal and force it to disk before returning."""
        line = (json.dumps(entry, sort_keys=True, ensure_ascii=True, default=repr) + '\n').encode('ascii')
        with open(os.path.join(self.directory, JOURNAL), 'ab') as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())


# ---------------------------------------------------------------------------------------------------------------
# Listings (Section 4, "Listings").
class ListingPathError(Exception):
    pass


def root_state(root):
    """`listed` (a readable directory), `absent` (nothing exists there) or `inaccessible`, with the error if any.

    An absent root is an observation: its listing is empty and complete. An inaccessible root is not: nothing below
    it was observed.
    """
    try:
        status = os.lstat(root)
    except (FileNotFoundError, NotADirectoryError):
        return 'absent', None
    except OSError as exc:
        return 'inaccessible', type(exc).__name__
    if not stat.S_ISDIR(status.st_mode):
        return 'inaccessible', 'the root is not a directory'
    return 'listed', None


def walk_regular(root, select=None, copy_root=None):
    """Regular files under `root` as (relative path, size, SHA256), with symbolic links and other entries apart.

    Every failure to enumerate a directory (`os.walk`'s `onerror`) or to read a file is recorded in `errors`, never
    skipped: a walk with errors, or with an inaccessible root, is incomplete, and no comparison may treat its rows as
    a complete listing (`complete` is false). An absent root gives an empty, complete listing.
    """
    state, error = root_state(root)
    result = {'root': state, 'exists': state != 'absent', 'rows': [], 'links': [], 'irregular': [], 'errors': []}
    if state != 'listed':
        if state == 'inaccessible':
            result['errors'].append({'path': '.', 'error': error})
        result['complete'] = state == 'absent'
        return result

    def relative(path):
        return os.path.relpath(path, root).replace(os.sep, '/') if path else '?'

    def onerror(exc):
        result['errors'].append({'path': relative(getattr(exc, 'filename', None)), 'error': type(exc).__name__})

    for dirpath, dirnames, filenames in os.walk(root, onerror=onerror, followlinks=False):
        dirnames.sort()
        for name in dirnames:
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                result['links'].append(relative(full))
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = relative(full)
            if select is not None and not select(rel):
                continue
            try:
                mode = os.lstat(full).st_mode
            except OSError as exc:
                result['errors'].append({'path': rel, 'error': type(exc).__name__})
                continue
            if stat.S_ISLNK(mode):
                result['links'].append(rel)
                continue
            if not stat.S_ISREG(mode):
                result['irregular'].append(rel)
                continue
            copy_to = os.path.join(copy_root, *rel.split('/')) if copy_root is not None else None
            try:
                size, digest = hash_file(full, copy_to)
            except OSError as exc:
                result['errors'].append({'path': rel, 'error': type(exc).__name__})
                continue
            result['rows'].append((rel, size, digest))
    result['complete'] = not result['errors']
    return result


def walk_names(root):
    """Every regular-file path under `root` (no reading), with every enumeration failure recorded, never skipped."""
    state, error = root_state(root)
    paths, errors = [], []
    if state != 'listed':
        if state == 'inaccessible':
            errors.append({'path': '.', 'error': error})
        return paths, errors

    def onerror(exc):
        errors.append({'path': getattr(exc, 'filename', None), 'error': type(exc).__name__})

    for dirpath, _dirnames, filenames in os.walk(root, onerror=onerror, followlinks=False):
        for name in filenames:
            paths.append(os.path.normpath(os.path.join(dirpath, name)))
    return paths, errors


def file_status(path):
    """`regular`, `missing` (observed absent), `not regular` (a link or another kind) or `inaccessible: <error>`."""
    try:
        mode = os.lstat(path).st_mode
    except (FileNotFoundError, NotADirectoryError):
        return 'missing'
    except OSError as exc:
        return f'inaccessible: {type(exc).__name__}'
    return 'regular' if stat.S_ISREG(mode) else 'not regular'


def listing_bytes(fields):
    """`fields` are (tag/relative path, size, SHA256). UTF-8, TAB-separated, LF after every line, sorted by path."""
    lines = []
    for field, size, digest in fields:
        if '\t' in field or '\n' in field:
            raise ListingPathError(f'path holds a TAB or LF byte: {field!r}')
        try:
            encoded = field.encode('utf-8')
        except UnicodeEncodeError as exc:
            raise ListingPathError(f'path is not valid UTF-8: {field!r}') from exc
        if not HEX64.fullmatch(digest) or not isinstance(size, int) or size < 0:
            raise ListingPathError(f'malformed size or digest for {field!r}')
        lines.append((encoded, encoded + b'\t' + str(size).encode('ascii') + b'\t' + digest.encode('ascii') + b'\n'))
    lines.sort(key=lambda item: item[0])
    keys = [key for key, _ in lines]
    if len(set(keys)) != len(keys):
        raise ListingPathError('a path field occurs twice')
    return b''.join(line for _, line in lines)


def tagged(tag, rows):
    return [(f'{tag}/{rel}', size, digest) for rel, size, digest in rows]


def in_pycache(rel):
    return '__pycache__' in rel.split('/')[:-1]


def affected_fields(tag, errors):
    """The listing fields that a walk with these errors leaves unobserved, as tagged path prefixes. Pure.

    An error at the root (`.`, or a path that could not be named) leaves the whole tag unobserved; an error at a
    directory leaves everything under it; an error at a file leaves that file.
    """
    prefixes = []
    for error in errors:
        path = error.get('path') if isinstance(error, dict) else error[0]
        prefixes.append(tag if path in ('.', '?', '', None) else f'{tag}/{path}')
    return prefixes


def listing_fields(data):
    """Listing bytes (as `listing_bytes` writes them) back to {field: [size, SHA256]}. Pure."""
    fields = {}
    for line in data.split(b'\n'):
        if line:
            field, size, digest = line.split(b'\t')
            fields[field.decode('utf-8')] = [int(size), digest.decode('ascii')]
    return fields


def compare_listing_fields(first, second, affected):
    """Two listings ({field: [size, SHA256]}) compared field by field. Pure. Returns (state, differing, unobserved).

    `affected` are field prefixes that either reading could not enumerate or read. A field outside every affected
    prefix that differs, or that one listing holds and the other does not, is an observed difference: the state is
    False whatever else is unknown. With no observed difference, any affected prefix leaves the state None (an error
    may hide a difference, so equality is not established). Otherwise True.
    """
    def is_affected(field):
        return any(field == prefix or field.startswith(prefix + '/') for prefix in affected)

    differing, unobserved = [], []
    for field in sorted(set(first) | set(second), key=lambda f: f.encode('utf-8', 'surrogateescape')):
        if list(first.get(field) or []) != list(second.get(field) or []):
            (unobserved if is_affected(field) else differing).append(field)
    return comparison_state(differing, unobserved or affected), differing, unobserved


def compare_file_entries(first, second):
    """Two lists of listed project files compared path by path. Pure. Returns (state, differing, unobserved).

    The set of paths comes from Git and is observed: a path in one list only is an observed difference. A file that
    could not be read at either instant is unobserved; any other difference in size or SHA256 is observed.
    """
    a = {entry['path']: entry for entry in first}
    b = {entry['path']: entry for entry in second}
    differing, unobserved = [], []
    for path in sorted(set(a) | set(b), key=path_bytes):
        if path not in a or path not in b:
            differing.append(path)
        elif 'error' in a[path] or 'error' in b[path]:
            unobserved.append(path)
        elif canonical_json(a[path]) != canonical_json(b[path]):
            differing.append(path)
    return comparison_state(differing, unobserved), differing, unobserved


def pycache_listing():
    """The bytecode listing bytes and their detail (see `pycache_reading`)."""
    fields, detail = pycache_reading()
    return listing_bytes(fields), detail


def pycache_reading():
    """Section 4, "The bytecode policy": every file in every `__pycache__` directory under the three roots."""
    roots = (('tools', TOOLS), ('site-packages', SITE_PACKAGES), ('base-prefix', sys.base_prefix))
    fields, detail = [], {}
    for tag, root in roots:
        walked = walk_regular(root, select=in_pycache)
        fields.extend(tagged(tag, walked['rows']))
        # Each of the three roots must exist and be enumerated completely: an absent root is not a complete reading
        # of a declared tree, and an enumeration error may hide cache files from both readings.
        detail[tag] = {'root_private': root, 'files': len(walked['rows']), 'root': walked['root'],
                       'errors': walked['errors'], 'complete': walked['root'] == 'listed' and walked['complete'],
                       'links_in_pycache': [rel for rel in walked['links'] if in_pycache(rel)],
                       'irregular': walked['irregular']}
    return fields, detail


# ---------------------------------------------------------------------------------------------------------------
# User-level observation (Section 5).
def observe_user_level():
    """One user-level observation of Section 5: for each path, `observed` is true only if it was fully recorded.

    A path that does not exist is observed (`exists` false). A path whose type, or a directory whose entries,
    could not be read is not observed: it carries the error, and no equality can be established for it.
    """
    home = pwd.getpwuid(os.getuid()).pw_dir
    observation = {}
    for rel in USER_LEVEL_PATHS:
        path = os.path.join(home, rel) if rel else home
        key = rel or '.'
        try:
            mode = os.lstat(path).st_mode
        except (FileNotFoundError, NotADirectoryError):
            observation[key] = {'observed': True, 'exists': False}
            continue
        except OSError as exc:
            observation[key] = {'observed': False, 'error': type(exc).__name__}
            continue
        kind = ('directory' if stat.S_ISDIR(mode) else 'file' if stat.S_ISREG(mode)
                else 'symlink' if stat.S_ISLNK(mode) else 'other')
        entry = {'observed': True, 'exists': True, 'type': kind}
        if kind == 'directory':
            try:
                names = []
                with os.scandir(path) as iterator:
                    for item in iterator:
                        item_kind = ('symlink' if item.is_symlink() else
                                     'directory' if item.is_dir(follow_symlinks=False) else
                                     'file' if item.is_file(follow_symlinks=False) else 'other')
                        names.append([item.name, item_kind])
                entry['entries'] = sorted(names)
            except OSError as exc:
                entry = {'observed': False, 'exists': True, 'type': kind, 'error': type(exc).__name__}
        observation[key] = entry
    return home, observation


def compare_user_level(before, after):
    """Compare the two user-level observations of Section 5. Pure.

    Returns the paths that were not observed at either instant (equality cannot be established for them, which is
    an operational inability, never a pass), the paths observed at both instants that differ (S01), and whether the
    user-level AiiDA directory appeared: absent at the first observation and present at the second (S01).
    """
    unobserved, differing = [], []
    for key in [rel or '.' for rel in USER_LEVEL_PATHS]:
        first, second = before.get(key), after.get(key)
        if not (isinstance(first, dict) and first.get('observed') is True
                and isinstance(second, dict) and second.get('observed') is True):
            unobserved.append(key)
        elif canonical_json(first) != canonical_json(second):
            differing.append(key)
    aiida_first, aiida_second = before.get('.aiida', {}), after.get('.aiida', {})
    if aiida_first.get('observed') is True and aiida_second.get('observed') is True:
        appeared = aiida_first.get('exists') is False and aiida_second.get('exists') is True
    else:
        appeared = None
    return {'unobserved': unobserved, 'differing': differing, 'aiida_dir_appeared': appeared,
            'complete': not unobserved}


def aiida_dir_status(baseline):
    """Whether `~/.aiida` has appeared since the launcher's first observation (`baseline`: its `.aiida` entry).

    Returns `appeared` (absent then, present now: S01), `absent`, `pre-existing` (present at the first observation,
    so it cannot appear; equality of the two observations still covers a change) or `unobserved` (the baseline was
    not observed, so an appearance cannot be established).
    """
    if not isinstance(baseline, dict) or baseline.get('observed') is not True:
        return 'unobserved'
    if baseline.get('exists') is not False:
        return 'pre-existing'
    home = pwd.getpwuid(os.getuid()).pw_dir
    return 'appeared' if os.path.lexists(os.path.join(home, '.aiida')) else 'absent'


def check_aiida_dir(ctx, name, status, stop):
    """Record the appearance check of `~/.aiida` (S01); with `stop`, an appearance ends the run."""
    if status == 'unobserved':
        return ctx.not_established(name, 'the first observation of ~/.aiida was not made')
    detail = {'status': status}
    if stop:
        ctx.require(name, 'S01', status != 'appeared', detail)
        return True
    return ctx.check(name, 'S01', status != 'appeared', detail)


# ---------------------------------------------------------------------------------------------------------------
# Section 5 environment records.
def check_launcher_record(record):
    problems = []
    if sorted(record) != sorted(ALLOW_LIST):
        problems.append(f'names {sorted(record)} differ from the allow-list {sorted(ALLOW_LIST)}')
    expected = launcher_record()
    for name in ALLOW_LIST:
        if record.get(name) != expected[name]:
            problems.append(f'value of {name} differs from its declared value')
    for name in PLATFORM_INJECTED + ABSENT_NAMES:
        if name in record:
            problems.append(f'{name} is present in the launcher record')
    return problems


def check_interpreter_record(record, launcher):
    problems = []
    missing = [name for name in ALLOW_LIST if name not in record]
    if missing:
        problems.append(f'allow-list names missing: {missing}')
    outside = sorted(name for name in record if name not in ALLOW_LIST and name not in PLATFORM_INJECTED)
    if outside:
        problems.append(f'names outside the allow-list and the platform-injected name: {outside}')
    for name in ALLOW_LIST:
        if name in record and record[name] != launcher.get(name):
            problems.append(f'value of {name} differs from the launcher record')
    return problems


# ---------------------------------------------------------------------------------------------------------------
# F3: the build identity and the host record (Section 3).
def parse_lock(data):
    entries = {}
    for raw in data.decode('utf-8').splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]*)==(\S+)((?:\s+--hash=sha256:[0-9a-f]{64})*)', line)
        if match is None:
            raise ValueError(f'unparsed lock line: {raw!r}')
        key = (normalize_name(match.group(1)), match.group(2))
        if key in entries:
            raise ValueError(f'duplicate lock entry: {raw!r}')
        entries[key] = re.findall(r'--hash=sha256:([0-9a-f]{64})', match.group(3))
    return entries


def wheel_index():
    index, unparsed = {}, []
    for name in sorted(os.listdir(WHEELHOUSE)):
        if not name.endswith('.whl'):
            continue
        parts = name[:-4].split('-')
        if len(parts) not in (5, 6):
            unparsed.append(name)
            continue
        index.setdefault((normalize_name(parts[0]), parts[1]), []).append(name)
    return index, unparsed


def record_hash_hex(field):
    algorithm, _, encoded = field.partition('=')
    if algorithm != 'sha256' or not encoded:
        return None
    return base64.urlsafe_b64decode(encoded + '=' * (-len(encoded) % 4)).hex()


class HashCache:
    """Per-reading cache, so a file listed by two RECORDs is read once in one reading, never across readings."""

    def __init__(self):
        self.values = {}

    def get(self, path):
        if path not in self.values:
            self.values[path] = hash_file(path)[1]
        return self.values[path]


def read_distributions(lock_entries, cache):
    """`distributions` per the applicability rule, with the installed-RECORD check for entries of every status."""
    wheels, unparsed_wheels = wheel_index()
    dists = list(importlib.metadata.distributions(path=[SITE_PACKAGES]))
    dist_info_dirs = sorted(name for name in os.listdir(SITE_PACKAGES) if name.endswith('.dist-info'))
    public, private, failures, unestablished = [], [], [], []
    listed_paths = set()
    wheel_file_map = {}
    for dist in sorted(dists, key=lambda d: (normalize_name(d.metadata['Name']), d.metadata['Version'])):
        name, version = dist.metadata['Name'], dist.metadata['Version']
        key = (normalize_name(name), version)
        info_dir = str(dist._path)
        record_path = os.path.join(info_dir, 'RECORD')
        detail = {'name': name, 'version': version, 'dist_info_private': info_dir}

        installed = {'compared': 0, 'mismatch': [], 'missing': [], 'empty_hash': [], 'bytecode_listed': [],
                     'unsupported_hash': [], 'inaccessible': []}
        try:
            with open(record_path, 'rb') as handle:
                record_bytes = handle.read()
        except OSError as exc:
            record_bytes = None
            installed['inaccessible'].append(['RECORD', type(exc).__name__])
        rows = list(csv.reader(io.StringIO(record_bytes.decode('utf-8')))) if record_bytes is not None else []
        for row in rows:
            if not row:
                continue
            rel, field = row[0], (row[1] if len(row) > 1 else '')
            full = os.path.normpath(os.path.join(SITE_PACKAGES, rel))
            listed_paths.add(full)
            if is_bytecode_cache(rel):
                installed['bytecode_listed'].append(rel)
                continue
            if not field:
                installed['empty_hash'].append(rel)
                continue
            want = record_hash_hex(field)
            if want is None:
                installed['unsupported_hash'].append(rel)
                continue
            status = file_status(full)
            if status in ('missing', 'not regular'):
                installed['missing'].append(rel)
                continue
            try:
                if status != 'regular':
                    raise PermissionError(status)
                digest = cache.get(full)
            except OSError as exc:
                installed['inaccessible'].append([rel, str(exc) or type(exc).__name__])
                continue
            installed['compared'] += 1
            if digest != want:
                installed['mismatch'].append(rel)
        detail['installed_record'] = installed
        # Observed discrepancies fail whatever else is unknown; with none, an unread file leaves the check
        # incomplete (None), never true.
        installed_ok = comparison_state(installed['mismatch'] or installed['missing'] or installed['unsupported_hash'],
                                        installed['inaccessible'])
        if installed_ok is False:
            failures.append(f'installed RECORD check failed for {name} {version}')
        if installed['inaccessible']:
            unestablished.append(f'installed RECORD of {name} {version}: {len(installed["inaccessible"])} files '
                                 'could not be read')

        entry = {'name': name, 'version': version, 'in_lock': key in lock_entries}
        entry['lock_hashes'] = list(lock_entries[key]) if entry['in_lock'] else []
        candidates = wheels.get(key, [])
        detail['wheel_candidates'] = candidates
        if not entry['in_lock']:
            entry['wheel_sha256'] = 'not applicable: not in lock'
            entry['wheel_record_match'] = 'not applicable: not in lock'
        elif not candidates:
            entry['wheel_sha256'] = 'not available'
            entry['wheel_record_match'] = 'not established'
        else:
            digests, unreadable_wheels = {}, {}
            for candidate in candidates:
                try:
                    digests[candidate] = cache.get(os.path.join(WHEELHOUSE, candidate))
                except OSError as exc:
                    unreadable_wheels[candidate] = type(exc).__name__
            if len(candidates) != 1:
                detail['wheel_ambiguity'] = {c: digests.get(c, INCOMPLETE) for c in candidates}
            if unreadable_wheels:
                # The wheel exists but its bytes could not be read: its digest and its RECORD comparison are
                # incomplete, never `not available` and never a mismatch.
                detail['wheel_unreadable'] = unreadable_wheels
                unestablished.append(f'wheel of {name} {version} could not be read: {sorted(unreadable_wheels)}')
                entry['wheel_sha256'] = INCOMPLETE
                entry['wheel_record_match'] = INCOMPLETE if len(candidates) == 1 else False
            else:
                chosen = [c for c in candidates if digests[c] in entry['lock_hashes']]
                wheel_name = chosen[0] if len(chosen) == 1 else candidates[0]
                entry['wheel_sha256'] = digests[wheel_name]
                detail['wheel_file'] = wheel_name
                check = compare_wheel_record(os.path.join(WHEELHOUSE, wheel_name), name, cache)
                detail['wheel_record'] = {k: v for k, v in check.items() if k != 'file_map'}
                if check['ok'] is None:
                    unestablished.append(f'wheel RECORD comparison of {name} {version}: '
                                         f'{len(check["inaccessible"])} files could not be read')
                if len(candidates) != 1 or check['ok'] is False:
                    entry['wheel_record_match'] = False  # observed: ambiguous wheels, or a listed discrepancy
                elif check['ok'] is None:
                    entry['wheel_record_match'] = INCOMPLETE
                else:
                    entry['wheel_record_match'] = True
                    for full, want in check['file_map'].items():
                        wheel_file_map[full] = {'distribution': name, 'version': version, 'sha256': want}
        if record_bytes is None:
            entry['installed_record_sha256'] = INCOMPLETE
        else:
            entry['installed_record_sha256'] = sha256_bytes(record_bytes)
        entry['status'] = distribution_status(entry)
        if entry['status'] == 'fits no status':
            failures.append(f'{name} {version} fits none of the three statuses')
        elif entry['status'] == INCOMPLETE:
            unestablished.append(f'{name} {version}: no status can be assigned until every applicable comparison '
                                 'is made')
        public.append({k: entry[k] for k in DISTRIBUTION_KEYS})
        detail['installed_record_ok'] = installed_ok  # true, false (observed) or null (incomplete)
        private.append(detail)

    # Section 3, "Unlisted files": files in site-packages that no installed RECORD lists. An enumeration failure
    # leaves the record incomplete; it is recorded, never skipped. An installed RECORD that could not be read lists
    # files that cannot be known, so the unlisted set is then marked incomplete rather than read as observed.
    unlisted = []
    names, walk_errors = walk_names(SITE_PACKAGES)
    for full in names:
        if full not in listed_paths:
            unlisted.append(os.path.relpath(full, SITE_PACKAGES).replace(os.sep, '/'))
    if walk_errors:
        unestablished.append(f'the enumeration of site-packages for unlisted files failed at {len(walk_errors)} '
                             'places')
    unread_records = [f'{d["name"]} {d["version"]}' for d in private
                      if any(item[0] == 'RECORD' for item in d['installed_record']['inaccessible'])]
    return {
        'public': public,
        'private': private,
        'failures': failures,
        'unestablished': unestablished,
        'unlisted_enumeration_errors': walk_errors[:50],
        'unlisted_complete': not walk_errors and not unread_records,
        'unlisted_unread_records': unread_records,
        'wheel_file_map': wheel_file_map,
        'unlisted_site_packages_files': sorted(unlisted),
        'dist_info_directories': len(dist_info_dirs),
        'distributions_enumerated': len(dists),
        'unparsed_wheel_names': unparsed_wheels,
    }


def compare_wheel_record(wheel_path, dist_name, cache):
    """The wheel's own RECORD, read without extraction, against the installed files under the wheel-path rule."""
    result = {'compared': 0, 'mismatch': [], 'missing': [], 'empty_hash': [], 'bytecode_skipped': [],
              'data_scripts_skipped': [], 'unmapped': [], 'unsupported_hash': [], 'inaccessible': [],
              'record_member': None, 'file_map': {}}
    try:
        with zipfile.ZipFile(wheel_path) as archive:
            members = [n for n in archive.namelist() if re.fullmatch(r'[^/]+\.dist-info/RECORD', n)]
            if len(members) != 1:
                result['record_members'] = members
                result['ok'] = False
                return result
            result['record_member'] = members[0]
            data_prefix = members[0][:-len('.dist-info/RECORD')] + '.data/'
            text = archive.read(members[0]).decode('utf-8')
    except OSError as exc:
        # The archive could not be read: nothing was compared, nothing was observed to differ.
        result['inaccessible'].append(['wheel archive', type(exc).__name__])
        result['ok'] = None
        return result
    except (zipfile.BadZipFile, UnicodeDecodeError) as exc:
        result['archive_problem'] = f'{type(exc).__name__}: {exc}'
        result['ok'] = False
        return result
    for row in csv.reader(io.StringIO(text)):
        if not row:
            continue
        rel, field = row[0], (row[1] if len(row) > 1 else '')
        if not field:
            result['empty_hash'].append(rel)
            continue
        if is_bytecode_cache(rel):
            result['bytecode_skipped'].append(rel)
            continue
        if rel.startswith(data_prefix):
            scheme, _, sub = rel[len(data_prefix):].partition('/')
            if scheme == 'scripts':
                result['data_scripts_skipped'].append(rel)
                continue
            if scheme in ('purelib', 'platlib'):
                full = os.path.join(SITE_PACKAGES, sub)
            elif scheme == 'headers':
                full = os.path.join(ENV, 'include', 'site', 'python3.12', dist_name, sub)
            elif scheme == 'data':
                full = os.path.join(ENV, sub)
            else:
                result['unmapped'].append(rel)
                continue
        else:
            full = os.path.join(SITE_PACKAGES, rel)
        full = os.path.normpath(full)
        want = record_hash_hex(field)
        if want is None:
            result['unsupported_hash'].append(rel)
            continue
        status = file_status(full)
        if status in ('missing', 'not regular'):
            result['missing'].append(rel)
            continue
        try:
            if status != 'regular':
                raise PermissionError(status)
            digest = cache.get(full)
        except OSError as exc:
            # Not observed: neither a match nor a mismatch. The reading that holds it is not established.
            result['inaccessible'].append([rel, str(exc) or type(exc).__name__])
            continue
        result['compared'] += 1
        if digest != want:
            result['mismatch'].append(rel)
        else:
            result['file_map'][full] = want
    result['ok'] = comparison_state(result['mismatch'] or result['missing'] or result['unmapped']
                                    or result['unsupported_hash'], result['inaccessible'])
    return result


def comparison_state(observed_failures, unobserved):
    """The state of a comparison made of parts. Pure.

    False when any part was observed to fail, whatever else is unknown; None (incomplete, not established) when no
    part failed but some part could not be observed; True only when every part was observed and none failed.
    """
    if observed_failures:
        return False
    if unobserved:
        return None
    return True


def distribution_status(entry):
    """The applicability rule of Section 3: exactly one status, `fits no status`, or INCOMPLETE.

    A field holding INCOMPLETE was not fully observed. The entry fits no status when its observed fields already
    exclude every status, whatever the unobserved ones hold (an observed violation stands); it is INCOMPLETE when
    the unobserved fields could still make it `locked-verified`. INCOMPLETE is never a status and never a pass.
    """
    hashes = entry['lock_hashes']
    wheel, match = entry['wheel_sha256'], entry['wheel_record_match']
    if INCOMPLETE in (wheel, match):
        wheel_possible = wheel == INCOMPLETE or (isinstance(wheel, str) and HEX64.fullmatch(wheel) is not None
                                                 and wheel in hashes)
        could_verify = entry['in_lock'] is True and bool(hashes) and wheel_possible and match in (True, INCOMPLETE)
        return INCOMPLETE if could_verify else 'fits no status'
    if (entry['in_lock'] is True and hashes and isinstance(entry['wheel_sha256'], str)
            and HEX64.fullmatch(entry['wheel_sha256']) and entry['wheel_sha256'] in hashes
            and entry['wheel_record_match'] is True):
        return 'locked-verified'
    if (entry['in_lock'] is True and hashes and entry['wheel_sha256'] == 'not available'
            and entry['wheel_record_match'] == 'not established'):
        return 'locked-wheel-unavailable'
    if (entry['in_lock'] is False and hashes == [] and entry['wheel_sha256'] == 'not applicable: not in lock'
            and entry['wheel_record_match'] == 'not applicable: not in lock'):
        return 'not-in-lock'
    return 'fits no status'


def declared_entry_state(entry, version, wheel_sha256):
    """The declared comparison of an `aiida_core`, `ase` or `numpy` entry: True, False (observed) or None. Pure.

    `wheel_sha256` is None for numpy, whose wheel digest is checked by membership only. A missing entry, an observed
    version or wheel digest that differs, or any status other than locked-verified or INCOMPLETE, fails. An INCOMPLETE
    status with every observed value as declared is None: not established, never a pass and never S10.
    """
    if entry is None or entry['version'] != version:
        return False
    if wheel_sha256 is not None and entry['wheel_sha256'] not in (wheel_sha256, INCOMPLETE):
        return False
    if entry['status'] == INCOMPLETE:
        return None
    if entry['status'] != 'locked-verified':
        return False
    return wheel_sha256 is None or entry['wheel_sha256'] == wheel_sha256


def read_build_identity(lock_bytes, child_env):
    """One reading of every F3 source. Returns (the public `build_identity` value, private detail, failures)."""
    cache = HashCache()
    python = {
        'implementation': platform.python_implementation(),
        'version': platform.python_version(),
        'build': {'python_build': list(platform.python_build()), 'python_compiler': platform.python_compiler()},
        'executable': os.path.relpath(sys.executable, sys.prefix).replace(os.sep, '/'),
        'interpreter_sha256': hash_file(os.path.realpath(sys.executable))[1],
    }
    lock_entries = parse_lock(lock_bytes)
    distributions = read_distributions(lock_entries, cache)
    bash_probe = run_child(['/bin/bash', '--noprofile', '--norc', '-c', 'printf %s "$BASH_VERSION"'], child_env)
    if bash_probe['exit'] != 0:
        raise OperationalError(f'the Bash version probe exited {bash_probe["exit"]}')
    uname = os.uname()
    with open(SYSTEM_VERSION_PLIST, 'rb') as handle:
        plist_bytes = handle.read()
    plist = plistlib.loads(plist_bytes)
    by_name = {}
    for entry in distributions['public']:
        by_name.setdefault(normalize_name(entry['name']), []).append(entry)

    def key_entry(name):
        found = by_name.get(name, [])
        return found[0] if len(found) == 1 else None

    aiida_entry, ase_entry, numpy_entry = key_entry('aiida-core'), key_entry('ase'), key_entry('numpy')
    public = {
        'python': python,
        'distributions': distributions['public'],
        'aiida_core': ({'version': aiida_entry['version'], 'wheel_sha256': aiida_entry['wheel_sha256']}
                       if aiida_entry else None),
        'ase': {'version': ase_entry['version'], 'wheel_sha256': ase_entry['wheel_sha256']} if ase_entry else None,
        'numpy': ({'version': numpy_entry['version'], 'wheel_sha256': numpy_entry['wheel_sha256']}
                  if numpy_entry else None),
        'lock_sha256': sha256_bytes(lock_bytes),
        'bash': {'path': '/bin/bash', 'version': bash_probe['stdout'].decode('utf-8'),
                 'sha256': hash_file('/bin/bash')[1]},
        'operating_system': {
            'sysname': uname.sysname, 'release': uname.release, 'version': uname.version, 'machine': uname.machine,
            'product_name': plist.get('ProductName'), 'product_version': plist.get('ProductVersion'),
            'product_build': plist.get('ProductBuildVersion'), 'plist_sha256': sha256_bytes(plist_bytes)},
        'engine': NA,
        'engine_banner': NA,
        'engine_build_identity': NA,
    }
    failures = {'S10': [], 'S11': []}
    if python['implementation'] != PYTHON_IMPLEMENTATION or python['version'] != PYTHON_VERSION:
        failures['S10'].append(f'python reads {python["implementation"]} {python["version"]}')
    if python['executable'] != 'bin/python' or sys.executable != os.path.join(sys.prefix, 'bin', 'python'):
        failures['S10'].append('sys.executable is not sys.prefix joined with bin/python')
    if os.path.realpath(sys.prefix) != os.path.realpath(ENV):
        failures['S10'].append('sys.prefix is not the declared environment')
    for message in distributions['failures']:
        failures['S11' if 'fits none' in message else 'S10'].append(message)
    unestablished = list(distributions['unestablished'])
    # A permitted status other than locked-verified fails the declared comparison for these three (S10); an entry
    # that fits no status at all is already listed under S11. An entry whose status is INCOMPLETE fails only on what
    # was observed (its version, its recorded wheel digest); otherwise its declared comparison is not established.
    declared_checks = [(label, entry, declared['version'], declared['wheel_sha256'])
                       for label, entry, declared in (('aiida_core', aiida_entry, DECLARED_AIIDA_CORE),
                                                      ('ase', ase_entry, DECLARED_ASE))]
    declared_checks.append(('numpy', numpy_entry, DECLARED_NUMPY_VERSION, None))
    for label, entry, version, wheel in declared_checks:
        state = declared_entry_state(entry, version, wheel)
        if state is False:
            failures['S10'].append(f'{label} is not locked-verified at the declared version'
                                   + (' and wheel digest' if wheel is not None else ''))
        elif state is None:
            unestablished.append(f'{label}: whether it is locked-verified at the declared values is not established')
    if public['lock_sha256'] != LOCK_SHA256:
        failures['S10'].append('lock_sha256 differs from the declared digest')
    private = {
        'resolved_executable_private': os.path.realpath(sys.executable),
        'sys_executable_private': sys.executable,
        'sys_prefix_private': sys.prefix,
        'sys_base_prefix_private': sys.base_prefix,
        'bash_probe': child_summary(bash_probe),
        'distributions_detail': distributions['private'],
        'unlisted_site_packages_files': distributions['unlisted_site_packages_files'],
        'unlisted_enumeration_errors': distributions['unlisted_enumeration_errors'],
        'unlisted_complete': distributions['unlisted_complete'],
        'unestablished': unestablished,
        'dist_info_directories': distributions['dist_info_directories'],
        'distributions_enumerated': distributions['distributions_enumerated'],
        'unparsed_wheel_names': distributions['unparsed_wheel_names'],
        'wheel_file_map_size': len(distributions['wheel_file_map']),
    }
    return public, private, failures, distributions['wheel_file_map']


def read_host_record(child_env):
    """The F7 host record: each value with its source and status; a value not observed is null with a reason."""
    record = {'host_name': {'value': os.uname().nodename, 'source': HOST_SOURCES['host_name'],
                            'status': 'observed'}}
    children = {}
    for key, argv, convert in (('cpu_model', ['/usr/sbin/sysctl', '-n', 'machdep.cpu.brand_string'], str),
                               ('memory_bytes', ['/usr/sbin/sysctl', '-n', 'hw.memsize'], int)):
        result = run_child(argv, child_env)
        children[key] = child_summary(result)
        text = result['stdout'].decode('utf-8', 'replace').rstrip('\n')
        try:
            if result['exit'] != 0 or text == '':
                raise ValueError(f'exit {result["exit"]}, {len(text)} characters of output')
            value = convert(text)
        except ValueError as exc:
            record[key] = {'value': None, 'source': HOST_SOURCES[key], 'status': 'not observed',
                           'reason': str(exc)}
        else:
            record[key] = {'value': value, 'source': HOST_SOURCES[key], 'status': 'observed'}
    count = os.cpu_count()
    if count is None:
        record['logical_cpu_count'] = {'value': None, 'source': HOST_SOURCES['logical_cpu_count'],
                                       'status': 'not observed', 'reason': 'os.cpu_count() returned None'}
    else:
        record['logical_cpu_count'] = {'value': count, 'source': HOST_SOURCES['logical_cpu_count'],
                                       'status': 'observed'}
    return {key: record[key] for key in HOST_SOURCES}, children


# ---------------------------------------------------------------------------------------------------------------
# F1: Git, tracked and untracked files, the environment superset (Section 4).
def read_git_state(rec, tag, diff_commit=None):
    """The declared Git invocations under the declared Git environment, with the Section 4 preconditions."""
    commands = {}

    def git(name, args):
        argv = GIT + list(args)
        proc = subprocess.run(argv, cwd=REPO, env=dict(GIT_ENV), stdin=subprocess.DEVNULL, capture_output=True)
        rec.write_bytes(f'{tag}-git-{name}.stdout', proc.stdout)
        commands[name] = {'argv': argv, 'exit': proc.returncode, 'stdout_sha256': sha256_bytes(proc.stdout),
                          'stdout_bytes': len(proc.stdout), 'stderr': proc.stderr.decode('utf-8', 'replace')}
        if proc.returncode != 0:
            raise OperationalError(f'git {name} exited {proc.returncode}')
        return proc.stdout

    state = {'commands': commands}
    state['git_version'] = git('version', ['--version']).decode('utf-8')
    config = git('config', ['config', '--list', '--show-origin', '-z'])
    state['git_config_sha256'] = sha256_bytes(config)
    state['object_format'] = git('object-format', ['rev-parse', '--show-object-format']).decode('ascii').strip()
    state['git_path_index'] = git('git-path-index', ['rev-parse', '--git-path', 'index']).decode('utf-8').strip()
    state['commit'] = git('commit', ['rev-parse', '--verify', 'HEAD^{commit}']).decode('ascii').strip()
    stage = git('ls-stage', ['ls-files', '--stage', '-z'])
    state['index_state_sha256'] = sha256_bytes(stage)
    debug = git('ls-debug', ['ls-files', '--debug'])
    untracked = git('untracked', ['ls-files', '--others', '--exclude-standard', '-z'])
    commit_for_diff = diff_commit or state['commit']
    state['code_diff'] = git('diff-index', ['diff-index', '-p', '--binary', '--no-color', '--no-ext-diff',
                                            '--no-textconv', '--no-renames', '--src-prefix=a/', '--dst-prefix=b/',
                                            commit_for_diff])
    state['code_diff_sha256'] = sha256_bytes(state['code_diff'])
    state['diff_commit'] = commit_for_diff

    pre = {}
    # Bounded repository configuration and rules.
    parts = config.split(b'\0')
    if parts and parts[-1] == b'':
        parts = parts[:-1]
    entries = []
    for index in range(0, len(parts) - 1, 2):
        origin = parts[index].decode('utf-8', 'replace')
        key = parts[index + 1].decode('utf-8', 'replace').split('\n', 1)[0]
        entries.append((origin, key))
    pre['config_pairs_complete'] = len(parts) % 2 == 0
    pre['config_all_origin_repository'] = all(origin == 'file:.git/config' for origin, _ in entries)
    forbidden = sorted({key for _, key in entries if key.lower() in GIT_FORBIDDEN_KEYS
                        or key.lower().startswith(GIT_FORBIDDEN_PREFIXES)})
    pre['config_no_forbidden_key'] = not forbidden
    state['config_entries'] = len(entries)
    state['config_forbidden_keys'] = forbidden
    # Index entries.
    index_paths, bad_entries = [], []
    for raw in stage.split(b'\0'):
        if not raw:
            continue
        meta, _, path = raw.partition(b'\t')
        fields = meta.split(b' ')
        decoded = path.decode('utf-8', 'surrogateescape')
        if len(fields) != 3 or fields[2] != b'0' or fields[0] == b'160000':
            bad_entries.append(decoded)
        index_paths.append(decoded)
    pre['index_stage0_no_gitlink'] = not bad_entries
    state['index_entries'] = len(index_paths)
    flags = re.findall(r'flags: (\S+)', debug.decode('utf-8', 'replace'))
    pre['debug_flags_all_zero'] = len(flags) == len(index_paths) and all(value == '0' for value in flags)
    state['debug_flags_fields'] = len(flags)
    untracked_paths = [raw.decode('utf-8', 'surrogateescape') for raw in untracked.split(b'\0') if raw]
    state['index_paths'] = index_paths
    state['untracked_paths'] = untracked_paths
    pre['object_format_sha1'] = state['object_format'] == 'sha1'
    pre['git_path_index'] = state['git_path_index'] == '.git/index'
    irregular = []
    for rel in index_paths + untracked_paths:
        try:
            mode = os.lstat(os.path.join(REPO, rel)).st_mode
        except FileNotFoundError:
            irregular.append(f'{rel} (missing)')
            continue
        if not stat.S_ISREG(mode):
            irregular.append(rel)
    pre['index_and_untracked_regular_files'] = not irregular
    state['irregular_paths'] = irregular
    pre['no_info_attributes'] = not os.path.lexists(os.path.join(REPO, '.git', 'info', 'attributes'))
    directories = {''}
    for rel in index_paths + untracked_paths:
        parts_rel = rel.split('/')[:-1]
        for depth in range(1, len(parts_rel) + 1):
            directories.add('/'.join(parts_rel[:depth]))
    attributes = sorted(d or '.' for d in directories
                        if os.path.lexists(os.path.join(REPO, *(d.split('/') if d else []), '.gitattributes')))
    pre['no_gitattributes_on_listed_paths'] = not attributes
    state['gitattributes_found'] = attributes
    with open(os.path.join(REPO, '.git', 'info', 'exclude'), 'rb') as handle:
        state['info_exclude_sha256'] = sha256_bytes(handle.read())
    with open(os.path.join(REPO, '.git', 'index'), 'rb') as handle:
        state['raw_index_sha256'] = sha256_bytes(handle.read())
    state['preconditions'] = pre
    return state


def read_listed_file(rel):
    """(state, bytes) of a listed path: `ok` with its bytes; `missing` (absent or not a regular file: an observed
    difference); or `inaccessible: <error>` (not observed, so no comparison of it can be made)."""
    path = os.path.join(REPO, rel)
    status = file_status(path)
    if status != 'regular':
        return (status if status.startswith('inaccessible') else 'missing'), None
    try:
        with open(path, 'rb') as handle:
            return 'ok', handle.read()
    except OSError as exc:
        return f'inaccessible: {type(exc).__name__}', None


def tracked_file_entries(paths):
    entries = []
    for rel in sorted(paths, key=path_bytes):
        state, data = read_listed_file(rel)
        if data is None:
            entry = {'path': rel, 'bytes': None, 'sha256': None}
            if state != 'missing':
                entry['error'] = state
            entries.append(entry)
            continue
        entries.append({'path': rel, 'bytes': len(data), 'sha256': sha256_bytes(data)})
    return entries


def untracked_file_entries(paths, copy_root=None):
    entries = []
    for rel in sorted(paths, key=path_bytes):
        state, data = read_listed_file(rel)
        if data is None:
            entry = {'path': rel, 'bytes': None, 'sha256': None, 'git_blob': None}
            if state != 'missing':
                entry['error'] = state
            entries.append(entry)
            continue
        if copy_root is not None:
            target = os.path.join(copy_root, *rel.split('/'))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'xb') as handle:
                handle.write(data)
        entries.append({'path': rel, 'bytes': len(data), 'sha256': sha256_bytes(data), 'git_blob': git_blob_id(data)})
    return entries


def entries_unreadable(entries):
    """The listed files that could not be read: not observed, so neither equal nor different."""
    return [entry['path'] for entry in entries if 'error' in entry]


def constant_from_source(source, name):
    """The literal value of a top-level `NAME = <literal>` in Python source, read with `ast`, never executed."""
    tree = ast.parse(source, filename=name)
    values = [ast.literal_eval(node.value) for node in tree.body
              if isinstance(node, ast.Assign) and len(node.targets) == 1
              and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name]
    if len(values) != 1:
        raise ValueError(f'{name} is assigned {len(values)} times at top level')
    return values[0]


# ---------------------------------------------------------------------------------------------------------------
# F4: the sidecar and the stage checks (Section 6).
class SidecarError(Exception):
    pass


def build_sidecar(frozen_bytes):
    """The sidecar of Section 6, built from the frozen file's text by a plain-text parser that does not use ASE."""
    text = frozen_bytes.decode('ascii')
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines = lines[:-1]
    if len(lines) < 2:
        raise SidecarError('the frozen file has no header')
    count = int(lines[0].strip())
    match = re.search(r'(?:^|\s)Properties=(\S+)', lines[1])
    if match is None or match.group(1) != FROZEN_PROPERTIES:
        raise SidecarError('the Properties declaration differs from the declared one')
    atom_lines = lines[2:]
    if len(atom_lines) != count:
        raise SidecarError(f'{len(atom_lines)} atom lines for a declared count of {count}')
    sites = []
    for index, line in enumerate(atom_lines):
        fields = line.split()
        if len(fields) != 7:
            raise SidecarError(f'site {index} has {len(fields)} fields, not the 7 required')
        sites.append({'index': index, 'atom_id': fields[4], 'element': fields[0],
                      'position': [fields[1], fields[2], fields[3]], 'map_num': fields[5],
                      'radical_electrons': fields[6]})
    return serialize_sidecar({'format': SIDECAR_FORMAT, 'source_sha256': sha256_bytes(frozen_bytes), 'sites': sites})


def serialize_sidecar(value):
    return (json.dumps(value, ensure_ascii=True, separators=(',', ':')) + '\n').encode('ascii')


def parse_sidecar(data):
    if data is None:
        raise SidecarError('the sidecar is missing')
    value = json.loads(data.decode('ascii'))
    if not isinstance(value, dict) or list(value) != ['format', 'source_sha256', 'sites']:
        raise SidecarError('the sidecar keys differ from the declared keys and order')
    if value['format'] != SIDECAR_FORMAT or not isinstance(value['source_sha256'], str) \
            or not HEX64.fullmatch(value['source_sha256']):
        raise SidecarError('the sidecar format or source digest is malformed')
    sites = value['sites']
    if not isinstance(sites, list):
        raise SidecarError('the sidecar sites are not a list')
    for index, site in enumerate(sites):
        if not isinstance(site, dict) or list(site) != SIDECAR_SITE_KEYS:
            raise SidecarError(f'site {index} keys differ from the declared keys and order')
        if type(site['index']) is not int or site['index'] != index:
            raise SidecarError(f'site {index} carries index {site["index"]!r}')
        for key in ('atom_id', 'element', 'map_num', 'radical_electrons'):
            if not isinstance(site[key], str):
                raise SidecarError(f'site {index} {key} is not a string')
        position = site['position']
        if not isinstance(position, list) or len(position) != 3 or not all(isinstance(p, str) for p in position):
            raise SidecarError(f'site {index} position is not three strings')
    ids = [site['atom_id'] for site in sites]
    if len(set(ids)) != len(ids):
        raise SidecarError('an atom_id occurs more than once')
    return value


def is_integer_scalar(value):
    if isinstance(value, bool) or type(value).__name__ in ('bool_', 'bool'):
        return False
    return isinstance(value, numbers.Integral)


def view_from_atoms(atoms):
    native = {}
    for key in NATIVE_ARRAYS:
        if key in atoms.arrays:
            native[key] = [value for value in atoms.arrays[key]]
    return {'kind': 'ase.Atoms', 'elements': list(atoms.get_chemical_symbols()),
            'positions': [[float(c) for c in row] for row in atoms.get_positions()], 'native': native}


def view_from_structure(structure):
    elements, positions = [], []
    for site in structure.sites:
        kind = structure.get_kind(site.kind_name)
        elements.append(kind.symbols[0] if len(kind.symbols) == 1 else repr(kind.symbols))
        positions.append([float(c) for c in site.position])
    return {'kind': 'StructureData', 'elements': elements, 'positions': positions, 'native': {}}


def view_from_job_file(data):
    """A job's `w1_structure_in.extxyz`, read as text: species and three positions per line, no native arrays."""
    lines = data.decode('ascii').split('\n')
    if lines and lines[-1] == '':
        lines = lines[:-1]
    count = int(lines[0])
    if lines[1] != 'Properties=species:S:1:pos:R:3' or len(lines) != count + 2:
        raise SidecarError('the job structure file does not have the declared structure')
    elements, positions, texts = [], [], []
    for line in lines[2:]:
        fields = line.split()
        if len(fields) != 4:
            raise SidecarError(f'a job structure line has {len(fields)} fields')
        elements.append(fields[0])
        positions.append([float(f) for f in fields[1:]])
        texts.append(fields[1:])
    return {'kind': 'job input file', 'elements': elements, 'positions': positions, 'native': {},
            'position_texts': texts}


def f4_stage_check(view, sidecar):
    """Site association, native arrays where present, and the fixed-set fixture, for one stage."""
    failures, observed = [], {}
    sites = sidecar['sites']
    if len(view['elements']) != len(sites) or len(view['positions']) != len(sites):
        return [f'{len(view["elements"])} sites against {len(sites)} sidecar sites'], observed
    for index, site in enumerate(sites):
        if view['elements'][index] != site['element']:
            failures.append(f'site {index}: element {view["elements"][index]!r} differs from {site["element"]!r}')
        expected = [float(text) for text in site['position']]
        if [float(c) for c in view['positions'][index]] != expected:
            failures.append(f'site {index}: position differs from the sidecar position strings')
    for key in NATIVE_ARRAYS:
        if key not in view['native']:
            observed[key] = 'absent (non-survival recorded as observed)'
            continue
        values = view['native'][key]
        observed[key] = 'present'
        if len(values) != len(sites):
            failures.append(f'native {key} has {len(values)} values for {len(sites)} sites')
            continue
        for index, value in enumerate(values):
            text = sites[index][key]
            if key == 'atom_id':
                if not isinstance(value, str) or value != text:
                    failures.append(f'site {index}: native atom_id {value!r} differs from {text!r}')
            elif not INT_STRING.fullmatch(text):
                failures.append(f'site {index}: sidecar {key} {text!r} is not a base-10 integer string')
            elif not is_integer_scalar(value) or int(value) != int(text, 10):
                failures.append(f'site {index}: native {key} {value!r} differs from {text!r} or is not an integer')
    ids = [site['atom_id'] for site in sites]
    for atom_id in FIXTURE_ATOM_IDS:
        if ids.count(atom_id) != 1:
            failures.append(f'fixture member {atom_id} found {ids.count(atom_id)} times in the sidecar')
            continue
        index = ids.index(atom_id)
        if view['elements'][index] != sites[index]['element'] or \
                [float(c) for c in view['positions'][index]] != [float(t) for t in sites[index]['position']]:
            failures.append(f'fixture member {atom_id} at site {index} differs')
    return failures, observed


def f4_full_check(view, sidecar_bytes, regeneration):
    """Sidecar carriage against the checker's regeneration, then the stage check of Section 6."""
    if sidecar_bytes is None:
        return ['the sidecar is missing'], {}
    failures = []
    if sidecar_bytes != regeneration:
        failures.append('the sidecar bytes differ from the checker regeneration')
    try:
        sidecar = parse_sidecar(sidecar_bytes)
    except (SidecarError, ValueError) as exc:
        return failures + [f'the sidecar does not parse: {exc}'], {}
    stage_failures, observed = f4_stage_check(view, sidecar)
    return failures + stage_failures, observed


def negative_cases(regeneration):
    """Section 6: six cases on local synthetic data, not AiiDA jobs. Each must fail."""
    base = json.loads(regeneration.decode('ascii'))

    def synthetic_view(sidecar):
        native = {'atom_id': [s['atom_id'] for s in sidecar['sites']],
                  'map_num': [int(s['map_num']) for s in sidecar['sites']],
                  'radical_electrons': [int(s['radical_electrons']) for s in sidecar['sites']]}
        return {'kind': 'synthetic', 'elements': [s['element'] for s in sidecar['sites']],
                'positions': [[float(t) for t in s['position']] for s in sidecar['sites']], 'native': native}

    def index_of(sidecar, atom_id):
        return [s['atom_id'] for s in sidecar['sites']].index(atom_id)

    cases = {}
    # 1. Exchanging D-O1-H1 with D-O2-H1 in the structure.
    view = synthetic_view(base)
    a, b = index_of(base, 'D-O1-H1'), index_of(base, 'D-O2-H1')
    for field in ('elements', 'positions'):
        view[field][a], view[field][b] = view[field][b], view[field][a]
    for key in NATIVE_ARRAYS:
        view['native'][key][a], view['native'][key][b] = view['native'][key][b], view['native'][key][a]
    cases['exchange D-O1-H1 with D-O2-H1'] = f4_full_check(view, regeneration, regeneration)
    # 2. A duplicate atom_id.
    duplicate = copy.deepcopy(base)
    duplicate['sites'][index_of(base, 'D-O2-H1')]['atom_id'] = 'D-O1-H1'
    cases['duplicate atom_id'] = f4_full_check(synthetic_view(base), serialize_sidecar(duplicate), regeneration)
    # 3. A missing sidecar.
    cases['missing sidecar'] = f4_full_check(synthetic_view(base), None, regeneration)
    # 4. A missing fixture member.
    missing = copy.deepcopy(base)
    missing['sites'][index_of(base, 'D-O3')]['atom_id'] = 'D-O3-removed'
    cases['missing fixture member'] = f4_full_check(synthetic_view(base), serialize_sidecar(missing), regeneration)
    # 5. One wrong map_num value in an otherwise complete sidecar.
    wrong = copy.deepcopy(base)
    wrong['sites'][0]['map_num'] = str(int(wrong['sites'][0]['map_num']) + 1)
    cases['one wrong map_num'] = f4_full_check(synthetic_view(base), serialize_sidecar(wrong), regeneration)
    # 6. A permuted map that has been copied: the identity fields are permuted and the native arrays copied from it.
    permuted = copy.deepcopy(base)
    order = list(reversed(range(len(base['sites']))))
    for index, source in enumerate(order):
        for key in ('atom_id', 'map_num', 'radical_electrons'):
            permuted['sites'][index][key] = base['sites'][source][key]
    cases['permuted map that has been copied'] = f4_full_check(synthetic_view(permuted), serialize_sidecar(permuted),
                                                               regeneration)
    return {name: {'failed': bool(failures), 'failures': failures} for name, (failures, _obs) in cases.items()}


# ---------------------------------------------------------------------------------------------------------------
# Module listings and classes (Section 3, "The libraries actually used").
def file_record(path):
    """Type, size, SHA256 and file identity (device and inode, independent of the path's spelling) of one file."""
    try:
        status = os.lstat(path)
    except (FileNotFoundError, NotADirectoryError) as exc:
        return {'exists': False, 'error': type(exc).__name__}
    except OSError as exc:
        return {'exists': None, 'inaccessible': True, 'error': type(exc).__name__}
    identity = [status.st_dev, status.st_ino]
    if stat.S_ISLNK(status.st_mode):
        return {'exists': True, 'type': 'symlink', 'identity': identity}
    if not stat.S_ISREG(status.st_mode):
        return {'exists': True, 'type': 'other', 'identity': identity}
    try:
        size, digest = hash_file(path)
    except OSError as exc:
        return {'exists': True, 'type': 'file', 'inaccessible': True, 'error': type(exc).__name__,
                'identity': identity}
    return {'exists': True, 'type': 'file', 'bytes': size, 'sha256': digest, 'identity': identity,
            'realpath': os.path.realpath(path)}


UNREADABLE = object()


def raw_namespace(obj):
    """The object's own attribute namespace, read through the generic `object.__getattribute__`, so that no
    `__getattr__` or `__getattribute__` defined by the object, its class or its metaclass runs. Only a plain `dict`
    or a mapping proxy is accepted; anything else is `UNREADABLE`."""
    try:
        namespace = object.__getattribute__(obj, '__dict__')
    except Exception:
        return UNREADABLE
    if type(namespace) is dict or type(namespace) is types.MappingProxyType:
        return namespace
    return UNREADABLE


def static_attribute(obj, name):
    """`name` from the object's own namespace (`raw_namespace`), None when absent, `UNREADABLE` when unreadable."""
    namespace = raw_namespace(obj)
    if namespace is UNREADABLE:
        return UNREADABLE
    return namespace.get(name)


def is_str(value):
    """A type test that never looks up `__class__` on the value (unlike `isinstance`)."""
    return issubclass(type(value), str)


def module_listing(modules):
    """One listing of every entry of a one-statement copy of sys.modules, modules and other objects alike.

    For each entry it records the module file named by `__file__`, the cached bytecode file named by `__cached__`
    and the origin named by `__spec__`, read from the entry's own namespace without running any of its code. Every
    entry is then classified (`classify_module`); none is exempted.
    """
    rows = []
    for name in sorted(modules):
        obj = modules[name]
        is_module = issubclass(type(obj), types.ModuleType)
        file, cached = static_attribute(obj, '__file__'), static_attribute(obj, '__cached__')
        spec = static_attribute(obj, '__spec__')
        origin = static_attribute(spec, 'origin') if spec is not None and spec is not UNREADABLE else None
        loader = static_attribute(spec, 'loader') if spec is not None and spec is not UNREADABLE else None
        row = {'name': name,
               'is_module': is_module,
               'object_type': f'{type(obj).__module__}.{type(obj).__qualname__}',
               'file': file if is_str(file) else None,
               'cached': cached if is_str(cached) else None,
               'spec_origin': origin if is_str(origin) else None,
               'namespace': (spec is not None and spec is not UNREADABLE and origin is None
                             and issubclass(type(loader), importlib.machinery.NamespaceLoader))}
        unreadable = [label for label, value in (('__file__', file), ('__cached__', cached), ('__spec__', spec),
                                                 ('origin', origin), ('loader', loader)) if value is UNREADABLE]
        if unreadable:
            row['unreadable_attributes'] = unreadable
        if not is_module:
            owner = static_attribute(obj, '__module__')
            row['defined_in'] = owner if is_str(owner) else None
        if is_str(file):
            row['file_record'] = file_record(os.path.abspath(file))
        if is_str(cached) and os.path.lexists(cached):
            row['cached_record'] = file_record(os.path.abspath(cached))
        rows.append(row)
    return {'modules': rows, 'entries': len(rows), 'non_module_entries': [r['name'] for r in rows
                                                                          if not r['is_module']]}


def classify_module(row, ctx):
    """The four classes of Section 3, in their declared order, for any entry. Returns (class, failures, unknown).

    The class is decided from the entry's attributes and path alone, so it never depends on reading the file.
    `failures` are comparisons observed to fail; `unknown` are comparisons that could not be made because the file's
    type (its `lstat`) or its bytes could not be read. An unreadable file never hides a failure decidable without
    its bytes (its location, whether it is listed or captured, its type when `lstat` succeeded), and never becomes a
    pass or an invented mismatch. An entry that satisfies no declared class, a non-module object included, is
    `unassigned`, which fails.
    """
    if row['spec_origin'] in ('built-in', 'frozen') or row['namespace']:
        return 'no file', [], []
    if row['file'] is None:
        kind = 'module' if row.get('is_module', True) else f'non-module object ({row.get("object_type")})'
        return 'unassigned', [f'a {kind} with no module file that is not built-in, frozen or a namespace module'], []
    path = os.path.normpath(os.path.abspath(row['file']))
    record = row.get('file_record') or {}
    type_known = record.get('exists') is not None
    readable = 'sha256' in record and not record.get('inaccessible')
    not_read = 'the file could not be read'
    failures, unknown = [], []
    if under(path, SITE_PACKAGES):
        if type_known and record.get('type') != 'file':
            return 'environment packages', [f'module file is not a regular file: {record}'], []
        if not type_known:
            unknown.append('whether the module file is a regular file: its type could not be observed')
        listed = ctx.wheel_file_map.get(path)
        if listed is None:
            failures.append('not listed with a non-empty hash in the RECORD of a locked-verified wheel')
        elif not readable:
            unknown.append(f'SHA256 against the wheel RECORD hash: {not_read}')
        elif record['sha256'] != listed['sha256']:
            failures.append('SHA256 differs from the wheel RECORD hash')
        rel = os.path.relpath(path, SITE_PACKAGES).replace(os.sep, '/')
        captured = ctx.capture_environment.get(rel)
        if captured is None:
            failures.append('not a file of the code_private capture')
        elif not readable:
            unknown.append(f'SHA256 against the code_private capture: {not_read}')
        elif captured != record['sha256']:
            failures.append('SHA256 differs from the code_private capture')
        return 'environment packages', failures, unknown
    if under(path, ctx.base_prefix):
        if type_known and record.get('type') != 'file':
            return 'standard library', [f'not a regular file: {record}'], []
        if not type_known:
            unknown.append('whether the module file is a regular file: its type could not be observed')
        if not readable:
            # Section 3 requires the SHA256 of every module file of this class too. Unread, it is not established:
            # never a pass and never a mismatch.
            unknown.append(f'the SHA256 that the standard library class requires: {not_read}')
        return 'standard library', [], unknown
    if under(path, REPO) and not under(path, ENV):
        rel = os.path.relpath(path, REPO).replace(os.sep, '/')
        if rel not in PROJECT_FILES:
            return 'project', [f'{rel} is not one of the project files'], []
        captured = ctx.capture_untracked.get(rel)
        if captured is None or (type_known and record.get('type') != 'file'):
            return 'project', [f'{rel} differs from its F1 capture'], []
        if not readable:
            return 'project', [], [f'{rel}: SHA256 against its F1 capture: {not_read}']
        if captured != record.get('sha256'):
            return 'project', [f'{rel} differs from its F1 capture'], []
        return 'project', [], []
    return 'other location', ['module file outside the classes of Section 3'], []


def listed_file_key(row):
    """The identity of what an entry lists: its file (device and inode), else its normalized path, else its name.

    Registry names and path spellings do not enter a file's identity, so an alias of a file is the same file.
    """
    record = row.get('file_record') or {}
    if record.get('identity') is not None:
        return ('file', record['identity'][0], record['identity'][1])
    if row.get('file') is not None:
        return ('path', os.path.normpath(os.path.abspath(row['file'])))
    return ('name', row['name'])


def module_check_decision(classes, conditions):
    """How a module-class check is recorded, from `check_module_listing`'s result. Pure.

    'stop' when any of `conditions` (S10, and S14 at the run end) has an observed failure, whatever else is unknown;
    'not established' when nothing failed but some entry, file, digest or identity could not be observed; 'pass'
    only when every entry was observed and passed. A check is never a pass while anything it requires is unknown.
    """
    if any(classes[condition] for condition in conditions):
        return 'stop'
    if classes['unestablished']:
        return 'not established'
    return 'pass'


def check_module_listing(listing, ctx, first_listing=None):
    """Class checks of one listing. Returns the S10 and S14 failures, what could not be established, and observations.

    With `first_listing` (the input-point listing), an entry is first listed at the run end when the file it lists,
    identified by `listed_file_key`, was not listed at the input point. A new registry name for a file already
    listed is an alias: recorded as an observation, never as a first listing. When a file's identity could not be
    observed (its `lstat` failed) at either listing, whether it was first listed at the run end is unknown: recorded
    as not established, never as S14 and never as an alias. Every condition decidable from the entry's attributes,
    path or identity is evaluated whether or not the file's bytes could be read; only comparisons of bytes become
    unknown.
    """
    results, failures_s10, failures_s14, aliases, unestablished = [], [], [], [], []
    project_listed = set()
    first_keys, first_names, first_identity_unknown = set(), set(), False
    if first_listing is not None:
        first_keys = {listed_file_key(row) for row in first_listing['modules']}
        first_names = {row['name'] for row in first_listing['modules']}
        # A file listed at the input point without an observed identity may be any later file: an unmatched
        # run-end file cannot then be shown to be new.
        first_identity_unknown = any(row.get('file') is not None and (row.get('file_record') or {}).get('exists')
                                     is None for row in first_listing['modules'])
    for row in listing['modules']:
        module_class, failures, unknown = classify_module(row, ctx)
        record = row.get('file_record') or {}
        if module_class == 'project':
            rel = os.path.relpath(os.path.normpath(row['file']), REPO).replace(os.sep, '/')
            if rel in PROJECT_FILES:
                project_listed.add(rel)
        key = listed_file_key(row)
        if first_listing is None or key in first_keys:
            first_at_run_end = False
        elif row.get('file') is not None and (record.get('exists') is None or first_identity_unknown):
            first_at_run_end = None  # an identity at one of the two listings could not be observed
        else:
            first_at_run_end = True
        if first_listing is not None and first_at_run_end is False and row['name'] not in first_names:
            aliases.append({'name': row['name'], 'class': module_class})
        results.append({'name': row['name'], 'is_module': row.get('is_module', True), 'class': module_class,
                        'failures': failures, 'unknown': unknown, 'first_listed_at_run_end': first_at_run_end})
        attributable = module_class in ('project', 'other location', 'unassigned')
        if first_at_run_end and attributable:
            failures_s14.append(f'{row["name"]} ({module_class}) first listed at the run end: {failures}')
        elif failures:
            failures_s10.append(f'{row["name"]} ({module_class}): {failures}')
        if first_at_run_end is None and attributable:
            unestablished.append(f'{row["name"]} ({module_class}): whether its file was first listed at the run end '
                                 'could not be observed')
        unestablished.extend(f'{row["name"]} ({module_class}): {item}' for item in unknown)
    if sorted(project_listed) != PROJECT_FILES:
        failures_s10.append(f'project module files {sorted(project_listed)} differ from {PROJECT_FILES}')
    counts = {}
    for item in results:
        counts[item['class']] = counts.get(item['class'], 0) + 1
    return {'classes': results, 'class_counts': counts, 'project_files': sorted(project_listed),
            'aliases_first_listed_at_run_end': aliases, 'S10': failures_s10, 'S14': failures_s14,
            'unestablished': unestablished}


# ---------------------------------------------------------------------------------------------------------------
# The runner's context: checks, stops and operational records.
def allowed_conditions(name):
    """The Section 8 conditions that check `name` may fire, from `CHECK_CONDITIONS`."""
    allowed = CHECK_CONDITIONS.get(name, ())
    return (allowed,) if isinstance(allowed, str) else tuple(allowed)


class Context:
    """Every check, stop and operational event of the runner, in the order they were made.

    Each check carries a sequence number and `after_stop`, true when a Section 8 condition had already fired when
    the check was made. A check absent from `checks` was not reached; `not_reached` gives the reason where known.
    Every phase change, check, stop, not-reached reason and operational event is also appended to the runner
    journal as it is recorded, so that it survives a runner killed before it can write its result.
    """

    def __init__(self, rec):
        self.rec = rec
        self._phase = None
        self.checks = {}
        self.stops = []
        self.operational = []
        self.not_reached = {}
        self.sequence = 0
        self.captured = False
        self.capture_incomplete = {}
        self.capture_affected = {'environment': [], 'pycache': []}
        self.capture_pycache_fields = {}
        self.aiida_loaded = False
        self.terminated = None
        self.jobs = {}
        self.inputs = {}
        self.wheel_file_map = {}
        self.capture_environment = {}
        self.capture_untracked = {}
        self.base_prefix = os.path.normpath(sys.base_prefix)
        self.phase = 'start'

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value
        self._journal({'kind': 'phase', 'phase': value})

    def _journal(self, entry):
        entry = dict(entry, time=time.time())
        self.rec.journal(entry)

    def _record(self, name, entry, conditions=(), operational=None):
        """Record one check with every condition it fires and its operational event, as ONE logical event.

        A single journal line carries the check, its stops and its operational event, and is forced to disk before
        any of them enters memory, so the journal holds all of them or none. A snapshot written by a signal handler
        can still fall between the in-memory updates; `reconcile_record` restores from the durable check whatever
        such a snapshot lacks.
        """
        if name in self.checks:
            raise OperationalError(f'check {name} recorded twice')
        self.sequence += 1
        entry.update({'phase': self.phase, 'sequence': self.sequence, 'after_stop': bool(self.stops)})
        stops = []
        for condition in conditions:
            stops.append({'condition': condition, 'description': STOP_CONDITIONS[condition], 'check': name,
                          'phase': self.phase, 'sequence': self.sequence,
                          'after_first_stop': bool(self.stops or stops)})
        if operational is not None:
            operational = dict(operational, phase=operational.get('phase', self.phase))
        self._journal({'kind': 'check', 'name': name, 'entry': entry, 'stops': stops, 'operational': operational})
        self.checks[name] = entry
        self.stops.extend(stops)
        if operational is not None:
            self.operational.append(operational)
        for stop in stops:
            self.rec.progress(f'STOP CONDITION {stop["condition"]} fired at check {name}')

    def add_operational(self, event):
        """Record one operational event (not a Section 8 condition), in memory and in the journal."""
        event = dict(event, phase=event.get('phase', self.phase))
        self.operational.append(event)
        self._journal({'kind': 'operational', 'event': event})

    def check(self, name, condition, passed, detail=None):
        """Record one check. A condition that `CHECK_CONDITIONS` does not allow for this check is a wiring defect."""
        if condition is not None and condition not in allowed_conditions(name):
            raise OperationalError(f'check {name} may not fire {condition}')
        fired = (condition,) if not passed and condition is not None else ()
        self._record(name, {'passed': bool(passed), 'condition': condition, 'detail': detail, 'error': False}, fired)
        return bool(passed)

    def not_established(self, name, detail):
        """A check that could not be made on its evidence: an operational inability, never a pass or a stop."""
        self._record(name, {'passed': False, 'condition': None, 'detail': detail, 'error': True},
                     operational={'check': name, 'not_established': detail})
        self.rec.progress(f'not established: {name}')
        return False

    def skip(self, name, reason):
        """A check whose prerequisite was not reached: it stays not reached, recorded with the reason."""
        self.not_reached[name] = {'phase': self.phase, 'reason': reason}
        self._journal({'kind': 'not_reached', 'name': name, 'reason': self.not_reached[name]})

    def require(self, name, condition, passed, detail=None):
        if not self.check(name, condition, passed, detail):
            raise W1Stop(f'{condition} at {name}')

    def guarded(self, name, condition, function):
        """Run a check function returning (passed, detail); `passed` None means it could not be established.

        A defect in the function is an operational error, not a stop.
        """
        try:
            passed, detail = function()
        except Exception:
            return self.not_established(name, {'checker_error': traceback.format_exc()})
        if passed is None:
            return self.not_established(name, detail)
        return self.check(name, condition, passed, detail)

    def multi(self, name, failures_by_condition, detail=None):
        """One check whose failures may fire several conditions; each failing condition is recorded."""
        for condition in failures_by_condition:
            if condition not in allowed_conditions(name):
                raise OperationalError(f'check {name} may not fire {condition}')
        failing = [cond for cond, items in failures_by_condition.items() if items]
        if not failing:
            return self.check(name, None, True, detail)
        self._record(name, {'passed': False, 'condition': failing, 'detail': detail, 'error': False,
                            'failures': failures_by_condition}, failing)
        return False

    def snapshot(self):
        """Everything recorded so far, for the runner result or a termination record."""
        return {'phase': self.phase, 'checks': self.checks, 'stops': self.stops, 'operational': self.operational,
                'not_reached': self.not_reached, 'terminated': self.terminated,
                'jobs': {label: (node.uuid if node is not None else None) for label, node in self.jobs.items()}}


# ---------------------------------------------------------------------------------------------------------------
# Runner phases.
def phase_interpreter(ctx):
    ctx.phase = 'interpreter record'
    rec = ctx.rec
    with open(os.path.join(RECORDS, '00-launcher-record.json'), 'rb') as handle:
        launcher = json.loads(handle.read())['launcher_record']
    ctx.launcher = launcher
    with open(os.path.join(RECORDS, '01-user-level-before.json'), 'rb') as handle:
        ctx.aiida_baseline = json.loads(handle.read())['observation'].get('.aiida')
    flags = {name: getattr(sys.flags, name) for name in ('ignore_environment', 'no_user_site',
                                                          'dont_write_bytecode', 'isolated', 'safe_path')}
    record = {
        'interpreter_record_at_start': _INTERPRETER_RECORD_AT_START,
        'platform_injected_present': {name: name in _INTERPRETER_RECORD_AT_START for name in PLATFORM_INJECTED},
        'sys_flags': flags,
        'sys_argv': list(sys.argv),
        'sys_executable_private': sys.executable,
        'sys_prefix_private': sys.prefix,
        'sys_base_prefix_private': sys.base_prefix,
        'sys_path_private': list(sys.path),
        'cwd_private': os.getcwd(),
        'pid': os.getpid(),
        'startup_modules': sorted(sys.modules),
    }
    rec.write_json('10-interpreter-record-start.json', record)
    invocation = []
    if os.path.realpath(os.getcwd()) != os.path.realpath(REPO):
        invocation.append('the working directory is not the repository root')
    if sys.executable != ENV_PY:
        invocation.append('sys.executable is not the environment interpreter path')
    if flags['ignore_environment'] != 1 or flags['no_user_site'] != 1:
        invocation.append('the interpreter does not run with -E -s')
    if sys.argv[1:] != ['run']:
        invocation.append(f'unexpected arguments {sys.argv[1:]}')
    if invocation:
        raise OperationalError(f'runner invocation differs from Section 2: {invocation}')
    problems = check_interpreter_record(_INTERPRETER_RECORD_AT_START, launcher)
    ctx.require('interpreter.record_start', 'S02', not problems, problems)
    # Section 4, "The bytecode policy": the flag must read 1. No provenance input exists yet, so a failure here is
    # not S09; the bytecode policy cannot be established, and the runner ends with an operational stop.
    ctx.dont_write_bytecode = flags['dont_write_bytecode']
    if not ctx.check('interpreter.dont_write_bytecode', None, flags['dont_write_bytecode'] == 1,
                     {'dont_write_bytecode': flags['dont_write_bytecode']}):
        raise OperationalError('sys.flags.dont_write_bytecode does not read 1: the bytecode policy of Section 4 '
                               'cannot be established')


def phase_first_reading(ctx):
    ctx.phase = 'first F3 reading'
    rec = ctx.rec
    rec.progress('first F3 reading and host record')
    with open(LOCK_PATH, 'rb') as handle:
        ctx.lock_bytes = handle.read()
    public, private, failures, wheel_file_map = read_build_identity(ctx.lock_bytes, ctx.launcher)
    host, host_children = read_host_record(ctx.launcher)
    env_child = run_child(['/usr/bin/env'], ctx.launcher)
    ctx.build_identity_first = public
    ctx.host_record_first = host
    ctx.wheel_file_map = wheel_file_map
    rec.write_json('11-build-identity-first.json', {'build_identity': public, 'private': private,
                                                    'failures': failures})
    rec.write_json('12-host-record-first.json', {'host_record': host, 'children': host_children})
    rec.write_json('13-runner-children.json', {'usr_bin_env_with_launcher_record': child_summary(env_child)})
    detail = {'statuses': {s: sum(1 for e in public['distributions'] if e['status'] == s)
                           for s in STATUSES + ('fits no status', INCOMPLETE)},
              'unestablished': private['unestablished']}
    if failures['S10'] or failures['S11']:
        ctx.multi('f3.first_reading', {'S10': failures['S10'], 'S11': failures['S11']}, detail)
        raise W1Stop('first F3 reading')
    if private['unestablished']:
        # A file that could not be read, or a directory that could not be enumerated, is not observed: the reading
        # is incomplete, which is an operational inability, never a pass and never S10 or S11.
        ctx.not_established('f3.first_reading', detail)
        raise OperationalError('the first F3 reading could not read or enumerate every required file')
    ctx.multi('f3.first_reading', {'S10': [], 'S11': []}, detail)


def phase_capture(ctx):
    ctx.phase = 'capture point'
    rec = ctx.rec
    rec.progress('capture point reached: Git state, tracked and untracked files')
    git = read_git_state(rec, 'capture')
    ctx.git_capture = git
    pre = dict(git['preconditions'])
    if not all(pre.values()):
        failed = sorted(name for name, ok in pre.items() if not ok)
        rec.write_json('20-capture-record.json', {'preconditions': pre,
                                                  'git': {k: v for k, v in git.items() if k != 'code_diff'}})
        ctx.require('capture.preconditions', 'S06', False, {'failed': failed, 'irregular': git['irregular_paths'],
                                                            'gitattributes': git['gitattributes_found']})
    tracked = tracked_file_entries(git['index_paths'])
    untracked = untracked_file_entries(git['untracked_paths'], copy_root=CAPTURE_UNTRACKED)
    ctx.capture_untracked = {entry['path']: entry['sha256'] for entry in untracked}
    pre['project_files_untracked'] = all(path in ctx.capture_untracked for path in PROJECT_FILES)
    tools_pycache = walk_regular(os.path.join(TOOLS, '__pycache__'))
    project_bytecode = [rel for rel, _s, _d in tools_pycache['rows']
                        if rel.split('.')[0] in ('w1_driver', 'w1_job')]
    # Each precondition is True, False (observed to fail) or None (not observed): a failure observed in one part is
    # kept whatever another part leaves unknown, and an unknown part never reads as a pass.
    pre['project_files_no_cached_bytecode'] = comparison_state(project_bytecode or tools_pycache['links'],
                                                               not tools_pycache['complete'])

    rec.progress('capture point: environment superset (every regular file of site-packages)')
    environment = walk_regular(SITE_PACKAGES, copy_root=CAPTURE_SITE_PACKAGES)
    pre['site_packages_no_symlink'] = comparison_state(environment['links'], not environment['complete'])
    config_walk, tmp_walk = walk_regular(CONFIG_DIR), walk_regular(TMPDIR)
    listing_problems = []
    pycache_fields, pycache_detail = pycache_reading()
    try:
        environment_listing = listing_bytes(tagged('site-packages', environment['rows']))
        pycache = listing_bytes(pycache_fields)
        config_listing = listing_bytes(tagged('aiida-config', config_walk['rows']))
        tmp_listing = listing_bytes(tagged('tmpdir', tmp_walk['rows']))
    except ListingPathError as exc:
        listing_problems.append(str(exc))
        environment_listing = pycache = config_listing = tmp_listing = b''
    pre['listing_paths_serializable'] = not listing_problems
    # Section 4 requires every regular file of site-packages and every file of the three `__pycache__` trees, and
    # the bytes of every listed project file. A root that is absent where one is required, an inaccessible root, an
    # enumeration error or an unreadable file leaves the capture incomplete: not established, never a pass.
    incomplete = {}
    if environment['root'] != 'listed' or environment['errors']:
        incomplete['site-packages'] = {'root': environment['root'], 'errors': environment['errors'][:50]}
    if tools_pycache['root'] == 'inaccessible' or tools_pycache['errors']:
        incomplete['tools/__pycache__'] = {'root': tools_pycache['root'], 'errors': tools_pycache['errors'][:50]}
    for tag, part in (pycache_detail or {}).items():
        if not part['complete']:
            incomplete[f'__pycache__ under {tag}'] = {'root': part['root'], 'errors': part['errors'][:50]}
    unreadable = entries_unreadable(tracked) + entries_unreadable(untracked)
    if unreadable:
        incomplete['listed project files'] = unreadable[:50]
    for name, walked in (('aiida-config', config_walk), ('tmpdir', tmp_walk)):
        if not walked['complete']:
            ctx.add_operational({'event': f'the observed-only {name} listing is incomplete at the capture point',
                                 'root': walked['root'], 'errors': walked['errors'][:50]})
    ctx.capture_incomplete = incomplete
    ctx.capture_environment = {rel: digest for rel, _size, digest in environment['rows']}
    # What the capture could not observe, in full, for the field-by-field comparisons at the run end.
    ctx.capture_affected = {
        'environment': affected_fields('site-packages', environment['errors']),
        'pycache': [prefix for tag, part in pycache_detail.items() for prefix in affected_fields(tag, part['errors'])]}
    ctx.capture_pycache_fields = {field: [size, digest] for field, size, digest in pycache_fields}

    with open(os.path.join(TOOLS, 'w1_job.py'), 'rb') as handle:
        job_source = handle.read()
    if sha256_bytes(job_source) != ctx.capture_untracked.get(JOB_REL):
        raise OperationalError('tools/w1_job.py changed while it was being captured')
    payload_constant = constant_from_source(job_source, 'W1_PAYLOAD')
    fixture_constant = constant_from_source(job_source, 'W1_FIXTURE_DIFF')
    with open(os.path.join(REPO, FROZEN_REL), 'rb') as handle:
        frozen = handle.read()
    tracked_by_path = {entry['path']: entry['sha256'] for entry in tracked}
    code_identity = {
        'commit': git['commit'],
        'object_format': git['object_format'],
        'git_version': git['git_version'],
        'git_environment': dict(GIT_ENV),
        'git_config_sha256': git['git_config_sha256'],
        'info_exclude_sha256': git['info_exclude_sha256'],
        'index_state_sha256': git['index_state_sha256'],
        'raw_index_sha256': git['raw_index_sha256'],
        'tracked_files': tracked,
        'code_diff_sha256': git['code_diff_sha256'],
        'untracked_files': untracked,
        'project_files': list(PROJECT_FILES),
        'environment_listing_sha256': sha256_bytes(environment_listing),
        'pycache_listing_sha256': sha256_bytes(pycache),
        'dont_write_bytecode': ctx.dont_write_bytecode,
        'payload_sha256': sha256_bytes(payload_constant.encode('ascii')),
        'fixture_diff_sha256': FIXTURE_DIFF_SHA256,
        'capture_point': CAPTURE_POINT,
    }
    ctx.code_identity = code_identity
    ctx.capture = {'code_diff': git['code_diff'], 'environment_listing': environment_listing,
                   'pycache_listing': pycache, 'frozen': frozen, 'fixture_constant': fixture_constant,
                   'payload_constant': payload_constant, 'tracked': tracked, 'untracked': untracked,
                   'environment_rows': environment['rows']}
    rec.write_bytes('20-listing-environment.txt', environment_listing)
    rec.write_bytes('20-listing-pycache.txt', pycache)
    rec.write_bytes('20-listing-aiida-config.txt', config_listing)
    rec.write_bytes('20-listing-tmpdir.txt', tmp_listing)
    with open(os.path.join(CAPTURE, 'code_diff.bin'), 'xb') as handle:
        handle.write(git['code_diff'])
    with open(os.path.join(CAPTURE, 'lock.txt'), 'xb') as handle:
        handle.write(ctx.lock_bytes)
    rec.write_json('20-capture-record.json', {
        'code_identity': code_identity,
        'preconditions': pre,
        'git': {k: v for k, v in git.items() if k not in ('code_diff',)},
        'environment': {'files': len(environment['rows']), 'bytes': sum(r[1] for r in environment['rows']),
                        'links': environment['links'], 'irregular': environment['irregular'],
                        'root': environment['root'], 'errors': environment['errors']},
        'incomplete': incomplete,
        'observed_only_listings': {'aiida-config': {'root': config_walk['root'], 'errors': config_walk['errors']},
                                   'tmpdir': {'root': tmp_walk['root'], 'errors': tmp_walk['errors']}},
        'pycache': pycache_detail,
        'tools_pycache_private': {'exists': tools_pycache['exists'], 'root': tools_pycache['root'],
                                  'errors': tools_pycache['errors'], 'files': tools_pycache['rows']},
        'listing_problems': listing_problems,
        'listing_sha256': {'environment': sha256_bytes(environment_listing), 'pycache': sha256_bytes(pycache),
                           'aiida-config': sha256_bytes(config_listing), 'tmpdir': sha256_bytes(tmp_listing)},
        'frozen_input': {'sha256': sha256_bytes(frozen), 'tracked_sha256': tracked_by_path.get(FROZEN_REL)},
        'fixture_constant_sha256': sha256_bytes(fixture_constant),
        'run_area_private': {'capture': CAPTURE, 'records': RECORDS},
    })
    failed = sorted(name for name, ok in pre.items() if ok is False)
    unknown = sorted(name for name, ok in pre.items() if ok is None)
    detail = {'failed': failed, 'unknown': unknown, 'irregular': git['irregular_paths'],
              'gitattributes': git['gitattributes_found'], 'site_packages_links': environment['links'],
              'listing_problems': listing_problems, 'incomplete': incomplete}
    if failed:
        # An observed precondition failure is S06 even if another precondition or the enumeration is unknown. The
        # run-end readings are still made; comparisons against an incomplete capture keep only observed differences.
        ctx.captured = True
        ctx.require('capture.preconditions', 'S06', False, detail)
    if incomplete or unknown:
        ctx.not_established('capture.preconditions', detail)
        raise OperationalError('the capture could not enumerate or read every required file')
    ctx.captured = True
    ctx.check('capture.preconditions', 'S06', True, detail)
    frozen_ok = sha256_bytes(frozen) == FROZEN_SHA256 == tracked_by_path.get(FROZEN_REL)
    ctx.require('capture.frozen_input', 'S12', frozen_ok, {'sha256': sha256_bytes(frozen)})


def phase_aiida_and_jobs(ctx):
    ctx.phase = 'import'
    rec = ctx.rec
    if not sys.path or sys.path[0] != TOOLS:
        sys.path.insert(0, TOOLS)
    rec.progress('importing w1_job (the first import outside the standard library)')
    import w1_job  # noqa: E402  -- the input point follows; see Section 4
    ctx.w1_job = w1_job
    from aiida import load_profile, orm
    from aiida.engine import run_get_node
    from aiida.manage.configuration import create_profile, get_config
    ctx.aiida_loaded = True
    status = aiida_dir_status(ctx.aiida_baseline)
    rec.write_json('30-import.json', {'sys_path_private': list(sys.path), 'w1_job_file_private': w1_job.__file__,
                                      'user_aiida_dir_status': status})
    check_aiida_dir(ctx, 'user_level.aiida_dir_after_import', status, stop=True)

    ctx.phase = 'profile'
    config = get_config(create=True)
    if PROFILE_NAME in config.profile_names:
        raise OperationalError('a profile named w1 already exists in the W1 configuration directory')
    profile = create_profile(config, storage_backend='core.sqlite_dos', storage_config={'filepath': STORAGE},
                             broker_backend=None, broker_config=None, name=PROFILE_NAME,
                             email='w1-wiring-test@localhost.invalid', first_name='W1', last_name='wiring test',
                             institution='project-local')
    config.set_default_profile(PROFILE_NAME, overwrite=True)
    config.store()
    profile = load_profile(PROFILE_NAME, allow_switch=True)
    profile_record = {'name': profile.name, 'storage_backend': profile.storage_backend,
                      'process_control_backend': profile.process_control_backend,
                      'dictionary_private': profile.dictionary, 'config_dirpath_private': config.dirpath}
    rec.write_json('31-profile.json', profile_record)
    if profile.storage_backend != 'core.sqlite_dos' or profile.process_control_backend is not None:
        raise OperationalError('the W1 profile is not core.sqlite_dos without a broker')
    if os.path.realpath(config.dirpath) != os.path.realpath(CONFIG_DIR):
        raise OperationalError('the configuration directory is not the project-local one')

    # The input point: w1_job and everything it imports are loaded and the profile is loaded; no input node exists.
    ctx.phase = 'input point'
    modules_now = sys.modules.copy()
    ctx.listing_input = module_listing(modules_now)
    rec.write_json('32-module-listing-input-point.json', ctx.listing_input)
    rec.progress(f'input point: {len(ctx.listing_input["modules"])} entries listed')
    # Every entry is classified here, before any input node or job exists; an entry that fails its class, or fits
    # none, fires S10 and ends the run before anything is created (Section 3, Section 8).
    classes = check_module_listing(ctx.listing_input, ctx)
    rec.write_json('32-module-classes-input-point.json', classes)
    detail = {'class_counts': classes['class_counts'], 'project_files': classes['project_files'],
              'non_module_entries': ctx.listing_input['non_module_entries'], 'unestablished': classes['unestablished']}
    decision = module_check_decision(classes, ('S10',))
    if decision == 'stop':
        ctx.multi('modules.input_point', {'S10': classes['S10']}, detail)
        raise W1Stop('module classes at the input point')
    if decision == 'not established':
        ctx.not_established('modules.input_point', detail)
        raise OperationalError('a module class check at the input point could not be made: a file or its '
                               'identity could not be read')
    ctx.multi('modules.input_point', {'S10': []}, detail)

    ctx.phase = 'computer and code'
    computer = orm.Computer(label=COMPUTER_LABEL, hostname='localhost',
                            description='W1 wiring test: local transport without a login shell',
                            transport_type='core.local', scheduler_type='core.direct', workdir=WORKDIR)
    computer.set_shebang('#!/bin/bash')
    computer.store()
    computer.configure(use_login_shell=False)
    readback = orm.Computer.collection.get(label=COMPUTER_LABEL)
    configuration = readback.get_configuration()
    computer_record = {'label': readback.label, 'uuid': readback.uuid, 'hostname': readback.hostname,
                       'transport_type': readback.transport_type, 'scheduler_type': readback.scheduler_type,
                       'shebang': readback.get_shebang(), 'workdir_private': readback.get_workdir(),
                       'metadata': readback.metadata, 'authinfo_params': configuration}
    rec.write_json('33-computer-readback.json', computer_record)
    public_record = {k: v for k, v in computer_record.items() if not k.endswith('_private')}
    # S03 fires only when `use_login_shell` reads back true. A missing or non-boolean value cannot establish the
    # no-login setting: an operational stop, not S03.
    login = configuration.get('use_login_shell', '<absent>')
    if login is True:
        ctx.require('computer.readback', 'S03', False, public_record)
    elif login is False:
        ctx.check('computer.readback', 'S03', True, public_record)
    else:
        ctx.not_established('computer.readback', {'use_login_shell': repr(login)})
        raise OperationalError('use_login_shell could not be read back as false')
    declared = {'transport_type': readback.transport_type == 'core.local',
                'scheduler_type': readback.scheduler_type == 'core.direct',
                'shebang': readback.get_shebang() == '#!/bin/bash',
                'workdir': os.path.realpath(readback.get_workdir()) == os.path.realpath(WORKDIR)}
    if not ctx.check('computer.declared_configuration', None, all(declared.values()), declared):
        raise OperationalError('the declared computer configuration of Section 2 could not be established')
    code = orm.InstalledCode(computer=readback, filepath_executable='/bin/bash', label=CODE_LABEL).store()
    ctx.code = code
    rec.write_json('34-code.json', {'label': code.label, 'uuid': code.uuid, 'pk': code.pk,
                                    'filepath_executable': str(code.filepath_executable),
                                    'computer': code.computer.label, 'node_type': code.node_type})

    ctx.phase = 'inputs'
    create_inputs(ctx, orm)
    ctx.phase = 'job 1'
    rec.progress('job 1 starts')
    job1 = run_job(ctx, run_get_node, orm, JOB_LABELS[0], dict(ctx.inputs))
    check_job(ctx, 'job1', job1, ctx.inputs)
    if ctx.terminated is not None:
        raise OperationalError(f'job 1 was interrupted: {ctx.terminated}')
    if ctx.stops:
        rec.progress('job 2 is not started: a Section 8 condition fired at or before job 1')
        raise W1Stop('after job 1')
    if job1 is None or not job1.is_finished_ok:
        rec.progress('job 2 is not started: job 1 did not finish cleanly')
        raise JobSequenceEnded('job 1 did not finish cleanly')
    ctx.phase = 'job 2'
    inputs2 = dict(ctx.inputs)
    inputs2['structure'] = job1.outputs.structure_out
    inputs2['identity'] = job1.outputs.identity_out
    ctx.inputs2 = inputs2
    rec.progress('job 2 starts')
    run_job(ctx, run_get_node, orm, JOB_LABELS[1], inputs2)
    if ctx.terminated is not None:
        raise OperationalError(f'job 2 was interrupted: {ctx.terminated}')


def create_inputs(ctx, orm):
    """Create every input node from the captured bytes and check each equals what was captured."""
    from ase.io import read as ase_read
    rec, w1_job, cap = ctx.rec, ctx.w1_job, ctx.capture
    try:
        regeneration = build_sidecar(cap['frozen'])
    except (SidecarError, ValueError) as exc:
        ctx.require('f4.sidecar_built', 'S12', False, str(exc))
    ctx.regeneration = regeneration
    ctx.check('f4.sidecar_built', 'S12', True)
    negative = negative_cases(regeneration)
    rec.write_json('36-negative-cases.json', negative)
    passing = [name for name, result in negative.items() if not result['failed']]
    ctx.require('negative_cases', 'S13', not passing, {'cases': negative, 'passing': passing})

    atoms = ase_read(io.StringIO(cap['frozen'].decode('ascii')), format='extxyz')
    t0_failures, t0_observed = f4_full_check(view_from_atoms(atoms), regeneration, regeneration)
    ctx.require('f4.T0', 'S12', not t0_failures, {'failures': t0_failures, 'native': t0_observed})

    nodes = {
        'structure': orm.StructureData(ase=atoms),
        'identity': orm.SinglefileData(io.BytesIO(regeneration), filename='w1_identity.json'),
        'fixed_set': orm.List(list(FIXTURE_ATOM_IDS)),
        'units': orm.Dict(copy.deepcopy(UNITS)),
        'code_diff': orm.SinglefileData(io.BytesIO(cap['code_diff']), filename='code_diff.bin'),
        'code_untracked': orm.FolderData(tree=CAPTURE_UNTRACKED),
        'code_private': orm.FolderData(tree=CAPTURE_SITE_PACKAGES),
        'code_identity': orm.Dict(copy.deepcopy(ctx.code_identity)),
        'fixture_diff': orm.SinglefileData(io.BytesIO(w1_job.W1_FIXTURE_DIFF), filename='fixture_diff.patch'),
        'defaults': orm.Dict(copy.deepcopy(DEFAULTS)),
        'build_identity': orm.Dict(copy.deepcopy(ctx.build_identity_first)),
        'lock': orm.SinglefileData(io.BytesIO(ctx.lock_bytes), filename='lock.txt'),
        'host_record': orm.Dict(copy.deepcopy(ctx.host_record_first)),
        'calc_performed': orm.Dict(copy.deepcopy(CALC_PERFORMED)),
        'seed': orm.Str(SEED),
        'per_claim': orm.Dict(copy.deepcopy(PER_CLAIM)),
        'env_policy': orm.Dict(copy.deepcopy(ENV_POLICY)),
    }
    if [port for port, _t, _r in w1_job.W1_INPUT_PORTS] != list(nodes):
        raise OperationalError('the input ports of w1_job differ from the driver input set')
    rec.progress('storing the input nodes (the code_private superset included)')
    for node in nodes.values():
        node.store()
    ctx.inputs = nodes
    ctx.inputs['code'] = ctx.code
    rec.write_json('35-inputs.json', {port: {'uuid': node.uuid, 'pk': node.pk, 'node_type': node.node_type}
                                      for port, node in ctx.inputs.items()})

    f1 = []
    if singlefile_bytes(nodes['code_diff']) != cap['code_diff']:
        f1.append('code_diff differs from the captured diff')
    stored_untracked = node_rows(nodes['code_untracked'])
    if stored_untracked != [(e['path'], e['bytes'], e['sha256']) for e in cap['untracked']]:
        f1.append('code_untracked differs from the captured untracked files')
    stored_listing = listing_bytes(tagged('site-packages', node_rows(nodes['code_private'])))
    if stored_listing != cap['environment_listing']:
        f1.append('code_private differs from the captured environment listing')
    fixture = singlefile_bytes(nodes['fixture_diff'])
    if fixture != cap['fixture_constant'] or sha256_bytes(fixture) != FIXTURE_DIFF_SHA256:
        f1.append('fixture_diff differs from the constant in the captured w1_job.py')
    if canonical_json(nodes['code_identity'].get_dict()) != canonical_json(ctx.code_identity):
        f1.append('code_identity differs from the capture record')
    ctx.require('inputs.f1_equal_capture', 'S06', not f1, f1)

    others = []
    if singlefile_bytes(nodes['identity']) != regeneration:
        others.append('identity differs from the sidecar regeneration')
    if singlefile_bytes(nodes['lock']) != ctx.lock_bytes:
        others.append('lock differs from the bytes read')
    for port, declared in (('units', UNITS), ('defaults', DEFAULTS), ('calc_performed', CALC_PERFORMED),
                           ('per_claim', PER_CLAIM), ('env_policy', ENV_POLICY),
                           ('build_identity', ctx.build_identity_first), ('host_record', ctx.host_record_first)):
        if canonical_json(nodes[port].get_dict()) != canonical_json(declared):
            others.append(f'{port} differs after storage')
    if nodes['fixed_set'].get_list() != FIXTURE_ATOM_IDS or nodes['seed'].value != SEED:
        others.append('fixed_set or seed differs after storage')
    mandatory = mandatory_content_failures(ctx, nodes)
    ctx.require('inputs.mandatory_contents', 'S09', not others and not mandatory,
                {'stored_equality': others, 'mandatory': mandatory})

    s1_failures, s1_observed = f4_full_check(view_from_structure(nodes['structure']),
                                             singlefile_bytes(nodes['identity']), regeneration)
    ctx.require('f4.S1', 'S12', not s1_failures, {'failures': s1_failures, 'native': s1_observed})


def singlefile_bytes(node):
    return node.base.repository.get_object_content(node.filename, mode='rb')


def node_rows(node, prefix=''):
    """(path, size, SHA256) of every file of a node's repository, sorted by path bytes."""
    rows = []
    for root, _dirs, files in node.base.repository.walk():
        for name in files:
            rel = (root / name).as_posix()
            data = node.base.repository.get_object_content(rel, mode='rb')
            rows.append((prefix + rel, len(data), sha256_bytes(data)))
    rows.sort(key=lambda row: path_bytes(row[0]))
    return rows


def run_job(ctx, run_get_node, orm, label, inputs):
    """One job, in-process through run_get_node with no daemon. An exception is recorded, never retried.

    aiida-core's runner turns SIGTERM or SIGINT into a kill of the running process (`aiida/engine/runners.py`
    249-265), so a ceiling termination during a job appears here as a killed job: it is recorded as an operational
    interruption, independently of the job's ordinary checks.
    """
    metadata = {'label': label, 'description': f'W1 provenance wiring test, {label}; software wiring only; '
                                               'no chemistry',
                'options': copy.deepcopy(ctx.w1_job.W1_OPTIONS)}
    exception_text = None
    started = time.time()
    try:
        _results, node = run_get_node(ctx.w1_job.W1Job, **inputs, metadata=metadata)
    except Exception:
        exception_text = traceback.format_exc()
        ctx.rec.progress(f'{label} raised; the job node is looked up and recorded')
        node = find_job_node(orm, label)
    ctx.jobs[label] = node
    record = {'label': label, 'seconds': round(time.time() - started, 3), 'launcher_exception': exception_text}
    if node is None:
        ctx.add_operational({'event': 'no job node exists', 'label': label,
                                'exception': exception_text})
    else:
        record.update(job_record(orm, node))
        if node.is_killed:
            ctx.terminated = f'{label} was killed (runner interrupt)'
            ctx.add_operational({'event': 'job killed', 'label': label,
                                    'process_status': node.process_status})
            ctx.rec.write_json(f'95-{label}-interrupted.json', {'event': ctx.terminated, 'time': time.time(),
                                                               'phase': ctx.phase})
    ctx.rec.write_json(f'40-{label}.json', record)
    ctx.rec.progress(f'{label} ended: exit status {record.get("exit_status")}, state {record.get("process_state")}')
    return node


def find_job_node(orm, label):
    found = orm.QueryBuilder().append(orm.CalcJobNode, filters={'label': label}).all(flat=True)
    return found[0] if len(found) == 1 else None


def job_record(orm, node):
    options = {}
    for name in ('resources', 'withmpi', 'environment_variables', 'environment_variables_double_quotes',
                 'prepend_text', 'append_text', 'custom_scheduler_commands', 'import_sys_environment',
                 'submit_script_filename', 'scheduler_stdout', 'scheduler_stderr', 'parser_name',
                 'additional_retrieve_list', 'max_wallclock_seconds', 'mpirun_extra_params'):
        options[name] = node.get_option(name)
    logs = []
    for log in orm.Log.collection.get_logs_for(node):
        message = log.message
        logs.append({'levelname': log.levelname, 'time': str(log.time), 'bytes': len(message.encode('utf-8')),
                     'sha256': sha256_bytes(message.encode('utf-8')), 'head': message[:400]})
    return {
        'uuid': node.uuid, 'pk': node.pk, 'process_type': node.process_type,
        'process_state': node.process_state.value if node.process_state is not None else None,
        'exit_status': node.exit_status, 'exit_message': node.exit_message,
        'is_finished_ok': node.is_finished_ok, 'is_excepted': node.is_excepted, 'is_killed': node.is_killed,
        'exception': node.exception, 'options': options, 'retrieve_list': node.get_retrieve_list(),
        'remote_workdir_private': node.get_remote_workdir(), 'job_id': node.get_job_id(),
        'scheduler_state': str(node.get_scheduler_state()), 'logs': logs,
    }


def presubmit_reports(orm, node, marker):
    """The `presubmit` reports that W1Job wrote to the job node's log."""
    reports = []
    for log in orm.Log.collection.get_logs_for(node):
        position = log.message.find(marker)
        if position >= 0:
            reports.append(json.loads(log.message[position + len(marker):]))
    return reports


JOB_CHECKS = ('finished_ok', 'process_type', 'links', 'options_and_uuids', 'presubmit', 'binding',
              'submission_inventory', 'payload_record', 'input_manifest', 'f4', 'mandatory_contents')


def job_state(node, reports):
    """The facts about one job on which its checks depend."""
    if node is None:
        return {'exists': False}
    return {'exists': True, 'finished_ok': bool(node.is_finished_ok), 'killed': bool(node.is_killed),
            'excepted': bool(node.is_excepted), 'exit_status': node.exit_status, 'reports': len(reports),
            'report_passed': reports[0].get('passed') if len(reports) == 1 else None,
            'workdir': node.get_remote_workdir() is not None}


def job_check_plan(state):
    """Which per-job checks are made, from the job's actual state. Pure.

    Returns {check: 'make'} or {check: 'not reached: ...' | 'not established: ...'}. A check whose prerequisite was
    never reached stays not reached; a check whose evidence exists but cannot be read consistently is not
    established. Neither is a failure, and neither fires a Section 8 condition.
    """
    if not state.get('exists'):
        return {name: 'not reached: no job node exists' for name in JOB_CHECKS}
    plan = {name: 'make' for name in ('finished_ok', 'process_type', 'links', 'options_and_uuids',
                                      'mandatory_contents')}
    reports = state['reports']
    if reports == 1:
        plan['presubmit'] = 'make'
    elif reports > 1:
        plan['presubmit'] = 'not established: more than one presubmit report exists for one job'
    elif state['finished_ok']:
        plan['presubmit'] = 'not established: the job finished but no presubmit report exists'
    else:
        plan['presubmit'] = 'not reached: presubmit was not reached'
    uploaded = reports == 1 and state['report_passed'] is True and state['workdir']
    for name in ('binding', 'submission_inventory'):
        if state['killed']:
            plan[name] = 'not established: the job was killed'
        elif uploaded:
            plan[name] = 'make'
        elif plan['presubmit'].startswith('not established'):
            plan[name] = 'not established: the presubmit report cannot be attributed'
        else:
            plan[name] = 'not reached: the submission was not uploaded'
    for name in ('payload_record', 'input_manifest', 'f4'):
        plan[name] = 'make' if state['finished_ok'] else ('not reached: the job did not finish cleanly, so its '
                                                          'outputs are not attached')
    return plan


def finished_ok_verdict(state):
    """(passed, Section 8 condition or None, operational) for a job's end state. Pure.

    S08 only for an actual exit status 310, 311 or 312; S04 only when the job excepted because its presubmit
    validation raised (its one report did not pass). A killed or otherwise excepted job is an operational event.
    """
    if state['finished_ok']:
        return True, None, False
    if state['exit_status'] in (310, 311, 312):
        return False, 'S08', False
    if state['excepted'] and state['reports'] == 1 and state['report_passed'] is False:
        return False, 'S04', False
    if state['killed'] or state['excepted']:
        return False, None, True
    return False, None, False


def make_planned(ctx, name, plan_entry, condition, function):
    """Make one planned check, or record why it is not reached or not established."""
    if plan_entry == 'make':
        return ctx.guarded(name, condition, function)
    if plan_entry.startswith('not established'):
        return ctx.not_established(name, plan_entry)
    ctx.skip(name, plan_entry)
    return None


def check_job(ctx, key, node, expected_inputs):
    """Every per-job check of Sections 3, 5 and 6, each made only when its prerequisites exist."""
    from aiida import orm
    from aiida.common.links import LinkType
    w1_job = ctx.w1_job
    reports = presubmit_reports(orm, node, w1_job.PRESUBMIT_MARKER) if node is not None else []
    for index, report in enumerate(reports):
        ctx.rec.write_json(f'41-{key}-presubmit-report-{index + 1}.json', report)
    state = job_state(node, reports)
    plan = job_check_plan(state)
    ctx.rec.write_json(f'41-{key}-check-plan.json', {'state': state, 'plan': plan})
    if not state['exists']:
        for name in JOB_CHECKS:
            ctx.skip(f'{key}.{name}', plan[name])
        return

    passed, condition, operational = finished_ok_verdict(state)
    if operational:
        ctx.add_operational({'event': f'{key} did not finish',
                                'killed': state['killed'], 'excepted': state['excepted'],
                                'exception': node.exception})
    ctx.check(f'{key}.finished_ok', condition, passed,
              {'exit_status': state['exit_status'], 'killed': state['killed'], 'excepted': state['excepted']})
    ctx.check(f'{key}.process_type', 'S05', node.process_type == PROCESS_TYPE, {'process_type': node.process_type})

    def presubmit():
        report = reports[0]
        if report.get('node_uuid') != node.uuid:
            return None, 'the presubmit report names another node'
        detail = {'violations': report.get('violations'), 'script_line_kinds': report.get('script_line_kinds'),
                  'inventory_problems': report.get('inventory_problems'),
                  'enumeration_errors': report.get('enumeration_errors')}
        if report.get('passed') is None:
            return None, detail  # the validation could not be made: not established, never S04
        return report.get('passed') is True, detail
    make_planned(ctx, f'{key}.presubmit', plan['presubmit'], 'S04', presubmit)

    def links():
        incoming = node.base.links.get_incoming(link_type=LinkType.INPUT_CALC).all()
        labels = sorted(triple.link_label for triple in incoming)
        required = sorted([port for port, _t, _r in w1_job.W1_INPUT_PORTS] + ['code'])
        missing = sorted(set(required) - set(labels))
        detail = {'labels': labels, 'missing': missing, 'extra': sorted(set(labels) - set(required))}
        ok = not missing and len(labels) == len(set(labels))
        if key == 'job2':
            job1 = ctx.jobs.get(JOB_LABELS[0])
            created = {} if job1 is None else {
                triple.link_label: triple.node.uuid
                for triple in job1.base.links.get_outgoing(link_type=LinkType.CREATE).all()}
            by_label = {triple.link_label: triple.node.uuid for triple in incoming}
            from_job1 = (by_label.get('structure') == created.get('structure_out')
                         and by_label.get('identity') == created.get('identity_out')
                         and created.get('structure_out') is not None and created.get('identity_out') is not None)
            detail['structure_and_identity_created_by_job1'] = from_job1
            ok = ok and from_job1
        return ok, detail
    make_planned(ctx, f'{key}.links', plan['links'], 'S07', links)

    def options_and_uuids():
        # Section 5: the binding covers the exact inputs, options and code. A difference fails criterion 4; it is
        # not evidence that copies of a submission file differ, so it fires no Section 8 condition.
        problems = []
        incoming = {t.link_label: t.node.uuid
                    for t in node.base.links.get_incoming(link_type=LinkType.INPUT_CALC).all()}
        for port, expected in expected_inputs.items():
            if incoming.get(port) != expected.uuid:
                problems.append(f'input {port} is not the declared node')
        for name, value in w1_job.W1_OPTIONS.items():
            if node.get_option(name) != value:
                problems.append(f'option {name} reads {node.get_option(name)!r}')
        declared_defaults = {'import_sys_environment': True, 'submit_script_filename': '_aiidasubmit.sh',
                             'scheduler_stdout': '_scheduler-stdout.txt', 'scheduler_stderr': '_scheduler-stderr.txt',
                             'parser_name': None}
        for name, value in declared_defaults.items():
            if node.get_option(name) != value:
                problems.append(f'option {name} reads {node.get_option(name)!r}')
        retrieve = node.get_retrieve_list()
        if retrieve is not None and list(retrieve) != list(w1_job.W1_OUTPUT_FILES) + ['_scheduler-stdout.txt',
                                                                                    '_scheduler-stderr.txt']:
            problems.append(f'retrieve list reads {retrieve!r}')
        if node.computer is None or node.computer.label != COMPUTER_LABEL:
            problems.append('the job computer is not w1-local-nologin')
        code_nodes = [t.node for t in node.base.links.get_incoming(link_type=LinkType.INPUT_CALC).all()
                      if t.link_label == 'code']
        if len(code_nodes) != 1 or code_nodes[0].label != CODE_LABEL \
                or str(code_nodes[0].filepath_executable) != '/bin/bash':
            problems.append('the job code is not w1-bash with executable /bin/bash')
        workdir = node.get_remote_workdir()
        if workdir is not None and not under(os.path.realpath(workdir), os.path.realpath(WORKDIR)):
            problems.append('the job work directory is not inside the project-local work area')
        return not problems, problems
    make_planned(ctx, f'{key}.options_and_uuids', plan['options_and_uuids'], None, options_and_uuids)

    job_inputs = {t.link_label: t.node for t in node.base.links.get_incoming(link_type=LinkType.INPUT_CALC).all()}
    binding = {}

    def binding_check():
        binding.update(job_binding(ctx, key, node, reports[0], job_inputs))
        if not binding['established']:
            return None, binding['why_not_established']
        return not binding['copies_differ'], {'copies_differ': binding['copies_differ'][:200]}
    make_planned(ctx, f'{key}.binding', plan['binding'], 'S04', binding_check)

    def inventory_check():
        if not binding.get('established'):
            return None, 'the binding was not established'
        return not binding['incomplete'], {'incomplete': binding['incomplete'][:200],
                                           'expected_files': binding['expected_files']}
    make_planned(ctx, f'{key}.submission_inventory', plan['submission_inventory'], None, inventory_check)

    outputs = {triple.link_label: triple.node
               for triple in node.base.links.get_outgoing(link_type=LinkType.CREATE).all()}
    make_planned(ctx, f'{key}.payload_record', plan['payload_record'], 'S10',
                 lambda: check_payload_record(ctx, singlefile_bytes(outputs['env_record'])))
    make_planned(ctx, f'{key}.input_manifest', plan['input_manifest'], None,
                 lambda: check_input_manifest(ctx, node, outputs['input_manifest'], job_inputs))
    make_planned(ctx, f'{key}.f4', plan['f4'], 'S12', lambda: check_job_f4(ctx, key, node, outputs))
    make_planned(ctx, f'{key}.mandatory_contents', plan['mandatory_contents'], 'S09', lambda: (
        lambda failures: (not failures, failures))(mandatory_content_failures(ctx, job_inputs, outputs)))


def binding_verdict(inventory, generated, reported, stored, work):
    """The three-way byte binding of Section 5 and the declared-inventory completeness, within one job. Pure.

    `inventory` is required by the declared ports and their stored inputs; `generated` are the files aiida-core
    writes; `reported`, `stored` and `work` are the presubmit digests, the node repository and the work directory,
    each {path: (size, SHA256)}, with `work` None when the work directory could not be read.
    - copies_differ (S04): a submission file whose three copies are not byte-identical, one copy absent included;
    - incomplete (criterion 4, no Section 8 condition): a declared or generated file absent from all three copies,
      three identical copies that differ from the declared stored input, or an undeclared file in the submission;
    - established False: the work directory could not be read, so no binding can be made.
    """
    if work is None:
        return {'established': False, 'why_not_established': 'the work directory could not be read',
                'copies_differ': [], 'incomplete': [], 'work_only': []}
    submission = set(reported) | set(stored) | set(inventory) | set(generated)
    copies_differ, incomplete = [], []
    for path in sorted(submission, key=path_bytes):
        copies = [reported.get(path), stored.get(path), work.get(path)]
        present = [tuple(copy_) for copy_ in copies if copy_ is not None]
        if present and (len(present) < 3 or len(set(present)) > 1):
            copies_differ.append(path)
        elif not present:
            incomplete.append(f'absent from all three copies: {path}')
        elif path in inventory and present[0] != tuple(inventory[path]):
            incomplete.append(f'the copies differ from the declared stored input: {path}')
        if present and path not in inventory and path not in generated:
            incomplete.append(f'undeclared file in the submission: {path}')
    work_only = sorted((path for path in work if path not in submission), key=path_bytes)
    return {'established': True, 'copies_differ': copies_differ, 'incomplete': incomplete, 'work_only': work_only}


def work_directory_copy(workdir, digests_of):
    """The work-directory copy of a job's submission, or None with the reason when it was not observed.

    `digests_of` is `w1_job.folder_file_digests`. An absent work directory is observed: every copy in it is absent.
    A directory that could not be enumerated or read completely is not observed: no binding can be made from it,
    and none of its missing rows may be read as a copy that differs.
    """
    if not workdir:
        return None, {'why_not_established': 'no work directory is recorded on the job node'}, []
    rows, irregular, errors = digests_of(workdir)
    if errors:
        return None, {'why_not_established': 'the work directory could not be enumerated or read completely',
                      'errors': errors[:50]}, irregular
    return {path: (size, digest) for path, size, digest in rows}, {}, irregular


def job_binding(ctx, key, node, report, job_inputs):
    """Gather the three copies and the declared inventory of one job and apply `binding_verdict`."""
    w1_job = ctx.w1_job
    reported = {path: (size, digest) for path, size, digest in report['files']}
    stored = w1_job.node_repository_digests(node)
    work, work_detail, work_irregular = work_directory_copy(node.get_remote_workdir(), w1_job.folder_file_digests)
    inventory, inventory_problems = w1_job.expected_submission_inventory(w1_job.port_contents(job_inputs))
    verdict = binding_verdict(inventory, w1_job.GENERATED_FILES, reported, stored, work)
    if work is None:
        verdict['why_not_established'] = work_detail
    verdict['incomplete'] = inventory_problems + verdict['incomplete'] + [
        f'work directory entry that is not a regular file: {path}' for path in work_irregular]
    verdict['expected_files'] = len(inventory)
    allowed_outputs = set(w1_job.W1_OUTPUT_FILES) | {'_scheduler-stdout.txt', '_scheduler-stderr.txt'}
    verdict['unexpected_work_only_files'] = [p for p in verdict['work_only'] if p not in allowed_outputs]
    ctx.rec.write_json(f'42-{key}-binding.json', {
        'reported_files': len(reported), 'stored_files': len(stored),
        'work_files': None if work is None else len(work), 'expected_inventory_sha256':
        w1_job.inventory_sha256(inventory), 'verdict': verdict})
    return verdict


def check_payload_record(ctx, data):
    """The payload-record comparisons of Section 3, for one job."""
    parsed = ctx.w1_job.parse_env_record(data)
    keys, environment = parsed['keys'], parsed['environment']
    bi = ctx.build_identity_first
    problems = []
    if keys['dollar_zero'] != 'w1_payload.sh':
        problems.append(f'dollar_zero reads {keys["dollar_zero"]!r}')
    flags = keys['shell_flags']
    if 'e' not in flags or 'u' not in flags or 'i' in flags:
        problems.append(f'shell_flags reads {flags!r}')
    if keys['login_shell'] != 'off':
        problems.append(f'login_shell reads {keys["login_shell"]!r}')
    if keys['bash_version'] != bi['bash']['version']:
        problems.append('bash_version differs from build_identity.bash.version')
    if keys['bash_path'] != '/bin/bash':
        problems.append(f'bash_path reads {keys["bash_path"]!r}')
    for line_key, os_key in (('uname_s', 'sysname'), ('uname_r', 'release'), ('uname_m', 'machine')):
        if keys[line_key] != bi['operating_system'][os_key]:
            problems.append(f'{line_key} differs from build_identity.operating_system.{os_key}')
    names = [name for name, _ in environment]
    values = dict(environment)
    if len(set(names)) != len(names):
        problems.append('a name occurs twice in the /usr/bin/env output')
    required = ALLOW_LIST + ['OMP_NUM_THREADS']
    allowed = set(required + SHELL_MAINTAINED + PLATFORM_INJECTED)
    missing = [name for name in required if name not in values]
    outside = sorted(name for name in values if name not in allowed)
    if missing:
        problems.append(f'names missing: {missing}')
    if outside:
        problems.append(f'names outside the permitted set: {outside}')
    for name in ALLOW_LIST:
        if name in values and values[name] != ctx.launcher[name]:
            problems.append(f'{name} differs from the launcher record')
    if values.get('OMP_NUM_THREADS') != '1':
        problems.append('OMP_NUM_THREADS is not 1')
    for name in PLATFORM_INJECTED:
        if name in values and values[name] != _INTERPRETER_RECORD_AT_START.get(name):
            problems.append(f'{name} differs from its interpreter-record value')
    present_absent = [name for name in ABSENT_NAMES if name in values]
    if present_absent:
        problems.append(f'names that must be absent are present: {present_absent}')
    return not problems, {'keys': keys, 'names': sorted(names),
                          'platform_injected_present': [n for n in PLATFORM_INJECTED if n in values],
                          'problems': problems}


def check_input_manifest(ctx, node, manifest_node, job_inputs):
    """Criterion 5's additional check: the stored `input_manifest` against the declared inventory and the stored
    submission files. No job exit code is involved, so a failure fires no Section 8 condition."""
    w1_job = ctx.w1_job
    entries = [list(e) for e in manifest_node.get_dict()['entries']]
    inventory, inventory_problems = w1_job.expected_submission_inventory(w1_job.port_contents(job_inputs))
    status, problems = w1_job.classify_manifest(entries, inventory, w1_job.node_repository_digests(node))
    if inventory_problems or status is None:
        return None, {'inventory_problems': inventory_problems, 'problems': problems[:200]}
    return status == 0, {'entries': len(entries), 'classification': status, 'problems': problems[:200]}


def check_job_f4(ctx, key, node, outputs):
    """The F4 checks at this job's stages: its input file, T1 and its output structure, and sidecar carriage."""
    from ase.io import read as ase_read
    regeneration = ctx.regeneration
    retrieved = outputs['retrieved']
    input_file = node.base.repository.get_object_content('w1_structure_in.extxyz', mode='rb')
    output_file = retrieved.base.repository.get_object_content('w1_structure_out.extxyz', mode='rb')
    t1 = ase_read(io.StringIO(output_file.decode('ascii')), format='extxyz')
    identity_in = node.base.repository.get_object_content('w1_identity.json', mode='rb')
    stages = {
        'job input file': view_from_job_file(input_file),
        'T1 (ASE read of the payload copy)': view_from_atoms(t1),
        'structure_out': view_from_structure(outputs['structure_out']),
    }
    results = {}
    failures = []
    for stage, view in stages.items():
        stage_failures, observed = f4_full_check(view, identity_in, regeneration)
        results[stage] = {'failures': stage_failures, 'native': observed}
        failures.extend(f'{stage}: {f}' for f in stage_failures)
    carriage = {'identity input': identity_in == regeneration,
                'identity_out': singlefile_bytes(outputs['identity_out']) == regeneration,
                'retrieved copy': retrieved.base.repository.get_object_content('w1_identity_out.json',
                                                                               mode='rb') == regeneration}
    failures.extend(f'sidecar carriage fails at {name}' for name, ok in carriage.items() if not ok)
    texts = stages['job input file']['position_texts']
    sidecar_positions = [s['position'] for s in json.loads(regeneration.decode('ascii'))['sites']]
    results['position_text_identical_to_frozen_file'] = texts == sidecar_positions
    results['sidecar_carriage'] = carriage
    ctx.rec.write_json(f'43-{key}-f4.json', results)
    return not failures, {'failures': failures[:100]}


def mandatory_content_failures(ctx, inputs, outputs=None):
    """Criterion 5: each stored provenance input against its Section 3 declaration, key by key."""
    failures = []

    def exact(port, declared):
        value = inputs[port].get_dict()
        if not value:
            failures.append(f'{port}: empty mapping')
        if sorted(value) != sorted(declared):
            failures.append(f'{port}: keys {sorted(value)} differ from {sorted(declared)}')
        if canonical_json(value) != canonical_json(declared):
            failures.append(f'{port}: a value differs from its declaration')
        return value

    defaults = exact('defaults', DEFAULTS)
    for name, entry in defaults.items():
        if name == 'engine_defaults':
            continue
        if not isinstance(entry, dict) or sorted(entry) != ['defined_by', 'kind', 'value']:
            failures.append(f'defaults.{name}: entry is not {{value, kind, defined_by}}')
        elif entry['kind'] not in DEFAULT_KINDS or not re.match(
                r'aiida-core 2\.9\.2, aiida/[a-z_/]+\.py, lines \d', entry['defined_by']):
            failures.append(f'defaults.{name}: kind or defined_by malformed')
    exact('calc_performed', CALC_PERFORMED)
    exact('units', UNITS)
    exact('per_claim', PER_CLAIM)
    exact('env_policy', ENV_POLICY)
    if inputs['seed'].value != SEED:
        failures.append('seed is not `none`')

    host = inputs['host_record'].get_dict()
    if sorted(host) != sorted(HOST_SOURCES):
        failures.append(f'host_record keys {sorted(host)} differ')
    for name, source in HOST_SOURCES.items():
        entry = host.get(name)
        if not isinstance(entry, dict):
            failures.append(f'host_record.{name} missing')
            continue
        if entry.get('source') != source or entry.get('status') not in ('observed', 'not observed'):
            failures.append(f'host_record.{name}: source or status differs')
        if entry.get('status') == 'observed' and (sorted(entry) != ['source', 'status', 'value']
                                                  or entry['value'] is None):
            failures.append(f'host_record.{name}: observed without a value, or extra keys')
        if entry.get('status') == 'not observed' and (sorted(entry) != ['reason', 'source', 'status', 'value']
                                                      or entry['value'] is not None or not entry['reason']):
            failures.append(f'host_record.{name}: not observed with a value, or without a reason')

    bi = inputs['build_identity'].get_dict()
    if list(sorted(bi)) != sorted(BUILD_IDENTITY_KEYS):
        failures.append(f'build_identity keys {sorted(bi)} differ')
    python = bi.get('python', {})
    if sorted(python) != sorted(PYTHON_KEYS) or python.get('implementation') != PYTHON_IMPLEMENTATION \
            or python.get('version') != PYTHON_VERSION or python.get('executable') != 'bin/python' \
            or not HEX64.fullmatch(str(python.get('interpreter_sha256'))) \
            or sorted(python.get('build', {})) != ['python_build', 'python_compiler']:
        failures.append('build_identity.python differs from its declaration')
    lock_bytes = singlefile_bytes(inputs['lock'])
    lock_entries = parse_lock(lock_bytes)
    for entry in bi.get('distributions', []):
        if sorted(entry) != sorted(DISTRIBUTION_KEYS):
            failures.append(f'distribution entry keys differ: {sorted(entry)}')
            continue
        key = (normalize_name(entry['name']), entry['version'])
        if entry['in_lock'] is not (key in lock_entries):
            failures.append(f'{entry["name"]}: in_lock differs from the stored lock')
        expected_hashes = lock_entries.get(key, []) if entry['in_lock'] else []
        if entry['lock_hashes'] != expected_hashes or (entry['in_lock'] and not expected_hashes):
            failures.append(f'{entry["name"]}: lock_hashes differ from the stored lock')
        if entry['status'] not in STATUSES or distribution_status(entry) != entry['status']:
            failures.append(f'{entry["name"]}: entry fits none of the three statuses')
        if not HEX64.fullmatch(str(entry['installed_record_sha256'])):
            failures.append(f'{entry["name"]}: installed_record_sha256 malformed')
    by_name = {normalize_name(e['name']): e for e in bi.get('distributions', []) if isinstance(e, dict)}
    for label, name, declared in (('aiida_core', 'aiida-core', DECLARED_AIIDA_CORE), ('ase', 'ase', DECLARED_ASE)):
        entry = by_name.get(name, {})
        if bi.get(label) != declared or entry.get('status') != 'locked-verified' \
                or entry.get('version') != declared['version'] or entry.get('wheel_sha256') != declared['wheel_sha256']:
            failures.append(f'build_identity.{label} differs from its declaration')
    numpy_entry = by_name.get('numpy', {})
    if bi.get('numpy', {}).get('version') != DECLARED_NUMPY_VERSION or numpy_entry.get('status') != 'locked-verified' \
            or bi.get('numpy', {}).get('wheel_sha256') != numpy_entry.get('wheel_sha256') \
            or numpy_entry.get('wheel_sha256') not in numpy_entry.get('lock_hashes', []):
        failures.append('build_identity.numpy differs from its declaration')
    if bi.get('lock_sha256') != LOCK_SHA256 or sha256_bytes(lock_bytes) != LOCK_SHA256:
        failures.append('lock_sha256 differs from the declared digest or from the stored lock')
    bash = bi.get('bash', {})
    if sorted(bash) != ['path', 'sha256', 'version'] or bash.get('path') != '/bin/bash':
        failures.append('build_identity.bash differs from its declaration')
    if sorted(bi.get('operating_system', {})) != sorted(OS_KEYS):
        failures.append('build_identity.operating_system keys differ')
    for name in ('engine', 'engine_banner', 'engine_build_identity'):
        if bi.get(name) != NA:
            failures.append(f'build_identity.{name} is not N/A')

    ci = inputs['code_identity'].get_dict()
    if sorted(ci) != sorted(CODE_IDENTITY_KEYS):
        failures.append(f'code_identity keys {sorted(ci)} differ')
    if ci.get('object_format') != 'sha1' or ci.get('git_environment') != GIT_ENV \
            or ci.get('project_files') != PROJECT_FILES or ci.get('dont_write_bytecode') != 1 \
            or ci.get('fixture_diff_sha256') != FIXTURE_DIFF_SHA256 or ci.get('capture_point') != CAPTURE_POINT:
        failures.append('code_identity: a declared exact value differs')
    for name in ('git_config_sha256', 'info_exclude_sha256', 'index_state_sha256', 'raw_index_sha256',
                 'code_diff_sha256', 'environment_listing_sha256', 'pycache_listing_sha256', 'payload_sha256'):
        if not HEX64.fullmatch(str(ci.get(name))):
            failures.append(f'code_identity.{name} malformed')
    if ci.get('code_diff_sha256') != sha256_bytes(singlefile_bytes(inputs['code_diff'])):
        failures.append('code_identity.code_diff_sha256 differs from the stored code_diff')
    stored_untracked = []
    job_source = None
    for path, size, digest in node_rows(inputs['code_untracked']):
        data = inputs['code_untracked'].base.repository.get_object_content(path, mode='rb')
        stored_untracked.append({'path': path, 'bytes': size, 'sha256': digest, 'git_blob': git_blob_id(data)})
        if path == JOB_REL:
            job_source = data
    if ci.get('untracked_files') != stored_untracked:
        failures.append('code_identity.untracked_files differs from the stored code_untracked')
    listing = listing_bytes(tagged('site-packages', node_rows(inputs['code_private'])))
    if ci.get('environment_listing_sha256') != sha256_bytes(listing):
        failures.append('code_identity.environment_listing_sha256 differs from the stored code_private')
    if job_source is None:
        failures.append('the captured w1_job.py is not in the stored code_untracked')
    elif ci.get('payload_sha256') != sha256_bytes(constant_from_source(job_source, 'W1_PAYLOAD').encode('ascii')):
        failures.append('code_identity.payload_sha256 differs from the payload constant in the captured w1_job.py')
    if outputs is not None and 'input_manifest' in outputs:
        listed = dict(tuple(e) for e in outputs['input_manifest'].get_dict()['entries'])
        if listed.get('w1_payload.sh') != ci.get('payload_sha256'):
            failures.append('code_identity.payload_sha256 differs from the job input manifest digest of w1_payload.sh')
    return failures


# ---------------------------------------------------------------------------------------------------------------
# The run end: second readings and every run-end comparison, then the chain checks and the closure inventory.
def compare_build_identity_run_end(first, second):
    """The run-end comparisons that the F3 table of Section 3 declares, field by field. Pure.

    "Equal at run end" is declared for: `python.implementation`, `.version`, `.build`, `.interpreter_sha256`; each
    distribution's `installed_record_sha256` (matched by normalized name and version); `bash.sha256`; and all eight
    `operating_system` fields. Nothing else is compared between the two readings: in particular a distribution's
    other fields, which the table compares only against the lock, the wheel or a declared value.
    """
    failures = []
    first_python, second_python = first.get('python') or {}, second.get('python') or {}
    for key in ('implementation', 'version', 'build', 'interpreter_sha256'):
        if canonical_json(first_python.get(key)) != canonical_json(second_python.get(key)):
            failures.append(f'python.{key} differs at the run end')
    first_records = {(normalize_name(e['name']), e['version']): e['installed_record_sha256']
                     for e in first.get('distributions') or []}
    second_records = {(normalize_name(e['name']), e['version']): e['installed_record_sha256']
                      for e in second.get('distributions') or []}
    for key in sorted(first_records):
        if INCOMPLETE in (first_records[key], second_records.get(key)):
            continue  # not read at one instant: unknown, never a difference; the reading is incomplete
        if second_records.get(key) != first_records[key]:
            failures.append(f'installed_record_sha256 of {key[0]} {key[1]} differs at the run end')
    if (first.get('bash') or {}).get('sha256') != (second.get('bash') or {}).get('sha256'):
        failures.append('bash.sha256 differs at the run end')
    first_os, second_os = first.get('operating_system') or {}, second.get('operating_system') or {}
    for key in OS_KEYS:
        if first_os.get(key) != second_os.get(key):
            failures.append(f'operating_system.{key} differs at the run end')
    return failures


def compare_host_record_run_end(first, second):
    """Section 3, F7 host record: each observed value is equal at run end. Pure."""
    return [key for key in HOST_SOURCES
            if (first.get(key) or {}).get('status') == 'observed'
            and canonical_json(first.get(key)) != canonical_json(second.get(key))]


def compare_code_identity_run_end(stored, run_end, code_diff_sha256, capture=None, field_states=None):
    """The run-end comparisons of the F1 code identity table (Section 4), on the stored values. Pure.

    Returns (failures, unknown). For a key in `field_states` (a value read by walking or reading files), when the
    stored value equals the capture value the field-by-field state of the capture-to-run-end comparison decides:
    False is an observed difference, None is unknown. When the stored value differs from the capture value, it is
    compared with the run-end value only if that reading was complete and equal to the capture (state True);
    otherwise it is unknown, because a digest of an incomplete reading cannot show a difference.
    """
    pairs = {
        'commit': run_end['commit'], 'git_version': run_end['git_version'],
        'git_config_sha256': run_end['git_config_sha256'], 'info_exclude_sha256': run_end['info_exclude_sha256'],
        'index_state_sha256': run_end['index_state_sha256'], 'tracked_files': run_end['tracked_files'],
        'untracked_files': run_end['untracked_files'],
        'environment_listing_sha256': run_end['environment_listing_sha256'],
        'pycache_listing_sha256': run_end['pycache_listing_sha256'],
    }
    field_states = field_states or {}
    failures, unknown = [], []
    for key, value in pairs.items():
        same = canonical_json(stored.get(key)) == canonical_json(value)
        if key in field_states:
            if canonical_json(stored.get(key)) == canonical_json((capture or {}).get(key)):
                state = field_states[key]
            else:
                state = same if field_states[key] is True else None
        else:
            state = same
        if state is False:
            failures.append(f'code_identity.{key} differs at the run end')
        elif state is None:
            unknown.append(key)
    if stored.get('code_diff_sha256') != code_diff_sha256:
        failures.append('code_identity.code_diff_sha256 differs from the diff produced again at the run end')
    if run_end['object_format'] != 'sha1':
        failures.append('object_format is not sha1 at the run end')
    return failures, unknown


def phase_run_end(ctx):
    ctx.phase = 'run end'
    rec = ctx.rec
    if ctx.aiida_loaded and hasattr(ctx, 'listing_input'):
        modules_now = sys.modules.copy()
        ctx.listing_run_end = module_listing(modules_now)
        rec.write_json('50-module-listing-run-end.json', ctx.listing_run_end)
    rec.progress('run end: second readings')
    interpreter_end = dict(os.environ)
    rec.write_json('53-interpreter-record-end.json', {'interpreter_record_end': interpreter_end})
    problems = check_interpreter_record(interpreter_end, ctx.launcher)
    ctx.check('interpreter.record_end', 'S02', not problems, problems)

    lock_bytes = singlefile_bytes(ctx.inputs['lock']) if 'lock' in ctx.inputs else ctx.lock_bytes
    second, second_private, second_failures, _map = read_build_identity(lock_bytes, ctx.launcher)
    host_second, host_children = read_host_record(ctx.launcher)
    rec.write_json('51-build-identity-run-end.json', {'build_identity': second, 'private': second_private,
                                                      'failures': second_failures})
    rec.write_json('52-host-record-run-end.json', {'host_record': host_second, 'children': host_children})
    run_end_build = compare_build_identity_run_end(ctx.build_identity_first, second)
    build_detail = {'run_end_comparisons_failed': run_end_build, 'second_reading_failures': second_failures,
                    'unestablished': second_private['unestablished']}
    if run_end_build or second_failures['S10'] or second_failures['S11']:
        ctx.multi('runend.build_identity', {'S10': run_end_build + second_failures['S10'],
                                            'S11': second_failures['S11']}, build_detail)
    elif second_private['unestablished']:
        ctx.not_established('runend.build_identity', build_detail)
    else:
        ctx.multi('runend.build_identity', {'S10': [], 'S11': []}, build_detail)
    host_differing = compare_host_record_run_end(ctx.host_record_first, host_second)
    ctx.check('runend.host_record', 'S10', not host_differing, {'differing': host_differing})

    rec.progress('run end: Section 4 comparisons')
    git = read_git_state(rec, 'runend', diff_commit=ctx.code_identity['commit'])
    tracked = tracked_file_entries(git['index_paths'])
    untracked = untracked_file_entries(git['untracked_paths'])
    environment = walk_regular(SITE_PACKAGES)
    pycache_fields, pycache_detail = pycache_reading()
    config_walk, tmp_walk = walk_regular(CONFIG_DIR), walk_regular(TMPDIR)
    comparisons = {}
    listing_problem = None
    try:
        environment_listing = listing_bytes(tagged('site-packages', environment['rows']))
        pycache = listing_bytes(pycache_fields)
        config_listing = listing_bytes(tagged('aiida-config', config_walk['rows']))
        tmp_listing = listing_bytes(tagged('tmpdir', tmp_walk['rows']))
        comparisons['listings_serializable'] = True
    except ListingPathError as exc:
        comparisons['listings_serializable'] = False
        listing_problem = str(exc)
        environment_listing = pycache = config_listing = tmp_listing = b''
    for name, walked in (('aiida-config', config_walk), ('tmpdir', tmp_walk)):
        if not walked['complete']:
            ctx.add_operational({'event': f'the observed-only {name} listing is incomplete at the run end',
                                 'root': walked['root'], 'errors': walked['errors'][:50]})
    rec.write_bytes('54-listing-environment.txt', environment_listing)
    rec.write_bytes('54-listing-pycache.txt', pycache)
    rec.write_bytes('54-listing-aiida-config.txt', config_listing)
    rec.write_bytes('54-listing-tmpdir.txt', tmp_listing)
    ci = ctx.code_identity
    # Every comparison is made component by component and field by field, each True, False (observed to differ) or
    # None (not observed). A difference observed anywhere is kept whatever else is unknown; what an enumeration
    # error or an unreadable file leaves unobserved, at either instant, is never read as equal.
    env_state, env_differing, env_unobserved = compare_listing_fields(
        {f'site-packages/{rel}': [size, digest] for rel, size, digest in ctx.capture['environment_rows']},
        {f'site-packages/{rel}': [size, digest] for rel, size, digest in environment['rows']},
        ctx.capture_affected['environment'] + affected_fields('site-packages', environment['errors']))
    pyc_state, pyc_differing, pyc_unobserved = compare_listing_fields(
        ctx.capture_pycache_fields, {field: [size, digest] for field, size, digest in pycache_fields},
        ctx.capture_affected['pycache'] + [prefix for tag, part in pycache_detail.items()
                                           for prefix in affected_fields(tag, part['errors'])])
    tracked_state, tracked_differing, tracked_unobserved = compare_file_entries(ci['tracked_files'], tracked)
    untracked_state, untracked_differing, untracked_unobserved = compare_file_entries(ci['untracked_files'],
                                                                                      untracked)
    comparisons.update({f'precondition.{name}': bool(ok) for name, ok in git['preconditions'].items()})
    comparisons.update({
        'precondition.site_packages_no_symlink': comparison_state(environment['links'], not environment['complete']),
        'commit': git['commit'] == ci['commit'],
        'object_format': git['object_format'] == 'sha1',
        'git_version': git['git_version'] == ci['git_version'],
        'git_config_sha256': git['git_config_sha256'] == ci['git_config_sha256'],
        'info_exclude_sha256': git['info_exclude_sha256'] == ci['info_exclude_sha256'],
        'index_state_sha256': git['index_state_sha256'] == ci['index_state_sha256'],
        'tracked_files': tracked_state,
        'code_diff_byte_identical': git['code_diff'] == ctx.capture['code_diff'],
        'untracked_files': untracked_state,
        'environment_listing': env_state,
        'pycache_listing': pyc_state,
    })
    fields_detail = {
        'environment_listing': {'differing': env_differing[:200], 'unobserved': env_unobserved[:200]},
        'pycache_listing': {'differing': pyc_differing[:200], 'unobserved': pyc_unobserved[:200]},
        'tracked_files': {'differing': tracked_differing, 'unobserved': tracked_unobserved},
        'untracked_files': {'differing': untracked_differing, 'unobserved': untracked_unobserved}}
    observed_only = {'raw_index_sha256_capture': ci['raw_index_sha256'],
                     'raw_index_sha256_run_end': git['raw_index_sha256'],
                     'aiida_config_listing_sha256': sha256_bytes(config_listing),
                     'tmpdir_listing_sha256': sha256_bytes(tmp_listing)}
    failed = sorted(name for name, ok in comparisons.items() if ok is False)
    unknown = sorted(name for name, ok in comparisons.items() if ok is None)
    rec.write_json('54-capture-run-end.json', {'comparisons': comparisons, 'fields': fields_detail,
                                               'listing_problem': listing_problem, 'observed_only': observed_only,
                                               'preconditions': git['preconditions'],
                                               'git': {k: v for k, v in git.items() if k != 'code_diff'},
                                               'site_packages': {'root': environment['root'],
                                                                 'errors': environment['errors'][:50],
                                                                 'links': environment['links']},
                                               'pycache': pycache_detail})
    detail = {'failed': failed, 'unknown': unknown, 'fields': fields_detail}
    section4 = comparison_state(failed, unknown)
    if section4 is None:
        ctx.not_established('runend.section4', detail)
    else:
        ctx.check('runend.section4', 'S06', section4, detail)

    # S09 concerns stored provenance inputs: their recorded values against the run-end readings. Without the
    # stored input nodes there is nothing to compare, and the check stays not reached.
    if all(port in ctx.inputs for port in ('code_identity', 'build_identity', 'host_record')):
        run_end_values = {
            'commit': git['commit'], 'git_version': git['git_version'],
            'git_config_sha256': git['git_config_sha256'], 'info_exclude_sha256': git['info_exclude_sha256'],
            'index_state_sha256': git['index_state_sha256'], 'tracked_files': tracked,
            'untracked_files': untracked, 'environment_listing_sha256': sha256_bytes(environment_listing),
            'pycache_listing_sha256': sha256_bytes(pycache), 'object_format': git['object_format']}
        # For the four values read by walking or reading files, the field-by-field state decides: an observed
        # difference fails, an unobserved one is unknown (never a failure invented from an incomplete digest).
        field_states = {'environment_listing_sha256': env_state, 'pycache_listing_sha256': pyc_state,
                        'tracked_files': tracked_state, 'untracked_files': untracked_state}
        code_failures, code_unknown = compare_code_identity_run_end(
            ctx.inputs['code_identity'].get_dict(), run_end_values, git['code_diff_sha256'], ci, field_states)
        stored_failures = (
            code_failures
            + compare_build_identity_run_end(ctx.inputs['build_identity'].get_dict(), second)
            + [f'host_record.{key} differs at the run end'
               for key in compare_host_record_run_end(ctx.inputs['host_record'].get_dict(), host_second)])
        unestablished = code_unknown + (['build_identity (second reading incomplete)']
                                        if second_private['unestablished'] else [])
        detail = {'failures': stored_failures, 'unestablished': unestablished}
        state = comparison_state(stored_failures, unestablished)
        if state is None:
            ctx.not_established('runend.mandatory_contents', detail)
        else:
            ctx.check('runend.mandatory_contents', 'S09', state, detail)
    else:
        ctx.skip('runend.mandatory_contents', 'not reached: the provenance input nodes were not created')
    if not ctx.aiida_loaded:
        for name in ('user_level.aiida_dir_at_run_end', 'modules.run_end'):
            ctx.skip(name, 'not reached: AiiDA was not imported')
        return
    run_end_aiida_checks(ctx)


def chain_check_plan(jobs_present, jobs_finished_ok, inputs_present):
    """Which chain-level checks are made at the run end, from what exists. Pure.

    `jobs_present` and `jobs_finished_ok` are (job 1, job 2) pairs of booleans. A check whose prerequisite does not
    exist stays not reached; in particular nothing about job 2 is a failure when job 2 was deliberately not started.
    """
    both = bool(jobs_present[0] and jobs_present[1])
    both_ok = bool(both and jobs_finished_ok[0] and jobs_finished_ok[1])
    no_inputs = 'not reached: the input nodes were not created'
    no_job2 = 'not reached: job 2 was not started'
    return {
        'chain.calcjob_nodes': 'make' if both else no_job2,
        'chain.job2_from_job1': 'make' if both else no_job2,
        'f1.inputs_of_both_jobs': 'make' if both else no_job2,
        'f4.sidecar_carriage': 'make' if both_ok else 'not reached: a job did not finish cleanly or was not started',
        'repository_keys': 'make' if both else 'not reached: the chain of two jobs does not exist',
        'f1.resolve_bytes': 'make' if inputs_present else no_inputs,
        'fixture_diff': 'make' if inputs_present else no_inputs,
    }


def run_end_aiida_checks(ctx):
    from aiida import orm
    from aiida.common.links import LinkType
    from aiida.manage import get_manager
    rec = ctx.rec
    check_aiida_dir(ctx, 'user_level.aiida_dir_at_run_end', aiida_dir_status(ctx.aiida_baseline), stop=False)
    if hasattr(ctx, 'listing_run_end'):
        second = check_module_listing(ctx.listing_run_end, ctx, first_listing=ctx.listing_input)
        rec.write_json('56-module-classes-run-end.json', second)
        detail = {'class_counts': second['class_counts'], 'project_files': second['project_files'],
                  'aliases_first_listed_at_run_end': second['aliases_first_listed_at_run_end'],
                  'first_listed_at_run_end': [c['name'] for c in second['classes'] if c['first_listed_at_run_end']],
                  'unestablished': second['unestablished']}
        decision = module_check_decision(second, ('S10', 'S14'))
        if decision == 'not established':
            ctx.not_established('modules.run_end', detail)
        else:
            ctx.multi('modules.run_end', {'S10': second['S10'], 'S14': second['S14']}, detail)

    job1 = ctx.jobs.get(JOB_LABELS[0])
    job2 = ctx.jobs.get(JOB_LABELS[1])
    if job2 is not None and 'job2.finished_ok' not in ctx.checks:
        check_job(ctx, 'job2', job2, ctx.inputs2)
    inputs_present = 'code_private' in ctx.inputs
    plan = chain_check_plan((job1 is not None, job2 is not None),
                            (bool(job1 is not None and job1.is_finished_ok),
                             bool(job2 is not None and job2.is_finished_ok)), inputs_present)
    rec.write_json('57-chain-check-plan.json', plan)
    if JOB_LABELS[1] not in ctx.jobs:
        for name in JOB_CHECKS:
            ctx.skip(f'job2.{name}', 'not reached: job 2 was not started')

    def calcjob_nodes():
        # Exactly two CalcJob nodes, `w1-job1` and `w1-job2` (criterion 1). A wrong completed chain fails
        # criterion 1; it is not a Section 8 condition.
        nodes = orm.QueryBuilder().append(orm.CalcJobNode).all(flat=True)
        labels = sorted(node.label for node in nodes)
        return labels == sorted(JOB_LABELS), {'labels': labels}
    make_planned(ctx, 'chain.calcjob_nodes', plan['chain.calcjob_nodes'], None, calcjob_nodes)

    def chain_from_job1():
        created = {t.link_label: t.node.uuid for t in job1.base.links.get_outgoing(link_type=LinkType.CREATE).all()}
        incoming = {t.link_label: t.node.uuid
                    for t in job2.base.links.get_incoming(link_type=LinkType.INPUT_CALC).all()}
        ok = (incoming.get('structure') == created.get('structure_out') is not None
              and incoming.get('identity') == created.get('identity_out') is not None)
        return ok, {'job2_structure_from_job1': incoming.get('structure') == created.get('structure_out'),
                    'job2_identity_from_job1': incoming.get('identity') == created.get('identity_out')}
    make_planned(ctx, 'chain.job2_from_job1', plan['chain.job2_from_job1'], 'S07', chain_from_job1)

    def carriage():
        out1 = {t.link_label: t.node for t in job1.base.links.get_outgoing(link_type=LinkType.CREATE).all()}
        out2 = {t.link_label: t.node for t in job2.base.links.get_outgoing(link_type=LinkType.CREATE).all()}
        in2 = {t.link_label: t.node for t in job2.base.links.get_incoming(link_type=LinkType.INPUT_CALC).all()}
        if 'identity_out' not in out1 or 'identity_out' not in out2 or 'structure_out' not in out2 \
                or 'identity' not in in2:
            return None, 'an output or input that sidecar carriage examines does not exist'
        copies = {'job 1 identity': singlefile_bytes(ctx.inputs['identity']),
                  'job 1 identity_out': singlefile_bytes(out1['identity_out']),
                  'job 2 identity': singlefile_bytes(in2['identity']),
                  'job 2 identity_out': singlefile_bytes(out2['identity_out'])}
        equal = {name: data == ctx.regeneration for name, data in copies.items()}
        s3_failures, _obs = f4_full_check(view_from_structure(out2['structure_out']), copies['job 2 identity'],
                                          ctx.regeneration)
        return all(equal.values()) and not s3_failures, {'identical_to_regeneration': equal,
                                                         'S3_failures': s3_failures}
    make_planned(ctx, 'f4.sidecar_carriage', plan['f4.sidecar_carriage'], 'S12', carriage)

    resolver = get_manager().get_profile_storage().get_repository() if inputs_present else None

    def resolve_bytes():
        problems = []
        items = {}
        for port in ('code_diff', 'code_untracked', 'code_private', 'fixture_diff'):
            node = ctx.inputs[port]
            count = 0
            for root, _dirs, files in node.base.repository.walk():
                for name in files:
                    rel = (root / name).as_posix()
                    key = node.base.repository.get_object(rel).key
                    data = resolver.get_object_content(key)
                    count += 1
                    if sha256_bytes(data) != key:
                        problems.append(f'{port}/{rel}: resolved bytes do not hash to their key')
            items[port] = count
        captured = {'code_diff': ctx.capture['code_diff'], 'fixture_diff': ctx.capture['fixture_constant']}
        for port, data in captured.items():
            key = ctx.inputs[port].base.repository.get_object(ctx.inputs[port].filename).key
            if resolver.get_object_content(key) != data:
                problems.append(f'{port}: bytes resolved by digest differ from the capture')
        return not problems, {'files_resolved': items, 'problems': problems[:100]}
    make_planned(ctx, 'f1.resolve_bytes', plan['f1.resolve_bytes'], None, resolve_bytes)

    def inputs_of_both_jobs():
        problems = []
        for label, node in ((JOB_LABELS[0], job1), (JOB_LABELS[1], job2)):
            incoming = {t.link_label: t.node.uuid
                        for t in node.base.links.get_incoming(link_type=LinkType.INPUT_CALC).all()}
            for port in ('code_diff', 'code_untracked', 'code_private', 'code_identity', 'fixture_diff'):
                if incoming.get(port) != ctx.inputs[port].uuid:
                    problems.append(f'{label}: {port} is not the stored F1 node')
        return not problems, problems
    make_planned(ctx, 'f1.inputs_of_both_jobs', plan['f1.inputs_of_both_jobs'], None, inputs_of_both_jobs)

    def fixture_diff():
        node = ctx.inputs['fixture_diff']
        data = singlefile_bytes(node)
        key = node.base.repository.get_object(node.filename).key
        source = ctx.inputs['code_untracked'].base.repository.get_object_content(JOB_REL, mode='rb')
        constant = constant_from_source(source, 'W1_FIXTURE_DIFF')
        checks = {'not_empty': len(data) > 0, 'equals_constant_in_captured_w1_job': data == constant,
                  'resolves_by_digest': resolver.get_object_content(key) == data and key == sha256_bytes(data),
                  'declared_sha256': sha256_bytes(data) == FIXTURE_DIFF_SHA256, 'bytes': len(data) == 94}
        return all(checks.values()), checks
    make_planned(ctx, 'fixture_diff', plan['fixture_diff'], 'S15', fixture_diff)

    if job1 is not None or job2 is not None:
        rec.progress('run end: closure inventory and repository keys')
        if plan['repository_keys'] == 'make':
            ctx.guarded('repository_keys', None, lambda: closure_inventory(ctx, orm, LinkType))
        else:
            # The inventory of what exists is still frozen as evidence; criterion 6 stays not reached.
            try:
                closure_inventory(ctx, orm, LinkType)
            except Exception:
                ctx.add_operational({'event': 'closure inventory failed',
                                        'traceback': traceback.format_exc()})
            ctx.skip('repository_keys', plan['repository_keys'])


def closure_inventory(ctx, orm, LinkType):
    """Every node, link, repository object and digest of the chain (Section 9). Frozen before any review."""
    nodes, links = {}, []

    def describe(node, role):
        if node.uuid in nodes:
            nodes[node.uuid]['roles'].append(role)
            return
        objects = []
        for root, _dirs, files in node.base.repository.walk():
            for name in files:
                rel = (root / name).as_posix()
                data = node.base.repository.get_object_content(rel, mode='rb')
                key = node.base.repository.get_object(rel).key
                objects.append({'path': rel, 'bytes': len(data), 'sha256': sha256_bytes(data), 'key': key,
                                'key_equals_sha256': key == sha256_bytes(data)})
        objects.sort(key=lambda o: path_bytes(o['path']))
        nodes[node.uuid] = {'roles': [role], 'pk': node.pk, 'node_type': node.node_type, 'label': node.label,
                            'process_type': getattr(node, 'process_type', None),
                            'attributes_sha256': sha256_bytes(canonical_json(node.base.attributes.all)),
                            'repository_objects': objects}

    for label in JOB_LABELS:
        job = ctx.jobs.get(label)
        if job is None:
            continue
        describe(job, label)
        for triple in job.base.links.get_incoming().all():
            describe(triple.node, f'{label} input {triple.link_label}')
            links.append({'source': triple.node.uuid, 'target': job.uuid, 'type': triple.link_type.value,
                          'label': triple.link_label})
        for triple in job.base.links.get_outgoing().all():
            describe(triple.node, f'{label} output {triple.link_label}')
            links.append({'source': job.uuid, 'target': triple.node.uuid, 'type': triple.link_type.value,
                          'label': triple.link_label})
    inventory = {'format': 'w1-closure-inventory-1', 'nodes': nodes,
                 'links': sorted(links, key=lambda l: (l['source'], l['target'], l['label']))}
    digest = ctx.rec.write_json('60-closure-inventory.json', inventory)
    ctx.closure_inventory_sha256 = digest
    bad = [f'{uuid}:{o["path"]}' for uuid, n in nodes.items() for o in n['repository_objects']
           if not o['key_equals_sha256']]
    objects = sum(len(n['repository_objects']) for n in nodes.values())
    return bool(nodes) and not bad, {'nodes': len(nodes), 'repository_objects': objects, 'key_mismatches': bad[:50],
                                     'closure_inventory_file_sha256': digest}


def persist_interruption(rec, ctx, signum):
    """Write everything recorded so far, independently of the runner result, when the runner is interrupted."""
    try:
        record = dict(ctx.snapshot())
        record.update({'format': 'w1-runner-interrupted-1', 'signal': signum, 'time': time.time()})
        rec.write_json('94-runner-interrupted.json', record)
    except Exception:
        rec.progress('the interruption record could not be written')


def run():
    """The runner, in the order of Sections 2 to 5. On a stop: retain everything, repair nothing, rerun nothing."""
    rec = Recorder(RECORDS)
    if not os.path.isfile(os.path.join(RECORDS, '00-launcher-record.json')):
        print('the runner is started only by the launcher', file=sys.stderr)
        return 3
    ctx = Context(rec)

    def terminated(signum, _frame):
        # Reached only outside a running AiiDA process: aiida-core replaces this handler while a process runs and
        # turns the signal into a kill of that process, which `run_job` records.
        ctx.terminated = f'signal {signum} during phase {ctx.phase}'
        rec.progress(f'runner terminated by signal {signum} during phase {ctx.phase}')
        persist_interruption(rec, ctx, signum)
        os._exit(128 + signum)
    signal.signal(signal.SIGTERM, terminated)

    rec.progress('runner started')
    ended = None
    try:
        phase_interpreter(ctx)
        phase_first_reading(ctx)
        phase_capture(ctx)
        phase_aiida_and_jobs(ctx)
        ended = 'the job sequence completed'
    except W1Stop as stop:
        ended = f'Section 8 stop: {stop}'
        rec.progress(f'stopped: {stop}')
    except JobSequenceEnded as stop:
        ended = f'job sequence ended without a Section 8 condition: {stop}'
        rec.progress(ended)
    except Exception:
        ended = f'operational error during phase {ctx.phase}'
        ctx.add_operational({'traceback': traceback.format_exc()})
        rec.progress(ended)
    phase_before_run_end = ctx.phase
    if ctx.terminated is not None:
        persist_interruption(rec, ctx, None)
        rec.progress('the run end is not made: the runner was interrupted')
    elif ctx.captured:
        try:
            phase_run_end(ctx)
        except Exception:
            ctx.add_operational({'phase': 'run end', 'traceback': traceback.format_exc()})
            rec.progress('operational error during the run end')
    result = dict(ctx.snapshot())
    result.update({
        'format': 'w1-runner-result-2',
        'ended': ended,
        'phase_reached': phase_before_run_end,
        'run_end_made': bool(ctx.captured and ctx.terminated is None),
        'closure_inventory_sha256': getattr(ctx, 'closure_inventory_sha256', None),
    })
    rec.write_json('90-runner-result.json', result)
    rec.progress('runner finished')
    if ctx.operational:
        return 2
    return 1 if ctx.stops or not all(c['passed'] for c in ctx.checks.values()) else 0


# ---------------------------------------------------------------------------------------------------------------
# The launcher (standard library only).
def evaluate(checks, not_reached=None, interrupted=False):
    """The status of each Section 7 criterion from the recorded checks. Pure.

    - unmet: a check of the criterion failed;
    - not established: a check could not be made on its evidence (an operational inability or checker defect);
    - interrupted (unknown): the run was interrupted and a check was neither recorded nor recorded as not reached,
      so whether its work was done is unknown; never reported as genuinely not reached;
    - not reached: a check recorded as not reached, a check never made in a run that ended normally, or a check made
      only after a Section 8 condition had fired, whose work is not credited (evidence retained, never credit);
    - demonstrated: every check was made before any Section 8 condition and passed.
    """
    not_reached = not_reached or {}
    criteria = {}
    for number, names in CRITERIA.items():
        missing = [name for name in names if name not in checks]
        unknown = [name for name in missing if interrupted and name not in not_reached]
        unreached = [name for name in missing if name not in unknown]
        errors = [name for name in names if name in checks and checks[name].get('error')]
        failed = [name for name in names if name in checks and not checks[name]['passed']
                  and not checks[name].get('error')]
        after_stop = [name for name in names if name in checks and checks[name]['passed']
                      and checks[name].get('after_stop')]
        if failed:
            status = 'unmet'
        elif errors:
            status = 'not established'
        elif unknown:
            status = 'interrupted (unknown)'
        elif unreached or after_stop:
            status = 'not reached'
        else:
            status = 'demonstrated'
        criteria[number] = {'status': status, 'failed': failed, 'not_established': errors, 'not_reached': unreached,
                            'interrupted_unknown': unknown, 'passed_after_a_stop_not_credited': after_stop}
    return criteria


def classify_outcome(conditions, operational, ceiling, criteria):
    """The W1 outcome. Pure. A Section 8 condition is never confused with an operational stop, and neither is a
    pass; a pass needs every criterion demonstrated, no condition, no operational event and no ceiling."""
    if conditions:
        return 'STOPPED: Section 8 condition(s) ' + ', '.join(conditions)
    if ceiling:
        return 'OPERATIONAL STOP: the wall-clock ceiling was reached (not a Section 8 condition)'
    if operational:
        return 'OPERATIONAL STOP (not a Section 8 condition)'
    if all(c['status'] == 'demonstrated' for c in criteria.values()):
        return 'PASS (software wiring evidence only)'
    return 'FAILED: a criterion is unmet or not reached without a Section 8 condition'


def read_runner_record(name):
    """(record, problem) for one runner snapshot: (None, None) when it does not exist; (record, None) when it parses
    as a snapshot; (None, problem) when it exists but cannot be read, does not parse (a write cut off by a kill), or
    lacks the fields of a snapshot. An unusable record stays on disk as it is and is reported as operational
    evidence; it never blocks another source and never stands for normal completion."""
    path = os.path.join(RECORDS, name)
    try:
        with open(path, 'rb') as handle:
            data = handle.read()
    except FileNotFoundError:
        return None, None
    except OSError as exc:
        return None, {'record': name, 'problem': f'unreadable: {type(exc).__name__}'}
    try:
        record = json.loads(data)
        if not (isinstance(record, dict) and isinstance(record.get('checks'), dict)
                and isinstance(record.get('stops'), list) and isinstance(record.get('operational'), list)):
            raise ValueError('not a runner snapshot: checks, stops or operational missing or of the wrong type')
    except ValueError as exc:
        return None, {'record': name, 'problem': f'malformed: {exc}', 'bytes': len(data),
                      'sha256': sha256_bytes(data)}
    return record, None


def journal_snapshot(path):
    """Rebuild the checks, stops, operational events, not-reached reasons and last phase from the runner journal.

    Reads one file. A line that does not parse (an entry being written when the runner was killed) is counted and
    ignored: the check it carried is then unknown, never a pass. Returns None when there is no journal; a journal
    that cannot be read gives an empty snapshot carrying the error.
    """
    snapshot = {'checks': {}, 'stops': [], 'operational': [], 'not_reached': {}, 'phase': None, 'entries': 0,
                'unreadable_lines': 0, 'error': None}
    try:
        handle = open(path, 'rb')
    except FileNotFoundError:
        return None
    except OSError as exc:
        snapshot['error'] = type(exc).__name__
        return snapshot
    with handle:
        for raw in handle:
            try:
                entry = json.loads(raw)
            except ValueError:
                snapshot['unreadable_lines'] += 1
                continue
            snapshot['entries'] += 1
            kind = entry.get('kind')
            if kind == 'phase':
                snapshot['phase'] = entry.get('phase')
            elif kind == 'check':
                snapshot['checks'][entry['name']] = entry['entry']
                snapshot['stops'].extend(entry.get('stops') or [])
                if entry.get('operational') is not None:
                    snapshot['operational'].append(entry['operational'])
            elif kind == 'operational':
                snapshot['operational'].append(entry['event'])
            elif kind == 'not_reached':
                snapshot['not_reached'][entry['name']] = entry['reason']
    return snapshot


def merge_records(source, journal):
    """The chosen runner record completed from the journal. Pure.

    Adds every check, stop, operational event and not-reached reason that the journal holds and `source` lacks;
    removes and changes nothing. `source` may be None. Returns the merged record and what was added.
    """
    merged = {'checks': dict((source or {}).get('checks') or {}), 'stops': list((source or {}).get('stops') or []),
              'operational': list((source or {}).get('operational') or []),
              'not_reached': dict((source or {}).get('not_reached') or {}),
              'added': {'checks': [], 'stops': 0, 'operational': 0, 'not_reached': []}}
    if journal is None:
        return merged
    for name, entry in journal['checks'].items():
        if name not in merged['checks']:
            merged['checks'][name] = entry
            merged['added']['checks'].append(name)
    present = {(stop.get('check'), stop.get('condition')) for stop in merged['stops']}
    for stop in journal['stops']:
        if (stop.get('check'), stop.get('condition')) not in present:
            merged['stops'].append(stop)
            present.add((stop.get('check'), stop.get('condition')))
            merged['added']['stops'] += 1
    events = {canonical_json(event) for event in merged['operational']}
    for event in journal['operational']:
        if canonical_json(event) not in events:
            merged['operational'].append(event)
            events.add(canonical_json(event))
            merged['added']['operational'] += 1
    for name, reason in journal['not_reached'].items():
        if name not in merged['not_reached']:
            merged['not_reached'][name] = reason
            merged['added']['not_reached'].append(name)
    merged['stops'].sort(key=lambda stop: stop_order(stop, merged['checks']))
    return merged


def check_conditions(entry):
    """The conditions a recorded check fired, in the order the runner fired them. Pure."""
    condition = (entry or {}).get('condition')
    if condition is None:
        return []
    return [condition] if isinstance(condition, str) else list(condition)


def stop_order(stop, checks):
    """The chronological position of a stop, as the runner wrote it: its check's sequence, then the position of its
    condition among the conditions that check fired. Pure."""
    entry = checks.get(stop.get('check')) or {}
    conditions = check_conditions(entry)
    position = conditions.index(stop.get('condition')) if stop.get('condition') in conditions else 0
    sequence = entry.get('sequence', stop.get('sequence'))
    return (sequence if sequence is not None else 0, position)


def reconcile_record(checks, stops, operational):
    """Restore every stop and operational event that a durably recorded check implies but the record lacks. Pure.

    A failed check names its conditions in `condition` (a string, or a list for `multi`, in firing order); each must
    have a stop entry for that check and condition. A check that could not be made (`error`) must have its
    operational event. A missing one is rebuilt from the check and marked `reconstructed_from`; nothing recorded is
    removed or changed. Chronology follows the runner's writer (`Context._record`): stops are ordered by the check's
    sequence and then by the condition's position within the check, and a rebuilt stop is `after_first_stop` exactly
    when any stop precedes it in that order, an earlier condition of the same check included, or when its check was
    itself made after a stop. Returns (stops, operational, reconstructed).
    """
    stops, operational, reconstructed = list(stops), list(operational), []
    present = {(stop.get('check'), stop.get('condition')) for stop in stops}
    with_event = {event.get('check') for event in operational if 'not_established' in event}
    for name, entry in sorted(checks.items(), key=lambda item: item[1].get('sequence', 0)):
        if entry.get('error'):
            if name not in with_event:
                operational.append({'check': name, 'not_established': entry.get('detail'),
                                    'phase': entry.get('phase'), 'reconstructed_from': 'durable not-established check'})
                reconstructed.append({'check': name, 'operational': True})
            continue
        if entry.get('passed'):
            continue
        for item in check_conditions(entry):
            if (name, item) in present:
                continue
            stop = {'condition': item, 'description': STOP_CONDITIONS.get(item), 'check': name,
                    'phase': entry.get('phase'), 'sequence': entry.get('sequence'),
                    'reconstructed_from': 'durable failed check'}
            position = stop_order(stop, checks)
            earlier = any(stop_order(other, checks) < position for other in stops)
            stop['after_first_stop'] = bool(entry.get('after_stop')) or earlier
            stops.append(stop)
            present.add((name, item))
            reconstructed.append({'check': name, 'condition': item})
    stops.sort(key=lambda stop: stop_order(stop, checks))
    return stops, operational, reconstructed


def finalize(rec, launcher_problems, before, after, runner_exit, ceiling=None):
    """The W1 result from the most complete durable runner record, the launcher's own checks and the ceiling.

    Source order: the runner result (written at the runner's end), then the interruption snapshot (written by the
    runner's SIGTERM handler or after a killed job), then the journal (appended as each item was recorded, so it
    survives SIGKILL). When the runner was started but its own result is missing (whatever ended it, the ceiling
    included), the run counts as interrupted: a check neither recorded nor recorded as not reached is
    `interrupted (unknown)`, because work in progress when the runner ended cannot be told from work never begun.
    With the runner's result present its account is complete, and a check it does not hold was not reached.
    """
    runner, runner_problem = read_runner_record('90-runner-result.json')
    interrupted, interrupted_problem = read_runner_record('94-runner-interrupted.json')
    journal = journal_snapshot(os.path.join(RECORDS, JOURNAL))
    record_problems = [problem for problem in (runner_problem, interrupted_problem) if problem is not None]
    if runner is not None:
        source, record_source = runner, '90-runner-result.json'
    elif interrupted is not None:
        source, record_source = interrupted, '94-runner-interrupted.json'
    elif journal is not None:
        source, record_source = journal, JOURNAL
    else:
        source, record_source = None, None
    runner_started = (runner_exit is not None or ceiling is not None or interrupted is not None
                      or journal is not None or bool(record_problems))
    run_interrupted = runner is None and runner_started
    # Every valid durable source yields the same conditions: the chosen snapshot is completed from the journal, and
    # every stop or operational event that a durable failed or not-established check implies is restored.
    merged = merge_records(source, journal if source is not journal else None)
    checks, stops, operational = merged['checks'], merged['stops'], merged['operational']
    stops, operational, reconstructed = reconcile_record(checks, stops, operational)
    for problem in record_problems:
        operational.append(dict(problem, phase='launcher', event='a runner record could not be used'))
    sequence = max([c.get('sequence', 0) for c in checks.values()] + [0])
    if interrupted is not None:
        operational.append({'phase': interrupted.get('phase'), 'event': 'runner interrupted',
                            'signal': interrupted.get('signal')})
    if ceiling is not None:
        operational.append({'phase': 'launcher', 'event': 'wall-clock ceiling reached', 'ceiling': ceiling})
    checks['launcher.record'] = {'passed': not launcher_problems, 'condition': 'S02', 'detail': launcher_problems,
                                 'error': False, 'phase': 'launcher', 'sequence': 0, 'after_stop': False}
    if launcher_problems:
        stops.insert(0, {'condition': 'S02', 'description': STOP_CONDITIONS['S02'], 'check': 'launcher.record',
                         'phase': 'launcher', 'after_first_stop': False})
    if after is not None:
        comparison = compare_user_level(before, after)
        after_stop = bool(stops)
        fired = bool(comparison['differing']) or comparison['aiida_dir_appeared'] is True
        if fired:
            checks['user_level'] = {'passed': False, 'condition': 'S01', 'detail': comparison, 'error': False,
                                    'phase': 'launcher', 'sequence': sequence + 1, 'after_stop': after_stop}
            stops.append({'condition': 'S01', 'description': STOP_CONDITIONS['S01'], 'check': 'user_level',
                          'phase': 'launcher', 'after_first_stop': after_stop})
        elif not comparison['complete']:
            checks['user_level'] = {'passed': False, 'condition': None, 'detail': comparison, 'error': True,
                                    'phase': 'launcher', 'sequence': sequence + 1, 'after_stop': after_stop}
        else:
            checks['user_level'] = {'passed': True, 'condition': None, 'detail': comparison, 'error': False,
                                    'phase': 'launcher', 'sequence': sequence + 1, 'after_stop': after_stop}
        if not comparison['complete']:
            operational.append({'phase': 'launcher', 'event': 'user-level observation incomplete: equality cannot '
                                'be established', 'unobserved': comparison['unobserved']})
    if run_interrupted:
        operational.append({'phase': 'runner', 'event': 'the runner ended without its result',
                            'runner_exit': runner_exit, 'record_source': record_source,
                            'journal_phase': journal.get('phase') if journal else None,
                            'journal_error': journal.get('error') if journal else None})
    not_reached = merged['not_reached']
    criteria = evaluate(checks, not_reached, run_interrupted)
    conditions = sorted({stop['condition'] for stop in stops})
    outcome = classify_outcome(conditions, operational, ceiling, criteria)
    final = {
        'format': 'w1-result-4',
        'outcome': outcome,
        'section8_conditions_fired': conditions,
        'first_stop': stops[0] if stops else None,
        'stops': stops,
        'operational': operational,
        'ceiling': ceiling,
        'criteria': criteria,
        'not_reached': not_reached,
        'interrupted': run_interrupted,
        'record_source': record_source,
        'record_problems': record_problems,
        'merged_from_journal': merged['added'],
        'reconstructed_from_durable_checks': reconstructed,
        'journal': ({'entries': journal['entries'], 'unreadable_lines': journal['unreadable_lines'],
                     'last_phase': journal['phase'], 'error': journal['error']} if journal else None),
        'runner_exit': runner_exit,
        'runner_ended': runner.get('ended') if runner else 'interrupted' if (interrupted or journal) else None,
        'runner_phase_reached': (runner or {}).get('phase_reached', (interrupted or journal or {}).get('phase')),
        'closure_inventory_sha256': runner.get('closure_inventory_sha256') if runner else None,
        'label': 'software wiring test only; not chemistry evidence; no chemistry evidence class applies',
    }
    rec.write_json('99-W1-RESULT.json', final)
    rec.progress(f'W1 outcome: {outcome}')
    return final


def last_progress_line():
    try:
        with open(os.path.join(RECORDS, 'progress.log'), 'r', encoding='utf-8') as handle:
            lines = handle.read().splitlines()
        return lines[-1] if lines else None
    except OSError:
        return None


def launch():
    if os.path.realpath(os.getcwd()) != os.path.realpath(REPO):
        print('the launcher must start from the repository root', file=sys.stderr)
        return 3
    if sys.executable != ENV_PY or sys.flags.ignore_environment != 1 or sys.flags.no_user_site != 1 \
            or sys.flags.dont_write_bytecode != 1 or sys.argv[1:] != ['launch']:
        print('the launcher must be started as <environment>/bin/python -E -s -B tools/w1_driver.py launch',
              file=sys.stderr)
        return 3
    if os.path.lexists(RUN):
        print('the W1 run area already exists: one attempt only, nothing was started', file=sys.stderr)
        return 3
    # Detach from the operator's process group, so that the end of the shell that started the launcher does not end
    # the attempt. The launcher's own process identifier, recorded below, is the authoritative launcher identity.
    try:
        session = os.setsid()
    except OSError as exc:
        session = f'not detached: {type(exc).__name__}'
    os.makedirs(RUN)
    for directory in (AIIDA_PATH, TMPDIR, WORKDIR, RECORDS, CAPTURE):
        os.mkdir(directory)
    rec = Recorder(RECORDS)
    rec.progress('launcher started')
    record = launcher_record()
    problems = check_launcher_record(record)
    argv = [ENV_PY, '-E', '-s', '-B', DRIVER_REL, 'run']
    rec.write_json('00-launcher-record.json', {
        'launcher_record': record, 'problems': problems, 'runner_argv_private': argv, 'cwd_private': REPO,
        'launcher_pid': os.getpid(), 'launcher_session': session, 'started': time.time(),
        'ceiling_seconds': CEILING_SECONDS,
        'grace_seconds': GRACE_SECONDS,
        'launcher_flags': {'ignore_environment': sys.flags.ignore_environment, 'no_user_site': sys.flags.no_user_site,
                           'dont_write_bytecode': sys.flags.dont_write_bytecode}})
    home, before = observe_user_level()
    rec.write_json('01-user-level-before.json', {'home_private': home, 'observation': before})
    if problems:
        rec.progress('the launcher record differs from the declaration: the runner is not started')
        finalize(rec, problems, before, None, None)
        return 1
    ceiling = None
    with open(os.path.join(RECORDS, 'runner-stdout.txt'), 'xb') as out, \
            open(os.path.join(RECORDS, 'runner-stderr.txt'), 'xb') as err:
        process = subprocess.Popen(argv, cwd=REPO, env=dict(record), stdin=subprocess.DEVNULL, stdout=out,
                                   stderr=err)
        rec.write_json('02-runner-started.json', {'runner_pid': process.pid, 'started': time.time()})
        rec.progress(f'runner started with pid {process.pid}')
        try:
            runner_exit = process.wait(timeout=CEILING_SECONDS)
        except subprocess.TimeoutExpired:
            # Brief 01, section 6: the ceiling is an operational stop, recorded here independently of the runner.
            ceiling = {'event': 'wall-clock ceiling reached', 'ceiling_seconds': CEILING_SECONDS, 'time': time.time(),
                       'runner_pid': process.pid, 'last_progress_line': last_progress_line(), 'sigkill': False}
            rec.write_json('92-ceiling-event.json', ceiling)
            rec.progress('wall-clock ceiling reached: SIGTERM to the runner')
            process.send_signal(signal.SIGTERM)
            try:
                runner_exit = process.wait(timeout=GRACE_SECONDS)
            except subprocess.TimeoutExpired:
                rec.progress('the runner did not end within the grace period: SIGKILL')
                process.kill()
                runner_exit = process.wait()
                ceiling['sigkill'] = True
                rec.write_json('93-ceiling-sigkill.json', {'time': time.time(), 'runner_pid': process.pid})
    rec.progress(f'runner ended with exit {runner_exit}')
    _home, after = observe_user_level()
    rec.write_json('91-user-level-after.json', {'observation': after})
    final = finalize(rec, problems, before, after, runner_exit, ceiling)
    if final['outcome'].startswith('PASS'):
        return 0
    return 1 if final['section8_conditions_fired'] else 2


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'launch':
        return launch()
    if mode == 'run':
        return run()
    print('usage: <environment>/bin/python -E -s -B tools/w1_driver.py launch', file=sys.stderr)
    return 3


if __name__ == '__main__':
    sys.exit(main())
