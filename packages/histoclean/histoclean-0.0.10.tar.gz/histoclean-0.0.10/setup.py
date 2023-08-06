from setuptools import setup, find_packages

setup(
    name='histoclean',
    version='0.0.10',
    description='Histoclean (initial package setup)',
    py_modules=["histoclean"],
    package_dir={'': 'src'},
    install_requires=[
        "Pillow", "opencv-python", "imageio",
        "numpy", "numba", "imagecorruptions",
        "openslide-python", "scipy", "imgaug",
        "scikit-image"
    ],
    include_package_data=True,
    package_data={"Icon": ["*.png", "*.ico"]}

)