###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#                                                                           
# Created by Slastnikova Anna <slastnikova02@mail.ru>   
# and Rami Al-Naim <alnaim.ri@starline.ru>                          
#   
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import setuptools

with open("README.md", "r") as file_with_description:
    long_description = file_with_description.read()

with open('requirements.txt') as file_with_requirements:
    requirements = file_with_requirements.read().splitlines()

setuptools.setup(
    name="hdmc",
    version="0.1",
    author="Slastnikova Anna",
    author_email="slastnikova02@mail.ru",
    description="HD map converter between Lanelet2 and Apollo OpenDRIVE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = ['converter', 'apollo', 'opendrive', "oscar", "lanelet2", "hdmap"],
    # url="https://gitlab.com/starline/",
    packages=['hdmapconverter'],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
