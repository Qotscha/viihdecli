from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open('src/version.py') as fp:
    exec(fp.read())

setup(
    name = 'viihdecli',
    description = 'Command line interface for handling Elisa Viihde recordings',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/Qotscha/viihdecli',
    author = 'Qotscha',
    version = __version__,
    packages = ['viihdecli'],
    package_dir = {'viihdecli': 'src'},
    python_requires='>=3.8',
    install_requires = [
        'keyring',
        'requests',
        'viihdexdl'
        ],
    entry_points = {
        'console_scripts': [
            'viihdecli = viihdecli.__main__:main',
            'viihdedl = viihdecli.viihdedl:main'
            ]
        },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14'
        ],
    project_urls = {'Documentation': 'https://github.com/Qotscha/viihdecli/blob/main/LUEMINUT.md'}
    )
