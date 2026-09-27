"""MS-001 Stage 0, item C3: provenance wiring test on one trivial, non-chemistry AiiDA job.

Evidence label: SOFTWARE WIRING TEST. The job adds two integers with bash through the
`core.arithmetic.add` calculation job that ships with aiida-core. It runs no chemistry engine and
evaluates no energy, force or gradient. It shows how AiiDA stores and hashes a job's inputs, outputs,
options and environment. It demonstrates nothing about chemistry, energies, forces or method readiness.

Alongside the job the script stores three data nodes as surrogates for the coordinate field: the
published activated-tool file as a SinglefileData, a StructureData converted from it, and the list of
its stable atom identifiers. These nodes are not inputs of the job.

Usage, from the repository root, with AIIDA_PATH set to a project-local directory whose default
profile was created by `verdi presto --no-broker`:

    python tools/c3_provenance_wiring.py <evidence.json> <requirements-lock.txt>

The evidence file contains local node identifiers and is kept private. No path, host name or user
name is written into the job's own files by this script.
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
M2_FILE = 'structures/donor-activated-EAOGe-C2-radical.extxyz'
M2_SHA256 = 'bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3'
CONTEXT_FILE = 'provenance-context.txt'
BANNER_FILE = 'engine-banner.txt'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> bytes:
    # Read-only queries; --no-optional-locks stops `git status` refreshing the index file.
    return subprocess.run(['git', '--no-optional-locks', '-C', str(REPO), *args],
                          check=True, capture_output=True).stdout


def code_identity() -> dict:
    untracked = git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')
    untracked = sorted(p for p in untracked if p)
    manifest = ''.join(f'{sha256((REPO / p).read_bytes())}  {p}\n' for p in untracked)
    return {
        'head_commit': git('rev-parse', 'HEAD').decode().strip(),
        'tracked_diff_sha256': sha256(git('diff', '--binary', 'HEAD')),
        'tracked_diff_bytes': len(git('diff', '--binary', 'HEAD')),
        'untracked_file_count': len(untracked),
        'untracked_manifest_sha256': sha256(manifest.encode()),
        'untracked_manifest': manifest,
        'driver': 'tools/c3_provenance_wiring.py',
        'driver_sha256': sha256(Path(__file__).read_bytes()),
    }


def repo_objects(node) -> list:
    """Every file in a node's repository, with the storage key and an independently computed SHA256."""
    rows = []
    for root, _dirs, files in node.base.repository.walk():
        for name in files:
            rel = str(root / name) if str(root) != '.' else name
            content = node.base.repository.get_object_content(rel, mode='rb')
            key = node.base.repository.get_object(rel).key
            rows.append({'path': rel, 'bytes': len(content), 'sha256': sha256(content),
                         'repository_key': key, 'key_equals_sha256': key == sha256(content)})
    return sorted(rows, key=lambda r: r['path'])


def describe(role: str, node) -> dict:
    return {'role': role, 'pk': node.pk, 'uuid': node.uuid, 'node_type': node.node_type,
            'aiida_hash': node.base.extras.get('_aiida_hash', None),
            'repository': repo_objects(node)}


def main(out_path: str, lock_path: str) -> int:
    if 'AIIDA_PATH' not in os.environ:
        sys.exit('AIIDA_PATH must point to a project-local directory before aiida is imported')
    home_aiida_before = (Path.home() / '.aiida').exists()

    import ase
    import numpy
    from ase.io import read

    import aiida
    from aiida import load_profile, orm
    from aiida.engine import run_get_node
    from aiida.plugins import CalculationFactory

    profile = load_profile()
    ident = code_identity()
    lock_sha256 = sha256(Path(lock_path).read_bytes())
    versions = {'python': sys.version.split()[0], 'ase': ase.__version__,
                'aiida-core': aiida.__version__, 'numpy': numpy.__version__,
                'requirements_lock_sha256': lock_sha256}

    # Surrogate nodes for the coordinate field (not inputs of the job).
    m2_bytes = (REPO / M2_FILE).read_bytes()
    if sha256(m2_bytes) != M2_SHA256:
        sys.exit(f'{M2_FILE} digest mismatch')
    m2_file = orm.SinglefileData(file=str(REPO / M2_FILE)).store()
    atoms = read(str(REPO / M2_FILE), format='extxyz')
    atom_ids = orm.List(list(atoms.arrays['atom_id'])).store()
    structure_check = {'atoms': len(atoms), 'pbc': [bool(p) for p in atoms.pbc],
                       'cell_is_zero': bool(not atoms.cell.any())}
    try:
        structure = orm.StructureData(ase=atoms).store()
        back = structure.get_ase()
        structure_check.update({
            'stored': True,
            'site_order_and_symbols_equal': back.get_chemical_symbols() == atoms.get_chemical_symbols(),
            'max_abs_position_difference_angstrom': float(abs(back.get_positions() - atoms.get_positions()).max()),
            'pbc_after': [bool(p) for p in back.pbc],
            'atom_id_array_after': 'atom_id' in back.arrays,
            'kind_names': sorted({s.kind_name for s in structure.sites}),
        })
    except Exception as exc:  # recorded, not hidden: a data-model finding
        structure = None
        structure_check.update({'stored': False, 'error_type': type(exc).__name__, 'error': str(exc)})

    computer = orm.load_computer('localhost')
    code = orm.InstalledCode(computer=computer, filepath_executable='/bin/bash', label='bash-c3',
                             default_calc_job_plugin='core.arithmetic.add').store()

    context_lines = [
        'evidence_class=software wiring test only; not chemistry evidence',
        f'code_identity.head_commit={ident["head_commit"]}',
        f'code_identity.tracked_diff_sha256={ident["tracked_diff_sha256"]}',
        f'code_identity.untracked_manifest_sha256={ident["untracked_manifest_sha256"]}',
        f'code_identity.driver_sha256={ident["driver_sha256"]}',
        *(f'software.{k}={v}' for k, v in versions.items()),
        'random_seed=none (the job has no stochastic component)',
    ]
    prepend = '\n'.join(
        [f"echo '{line}' >> {CONTEXT_FILE}" for line in context_lines]
        + [f'echo "env.OMP_NUM_THREADS=$OMP_NUM_THREADS" >> {CONTEXT_FILE}',
           f'echo "os=$(uname -srm)" >> {CONTEXT_FILE}',
           f'echo "cpu=$(sysctl -n machdep.cpu.brand_string)" >> {CONTEXT_FILE}',
           f'echo "ncpu=$(sysctl -n hw.ncpu) memsize_bytes=$(sysctl -n hw.memsize)" >> {CONTEXT_FILE}',
           f'bash --version | head -n 1 > {BANNER_FILE}'])

    ArithmeticAdd = CalculationFactory('core.arithmetic.add')
    results, node = run_get_node(ArithmeticAdd, x=orm.Int(2), y=orm.Int(3), code=code, metadata={
        'label': 'ms001-stage0-c3-wiring',
        'description': 'C3 provenance wiring test: integer addition in bash; no chemistry',
        'options': {
            'resources': {'num_machines': 1, 'num_mpiprocs_per_machine': 1},
            'max_wallclock_seconds': 120,
            'withmpi': False,
            'environment_variables': {'OMP_NUM_THREADS': '1'},
            'prepend_text': prepend,
            'additional_retrieve_list': [CONTEXT_FILE, BANNER_FILE],
        },
    })
    node.base.extras.set_many({
        'ms001_evidence_class': 'software wiring test only; not chemistry evidence',
        'ms001_random_seed': 'none',
        'ms001_code_identity': {k: v for k, v in ident.items() if k != 'untracked_manifest'},
        'ms001_versions': versions,
        'ms001_surrogate_nodes': {'m2_file': m2_file.uuid, 'atom_ids': atom_ids.uuid,
                                  'structure': structure.uuid if structure else None},
    })

    retrieved = node.outputs.retrieved
    context_text = retrieved.base.repository.get_object_content(CONTEXT_FILE, mode='r')
    evidence = {
        'label': 'software wiring test only; demonstrates nothing about chemistry, energies, forces or method readiness',
        'profile': {'name': profile.name, 'storage_backend': profile.storage_backend,
                    'broker': profile.process_control_backend},
        'versions': versions,
        'code_identity': ident,
        'job': {
            'process_label': node.process_label, 'process_state': node.process_state.value,
            'exit_status': node.exit_status, 'exit_message': node.exit_message,
            'is_finished_ok': node.is_finished_ok, 'result_sum': int(results['sum'].value),
            'version_attributes': node.base.attributes.get('version', None),
            'options': {k: node.get_option(k) for k in ('environment_variables', 'withmpi', 'resources',
                                                         'additional_retrieve_list', 'parser_name')},
            'scheduler_stdout': node.get_scheduler_stdout(), 'scheduler_stderr': node.get_scheduler_stderr(),
            'log_messages': [f'{log.levelname}: {log.message}' for log in orm.Log.collection.get_logs_for(node)],
            'computer': {'label': computer.label, 'hostname': computer.hostname,
                         'transport': computer.transport_type, 'scheduler': computer.scheduler_type},
            'code': {'label': code.label, 'type': code.node_type, 'filepath_executable': str(code.filepath_executable)},
        },
        'nodes': [describe('calcjob', node), describe('retrieved', retrieved),
                  describe('input_x', node.inputs.x), describe('input_y', node.inputs.y),
                  describe('output_sum', results['sum']), describe('code', code),
                  describe('surrogate_m2_file', m2_file), describe('surrogate_atom_ids', atom_ids)]
                 + ([describe('surrogate_structure', structure)] if structure else []),
        'retrieved_context': context_text,
        'structure_check': structure_check,
        'home_aiida_folder': {'existed_before': home_aiida_before,
                              'exists_after': (Path.home() / '.aiida').exists()},
    }
    Path(out_path).write_text(json.dumps(evidence, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'is_finished_ok': node.is_finished_ok, 'exit_status': node.exit_status,
                      'sum': evidence['job']['result_sum'], 'structure_stored': structure_check.get('stored'),
                      'home_aiida_exists_after': evidence['home_aiida_folder']['exists_after']}))
    return 0 if node.is_finished_ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
