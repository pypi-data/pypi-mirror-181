



from distutils.core import  setup
import setuptools
packages = ['Gexiangming']# 唯一的包名，自己取名
setup(name='Gexiangming',
	version='0.0.10',
	author='Xiangming Ge',
   packages=setuptools.find_packages(),)

# from setuptools import setup, find_packages

# setup(
    # name='Gexiangming',  # 包名
    # version='0.0.9',  # 版本
    # long_description=open('README.md').read(),  # 读取文件中介绍包的详细内容
    # author='Xiangming Ge',  # 作者
    # license='MIT License',  # 协议
    # packages=find_packages(),  # 包的目录
# )