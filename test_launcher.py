# SNAPBATCH_PATH=/zhangpai21/dm/snapbatches snapbatch-launch --env_style torchrun -J test_launch -H hostfile test_launcher.py
import torch
import torch.distributed as dist
import os
dist.init_process_group('nccl')
a = torch.tensor([dist.get_rank()], device=int(os.environ['LOCAL_RANK']))
print(dist.get_rank(), a)
dist.all_reduce(a)
if dist.get_rank() == 0:
    print(a)