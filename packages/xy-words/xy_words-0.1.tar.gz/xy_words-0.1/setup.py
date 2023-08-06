from setuptools import setup, find_packages, Extension
from wheel import *

setup(name='xy_words',
      version='0.1',
      description='星圆文字处理，基于snowNlp与jieba',
      author='Xingyuan55',
      author_email='dus0963@outlook.com',
      requires=['jieba', 'wheel'],  # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      # packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
      license="MPL"
      )
