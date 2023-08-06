from setuptools import find_packages, setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="maltk",
    packages=["malt", "malt/py_ui"],
    packages_dir=find_packages(),
    version="0.0.0.1",
    description="Model Assisted Object Labeling Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Matthew Sessions",
    keywords = [
        "tensorflow",
        "object detection",
        "object labeling",
        "image labeler",
        "model assisted labeling",
        "video to image"
    ],
    install_requires=[
        "PySide6",
        "tflite-support>=0.4.3",
        "pascal_voc_writer",
        "opencv-python",
    ],
    entry_points={"console_scripts": ["malt=malt.main:main", "maltk=malt.main:main"]},
)
