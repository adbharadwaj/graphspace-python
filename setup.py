from setuptools import setup, find_packages

install_requires = [i.strip() for i in open("requirements.txt").readlines()]

setup(name='graphspace_python',
      version='1.2.0',
      description='Python client for GraphSpace REST API',
      url='http://github.com/adbharadwaj/graphspace-python',
      author='Aditya Bharadwaj',
      author_email='adb@vt.edu',
      license='GPL3',
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering',
          'Environment :: Web Environment',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'License :: OSI Approved :: GNU General Public License (GPL)',
      ],
      packages=find_packages(),
      install_requires=install_requires,
      zip_safe=False)
