import os, io
from setuptools import setup, find_packages

setup(
    name='wonky',
    version='0.3.0',
    author='Sirsh',
    author_email='amartey@gmail.com',
    license='MIT',
    url='git@https://github.com/sirsh/wonky',
    keywords='software engineering tips for physicists',
    description='This project demonstrates some generally handy things that might be useful for creating numerics projects in physics, but keeping an eye on importing some best practices etc. from software engineering. ',
    long_description=('This project demonstrates some generally handy things that might be useful for creating numerics projects in physics, but keeping an eye on importing some best practices etc. from software engineering. '),
    packages=find_packages(),
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': [
            'wonky = wonky.__main__:main'
            ],
    },
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Computer Vision',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)

