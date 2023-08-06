# Pip_Package_Practice/setup.py
from setuptools import setup

setup(
    name='koslang',#module 이름
    version='0.1.0',
    description='This Package can detect slang in Korean sentence.',
    author='ChoiJaeHoon',
    author_email='diadiahun0902@gmail.com',
    python_requires='>=3.8',
    license='MIT',
    install_requires=["eunjeon","pandas"], #module 필요한 다른 module
    include_package_data=True,
    packages=['koslang'],
    package_data={'koslang':['*.csv']}
)