
# setup.py file for texlib

from distutils.core import setup

setup(name = 'texlib', version = '0.01',
      description = ("A package of Python modules for dealing with "
                     "various TeX-related file formats."),
      author = 'A.M. Kuchling',
      author_email = 'akuchlin@mems-exchange.org',
      url = "http://www.amk.ca/python/tex_wrap.html",

      packages = ['texlib'],
)
