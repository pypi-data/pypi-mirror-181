import os
from setuptools import setup, find_packages

# with open('requirements.txt') as f:
#     required = f.read().splitlines()
required = ['torch >= 1.7', 'torchvision', 'pyyaml', 'timm', 'scikit-learn', 'matplotlib', 'opencv-python']

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

exec(open('cvnets/__version__.py').read())
setup(
    name="cvnets",
    version=__version__,
    author="Jihoon Lucas Kim",
    description="Library for Computer Vision Deep Learning Networks",
    packages=find_packages(),
    package_data={'cvnets': ['**/*.yaml']},
    install_requires=required,
    include_package_data=True,
)