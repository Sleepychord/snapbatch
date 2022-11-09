# SnapBATCH

### Motivation
On slurm, if your task is queuing and you change the codes, the final launched code will be the modified version. Usually this behavior is not what we want. 

`snapbatch` replaces `sbatch` to solve this problem.

### Install 
```
pip install snapbatch
```

### Usage
```
snapbatch [-J your_job_name] [OPTIONS(1)...] [ : [OPTIONS(N)...]] script(0) [args(0)...]
```

`snapbatch` is a replacement of `sbatch` to create a snapshot of current working directory, and submit the command to `sbatch`.

This command simply:
1. commits the dirty changes of files monitored by git AND all untracked .py/.sh to a new branch. 
2. mirros this branch to the path of environment `SNAPBATCH_PATH`, default to `~/snapbatches`. (with `git worktree`, friendly to merge/commit/find/diff on these new workplaces than directly copying.)
3. runs `sbatch --chdir /copied_path/relative/path {--arg xxx ...} (the following args to snapbatch)`

### Purge branches
Please first manually move or delete the ~/snapbatches dir. (too dangerous to automate), then run the following command under the git working directory,
```
snapbatch_purge [n]
```
It keeps the last n snapbatch branches, default 0.

Author: mingding.thu dot gmail.com

### Other tools
```
snapbatch-dryrun [-J your_job_name] [OPTIONS(1)...] [ : [OPTIONS(N)...]] script(0) [args(0)...]
```
Only mirror the codes and print the `sbatch` command.

```
snapbatch-rsc [-J your_job_name] [OPTIONS(1)...] [ : [OPTIONS(N)...]] script(0) [args(0)...]
```
submit to the FAIR RSC cluster on dev server.

# snapbatch-launch

### Motivation
Sometimes, we develop codes on a SLURM cluster and want to run it on another cluster without management systems.

`snapbatch-launch` first mirrors the codes and launches a python or shell file on multiple machines with SLURM / torchrun environment variables, pretending that they are launched by `srun` / `torchrun`.

### Usage
First speficify environment variable `SNAPBATCH_PATH` as a path on a **shared filesystem**.
```
snapbatch-launch [-h] [-H HOSTFILE] [-J JOB_NAME][--job-id JOB_ID] [--chdir CHDIR] [--env_style {slurm,torchrun}] [-i INCLUDE] [-e EXCLUDE] [--num_nodes NUM_NODES] [--num_gpus NUM_GPUS] [--master_port MASTER_PORT] [--master_addr MASTER_ADDR] [--launcher LAUNCHER] [--launcher_args LAUNCHER_ARGS] [--force_multi]
user_script ...(user_args)
```

### Logs
`snapbatch-launch` will create a subfolder `snapbatch_backup_logs` under the mirrored working directory. It will capture and save outputs from different ranks (`rank_i.log`).

run `tail -f .../snapbatch_backup_logs/rank_0.log` to see the realtime output of the rank 0.

### Stop

The codes are modified from deepspeed, based on pdsh. You need to manually kill the processes on different nodes due to the disadvantage of pdsh. An example is 
```shell
pdsh -w ssh:node[0-1] "ps -ef | grep jobname | awk '{print \$2}' | xargs kill -9"
```