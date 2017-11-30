from setuptools import setup, find_packages

setup(name='emupy6502',
      version='1.0.0',
      description='Simple 6502 Emulator',
      author='Chris Green',
      author_email='crispg72@users.noreply.github.com',
      url='https://github.com/crispg72/emupy6502',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
     )
