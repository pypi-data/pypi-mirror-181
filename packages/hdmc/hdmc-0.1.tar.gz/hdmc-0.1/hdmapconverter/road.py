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


class Road:
    
    def __init__(self, id):
        self.id = id
        self.nodes = []
        self.type = None
        self.subtype = None

class Node:
    
    def __init__(self, id, lat, lng):
        self.id = id
        self.lat = float(lat)
        self.lng = float(lng)
        self.lanelet_node_type = None
