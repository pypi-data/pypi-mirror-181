# -*- coding: utf-8 -*-
"""
批量计算特征
"""
import os
from tqdm.auto import tqdm
from joblib import Parallel, delayed
from loguru import logger
import numpy as np
import torchaudio

from audio_feature.compute_fbank import ComputeFbank
from audio_feature.compute_melspectrogram import ComputeMelSpectrogram


""" 获取音频文件列表 """
def get_wav_list(wav_dir) -> list:
    wav_list = []

    logger.info("start counting wav_list ...")
    for dirpath, dirnames, filenames in tqdm(os.walk(wav_dir)):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # 过滤非wav文件
            if not file_path.endswith(".wav"):
                continue
            wav_list.append((filename[:-4], file_path))

    return wav_list


""" 计算并保存特征 """
def save_feature(compute_func, wav_path, out_path) -> None:
    wavform, sample_rate = torchaudio.load(wav_path)
    tensor_out = compute_func(wavform, sample_rate)
    np_out = tensor_out.numpy()
    np.save(out_path, np_out)


""" 批量计算特征主入口 """
def batch_compute(wav_dir, out_dir, nj=1,
                  feature_type="fbank", num_mel_bins=80,
                  frame_length=25, frame_shift=10, dither=0.0,
                  n_fft=2048, win_length=1200, hop_length=300,
                  resample_rate=16000
                  ) -> None:

    wav_list = get_wav_list(wav_dir)

    if feature_type == "fbank":
        compute_func = ComputeFbank(num_mel_bins=num_mel_bins,
                                    frame_length=frame_length,
                                    frame_shift=frame_shift,
                                    dither=dither,
                                    resample_rate=resample_rate)
        logger.info('\n[ fbank args ]:\nnj: {}\nnum_mel_bins: {}\nframe_length: {}\n'
                    'frame_shift: {}\ndither: {}\nresample_rate: {}'
                    .format(nj, num_mel_bins, frame_length, frame_shift, dither, resample_rate))
    elif feature_type == "mel":
        compute_func = ComputeMelSpectrogram(num_mel_bins=num_mel_bins,
                                             n_fft=n_fft,
                                             win_length=win_length,
                                             hop_length=hop_length,
                                             resample_rate=resample_rate)
        logger.info('\n[ mel args ]:\nnj: {}\nnum_mel_bins: {}\nn_fft: {}\n'
                    'win_length: {}\nhop_length: {}\nresample_rate: {}'
                    .format(nj, num_mel_bins, n_fft, win_length, hop_length, resample_rate))
    else:
        logger.error('feature_type must be "fbank" or "mel" !')
        return

    logger.info("start computing features ...")

    result = Parallel(n_jobs=nj, backend='multiprocessing')(delayed(save_feature)
                                                            (compute_func,
                                                             wav_info[1],
                                                             os.path.join(out_dir, wav_info[0]))
                                                            for wav_info in tqdm(wav_list))

