from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='nxpprog',
    version='1.0.2',
    author='libhal organization',
    description='Programmer for NXP arm processors using ISP protocol.', long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/libhal/nxpprog/',
    packages=find_packages('src'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
        'console_scripts': ['nxpprog=nxpprog.nxpprog:main'],
    },
    python_requires='>=3.9',
    install_requires=[
        'pyserial>=3.4',
        'click>=7.1.2',
        'rich==12.6.0',
    ]
)
