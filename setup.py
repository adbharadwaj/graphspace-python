from setuptools import setup, find_packages

install_requires = [i.strip() for i in open("requirements.txt").readlines()]

setup(name='graphspace_api',
      version='1.13',
      description='Python client for GraphSpace REST API',
      url='http://github.com/adbharadwaj/graphspace',
      author='Aditya Bharadwaj',
      author_email='adb@vt.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      zip_safe=False)