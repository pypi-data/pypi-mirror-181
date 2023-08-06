import setuptools

with open('README.rst','r') as fh:
    long_description = fh.read()
    
setuptools.setup(
    name = 'DiffDomain-py3',
    version = '0.1.4',
    author = 'Dechao Tian',
    author_email = 'tiandch@mail.sysu.edu.cn',
    description = 'DiffDomain can test the significant difference of TADs.',
    long_description = long_description,
    url = 'https://github.com/Tian-Dechao/diffDomain',
    packages = setuptools.find_packages(),
    install_requires=['hic-straw==1.3.1',
                     'TracyWidom',
                      'pandas',
                      'numpy',
                      'docopt',
                      'statsmodels',
                      'seaborn',
                      'matplotlib',
                      'h5py'
                     ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)