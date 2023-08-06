# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree
from lazycode.__version__ import __version__

from setuptools import find_packages, setup, Command

FILE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================================项目基础信息======================================
# 项目名称
NAME = 'lazycode'
# 项目描述
DESCRIPTION = 'My short description for my project.'
# 项目 URL 地址
URL = 'https://gitee.com/SL1559100227'
# 邮箱
EMAIL = 'ttw5656@163.com'
# 作者
AUTHOR = 'WSL'
# Python版本
REQUIRES_PYTHON = '>=3.9.12'
# 项目版本
VERSION = __version__

# 项目依赖的库
REQUIRED = []
with open(os.path.join(FILE_DIR, 'requirements.txt'), 'r', encoding='utf-8') as f:
    REQUIRED = [ele.strip() for ele in f.readlines()]

EXTRAS = {
    # 'fancy feature': ['django'],
}

here = os.path.abspath(os.path.dirname(__file__))

# 主页面描述
long_description = ''
with open(os.path.join(FILE_DIR, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    # 排除 tests 目录
    packages=find_packages(exclude=["tests", "lz_test", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # 添加自定义的命令
    cmdclass={
    },
)
