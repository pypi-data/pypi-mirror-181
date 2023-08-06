from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')
VERSION = '1.0.1'

setup(
    name="mkdocs-ubleiden-theme",
    version=VERSION,
    url='https://github.com/LeidenUniversityLibrary/mkdocs-ubleiden-theme',
    license='GPLv3',
    description='UBL theme for MkDocs, extending Material for MkDocs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Leiden University Libraries',
    author_email='beheer@library.leidenuniv.nl',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    install_requires=[
        'mkdocs-material>=8.5.11',
    ],
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'ubleiden = ubleiden_theme',
        ]
    },
    zip_safe=False
)
