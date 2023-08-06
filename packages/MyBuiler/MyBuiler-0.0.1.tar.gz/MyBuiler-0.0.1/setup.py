import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'MyBuiler',      
  packages = ['MyBuiler'], 
  version = '0.0.1', 
  license='MIT', 
  description = 'who is Builer?',
  long_description=DESCRIPTION,
  author = 'Builer',                 
  author_email = 'Test@gmail.com',     
  url = 'https://github.com/Narawit1994/',  
  download_url = 'https://github.com/Narawit1994/',  
  keywords = ['Builder', 'ASCII ART'],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)