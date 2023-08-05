import setuptools
import glob
import os


def read_requirements(fname):
    with open(fname, 'r', encoding='utf-8') as file:
        return [line.rstrip() for line in file]


setuptools.setup(
     name='sigc',
     use_scm_version=True,
     setup_requires=['setuptools_scm'],
     packages=setuptools.find_packages(where='src'),
     package_dir={'': 'src'},
     py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob.glob('src/*.py')],
     include_package_data=True,
     install_requires=read_requirements('requirements.txt'),
     author="Zan Yuan",
     author_email="yfinddream@gmail.com",
     description="gene signature score for gene expression matrix",
     long_description=open('README.rst').read(),
     url="https://github.com/seqyuan/sigc",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
