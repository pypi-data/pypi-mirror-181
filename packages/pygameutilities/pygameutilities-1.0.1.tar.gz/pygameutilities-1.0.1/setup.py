from setuptools import setup, find_packages


VERSION = '1.0.1'
DESCRIPTION = 'A small pygame library to make your life easier'
with open("README.md", "r") as f:
    LONGDESCRIPTION = f.read()



# Setting up
setup(
    name="pygameutilities",
    version=VERSION,
    author="Emilio Mendoza",
    author_email="Ironislife39@gmail.com",
    description=DESCRIPTION,
    long_description= LONGDESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'pygame', 'physics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)