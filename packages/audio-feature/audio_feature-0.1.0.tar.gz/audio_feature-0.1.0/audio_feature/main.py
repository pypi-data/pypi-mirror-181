# -*- coding: utf-8 -*-
"""
命令行入口
"""

import argparse

from audio_feature.batch_compute import batch_compute


def main():
    parser = argparse.ArgumentParser(description="compute features from audios")
    parser.add_argument("-ft", "--feature_type", default="fbank")
    parser.add_argument("-d", "--wav_dir", required=True)
    parser.add_argument("-o", "--out_dir", required=True)
    parser.add_argument("-nj", "--n_jobs", default=1)
    parser.add_argument("-f_len", "--frame_length", default=25)
    parser.add_argument("-f_sh", "--frame_shift", default=10)
    parser.add_argument("-di", "--dither", default=0.0)
    parser.add_argument("-fft", "--n_fft", default=2048)
    parser.add_argument("-w_len", "--win_length", default=1200)
    parser.add_argument("-h_len", "--hop_length", default=300)
    parser.add_argument("-n_mel", "--num_mel_bins", default=80)
    parser.add_argument("-re", "--resample_rate", default=16000)

    arg_dict = parser.parse_args()

    batch_compute(arg_dict.wav_dir, arg_dict.out_dir, nj=arg_dict.n_jobs,
                  feature_type=arg_dict.feature_type, num_mel_bins=arg_dict.num_mel_bins,
                  frame_length=arg_dict.frame_length, frame_shift=arg_dict.frame_shift, dither=arg_dict.dither,
                  n_fft=arg_dict.n_fft, win_length=arg_dict.win_length, hop_length=arg_dict.hop_length,
                  resample_rate=arg_dict.resample_rate
                  )