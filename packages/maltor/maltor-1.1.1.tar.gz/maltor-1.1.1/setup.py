from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='maltor',
    version='1.1.1',
    author='Thomas Gröbmair (Cryp7ic)',
    author_email='cryp7ic@tutanota.com',
    license='GPL',
    description='Maltor is A CLI tool for static malware analysis written in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Cryp7ic/Maltor',
    package_dir={'src': 'src'},
    py_modules=['maltor'],
    package_data={'src': ['src/*.txt']},
    packages=find_packages(include=['maltor', 'maltor.*']),
    include_package_data=True,
    install_requires=[requirements],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    entry_points={'console_scripts': ['maltor=src.maltor:main']},
)
