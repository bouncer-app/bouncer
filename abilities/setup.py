from setuptools import setup

required_modules = []

setup(name='abilities',
      version='0.0.1',
      description='Simple Declarative Authentication based on Ryan Bates excellent cancan library',
      url='http://github.com/jtushman/abilities',
      author='Jonathan Tushman',
      author_email='jonathan@zefr.com',
      install_requires=required_modules,
      license='MIT',
      packages=['abilities'],
      zip_safe=False)