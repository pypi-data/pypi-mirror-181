from setuptools import setup
from setuptools import find_packages

# reading long description from file
with open('README.md') as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ['requests', 'azure-storage-blob', 'azure-storage-file-share', 'msrest==0.6.21', 'azure-core']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Quality Assurance',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.8'
    ]

# calling the setup function
setup(name='azure-storage-utils',
      version='1.0.26',
      description='A utility for tracking volume in and out of azure storage containers',
      long_description=long_description,
      url='https://msazure.visualstudio.com/One/_git/RepoDepot',
      author='Matthew Warren',
      author_email='mawarren@microsoft.com',
      license='MIT',
      packages=find_packages(where='src', include=['*utils*']),
      package_dir={"": "src"},
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='maps flat blob storage accounts as if hierchical and compares changes between different mappings'
      )
