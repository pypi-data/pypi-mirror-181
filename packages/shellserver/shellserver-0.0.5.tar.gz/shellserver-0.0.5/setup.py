from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    page_description = f.read()

# Must be full path for build to find
with open('C:\\Users\\henri\\github\\shellserver\\requirements.txt') as f:
    requirements = f.read()

setup(
    name='shellserver',
    version='0.0.5',
    author='Henrique do Val',
    author_email='henrique.val@hotmail.com',
    description='Server to aid shell navigation',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HenriquedoVal/shellserver',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'shellserver = shellserver.cli:main',
        ]},
    install_requires=requirements,
    python_requires='>=3.10'
)
