from setuptools import find_packages, setup

import versioneer

setup(
    name='zoho_inventory_python_sdk',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/aporacloudmobile/zoho_inventory_python_sdk',
    license='',
    author='Carlos Paiva',
    author_email='carlospaiva87@gmail.com',
    description=''
)
