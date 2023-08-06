import torch
from typing import List, Tuple


def show_environment_setting(print_fn):
    msg = "CUDA INFO:"
    msg += f"\n\tIs CUDA supported by this system? {torch.cuda.is_available()}"
    msg += f"\n\tCUDA version: {torch.version.cuda}"
    msg += f"\n\tID of current CUDA device: {torch.cuda.current_device()}"
    msg += f"\n\tName of current CUDA device: {torch.cuda.get_device_name(torch.cuda.current_device())}"
    print_fn(msg)

def zero_pad_batching_one_dim(tensor_list: List[torch.Tensor]) -> Tuple[torch.Tensor, torch.Tensor]:
    max_len = max([len(tensor) for tensor in tensor_list])
    token_tensor = torch.zeros(len(tensor_list), max_len, dtype=tensor_list[0].dtype, device=tensor_list[0].device)
    mask_tensor = torch.ones_like(token_tensor, dtype=torch.bool)
    for idx, tensor in enumerate(tensor_list):
        token_tensor[idx, :len(tensor)] = tensor
        mask_tensor[idx, :len(tensor)] = False
    return token_tensor, mask_tensor

def zero_pad_batching_two_dim(tensor_list: List[torch.Tensor]) -> torch.Tensor:
    dim_one_max_len = max([len(tensor) for tensor in tensor_list])
    dim_two_max_len = max([len(tensor[0]) for tensor in tensor_list])
    token_tensor = torch.zeros(len(tensor_list), dim_one_max_len, dim_two_max_len, dtype=tensor_list[0].dtype, device=tensor_list[0].device)
    mask_tensor = torch.ones_like(token_tensor, dtype=torch.bool)
    for idx, tensor in enumerate(tensor_list):
        token_tensor[idx, :len(tensor), :len(tensor[0])] = tensor
        mask_tensor[idx, :len(tensor), len(tensor[0])] = False
    return token_tensor, mask_tensor

def zero_pad_batching(tensor_list: List[torch.Tensor]) -> torch.Tensor:
    tensor_item = tensor_list[0]
    if len(tensor_item.shape) == 1:
        return zero_pad_batching_one_dim(tensor_list)
    elif len(tensor_item.shape) == 2:
        return zero_pad_batching_two_dim(tensor_list)
    else:
        raise NotImplementedError(f"Only support 1D and 2D tensor, but found: {tensor_item.shape}")
    
if __name__ == "__main__":
    show_environment_setting()

