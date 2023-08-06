# -*- coding: utf-8 -*-
"""
计算mel图
"""

import torch
import torchaudio


""" 适配torch中使用 """
class ComputeMelSpectrogram(torch.nn.Module):
    def __init__(self, num_mel_bins=80,
                    n_fft=2048,
                    win_length=1200,
                    hop_length=300,
                    resample_rate=16000):
        super().__init__()

        mel_params = {"n_mels": num_mel_bins,
                      "n_fft": n_fft,
                      "win_length": win_length,
                      "hop_length": hop_length }
        self.to_melspec = torchaudio.transforms.MelSpectrogram(**mel_params)

        self.resample_rate = resample_rate
        self.mean_val, self.std_val = -4, 4

    def forward(self, waveform, sample_rate):
        if self.resample_rate != sample_rate:
            waveform = torchaudio.transforms.Resample(orig_freq=sample_rate,
                                                      new_freq=self.resample_rate)(waveform)

        mel_tensor = self.to_melspec(waveform)
        mel_tensor = (torch.log(1e-5 + mel_tensor) - self.mean_val) / self.std_val
        mel_tensor = mel_tensor.squeeze()

        return mel_tensor


""" 旧版本 暂不使用"""
def compute_melspectrogram(path,
                           n_mels=80,
                           n_fft=2048,
                           win_length=1200,
                           hop_length=300,
                           resample_rate=16000) -> torch.Tensor:
    mel_params = {
        "n_mels": n_mels,
        "n_fft": n_fft,
        "win_length": win_length,
        "hop_length": hop_length }

    mean_val, std_val = -4, 4

    to_melspec = torchaudio.transforms.MelSpectrogram(**mel_params)

    wav, sample_rate = torchaudio.load(path)

    if resample_rate != sample_rate:
        wav = torchaudio.transforms.Resample(orig_freq=sample_rate,
                                                  new_freq=resample_rate)(wav)

    mel_tensor = to_melspec(wav)
    mel_tensor = (torch.log(1e-5 + mel_tensor) - mean_val) / std_val
    mel_tensor = mel_tensor.squeeze()

    return mel_tensor
