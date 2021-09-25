from setuptools import setup, find_packages

setup(
    name="dipcoat-substrate",
    version="0.0.0",
    description="Python package for dip coating substrate image detection",
    author="Jisoo Song",
    author_email="jeesoo9595@snu.ac.kr",
    url="https://github.com/JSS95/dipcoat-substrate",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["opencv-python>=4.3.0",
                      "sphinx", "numpydoc", "sphinx_rtd_theme"]
)
