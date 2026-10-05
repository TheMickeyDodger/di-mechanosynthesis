"""MS-001 W1: the W1 CalcJob class, the node boundary of the provenance wiring test.

Evidence label: SOFTWARE WIRING TEST ONLY. The job runs `/bin/bash w1_payload.sh`, which records its own
environment, digests its input files and copies two files. It runs no chemistry engine and evaluates no
energy, force or gradient. A pass would be software wiring evidence only, never chemistry evidence.

Governing specification: docs/ms-001/C3-WIRING-TEST-PROPOSAL.md, revision 01, Sections 3 to 6. This module
has no registered entry point: the recorded process type must be exactly `w1_job.W1Job` (A9). It is imported
by tools/w1_driver.py with tools/ first on the import path, and is not meant to be run on its own.
"""

import hashlib
import io
import json
import os
import re
import shlex
import stat

from aiida import orm
from aiida.common.datastructures import CalcInfo, CodeInfo
from aiida.engine import CalcJob
from ase.io import read as ase_read

PROCESS_TYPE = 'w1_job.W1Job'

# Section 3, "The payload". Step 1 is exactly the ten declared lines; steps 2 and 3 follow. Step 2 streams the
# paths, sorted by their bytes, into shasum through xargs so that no single argument list exceeds the limit, and
# pipefail makes a failure anywhere in that pipeline end the script under `set -e`.
W1_PAYLOAD = r"""set -eu
printf 'dollar_zero=%s\n' "$0" > w1_env_record.txt
printf 'shell_flags=%s\n' "$-" >> w1_env_record.txt
if shopt -q login_shell; then echo 'login_shell=on' >> w1_env_record.txt; else echo 'login_shell=off' >> w1_env_record.txt; fi
printf 'bash_version=%s\n' "$BASH_VERSION" >> w1_env_record.txt
printf 'bash_path=%s\n' "$BASH" >> w1_env_record.txt
printf 'uname_s=%s\n' "$(/usr/bin/uname -s)" >> w1_env_record.txt
printf 'uname_r=%s\n' "$(/usr/bin/uname -r)" >> w1_env_record.txt
printf 'uname_m=%s\n' "$(/usr/bin/uname -m)" >> w1_env_record.txt
echo '# /usr/bin/env follows' >> w1_env_record.txt
/usr/bin/env >> w1_env_record.txt
set -o pipefail
/usr/bin/find w1_structure_in.extxyz w1_identity.json w1_fixed_set.json w1_units.json w1_inputs w1_payload.sh -type f -print0 | LC_ALL=C /usr/bin/sort -z | /usr/bin/xargs -0 /usr/bin/shasum -a 256 > w1_input_manifest.sha256
/bin/cp w1_structure_in.extxyz w1_structure_out.extxyz
/bin/cp w1_identity.json w1_identity_out.json
"""
W1_PAYLOAD_BYTES = W1_PAYLOAD.encode('ascii')
PAYLOAD_FILENAME = 'w1_payload.sh'

# Section 4, "The fixture diff": 94 ASCII bytes with LF endings and a final LF.
W1_FIXTURE_DIFF = (b'--- a/w1_fixture.txt\n'
                   b'+++ b/w1_fixture.txt\n'
                   b'@@ -1 +1,2 @@\n'
                   b' w1 fixture line 1\n'
                   b'+w1 fixture line 2\n')
W1_FIXTURE_DIFF_SHA256 = 'f3a3deb5cd0693c76b9bff397e811bff75eb253cb5f42265fe68e6582fdea609'
if len(W1_FIXTURE_DIFF) != 94 or hashlib.sha256(W1_FIXTURE_DIFF).hexdigest() != W1_FIXTURE_DIFF_SHA256:
    raise RuntimeError('W1_FIXTURE_DIFF differs from its declared 94 bytes and SHA256')

# Section 3 port table: port, node type, path written into the job folder. A trailing `/` marks a folder.
W1_INPUT_PORTS = (
    ('structure', 'StructureData', 'w1_structure_in.extxyz'),
    ('identity', 'SinglefileData', 'w1_identity.json'),
    ('fixed_set', 'List', 'w1_fixed_set.json'),
    ('units', 'Dict', 'w1_units.json'),
    ('code_diff', 'SinglefileData', 'w1_inputs/code_diff.bin'),
    ('code_untracked', 'FolderData', 'w1_inputs/code_untracked/'),
    ('code_private', 'FolderData', 'w1_inputs/code_private/'),
    ('code_identity', 'Dict', 'w1_inputs/code_identity.json'),
    ('fixture_diff', 'SinglefileData', 'w1_inputs/fixture_diff.patch'),
    ('defaults', 'Dict', 'w1_inputs/defaults.json'),
    ('build_identity', 'Dict', 'w1_inputs/build_identity.json'),
    ('lock', 'SinglefileData', 'w1_inputs/lock.txt'),
    ('host_record', 'Dict', 'w1_inputs/host_record.json'),
    ('calc_performed', 'Dict', 'w1_inputs/calc_performed.json'),
    ('seed', 'Str', 'w1_inputs/seed.txt'),
    ('per_claim', 'Dict', 'w1_inputs/per_claim.json'),
    ('env_policy', 'Dict', 'w1_inputs/env_policy.json'),
)

# The retrieve list is exactly these four outputs; aiida-core adds the two scheduler files (A6).
W1_OUTPUT_FILES = ('w1_structure_out.extxyz', 'w1_identity_out.json', 'w1_input_manifest.sha256',
                   'w1_env_record.txt')
W1_OUTPUT_PORTS = (
    ('structure_out', 'StructureData', 'w1_structure_out.extxyz'),
    ('identity_out', 'SinglefileData', 'w1_identity_out.json'),
    ('input_manifest', 'Dict', 'w1_input_manifest.sha256'),
    ('env_record', 'SinglefileData', 'w1_env_record.txt'),
)

# Section 3, "Other settings". `import_sys_environment` is not passed, so its default (true) is relied upon (A4).
W1_OPTIONS = {
    'resources': {'num_machines': 1, 'num_mpiprocs_per_machine': 1},
    'withmpi': False,
    'environment_variables': {'OMP_NUM_THREADS': '1'},
    'prepend_text': '',
    'append_text': '',
    'custom_scheduler_commands': '',
}

# The files that aiida-core itself writes into the job folder at `presubmit` (A5, A8): the submission script and
# the two preparation records. They belong to each job's submission inventory but are not inputs of Section 3.
GENERATED_FILES = ('_aiidasubmit.sh', '.aiida/calcinfo.json', '.aiida/job_tmpl.json')

EXTXYZ_HEADER = 'Properties=species:S:1:pos:R:3'
PRESUBMIT_MARKER = 'W1-PRESUBMIT-REPORT '
PARSE_MARKER = 'W1-PARSE-REPORT '
ENV_RECORD_KEYS = ('dollar_zero', 'shell_flags', 'login_shell', 'bash_version', 'bash_path', 'uname_s', 'uname_r',
                   'uname_m')
ENV_RECORD_SEPARATOR = '# /usr/bin/env follows'
_MANIFEST_LINE = re.compile(r'([0-9a-f]{64}) ([ *])(.+)')


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    """Canonical bytes of a Dict or List input as written into the job folder."""
    return (json.dumps(value, sort_keys=True, indent=1, ensure_ascii=True) + '\n').encode('ascii')


def structure_to_extxyz(structure):
    """Section 6 step 3: an extxyz header `Properties=species:S:1:pos:R:3`, each position formatted `%.8f`."""
    sites = structure.sites
    lines = [str(len(sites)), EXTXYZ_HEADER]
    for site in sites:
        kind = structure.get_kind(site.kind_name)
        if kind.is_alloy or kind.has_vacancies or len(kind.symbols) != 1:
            raise ValueError(f'kind {site.kind_name!r} is not a single element')
        x, y, z = site.position
        lines.append('%s %.8f %.8f %.8f' % (kind.symbols[0], x, y, z))
    return ('\n'.join(lines) + '\n').encode('ascii')


def path_key(path):
    return path.encode('utf-8', 'surrogateescape')


def submission_file_bytes(port, type_name, node):
    """The exact bytes that a single-file port is written as in the job folder (Section 3 table, Section 6 step 3)."""
    if port == 'structure':
        return structure_to_extxyz(node)
    if type_name == 'SinglefileData':
        return node.base.repository.get_object_content(node.filename, mode='rb')
    if type_name == 'Dict':
        return json_bytes(node.get_dict())
    if type_name == 'List':
        return json_bytes(node.get_list())
    if type_name == 'Str':
        return node.value.encode('utf-8')
    raise TypeError(f'no writer for port {port} of type {type_name}')


def port_contents(inputs):
    """The stored content of every declared port present in `inputs`: bytes for a file port, rows for a folder."""
    contents = {}
    for port, type_name, rel in W1_INPUT_PORTS:
        if port not in inputs:
            continue
        node = inputs[port]
        if rel.endswith('/'):
            digests = node_repository_digests(node)
            contents[port] = [[path, size, digest] for path, (size, digest)
                              in sorted(digests.items(), key=lambda item: path_key(item[0]))]
        else:
            contents[port] = submission_file_bytes(port, type_name, node)
    return contents


def expected_submission_inventory(contents):
    """The submission inventory that the declared ports and their stored contents require. Pure.

    Returns ({job-folder path: (size, SHA256)}, problems). Completeness is derived from every declared port of
    Section 3 and the payload, never from the files that happen to exist: a declared port without stored content
    is a problem, and so is content for an undeclared port.
    """
    inventory, problems = {}, []
    declared = [port for port, _type, _rel in W1_INPUT_PORTS]
    for port, _type, rel in W1_INPUT_PORTS:
        if port not in contents:
            problems.append(f'declared port {port} has no stored input content')
            continue
        value = contents[port]
        if rel.endswith('/'):
            for sub, size, digest in value:
                inventory[rel + sub] = (size, digest)
        else:
            inventory[rel] = (len(value), sha256_bytes(value))
    for port in sorted(set(contents) - set(declared)):
        problems.append(f'content given for the undeclared port {port}')
    inventory[PAYLOAD_FILENAME] = (len(W1_PAYLOAD_BYTES), sha256_bytes(W1_PAYLOAD_BYTES))
    return inventory, problems


def compare_folder_to_inventory(rows, inventory):
    """A job folder's files against the required inventory plus the files aiida-core generates. Pure.

    Every required path must be present with its required size and digest, every generated file must be present,
    and no other file may be present. Returns the list of problems.
    """
    present = {path: (size, digest) for path, size, digest in rows}
    problems = []
    for path in sorted(inventory, key=path_key):
        if path not in present:
            problems.append(f'declared submission file absent: {path}')
        elif tuple(present[path]) != tuple(inventory[path]):
            problems.append(f'declared submission file differs from its stored input: {path}')
    for path in GENERATED_FILES:
        if path not in present:
            problems.append(f'generated submission file absent: {path}')
    for path in sorted(set(present) - set(inventory) - set(GENERATED_FILES), key=path_key):
        problems.append(f'undeclared file in the submission: {path}')
    return problems


def classify_manifest(entries, inventory, stored):
    """The parser's exit status for the manifest, from Section 3's declared triggers. Pure.

    Returns (status, problems):
    - 311 when the manifest does not hold exactly one line for each declared input file and the payload (a path
      missing, or a path that is not declared): the file does not have the declared structure;
    - None when a declared file is absent from the stored submission, so the declared comparison cannot be made
      (the parser then raises: neither a pass nor a digest mismatch);
    - 312 when a manifest digest differs from the digest of the same file as stored for the submission, or the
      payload digest differs from the payload constant;
    - 0 otherwise.
    """
    listed = dict(entries)
    missing = sorted((path for path in inventory if path not in listed), key=path_key)
    extra = sorted((path for path in listed if path not in inventory), key=path_key)
    if missing or extra:
        return 311, ([f'declared file absent from the manifest: {path}' for path in missing]
                     + [f'manifest path is not a declared submission file: {path}' for path in extra])
    absent = sorted((path for path in inventory if path not in stored), key=path_key)
    if absent:
        return None, [f'declared file absent from the stored submission: {path}' for path in absent]
    problems = [f'manifest digest differs from the stored submission file: {path}'
                for path in sorted(inventory, key=path_key) if listed[path] != stored[path][1]]
    if listed[PAYLOAD_FILENAME] != sha256_bytes(W1_PAYLOAD_BYTES):
        problems.append('the manifest digest of w1_payload.sh differs from the payload constant')
    return (312, problems) if problems else (0, [])


def folder_file_digests(root):
    """Every file under `root`: (relative posix path, size, SHA256), sorted by the bytes of the path.

    Returns (rows, irregular, errors). Entries that are not regular files are returned in `irregular` and never
    followed. Every failure to enumerate a directory (`os.walk`'s `onerror`) or to read a file is returned in
    `errors`, never skipped: rows with errors are an incomplete inventory and must not be read as complete. An
    absent root gives no rows and no errors (nothing exists there); an inaccessible root is an error.
    """
    rows, irregular, errors = [], [], []
    try:
        root_mode = os.lstat(root).st_mode
    except (FileNotFoundError, NotADirectoryError):
        return rows, irregular, errors
    except OSError as exc:
        return rows, irregular, [['.', type(exc).__name__]]
    if not stat.S_ISDIR(root_mode):
        return rows, irregular, [['.', 'the root is not a directory']]

    def relative(path):
        return os.path.relpath(path, root).replace(os.sep, '/') if path else '?'

    def onerror(exc):
        errors.append([relative(getattr(exc, 'filename', None)), type(exc).__name__])

    for dirpath, dirnames, filenames in os.walk(root, onerror=onerror, followlinks=False):
        for name in list(dirnames):
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                irregular.append(relative(full))
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = relative(full)
            try:
                mode = os.lstat(full).st_mode
            except OSError as exc:
                errors.append([rel, type(exc).__name__])
                continue
            if not stat.S_ISREG(mode):
                irregular.append(rel)
                continue
            digest = hashlib.sha256()
            size = 0
            try:
                with open(full, 'rb') as handle:
                    for chunk in iter(lambda: handle.read(1 << 20), b''):
                        digest.update(chunk)
                        size += len(chunk)
            except OSError as exc:
                errors.append([rel, type(exc).__name__])
                continue
            rows.append([rel, size, digest.hexdigest()])
    rows.sort(key=lambda row: row[0].encode('utf-8', 'surrogateescape'))
    return rows, sorted(irregular), errors


def node_repository_digests(node):
    """Every file of a node's repository: {relative posix path: (size, SHA256)}."""
    out = {}
    for root, _dirs, files in node.base.repository.walk():
        for name in files:
            rel = (root / name).as_posix()
            data = node.base.repository.get_object_content(rel, mode='rb')
            out[rel] = (len(data), sha256_bytes(data))
    return out


def validate_submit_script(text):
    """Section 5 "The generated script": check `_aiidasubmit.sh` against A3 and A5.

    Returns (classification of every non-blank line, list of violations). The expected order follows A5: shebang,
    the direct scheduler's two output redirections (A3), the environment block with only `OMP_NUM_THREADS=1`, and
    the run line `/bin/bash w1_payload.sh`. Prepend and append text are empty, so nothing else may appear.
    """
    violations = []
    kinds = []
    for number, line in enumerate(text.split('\n')):
        if line.strip() == '':
            continue
        if number == 0 and line == '#!/bin/bash':
            kinds.append('shebang')
            continue
        if line == '# ENVIRONMENT VARIABLES BEGIN ###':
            kinds.append('env_begin')
            continue
        if line == '# ENVIRONMENT VARIABLES END ###':
            kinds.append('env_end')
            continue
        try:
            tokens = shlex.split(line)
        except ValueError:
            kinds.append('unparseable')
            violations.append(f'line {number + 1} cannot be tokenized: {line!r}')
            continue
        if '-l' in tokens or '--login' in tokens:
            violations.append(f'line {number + 1} carries a login flag: {line!r}')
        if tokens and tokens[0] in ('source', '.'):
            violations.append(f'line {number + 1} sources a file: {line!r}')
        if tokens[:2] == ['env', '--ignore-environment'] or tokens[:2] == ['env', '-i']:
            violations.append(f'line {number + 1} is an `env --ignore-environment` line: {line!r}')
        if tokens == ['exec', '>', '_scheduler-stdout.txt']:
            kinds.append('stdout_redirect')
        elif tokens == ['exec', '2>', '_scheduler-stderr.txt']:
            kinds.append('stderr_redirect')
        elif tokens == ['export', 'OMP_NUM_THREADS=1']:
            kinds.append('env_export_omp')
        elif tokens == ['/bin/bash', PAYLOAD_FILENAME]:
            kinds.append('run_line')
        else:
            kinds.append('other')
            violations.append(f'line {number + 1} is not a declared line: {line!r}')
    expected = ['shebang', 'stdout_redirect', 'stderr_redirect', 'env_begin', 'env_export_omp', 'env_end',
                'run_line']
    if kinds != expected:
        violations.append(f'non-blank line sequence {kinds} differs from the declared sequence {expected}')
    if 'bash -l' in text:
        violations.append('the text `bash -l` occurs in the script')
    if 'env --ignore-environment' in text:
        violations.append('the text `env --ignore-environment` occurs in the script')
    return kinds, violations


def parse_env_record(data):
    """Section 3 "The payload record": eight key lines, the separator, then `/usr/bin/env` output.

    Raises ValueError on any other structure.
    """
    text = data.decode('utf-8')
    if not text.endswith('\n'):
        raise ValueError('the payload record does not end with LF')
    lines = text[:-1].split('\n')
    if len(lines) < len(ENV_RECORD_KEYS) + 1:
        raise ValueError('the payload record is too short')
    keys = {}
    for index, key in enumerate(ENV_RECORD_KEYS):
        prefix = key + '='
        if not lines[index].startswith(prefix):
            raise ValueError(f'line {index + 1} does not start with {prefix!r}')
        keys[key] = lines[index][len(prefix):]
    if lines[len(ENV_RECORD_KEYS)] != ENV_RECORD_SEPARATOR:
        raise ValueError('the separator line is missing or differs')
    environment = []
    for line in lines[len(ENV_RECORD_KEYS) + 1:]:
        name, sep, value = line.partition('=')
        if not sep or not name:
            raise ValueError(f'an environment line has no NAME=: {line!r}')
        environment.append([name, value])
    return {'keys': keys, 'environment': environment}


def parse_manifest(data):
    """Section 3: `/usr/bin/shasum -a 256` lines. Returns [[path, sha256], ...] in file order."""
    text = data.decode('utf-8')
    if not text.endswith('\n'):
        raise ValueError('the manifest does not end with LF')
    entries = []
    for line in text[:-1].split('\n'):
        match = _MANIFEST_LINE.fullmatch(line)
        if match is None or match.group(3).startswith('\\'):
            raise ValueError(f'unparseable manifest line: {line!r}')
        entries.append([match.group(3), match.group(1)])
    paths = [path for path, _ in entries]
    if len(set(paths)) != len(paths):
        raise ValueError('a path occurs more than once in the manifest')
    return entries


def inventory_sha256(inventory):
    """The SHA256 of an inventory written as sorted `path TAB size TAB sha256 LF` lines."""
    lines = [f'{path}\t{size}\t{digest}\n' for path, (size, digest) in sorted(inventory.items(),
                                                                            key=lambda item: path_key(item[0]))]
    return sha256_bytes(''.join(lines).encode('utf-8', 'surrogateescape'))


class W1Job(CalcJob):
    """The W1 job: every provenance node is a real, required input port of each job (Section 3)."""

    @classmethod
    def define(cls, spec):
        super().define(spec)
        for port, type_name, rel in W1_INPUT_PORTS:
            spec.input(port, valid_type=getattr(orm, type_name), required=True,
                       help=f'W1 input, written into the job folder as `{rel}`.')
        for port, type_name, rel in W1_OUTPUT_PORTS:
            spec.output(port, valid_type=getattr(orm, type_name), required=True,
                        help=f'W1 output, built from `{rel}`.')
        spec.exit_code(310, 'ERROR_W1_MISSING_OUTPUT', message='A retrieved W1 file is missing.')
        spec.exit_code(311, 'ERROR_W1_MALFORMED_OUTPUT',
                       message='A W1 file does not parse, or the atom count differs from the sidecar.')
        spec.exit_code(312, 'ERROR_W1_MANIFEST_MISMATCH',
                       message='A manifest digest differs from the stored submission file.')

    def prepare_for_submission(self, folder):
        """Write every input into the sandbox folder itself, so that each is stored in the node repository."""
        root = folder.abspath
        for port, type_name, rel in W1_INPUT_PORTS:
            node = self.inputs[port]
            if rel.endswith('/'):
                target = os.path.join(root, *rel.rstrip('/').split('/'))
                os.makedirs(target, exist_ok=False)
                node.base.repository.copy_tree(target)
                continue
            data = submission_file_bytes(port, type_name, node)
            path = os.path.join(root, *rel.split('/'))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'xb') as handle:
                handle.write(data)
        with open(os.path.join(root, PAYLOAD_FILENAME), 'xb') as handle:
            handle.write(W1_PAYLOAD_BYTES)

        code_info = CodeInfo()
        code_info.code_uuid = self.inputs.code.uuid
        code_info.cmdline_params = [PAYLOAD_FILENAME]

        calc_info = CalcInfo()
        calc_info.codes_info = [code_info]
        calc_info.retrieve_list = list(W1_OUTPUT_FILES)
        calc_info.local_copy_list = []
        calc_info.remote_copy_list = []
        return calc_info

    def presubmit(self, folder):
        """Section 5: validate `_aiidasubmit.sh`, report every digest to the node log, raise on any violation.

        The report also compares the folder with the inventory that the declared ports and their stored inputs
        require (`inventory_problems`). That comparison is recorded for the checker; it is not a validation of
        Section 5 and does not raise.
        """
        calc_info = super().presubmit(folder)
        script_name = self.node.get_option('submit_script_filename')
        script_path = os.path.join(folder.abspath, script_name)
        with open(script_path, 'rb') as handle:
            script_bytes = handle.read()
        kinds, violations = validate_submit_script(script_bytes.decode('utf-8'))
        process_type = self.node.process_type
        if process_type != PROCESS_TYPE:
            violations.append(f'process type {process_type!r} differs from {PROCESS_TYPE!r}')
        files, irregular, enumeration_errors = folder_file_digests(folder.abspath)
        if irregular:
            violations.append(f'entries that are not regular files: {irregular}')
        inventory, inventory_problems = expected_submission_inventory(port_contents(self.inputs))
        inventory_problems = inventory_problems + compare_folder_to_inventory(files, inventory)
        report = {
            'format': 'w1-presubmit-report-3',
            'node_uuid': self.node.uuid,
            'process_type': process_type,
            'script_filename': script_name,
            'script_sha256': sha256_bytes(script_bytes),
            'script_line_kinds': kinds,
            'violations': violations,
            # False: a validation of Section 5 failed. None: the folder could not be enumerated completely, so the
            # validation could not be made (an inability, never a violation). True: it was made and passed.
            'passed': False if violations else (None if enumeration_errors else True),
            'enumeration_errors': enumeration_errors[:200],
            'expected_inventory_sha256': inventory_sha256(inventory),
            'expected_inventory_files': len(inventory),
            'inventory_problems': inventory_problems,
            'files': files,
        }
        self.report(PRESUBMIT_MARKER + json.dumps(report, sort_keys=True, separators=(',', ':')))
        if violations:
            raise RuntimeError(f'W1 presubmit validation failed: {violations}')
        if enumeration_errors:
            raise RuntimeError('W1 presubmit validation could not be made: the job folder could not be enumerated '
                               f'completely ({len(enumeration_errors)} errors); nothing is uploaded')
        return calc_info

    def parse_retrieved_output(self, retrieved_temporary_folder=None):
        """Attach the four declared outputs, or return 310, 311 or 312 and attach none."""
        retrieved = self.node.outputs.retrieved
        names = set(retrieved.base.repository.list_object_names())
        missing = [name for name in W1_OUTPUT_FILES if name not in names]
        if missing:
            self.report(PARSE_MARKER + json.dumps({'exit_status': 310, 'missing': missing}))
            return self.exit_codes.ERROR_W1_MISSING_OUTPUT

        content = {name: retrieved.base.repository.get_object_content(name, mode='rb') for name in W1_OUTPUT_FILES}
        try:
            sidecar = json.loads(content['w1_identity_out.json'].decode('ascii'))
            sites = sidecar['sites']
            if not isinstance(sites, list):
                raise ValueError('the sidecar `sites` value is not a list')
            atoms = ase_read(io.StringIO(content['w1_structure_out.extxyz'].decode('ascii')), format='extxyz')
            if len(atoms) != len(sites):
                raise ValueError(f'atom count {len(atoms)} differs from the sidecar site count {len(sites)}')
            parse_env_record(content['w1_env_record.txt'])
            entries = parse_manifest(content['w1_input_manifest.sha256'])
            structure_out = orm.StructureData(ase=atoms)
        except Exception as exception:  # any parse failure is exit code 311
            self.report(PARSE_MARKER + json.dumps({'exit_status': 311,
                                                   'error': f'{type(exception).__name__}: {exception}'}))
            return self.exit_codes.ERROR_W1_MALFORMED_OUTPUT

        inventory, inventory_problems = expected_submission_inventory(port_contents(self.inputs))
        if inventory_problems:
            raise RuntimeError(f'W1 parser: the declared inventory cannot be built: {inventory_problems}')
        status, problems = classify_manifest(entries, inventory, node_repository_digests(self.node))
        if status is None:
            self.report(PARSE_MARKER + json.dumps({'exit_status': None, 'problems': problems[:200]}))
            raise RuntimeError('W1 parser: a declared file is absent from the stored submission; the manifest '
                               'comparison of Section 3 cannot be made')
        if status == 311:
            self.report(PARSE_MARKER + json.dumps({'exit_status': 311, 'problems': problems[:200],
                                                   'problem_count': len(problems)}))
            return self.exit_codes.ERROR_W1_MALFORMED_OUTPUT
        if status == 312:
            self.report(PARSE_MARKER + json.dumps({'exit_status': 312, 'problems': problems[:200],
                                                   'problem_count': len(problems)}))
            return self.exit_codes.ERROR_W1_MANIFEST_MISMATCH

        self.out('structure_out', structure_out)
        self.out('identity_out', orm.SinglefileData(io.BytesIO(content['w1_identity_out.json']),
                                                    filename='w1_identity_out.json'))
        self.out('input_manifest', orm.Dict({
            'format': '/usr/bin/shasum -a 256',
            'manifest_sha256': sha256_bytes(content['w1_input_manifest.sha256']),
            'entries': entries,
        }))
        self.out('env_record', orm.SinglefileData(io.BytesIO(content['w1_env_record.txt']),
                                                  filename='w1_env_record.txt'))
        self.report(PARSE_MARKER + json.dumps({'exit_status': 0, 'manifest_entries': len(entries)}))
        return None
