from setuptools import setup

setup(name='stokepy',
      version='0.1',
      description='Stochastic models library for Python',
      url='https://github.com/bobbywlindsey/stokepy',
      author='Bobby Lindsey',
      author_email='me@bobbywlindsey.com',
      license='MIT',
      packages=['stokepy'],
      install_requires=[
          'numpy',
          'sympy',
          'matplotlib',
      ],
    #   dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'],
      )
