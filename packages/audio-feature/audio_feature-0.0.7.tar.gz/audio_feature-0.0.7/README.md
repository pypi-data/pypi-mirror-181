# 音频提取声学特征

## 安装
1. 自行安装依赖（可选），可以自己安装cpu版torch之类的，否则第2步会自动安装默认版
```shell
pip install torchaudio -i https://mirrors.aliyun.com/pypi/simple/
```
2. 安装此包
```shell
pip install audio_feature
```
## 使用方法
```python
import audio_feature

wav_path = "./test.wav"

# 传入音频文件，得到对应特征的tensor
fbank = audio_feature.compute_fbank(wav_path)
mel = audio_feature.compute_melspectrogram(wav_path)
print(fbank)
print(mel)
```
