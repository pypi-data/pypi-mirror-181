from setuptools import setup, find_packages

setup(
    name='dextrusion',
    version='0.0.1',
    description='DeXtrusion: automatic detection of cell extrusion in epithelial tissu',
      author='Gaëlle Letort and Alexis Villars',
      url='https://gitlab.pasteur.fr/gletort/dextrusion',
      package_dir={'':'src'},
      packages=find_packages('src'),
    install_requires=[
        "matplotlib",
        "numpy",
        "opencv-python",
        "tifffile>=2022.2.2",
        "roifile",
        "scikit-image",
        "scikit-learn",
        "scipy",
        "tensorflow==2.8", 
        "protobuf==3.19",
        "ipython"
    ],
)

