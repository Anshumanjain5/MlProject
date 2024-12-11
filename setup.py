from setuptools import find_packages, setup

def get_packages(path):
    with open(path, 'r') as f:
        requirements =  [line.strip() for line in f.readlines() if line.strip()] 

        if "-e ." in requirements:
            requirements.remove("-e .")
    
    return requirements

setup(
    name="MlProject",
    version="0.0.1",
    author="Anshuman jain",
    author_email="anshumanjain8886@gmail.com",
    packages=find_packages(),
    install_requires=get_packages("requirements.txt"),
)