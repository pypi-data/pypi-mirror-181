from setuptools import setup, find_packages


setup(
    name='monicahq-client',
    version='0.1.2',
    license='MIT',
    author="Darko Sajben",
    author_email='sajbendarko94@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/sajben94/monicahq-client',
    keywords='monicahq',
    install_requires=[
          'requests',
      ],
)
