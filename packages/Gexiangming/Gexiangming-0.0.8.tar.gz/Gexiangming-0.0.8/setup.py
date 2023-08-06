



#from distutils.core import  setup
#import setuptools
#packages = ['offshoreflac3d']# 唯一的包名，自己取名
#setup(name='offshoreflac3d',
#	version='0.0.4',
#	author='Xiangming Ge',
#    packages=setuptools.find_packages(),
#    package_dir={'requests': 'requests'},)

from setuptools import setup, find_packages

setup(
    name='Gexiangming',  # 包名
    version='0.0.8',  # 版本
    long_description=open('README.md').read(),  # 读取文件中介绍包的详细内容
    author='Xiangming Ge',  # 作者
    license='MIT License',  # 协议
    packages=find_packages(),  # 包的目录
)