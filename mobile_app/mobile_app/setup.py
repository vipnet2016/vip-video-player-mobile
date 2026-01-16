"""
Setup file for the VIP Video Player mobile application.
This file helps python-for-android build the application correctly.
"""

from setuptools import setup, find_packages

setup(
    name='vip-video-player',
    version='1.0',
    description='VIP Multi-line Video Player for Android',
    author='andy',
    packages=find_packages(),
    install_requires=[
        'kivy',
    ],
    entry_points={
        'console_scripts': [
            'main = main:main',
        ],
    },
    package_data={'': ['*.kv', '*.py']},
)