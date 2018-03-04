from distutils.core import setup

setup(
    name='normalizer',
    version='0.1dev',
    packages=['normalizer'],
    license='GNU GPLv3',
    description='Normalizes timestamps, durations, and Unicode for a CSV type',
    author='Frances Hocutt',
    author_email='frances.hocutt+gh@gmail.com',
    entry_points={
        'console_scripts': []
    }
)
