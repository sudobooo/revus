# setup.py

from setuptools import setup, find_packages

setup(
    name='automated_pr_review_app',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'gitpython',
        'openai',
        'langchain',
        'langchain-openai',
        'python-dotenv',
        'toml'
    ],
    entry_points={
        'console_scripts': [
            'run_auto_review=cli.auto_review:run_auto_review'
        ]
    },
    author='Your Name',
    description='Automated PR Review Application using OpenAI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
