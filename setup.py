from setuptools import setup

required_modules = []

setup(name='bouncer',
      version='0.1.9',
      description='Simple Declarative Authentication based on Ryan Bates excellent cancan library',
      url='http://github.com/jtushman/bouncer',
      author='Jonathan Tushman',
      author_email='jonathan@zefr.com',
      install_requires=required_modules,
      license='MIT',
      packages=['bouncer'],
      zip_safe=False)