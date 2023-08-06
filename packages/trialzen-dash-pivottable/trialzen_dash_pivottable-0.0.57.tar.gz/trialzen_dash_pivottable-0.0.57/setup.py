import json
import os
from setuptools import setup


with open(os.path.join('dash_pivottable', 'package.json')) as f:
    package = json.load(f)

package_name = "dash_pivottable"

setup(
    name="trialzen_dash_pivottable",
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package['description'] if 'description' in package else package_name,
    install_requires=['dash']
)
