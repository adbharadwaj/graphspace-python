from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n') if (line and not
                                                     line.startswith('--'))
    ]

setup(name='graphspace',
      version='1.0',
      description='Python client for GraphSpace REST API',
      url='http://github.com/adbharadwaj/graphspace',
      author='Aditya Bharadwaj',
      author_email='adb@vt.edu',
      long_description=long_description,
      license='MIT',
      packages=['graphspace'],
      install_requires=install_requires,
      zip_safe=False)