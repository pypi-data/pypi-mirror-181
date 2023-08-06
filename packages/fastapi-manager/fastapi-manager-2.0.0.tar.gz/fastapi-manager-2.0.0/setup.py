import re

from setuptools import setup, find_packages


def read(path):
    with open(path, 'r', encoding='utf8') as fp:
        content = fp.read()
    return content


def find_version(path):
    match = re.search(
        r'__version__ = [\'"](?P<version>[^\'"]*)[\'"]', read(path)
    )
    if match:
        return match['version']
    raise RuntimeError("Cannot find version information")


setup(
    name='fastapi-manager',
    version=find_version('fastapi_manager/version.py'),
    author='cheerxiong',
    author_email='cheerxiong0823@163.com',
    description='FastApi simple project initializer',
    long_description='README.md',
    url='https://gitee.com/cheerxiong/fastapi-manager',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read('requirements.txt').splitlines(),
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
