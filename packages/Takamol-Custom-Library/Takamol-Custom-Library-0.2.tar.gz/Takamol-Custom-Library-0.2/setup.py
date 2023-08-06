from setuptools import setup, find_packages


setup(
    name='Takamol-Custom-Library',
    version='0.2',
    license='',
    author="Haitham Al-Mughrabi",
    author_email='haitham.almughrabi@wareefunited.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='Takamol Custom Library',
    install_requires=[
        'selenium',
        'webdriver-manager'
    ],

)
