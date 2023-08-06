from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='drchrono',
    version='0.0.11',
    license='MIT',
    description='A wrapper for the drchrono API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Hants Williams",
    author_email='hantsawilliams@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/hantswilliams/drchrono-wrapper',
    keywords='drchrono api wrapper',
    install_requires=[
          'requests',
          'faker',
          'python-dotenv'
      ],

)

