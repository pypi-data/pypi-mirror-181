# -*- coding: utf-8 -*-
"""
提取fbank特征
"""
import torch
import torchaudio
import torchaudio.compliance.kaldi as kaldi


def compute_fbank(wav_file,
                  num_mel_bins=80,
                  frame_length=25,
                  frame_shift=10,
                  dither=0.0,
                  resample_rate=16000) -> torch.Tensor:

    waveform, sample_rate = torchaudio.load(wav_file)
    waveform = waveform * (1 << 15)
    if resample_rate != sample_rate:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate,
                                                  new_freq=resample_rate)(waveform)

    mat = kaldi.fbank(waveform,
                      num_mel_bins=num_mel_bins,
                      frame_length=frame_length,
                      frame_shift=frame_shift,
                      dither=dither,
                      energy_floor=0.0,
                      window_type='hamming',
                      sample_frequency=resample_rate)

    return mat