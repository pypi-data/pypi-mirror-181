from setuptools import setup

setup(name='distri_package',
      version='1.10',
      description='Gaussian and Binomial distributions',
      packages=['distri_package'],
      readme="README.md",
      long_description="""The purpose of this package is to help users analyze Binomial and Gaussian distributions. \n
            ## Install \n
            To pip install type: \n
            ```pip install distri_pack``` \n \n

            ## Files \n
            Binomialdistribution.py - Binomial distribution class for calculating and visualizing a Binomial distribution. \n
            Gaussiandistribution.py - Gaussian distribution class for calculating and visualizing a Gaussian distribution. \n
            Generaldistribution.py - Generic distribution class for calculating and visualizing a probability distribution. \n""",
      long_description_content_type='text/markdown',
      zip_safe=False)

    