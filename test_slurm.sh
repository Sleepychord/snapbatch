#!/bin/bash

#SBATCH --output %x.%j
#SBATCH --partition learnaccel
#SBATCH --ntasks 2
#SBATCH --cpus-per-task 1
#SBATCH --time 0-00:01:00

pwd
bash -c 'echo "ended at `date` on `hostname`"'
bash -c 'env'
# srun bash -c 'echo "ended at `date` on `hostname`"'