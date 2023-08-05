import os
os.environ['OMP_NUM_THREADS'] = '1'

from compute_fbank import compute_fbank
from compute_melspectrogram import compute_melspectrogram