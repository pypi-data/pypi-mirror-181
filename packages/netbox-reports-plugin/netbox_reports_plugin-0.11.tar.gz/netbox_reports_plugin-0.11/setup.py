from setuptools import find_packages, setup

list_packages = ['XlsxWriter']

setup(
    name='netbox_reports_plugin',
    version='0.11',
    description='netbox_reports_plugin',
    url='',
    author='Ilya Gulin',
    license='Apache 2.0',
    install_requires=[*list_packages],
    packages=find_packages(),
    include_package_data=True,
)
