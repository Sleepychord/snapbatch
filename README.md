# SnapBATCH

### Install 
```
pip install snapbatch
```

### Usage
```
snapbatch [-J your_job_name] [OPTIONS(1)...] [ : [OPTIONS(N)...]] script(0) [args(0)...]
```

`snapbatch` is a replacement of `sbatch` to create a snapshot of current working directory, and submit the command to `sbatch`.\n
This command simply:
1. commits the dirty changes of files monitored by git AND all untracked .py/.sh to a new branch. 
2. mirros this branch to the path of environment `SNAP_BATCHES`, default to `~/snapbatches`. (with `git worktree`, friendly to merge/commit/find/diff on these new workplaces than directly copying.)
3. runs `sbatch --chdir /copied_path/relative/path {--arg xxx ...} (the following args to snapbatch)`

### Purge branches
Please first manually move or delete the ~/snapbatches dir. (too dangerous to automate), then run the following command under the git working directory,
```
snapbatch_purge [n]
```
It keeps the last n snapbatch branches, default 0.

Author: mingding.thu dot gmail.com
