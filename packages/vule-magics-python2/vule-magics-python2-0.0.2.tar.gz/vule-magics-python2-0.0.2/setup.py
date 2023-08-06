import os
import setuptools

with open( os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "scripts/__VERSION__"), "r" ) as f:
    __VERSION__ =  f.read()


setuptools.setup(
    name="vule-magics-python2",
    version=__VERSION__,
    author="Le Tuan Vu",
    author_email="ltnv24@gmail.com",
    description="Vu's custom magic commands",
    long_description="",
    long_description_content_type="text/markdown",
    packages=['vule_sparkmagic', 'scripts'],
    install_requires=['ipython', 'pyspark'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)