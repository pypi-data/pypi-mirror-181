import setuptools

setuptools.setup(
    name='dataflow-policy-tags-inspection',
    version='1.0.0 ',
    install_requires=['google-cloud-datacatalog==3.7.1',
                      'google-cloud-dlp==3.9.2'],
    packages=setuptools.find_packages(),
)