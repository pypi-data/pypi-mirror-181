from setuptools import setup, find_packages

setup(name='audio_feature',
      version='0.1.0',
      description='get features from wav',
      long_description=open("README.md", encoding="utf-8").read(),
      long_description_content_type="text/markdown",
      author='AaronLi',
      author_email='1470409562@qq.com',
      install_requires= ["torchaudio",
                         "numpy",
                         "tqdm",
                         "joblib",
                         "loguru"], # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      # packages=['compute_fbank',
      #           'compute_melspectrogram',
      #           '__init__'], #指定目录中需要打包的py文件，注意不要.py后缀
      license="apache 3.0",

      entry_points={"console_scripts": [
                       "audio_feature = audio_feature.main:main",]
                    }
      )