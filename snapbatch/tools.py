import os
import logging
logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
import git
from git import Repo
from datetime import datetime

Instruction = '''
=========Instruction==========
Usage: snapbatch [-J your_job_name] [OPTIONS(1)...] [ : [OPTIONS(N)...]] script(0) [args(0)...]

`snapbatch` is a replacement of `sbatch` to create a snapshot of current working directory, and submit the command to `sbatch`.\n
This command simply:
1. commits the dirty changes of files monitored by git AND all untracked .py/.sh to a new branch.
2. mirrors this branch (using git worktree) to the path of environment `SNAP_BATCHES`, default to `~/snapbatches`.
3. runs `sbatch --chdir /copied_path/relative/path {--arg xxx ...} (the following args to snapbatch)`

Author: mingding.thu@gmail.com
==============================
'''

def get_working_dir_git():
    dir = os.getcwd()
    try:
        repo = Repo(search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError as e:
        logging.error(f''' 
            The working directory `{dir}` is not a git repo.
            Please use `git init` for initialization and make an initial commit.
        ''')
        raise e
    return repo

def new_branch(repo, timestamp):
    ob = repo.active_branch
    try:
        oh = repo.head.commit
    except ValueError as e:
        logging.error(f''' 
            Please make at least an initial commit on this branch.
        ''')
        raise e
    nb = f'__snapbatch__{timestamp}'
    repo.git.checkout(b=nb)
    return nb, oh, ob

def search_new_codes(repo):
    code_suffixes = ['py', 'sh']
    filtered = [
        fl for fl in repo.untracked_files 
        if fl.split('.')[-1] in code_suffixes
    ]
    if len(filtered) > 0:
        logging.info(f'Find untracked codes files {filtered}, also copying them...')
    return filtered

def commit_changes(repo, timestamp):
    repo.git.add('-u')
    repo.index.add(search_new_codes(repo))
    if len(repo.git.diff(cached=True)) > 0:
        repo.git.commit('-m', f'{timestamp}')
    else:
        logging.info(f'working tree clean, good, skip committing.')
    
def pipeline(jobname=None):
    repo = get_working_dir_git()
    dt = datetime.now()
    timestamp = str(dt.timestamp())
    if jobname is not None:
        timestamp += '_' + jobname
    else:
        logging.warning(f'No job name specified. It''s highly recommended to set via `-J` or `--job-name` for snapbatch and sbatch.')
    home = os.environ.get('SNAP_BATCHES', '~/snapbatches')
    home = os.path.expanduser(home)
    snap_path = os.path.join(home, timestamp) # TODO job name
    os.makedirs(snap_path, exist_ok=False)
    logging.info(f'Copying {repo.working_tree_dir} to {snap_path} ...')

    # old version: worktree is better
    # nb, oh, ob = new_branch(repo, timestamp)
    # commit_changes(repo, timestamp)
    # new_repo = repo.clone(snap_path, progress=git.RemoteProgress())
    # repo.head.reset(oh, '--soft')
    # repo.git.checkout(ob)

    try:
        oh = repo.head.commit
    except ValueError as e:
        logging.error(f''' 
            Please make at least an initial commit on this branch.
        ''')
        raise e
    commit_changes(repo, timestamp) # commit at master
    nb, _oh, ob = new_branch(repo, timestamp)
    repo.git.checkout(ob)
    repo.head.reset(oh, '--soft')
    # a new git command?
    os.system(f'git worktree add {snap_path} {nb}')
    return snap_path, repo.working_tree_dir

if __name__ == "__main__":
    pipeline('testtool')
