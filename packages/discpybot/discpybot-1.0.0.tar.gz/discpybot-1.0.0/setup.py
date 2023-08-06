import setuptools 
from setuptools import setup, find_packages


    
    
setup(
        name ='discpybot',
        version ='1.0.0',
        author ='Vibhu Agarwal',
        author_email ='',
        url ='https://github.com/DAARKKIBOI',
        description ='',
        long_description = 'A simple CLI that generates a template for a discord bot in python',
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'gfg = bot.main:main'
            ]
        },
        classifiers =[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        keywords ='geeksforgeeks gfg article python package vibhu4agarwal',
        install_requires = ['nextcord', 'datetime', 'humanfriendly', 'typer', 'requests'],
        zip_safe = False
)