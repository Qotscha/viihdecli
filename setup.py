from setuptools import setup

setup(
    name = 'viihdecli',
    description = 'Command line interface for handling Elisa Viihde recordings',
    long_description = 'Command line interface for handling Elisa Viihde recordings.',
    url = 'https://github.com/Qotscha/viihdecli',
    author = 'Qotscha',
    version = '0.19',
    packages = ['viihdecli'],
    package_dir = {'viihdecli': 'src'},
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
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
        ],
    project_urls = {'Documentation': 'https://github.com/Qotscha/viihdecli/blob/main/LUEMINUT.md'}
    )
