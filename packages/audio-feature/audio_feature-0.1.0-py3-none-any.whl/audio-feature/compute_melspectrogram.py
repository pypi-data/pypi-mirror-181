# -*- coding: utf-8 -*-
"""
计算mel图
"""

import torch
import torchaudio


def compute_melspectrogram(path,
                           n_mels=80,
                           n_fft=2048,
                           win_length=1200,
                           hop_length=300) -> torch.Tensor:
    mel_params = {
        "n_mels": n_mels,
        "n_fft": n_fft,
        "win_length": win_length,
        "hop_length": hop_length }

    mean_val, std_val = -4, 4

    to_melspec = torchaudio.transforms.MelSpectrogram(**mel_params)

    wav, sample_rate = torchaudio.load(path)
    mel_tensor = to_melspec(wav)
    mel_tensor = (torch.log(1e-5 + mel_tensor) - mean_val) / std_val
    mel_tensor = mel_tensor.squeeze()

    return mel_tensor
