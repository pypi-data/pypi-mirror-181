from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='prps',
      version='0.0.5',
      description='Connect to Pepper via ssh and run the rock paper scissors game.',
      long_description=readme(),
      url="https://github.com/D7017E/Rock-Paper-Scissors",
      author='D7017E',
      author_email="bersim-8@student.ltu.se",
      packages=['prps'],
      install_requires=[
        'paramiko',
      ],
      zip_safe=False)
      