from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='europemapper',
      version='0.0.1',
      description='Python package for generating Wikipedia style SVG maps of europe.',
      url='https://github.com/RadostW/europemapper/',
      author='Radost Waszkiewicz',
      author_email='radost.waszkiewicz@gmail.com',
      long_description=long_description,
      long_description_content_type='text/markdown',  # This is important!
      project_urls = {
          'Documentation': 'https://europemapper.readthedocs.io',
          'Source': 'https://github.com/RadostW/europemapper/'
      },
      license='MIT',
      packages=['europemapper'],
      zip_safe=False)
