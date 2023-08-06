# -*- coding: utf-8 -*-
"""
提取fbank特征
"""

import torch
import torchaudio
import torchaudio.compliance.kaldi as kaldi


""" 适配torch中使用 """
class ComputeFbank(torch.nn.Module):
    def __init__(self, num_mel_bins=80,
                  frame_length=25,
                  frame_shift=10,
                  dither=0.0,
                  resample_rate=16000):
        super().__init__()

        self.num_mel_bins = num_mel_bins
        self.frame_length = frame_length
        self.frame_shift = frame_shift
        self.dither = dither
        self.resample_rate = resample_rate


    def forward(self, waveform, sample_rate):

        if self.resample_rate != sample_rate:
            waveform = torchaudio.transforms.Resample(orig_freq=sample_rate,
                                                      new_freq=self.resample_rate)(waveform)

        waveform = waveform * (1 << 15)

        mat = kaldi.fbank(waveform,
                          num_mel_bins=self.num_mel_bins,
                          frame_length=self.frame_length,
                          frame_shift=self.frame_shift,
                          dither=self.dither,
                          energy_floor=0.0,
                          window_type='hamming',
                          sample_frequency=self.resample_rate)

        return mat


""" 旧版本 暂时不使用 """
def compute_fbank(wav_file,
                  num_mel_bins=80,
                  frame_length=25,
                  frame_shift=10,
                  dither=0.0,
                  resample_rate=16000) -> torch.Tensor:

    waveform, sample_rate = torchaudio.load(wav_file)

    if resample_rate != sample_rate:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate,
                                                  new_freq=resample_rate)(waveform)

    waveform = waveform * (1 << 15)


    mat = kaldi.fbank(waveform,
                      num_mel_bins=num_mel_bins,
                      frame_length=frame_length,
                      frame_shift=frame_shift,
                      dither=dither,
                      energy_floor=0.0,
                      window_type='hamming',
                      sample_frequency=resample_rate)

    return mat