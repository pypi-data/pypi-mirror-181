from setuptools import setup, find_packages

long_description = open('./README.md')

setup(
    name='ProMD',
    version='1.0.0',
    url='https://github.com/ZSendokame/ProMD',
    license='MIT license',
    author='ZSendokame',
    description='PMD is a library that contains ',
    long_description=long_description.read(),
    long_description_content_type='text/markdown',

    packages=(find_packages(include=['promd']))
)