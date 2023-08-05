import os
os.environ['OMP_NUM_THREADS'] = '1'

from audio_feature.compute_fbank import compute_fbank
from audio_feature.compute_melspectrogram import compute_melspectrogram