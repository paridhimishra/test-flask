import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="mmf",
    version="1.0.0",
    description="basic app to test flask",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)




"""

https://eggsac.readthedocs.io/en/latest/flaskr.html
# eggsac --python-package flaskr --keep

cd /tmp/flaskr_*/flaskr/
source bin/activate
python lib/python2.7/site-packages/Flaskr-*.egg/flaskr/flaskr.py


eggsac --python-package flaskr --tar-gzip --output-dir .


mkdir ~/flaskr_demo
tar -zxf flaskr.tar.gz --directory ~/flaskr_demo/

pushd ~/flaskr_demo/flaskr
source bin/activate
python lib/python2.7/site-packages/Flaskr-*.egg/flaskr/flaskr.py

"""