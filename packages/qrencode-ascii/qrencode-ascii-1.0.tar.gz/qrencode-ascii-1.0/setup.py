from distutils.core import setup, Extension

encode = Extension('qrencode_ascii._qrencode', sources=['qr_encode.c'], libraries=['qrencode'])

setup(name='qrencode-ascii',
      version='1.0',
      description='qrencode console version',
      author='Ricter Zheng',
      author_email='ricterzheng@gmail.com',
      url='https://github.com/RicterZ/pyqrencode-ascii/tree/master',
      long_description='''A simple wrapper for the C qrencode library.''',
      packages=['qrencode_ascii'],
      ext_modules=[encode],
      requires=[])

