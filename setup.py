from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='prediction_model',
      version="0.0.1",
      description="League of legends betting model",
      license="MIT",
      author="Arian Ziwary",
      author_email="arian.ziwary@yahoo.de",
      #url="https://github.com/aziwary",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
