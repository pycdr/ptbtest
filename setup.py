from distutils.core import setup
from setuptools import find_packages

with open("README.rst", 'r') as readme_file:
    setup(
        name='ptbtest',
        version='2.0',
        packages=['ptbtest', 'ptbtest.mocks'],
        url='https://github.com/python-telegram-bot/ptbtest',
        license='GNU General Public License v3.0',
        author='M.M. Tahmasbi',
        author_email='pycdremail@gmail.com',
        description='A test library for python-telegram-bot (ptb) package',
        long_description=readme_file.read(),
        install_requires=['python-telegram-bot', 'pytest'],
        keywords='python telegram bot unittest pytest test ptb ptbtest',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Testing',
            'Topic :: Internet',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ],
    )
