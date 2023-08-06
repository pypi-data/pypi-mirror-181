# -*- coding: utf-8 -*-
"""
命令行入口
"""

import argparse

from audio_feature.compute_fbank import compute_fbank
from audio_feature.compute_melspectrogram import compute_melspectrogram


def main():
    parser = argparse.ArgumentParser(description="compute features from audios")
    parser.add_argument("-ft", "--feature_type", default="fbank")
    parser.add_argument("-f", "--file", default="")

    arg_dict = parser.parse_args()
    if arg_dict.feature_type == "fbank":
        run_compute = compute_fbank
    else:
        run_compute = compute_melspectrogram

    tensor = run_compute(arg_dict.file)
    print(tensor)