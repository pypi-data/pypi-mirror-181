from setuptools import setup, find_packages

setup(
    entry_points='''
    [console_scripts]
    discpybot=discpybot:discpybot
    startbot=discpybot:startbot
    ''',
    name='discpybot',
    version='1.0.4',
    packages=find_packages(),
    install_requires=[
        'click',
        'nextcord', 
        'requests',
        'datetime',
        'humanfriendly',
    ],
    long_description='A simple CLI that generates a discord bot template in python.'
)