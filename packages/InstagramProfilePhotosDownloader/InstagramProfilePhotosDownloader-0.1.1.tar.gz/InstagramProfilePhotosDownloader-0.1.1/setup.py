"""
InstagramProfilePhotosDownloader
Copyright (C) 2022  Massimo Pavoni

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pathlib import Path

from setuptools import setup, find_packages

README = (Path(__file__).parent / "README.md").read_text()

setup(
    name='InstagramProfilePhotosDownloader',
    version='0.1.1',
    description="A simple scraping tool to download an Instagram profile photos.",
    long_description=README,
    long_description_content_type="text/markdown",
    author='Massimo Pavoni',
    author_email='maspavoni@gmail.com',
    url='https://github.com/massimopavoni/InstagramProfilePhotosDownloader',
    license_files='LICENSE',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Operating System :: OS Independent"],
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=[
        'selenium>=4.7',
        'requests>=2.28'],
    entry_points={
        'console_scripts': [
            'InstagramProfilePhotosDownloader=ippd.__main__:main',
            'ippd=ippd.__main__:main']})
