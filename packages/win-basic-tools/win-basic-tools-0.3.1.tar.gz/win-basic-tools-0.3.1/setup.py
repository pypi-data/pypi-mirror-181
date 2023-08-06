from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    page_description = f.read()

with open('C:\\Users\\henri\\github\\win-basic-tools\\requirements.txt') as f:
    requirements = f.read()

setup(
    name='win-basic-tools',
    version='0.3.1',
    author='Henrique do Val',
    author_email='henrique.val@hotmail.com',
    description='Gives some small tools for shells on Windows',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HenriquedoVal/win-basic-tools',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'win-basic-tools = win_basic_tools.setup_cmd:main',
        ]
    },
    install_requires=requirements,
    python_requires='>=3.6'
)
