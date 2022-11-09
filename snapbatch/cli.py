#!/usr/bin/env python
import os
import sys
from .tools import pipeline, Instruction, logging

def parse_job_name(argv):
    for i, part in enumerate(argv):
        if part.startswith('-J') or part.startswith('--job-name'):
            if '=' in part:
                return part.split('=')[-1]
            else:
                assert i + 1 <= len(argv) - 1
                return argv[i+1]
    return None

def main(dryrun=False):
    rest_args = sys.argv[1:]
    if len(rest_args) == 0:
        print(Instruction)
        exit(0)
    else:
        jobname = parse_job_name(rest_args)
        if jobname is not None:
            logging.info(f'Found job-name `{jobname}` by parsing -J or --job-name.')
        copied_root, current_root, timestamp = pipeline(jobname)
        wd = os.getcwd()
        copied_root = os.path.abspath(copied_root)
        current_root = os.path.abspath(current_root)
        wd = os.path.abspath(wd)
        assert wd.startswith(current_root), f'working dir {wd} should with in gitroot {current_root}'
        relative_path = os.path.relpath(wd, current_root)
        copied_wd = os.path.join(copied_root, relative_path)
        copied_wd = os.path.normpath(copied_wd)
        comm = f'sbatch --chdir {copied_wd} ' + ' '.join(rest_args)
        if not dryrun:
            logging.info(f'Running:\n{comm}')
            os.system(comm)
        else:
            return comm, copied_wd, timestamp

def dryrun():
    comm, copied_wd, timestamp = main(dryrun=True)
    logging.info(f'ToRun:\n{comm}')

def rscrun():
    comm, copied_wd, timestamp = main(dryrun=True)
    copy_comm = f'rsc rsync {copied_wd}/ :{copied_wd}'
    rsc_comms = f'{copy_comm} && rsc {comm}'
    logging.info(f'Running:\n{rsc_comms}')
    os.system(rsc_comms)

def launchrun():
    comm, copied_wd, timestamp = main(dryrun=True)
    os.makedirs(os.path.join(copied_wd, 'snapbatch_backup_logs'), exist_ok=True)
    from .launcher import launch
    launch(
        ['--job-id', timestamp]
        + comm.split()[1:] # args after snapbatch
        )

if __name__ == "__main__":
    main()

        

        
        
