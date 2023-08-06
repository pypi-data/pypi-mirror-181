# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: setup.py
# @AUthor: Fei Wu
# @Time: 12月, 13, 2022
import setuptools

with open("README.md", encoding='gb18030', errors='ignore') as fh:
  long_description = fh.read()

setuptools.setup(
  name="matchgroup",
  version="0.0.1",
  author="wufeipku",
  author_email="wufei.pku@163.com",
  # py_modules=['income_predict.flowincomepredict'],
  description="package for matching creators with PSM",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://git.woa.com/content_supply_chain/match_group_model",
  packages=setuptools.find_packages(),
  install_requires=['pandas==1.2.4','numpy==1.21.6','seaborn==0.11.1','scikit-learn==0.23.2',
                    'matplotlib==3.3.4','scipy==1.8.1','lightgbm==3.2.1','statsmodels==0.13.2','numba==0.55.1'],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)