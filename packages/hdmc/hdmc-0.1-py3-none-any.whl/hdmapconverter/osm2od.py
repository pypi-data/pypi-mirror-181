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


import numpy as np
import math
import datetime
import argparse
import utm

from geopy import distance
from lxml import etree
from tqdm import tqdm

from road import Node, Road

from proto.map import map_pb2
from proto.map import map_lane_pb2


utmz = {"zone":36, "letter":"N", "full":"36N"}

def readNodes(e):
    nodes = {}
    
    # Read all nodes and their coordinates into an array
    for node in e.findall('node'):
        n = Node(node.get("id"), node.get("lat"), node.get("lon"))

        for tag in node.findall('tag'):
            if tag.get('k') == "lanelet_node_type":
                n.lanelet_node_type = tag.get('v')

        nodes[node.get("id")] = n
    return nodes


def readRoads(e, nodes):
    roads = []

    # Desired road types
    driveable = ["motorway", "trunk", "primary", "secondary", "tertiary", "residential", "service", "living_street", "track", "road", "unclassified"]
    for r in driveable.copy():
        driveable.append(r + "_link")

    # Read all roads/ways into an array
    for road in e.findall('way'):
        road_id = road.get("id")
        r = Road(road_id)

        supported = False

        # print(road.findall('tag'))

        # Read all information about each road
        for tag in road.findall('tag'):
            # print(tag)
            if tag.get('k') == "type":
                r.type = tag.get('v')
            elif tag.get('k') == "subtype":
                r.subtype = tag.get('v')

        #     setattr(r, tag.get("k").replace(":", "_"), tag.get("v"))

        #     # Filter out unwanted roads
        #     if tag.get('k') == "highway":
        #         if tag.get('v') in driveable:
        #             supported = True
        # if not supported:
        #     continue
        
        # Get nodes
        road_nodes = road.findall('nd')
        
        # Connect to the nodes
        for nd in road_nodes:
            r.nodes.append(nodes[nd.get("ref")])
            
        if len(road_nodes) > 0:
            print("Road {} has {} nodes".format(road_id, len(road_nodes)))
            roads.append(r)
        else:
            print("Skip road {}".format(road_id))

    return roads

def readOSM(filename):
    e = etree.parse(filename).getroot()

    print("Reading file {}".format(filename))

    nodes = readNodes(e)
    roads = readRoads(e, nodes)

    print("Finished reading file, found {} nodes and {} roads.".format(len(nodes), len(roads)))

    return nodes, roads

def read_config(filename):
    f = open(filename)
    conf = {}
    for l in f:
        s = l.strip().split(",")
        s[0] = s[0].lower().replace(" ", "")
        if s[1] != "":
            s[1] = int(s[1])
        else:
            s[1] = None
        if s[2] != "":
            s[2] = float(s[2])
        else:
            s[2] = None
        conf[s[0]] = s[1:3]
    f.close()
    return conf

def format_coord(n):
    return "{:.9e}".format(n)

def buildTxt(filename, roads):
    # borderTypes = { 0 : "UNKNOWN",
    #                 1 : "DOTTED_YELLOW",
    #                 2 : "DOTTED_WHITE",
    #                 3 : "SOLID_YELLOW",
    #                 4 : "SOLID_WHITE",
    #                 5 : "DOUBLE_YELLOW",
    #                 6 : "CURB"}

    lane_width = 3.0
    map_pb = map_pb2.Map()
    types = []
    for road in roads:
        if road.type in ["stop_line", "zebra_marking", "traffic_light", 'traffic_sign']:
            continue

        lane_pb = map_pb.lane.add()
        lane_pb.id.id = road.id
        central_curve_pb = lane_pb.central_curve.segment.add()
        left_boundary_pb = lane_pb.left_boundary.curve.segment.add()
        right_boundary_pb = lane_pb.right_boundary.curve.segment.add()

        boundary_type = lane_pb.left_boundary.boundary_type.add()
        boundary_type.s = 0
        
        if road.type == "curbstone":
            boundary_type.types.append(6)
        else:
            boundary_type.types.append(0)

        boundary_type = lane_pb.right_boundary.boundary_type.add()
        boundary_type.s = 0
        boundary_type.types.append(0)

        left_boundary_points = find_parallel(road.nodes, True, lane_width/2, lane_width/2)
        right_boundary_points = find_parallel(road.nodes, False, lane_width/2, lane_width/2)
        
        types.append(str(road.type) + " " + str(road.subtype))

        len_points = min(len(left_boundary_points), len(right_boundary_points))
        for i in range(len_points):
            point_pb = central_curve_pb.line_segment.point.add()

            left_point = left_boundary_points[i]
            right_point = right_boundary_points[i]

            proj = utm.from_latlon((left_point[0] + right_point[0]) / 2,
                                   (left_point[1] + right_point[1]) / 2)[:2]
            point_pb.x = proj[0]
            point_pb.y = proj[1]

        for point in left_boundary_points:
            point_pb = left_boundary_pb.line_segment.point.add()
            proj = utm.from_latlon(point[0], point[1])[:2]
            point_pb.x = proj[0]
            point_pb.y = proj[1]
        
        for point in right_boundary_points:
            point_pb = right_boundary_pb.line_segment.point.add()
            proj = utm.from_latlon(point[0], point[1])[:2]
            point_pb.x = proj[0]
            point_pb.y = proj[1]
    
    print(set(types))
    map_file = open("./base_map.txt", 'w')
    map_file.write(str(map_pb))
    map_file.close()


def buildXML(filename, roads, pretty, conf):

    name = filename.split(".")[0].split("/")[-1]
    #filename = name + ".xml"
    filename = "base_map.xml"
    
    print("Building XML output...")

    root = etree.Element('OpenDRIVE')
    root.set("xmlns", "http://www.opendrive.org")
    tree = etree.ElementTree(root)

    # Setup header record
    header = etree.SubElement(root, "header")
    header.set("revMajor", "1")
    header.set("revMinor", "0")
    header.set("vendor", "StarLine")
    header.set("name", name)
    header.set("version", "1.0")
    header.set("date", datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    # Maximum and minimum coordinate values
    # North, south, east, west
    max_coord = [None,None,None,None]

    # Setup Geo Reference
    georef = etree.SubElement(header, "geoReference")
    georef.text = etree.CDATA("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

    junctions = {}
    for r in tqdm(roads, "Generating roads"):
        road = etree.SubElement(root, "road")

        num_lanes = 1
        lane_width = 3.0
        if hasattr(r, "name"):
            road.set("name", r.name)

            name = r.name.lower().replace(" ", "")
            if conf != None:
                if name in conf.keys():
                    if conf[name][0] != None:
                        num_lanes = conf[name][0]
                    if conf[name][1] != None:
                        lane_width = conf[name][1]
        else:
            road.set("name", "")

        road.set("id", r.id)

        road.set("junction", "-1")

        # Lanes
        lanes = etree.SubElement(road, "lanes")
        
        num_lanes = 0
        lane_nums = [0,0]
        if hasattr(r, "lanes_forward"):
            lane_nums[0] = int(r.lanes_forward)
        if hasattr(r, "lanes_backward"):
            lane_nums[1] = int(r.lanes_backward)

        if hasattr(r, "lanes"):
            lane_nums[0] = int(r.lanes)//2 + int(r.lanes)%2
            lane_nums[1] = int(r.lanes)//2

        num_lanes = lane_nums[0] + lane_nums[1]
        if num_lanes == 0:
            lane_nums[0] = 1
            num_lanes = 1

        laneSec = etree.SubElement(lanes, "laneSection")
        laneSec.set("singleSide", "true")          # True if both directions share the same laneSection

        boundaries = etree.SubElement(laneSec, "boundaries")

        # If the lane number is odd and greater than 1, only care about num_lanes-1 lanes
        if num_lanes > 1 and num_lanes % 2 != 0:
            num_lanes -= 1
        elif num_lanes == 0:
            num_lanes = 1

        setattr(r, "lanes", num_lanes)

        # Lane boundaries
        left_boundary = etree.SubElement(boundaries, "boundary")
        left_boundary.set("type", "leftBoundary")

        right_boundary = etree.SubElement(boundaries, "boundary")
        right_boundary.set("type", "rightBoundary")

        # Lane boundary geometries
        leftb_geo = etree.SubElement(left_boundary, "geometry")
        leftb_geo_ps = etree.SubElement(leftb_geo, "pointSet")

        rightb_geo = etree.SubElement(right_boundary, "geometry")
        rightb_geo_ps = etree.SubElement(rightb_geo, "pointSet")
        
        nodes = []
        for n in r.nodes:
            nodes.append([n.lat, n.lng])

        if num_lanes == 1:
            left_boundary_points = find_parallel(r.nodes, True, lane_width/2, lane_width/2)
            right_boundary_points = find_parallel(r.nodes, False, lane_width/2, lane_width/2)
        else:
            boundary_width = num_lanes/2.0 *lane_width
            left_boundary_points = find_parallel(r.nodes, True, boundary_width, boundary_width)
            right_boundary_points = find_parallel(r.nodes, False, boundary_width, boundary_width)

        for i in range(len(r.nodes)):
            # Left
            lp = etree.SubElement(leftb_geo_ps, "point")
            lp.set("x", format_coord(left_boundary_points[i][1]))
            lp.set("y", format_coord(left_boundary_points[i][0]))
            lp.set("z", format_coord(0.0))

            # Right
            rp = etree.SubElement(rightb_geo_ps, "point")
            rp.set("x", format_coord(right_boundary_points[i][1]))
            rp.set("y", format_coord(right_boundary_points[i][0]))
            rp.set("z", format_coord(0.0))

        # Center is supposed to store the reference line
        # Left/right stores the borders of left/right lanes

        center = etree.SubElement(laneSec, "center")
        center_lane = etree.SubElement(center, "lane")

        center_lane.set("id", "0")
        center_lane.set("uid", "{}_0".format(r.id))
        center_lane.set("type", "none")
        #center_lane.set("direction", "bidirection")
        #center_lane.set("turnType", "noTurn")   # Not sure what this means

        center_border = etree.SubElement(center_lane, "border")
        center_border.set("virtual", "FALSE")
        cl_geo = etree.SubElement(center_border, "geometry")
        cl_geo.set("sOffset", "0")
        cl_geo.set("x", format_coord(r.nodes[0].lng))
        cl_geo.set("y", format_coord(r.nodes[0].lat))
        cl_geo.set("z", format_coord(0.0))
        cl_geo.set("length", str(road_length(r.nodes)))

        cborder_type = etree.SubElement(center_border, "borderType")
        cborder_type.set("sOffset", "0")
        cborder_type.set("type", "solid" if num_lanes == 1 else "broken")
        cborder_type.set("color", "yellow")

        cl_geo_ps = etree.SubElement(cl_geo, "pointSet")

        center_nodes = nodes if num_lanes > 1 else find_parallel(r.nodes, True, lane_width/2.0, lane_width/2.0)
        for n in center_nodes:
            p = etree.SubElement(cl_geo_ps, "point")
            p.set("x", format_coord(n[1]))
            p.set("y", format_coord(n[0]))
            p.set("z", format_coord(0.0))

            # Check for min/max values:
            # North
            if max_coord[0] == None or max_coord[0] < n[0]:
                max_coord[0] = n[0]

            # South
            if max_coord[1] == None or max_coord[1] > n[0]:
                max_coord[1] = n[0]

            # East
            if max_coord[2] == None or max_coord[2] < n[1]:
                max_coord[2] = n[1]

            # West
            if max_coord[3] == None or max_coord[3] > n[1]:
                max_coord[3] = n[1]

        right = etree.SubElement(laneSec, "right")

        if num_lanes > 1:
            left = etree.SubElement(laneSec, "left")

        num_side_lanes = math.ceil(num_lanes/2)
        for i in range(num_side_lanes):
            # Right, only add this if num_lanes == 1
            right_lane = etree.SubElement(right, "lane")
            right_lane.set("id", "-{}".format(i+1))
            right_lane.set("uid", "{}_1{}".format(r.id, i+1))
            right_lane.set("type", "driving")
            right_lane.set("direction", "bidirection" if num_lanes == 1 else "forward")
            right_lane.set("turnType", "noTurn")    # Not sure what this means

            # Lane center
            right_center = etree.SubElement(right_lane, "centerLine")
                
            center_pos = i*lane_width+(lane_width/2)
            if num_lanes == 1:
                right_center_points = nodes
            else:
                right_center_points = find_parallel(r.nodes, False, center_pos,  center_pos)

            rc_geo = etree.SubElement(right_center, "geometry")
            rc_geo.set("sOffset", "0")
            rc_geo.set("x", format_coord(right_center_points[0][1]))
            rc_geo.set("y", format_coord(right_center_points[0][0]))
            rc_geo.set("z", format_coord(0.0))
            rc_geo.set("length", str(road_length(right_center_points)))

            rc_geo_ps = etree.SubElement(rc_geo, "pointSet")

            for n in right_center_points:
                p = etree.SubElement(rc_geo_ps, "point")
                p.set("x", format_coord(n[1]))
                p.set("y", format_coord(n[0]))
                p.set("z", format_coord(0.0))

            # Lane border
            right_border = etree.SubElement(right_lane, "border")
            right_border.set("virtual", "FALSE")     # "Identify whether the lane boundary exists in real world"

            rborder_type = etree.SubElement(right_border, "borderType")
            rborder_type.set("sOffset", "0")
            rborder_type.set("type", "solid" if i == num_side_lanes-1 else "broken")
            rborder_type.set("color", "yellow" if i == num_side_lanes-1 else "white")

            if num_lanes == 1:
                right_border_points = find_parallel(r.nodes, False, lane_width/2.0, lane_width/2.0)
            else:
                right_border_points = find_parallel(r.nodes, False, (i+1)*lane_width, (i+1)*lane_width)

            rb_geo = etree.SubElement(right_border, "geometry")
            rb_geo.set("sOffset", "0")
            rb_geo.set("x", format_coord(right_border_points[0][1]))
            rb_geo.set("y", format_coord(right_border_points[0][0]))
            rb_geo.set("z", format_coord(0.0))
            rb_geo.set("length", str(road_length(right_border_points)))

            rb_geo_ps = etree.SubElement(rb_geo, "pointSet")

            for n in right_border_points:
                p = etree.SubElement(rb_geo_ps, "point")
                p.set("x", format_coord(n[1]))
                p.set("y", format_coord(n[0]))
                p.set("z", format_coord(0.0))

            if num_lanes > 1:
                left_lane = etree.SubElement(left, "lane")
                left_lane.set("id", "{}".format(i+1))
                left_lane.set("uid", "{}_0{}".format(r.id, i+1))
                left_lane.set("type", "driving")
                left_lane.set("direction", "backward")
                left_lane.set("turnType", "noTurn")    # Not sure what this means

                # Lane center
                left_center = etree.SubElement(left_lane, "centerLine")
                    
                left_center_points = find_parallel(r.nodes, True, center_pos, center_pos)

                lc_geo = etree.SubElement(left_center, "geometry")
                lc_geo.set("sOffset", "0")
                lc_geo.set("x", format_coord(left_center_points[0][1]))
                lc_geo.set("y", format_coord(left_center_points[0][0]))
                lc_geo.set("z", format_coord(0.0))
                lc_geo.set("length", str(road_length(left_center_points)))

                lc_geo_ps = etree.SubElement(lc_geo, "pointSet")

                for n in left_center_points:
                    p = etree.SubElement(lc_geo_ps, "point")
                    p.set("x", format_coord(n[1]))
                    p.set("y", format_coord(n[0]))
                    p.set("z", format_coord(0.0))

                # Lane border
                left_border = etree.SubElement(left_lane, "border")
                left_border.set("virtual", "FALSE")     # "Identify whether the lane boundary exists in real world"

                lborder_type = etree.SubElement(left_border, "borderType")
                lborder_type.set("sOffset", "0")
                lborder_type.set("type", "solid" if i == num_side_lanes-1 else "broken")
                lborder_type.set("color", "yellow" if i == num_side_lanes-1 else "white")

                left_border_points = find_parallel(r.nodes, True, (i+1)*lane_width, (i+1)*lane_width)

                lb_geo = etree.SubElement(left_border, "geometry")
                lb_geo.set("sOffset", "0")
                lb_geo.set("x", format_coord(left_border_points[0][1]))
                lb_geo.set("y", format_coord(left_border_points[0][0]))
                lb_geo.set("z", format_coord(0.0))
                lb_geo.set("length", str(road_length(left_border_points)))

                lb_geo_ps = etree.SubElement(lb_geo, "pointSet")

                for n in left_border_points:
                    p = etree.SubElement(lb_geo_ps, "point")
                    p.set("x", format_coord(n[1]))
                    p.set("y", format_coord(n[0]))
                    p.set("z", format_coord(0.0))

            # Sample Associations
            # Distance from the center to the edges
            right_sample = etree.SubElement(right_lane, "sampleAssociates")
            right_road_sample = etree.SubElement(right_lane, "roadSampleAssociations")

            if num_lanes > 1:
                left_sample = etree.SubElement(left_lane, "sampleAssociates")
                left_road_sample = etree.SubElement(left_lane, "roadSampleAssociations")

            road_len = road_length(r.nodes)
            for s in range(len(r.nodes)):
                s_pos = road_len/len(r.nodes) * s
                right_samp = etree.SubElement(right_sample, "sampleAssociate")
                right_samp.set("sOffset", str(int(s_pos)))
                right_samp.set("leftWidth", str(lane_width/2))
                right_samp.set("rightWidth", str(lane_width/2))

                far_boundary = (num_lanes//2 + i + 0.5) * lane_width
                close_boundary = (math.ceil(num_lanes/2) - (i + 1) + 0.5) * lane_width
                right_road_samp = etree.SubElement(right_road_sample, "sampleAssociation")
                right_road_samp.set("sOffset", str(int(s_pos)))
                right_road_samp.set("leftWidth", str(far_boundary))
                right_road_samp.set("rightWidth", str(close_boundary))

                if num_lanes > 1:
                    left_samp = etree.SubElement(left_sample, "sampleAssociate")
                    left_samp.set("sOffset", str(int(s_pos)))
                    left_samp.set("leftWidth", str(lane_width/2))
                    left_samp.set("rightWidth", str(lane_width/2))

                    left_road_samp = etree.SubElement(left_road_sample, "sampleAssociation")
                    left_road_samp.set("sOffset", str(int(s_pos)))
                    left_road_samp.set("leftWidth", str(close_boundary))
                    left_road_samp.set("rightWidth", str(far_boundary))
        
        # Junctions
        # OSM draws junctions as a shared node between ways

        for road in roads:
            if r == road:
                continue

            for n in r.nodes:
                if n in road.nodes:
                    if n not in junctions.keys():
                        junctions[n] = set([])
                    junctions[n].update([r, road]) 

    for i, j in tqdm(enumerate(junctions.keys()), "Generating junctions", len(junctions)):
        junc = etree.SubElement(root, "junction")
        junc.set("id", str(i))
        
        junc_outline = etree.SubElement(junc, "outline")
        point = np.array(utm.from_latlon(j.lat, j.lng)[0:2])
        v = np.array([2*lane_width, 0])
        # This is probably a bit unnecessary as its the same in every iteration
        outline = list(map(lambda x: rotate_vector(x[1], x[0]*math.pi/2), enumerate([v]*4))) + point
        for c in outline:
            p = utm.to_latlon(c[0], c[1], utmz["zone"], utmz["letter"])
            cb = etree.SubElement(junc_outline, "cornerGlobal")
            cb.set("x", format_coord(p[1]))
            cb.set("y", format_coord(p[0]))
            cb.set("z", format_coord(0.0))

        # Generate connecting roads
        # Horrible code incoming
        vecs = []
        for r in junctions[j]:
            n_i = r.nodes.index(j)
            p = utm.from_latlon(j.lat, j.lng)
            if n_i == 0:
                p2 = utm.from_latlon(r.nodes[1].lat, r.nodes[1].lng)
                vecs.append({"vec" : np.array([p2[0]-p[0], p2[1]-p[1]]), "road" : r , "pos" : -2})
            elif n_i == len(r.nodes)-1:
                p2 = utm.from_latlon(r.nodes[-2].lat, r.nodes[-2].lng)
                vecs.append({"vec" : np.array([p2[0]-p[0], p2[1]-p[1]]), "road" : r , "pos" : 2})
            else:
                p0 = utm.from_latlon(r.nodes[n_i-1].lat, r.nodes[n_i-1].lng)
                p1 = utm.from_latlon(r.nodes[n_i+1].lat, r.nodes[n_i+1].lng)
                
                vecs.append({"vec" : np.array([p1[0]-p[0], p1[1]-p[1]]), "road" : r , "pos" : 1})
                vecs.append({"vec" : np.array([p0[0]-p[0], p0[1]-p[1]]), "road" : r , "pos" : -1})

        for v in vecs:
            v["vec"] = v["vec"]*lane_width/np.linalg.norm(v["vec"])

        conn_roads = []
        v = 0
        while v  < len(vecs)-1:
            v2 = v+1
            while v2 < len(vecs):
                v3 = vecs[v2]["vec"]-vecs[v]["vec"]
                if v3[0] != 0 and v3[1] != 0:
                    conn_roads.append({"vecs" : [vecs[v]["vec"], v3], "start" : {"road" : vecs[v]["road"], "pos" : vecs[v]["pos"]}, "end" : {"road" : vecs[v2]["road"], "pos" : vecs[v2]["pos"]}})
                v2 += 1
            v += 1

        conns = 0
        for r_id, r in enumerate(conn_roads):
            if r["start"]["road"] == r["end"]["road"]:
                continue
            road = etree.SubElement(root, "road")
            road.set("name", "connroad")
            road_id = "conn_{}_{}".format(i, str(r_id))
            road.set("id", road_id)
            road.set("junction", str(i))

            points = [point+r["vecs"][0], point+r["vecs"][0]+r["vecs"][1]]
            
            # Make curve
            center = np.array(utm.from_latlon(j.lat, j.lng)[:2])
            points = list(map(lambda x: points[0] + x, np.array(make_curve(np.array([0, 0]), center - points[0], points[1] - points[0]))))
            points = list(map(lambda x: utm.to_latlon(x[0], x[1], utmz["zone"], utmz["letter"]), points))

            road_geo_link = etree.SubElement(road, "link")
            rgl_pre = etree.SubElement(road_geo_link, "predecessor")
            rgl_pre.set("elementType", "road")
            rgl_pre.set("elementId", r["start"]["road"].id)
            rgl_pre.set("contactPoint", "start" if r["start"]["pos"] < 0 else "end")

            rgl_succ = etree.SubElement(road_geo_link, "successor")
            rgl_succ.set("elementType", "road")
            rgl_succ.set("elementId", r["end"]["road"].id)
            rgl_succ.set("contactPoint", "end" if r["start"]["pos"] > 0 else "start")
            
            conn_link = etree.Element("link")
            start_road = root.xpath("//road[@id = '{}']".format(r["start"]["road"].id))[0]
            if abs(r["start"]["pos"]) > 1:
                start_link = start_road.findall("link")
                if len(start_road.findall("link")) == 0:
                    start_link = etree.SubElement(start_road, "link")
                else:
                    start_link = start_link[0]
                if abs(r["start"]["pos"]) > 0:
                    succ = etree.SubElement(start_link, "successor" if r["start"]["pos"] < 0 else "predecessor")
                    succ.set("elementType", "road")
                    succ.set("elementId", road_id)
                    succ.set("contactPoint", "start")

                sr_lanes = start_road.xpath(".//left/lane | .//right/lane")
                for lane in sr_lanes:
                    sr_lane_link = lane.findall("link")
                    if len(sr_lane_link) == 0:
                        sr_lane_link = etree.SubElement(lane, "link")
                    else:
                        sr_lane_link = sr_lane_link[0]
                    sr_link = etree.SubElement(sr_lane_link, "successor" if r["start"]["pos"] < 0 else "predecessor") 
                    sr_link.set("id", "{}_11".format(road_id))

            sr_lanes = start_road.xpath(".//left/lane | .//right/lane")
            for lane in sr_lanes:
                conn_sr_link = etree.SubElement(conn_link, "predecessor")
                conn_sr_link.set("id", lane.get("uid"))

            end_road = root.xpath("//road[@id = '{}']".format(r["end"]["road"].id))[0]
            if abs(r["end"]["pos"]) > 1:
                end_link = end_road.findall("link")
                if len(end_road.findall("link")) == 0:
                    end_link = etree.SubElement(end_road, "link")
                else:
                    end_link = end_link[0]
                if abs(r["end"]["pos"]) > 0:
                    succ = etree.SubElement(end_link, "predecessor" if r["end"]["pos"] > 0 else "successor")
                    succ.set("elementType", "road")
                    succ.set("elementId", road_id)
                    succ.set("contactPoint", "end")

                er_lanes = end_road.xpath(".//left/lane | .//right/lane")
                for lane in er_lanes:
                    er_lane_link = lane.findall("link")
                    if len(er_lane_link) == 0:
                        er_lane_link = etree.SubElement(lane, "link")
                    else:
                        er_lane_link = er_lane_link[0]
                    er_link = etree.SubElement(er_lane_link, "predecessor" if r["end"]["pos"] > 0 else "successor") 
                    er_link.set("id", "{}_11".format(road_id))

            er_lanes = end_road.xpath(".//left/lane | .//right/lane")
            for lane in er_lanes:
                    conn_er_link = etree.SubElement(conn_link, "successor")
                    conn_er_link.set("id", lane.get("uid"))

            lanes = etree.SubElement(road, "lanes")
            lane_sec = etree.SubElement(lanes, "laneSection")
            lane_sec.set("singleSide", "true")
            
            start_width = lane_width
            end_width = lane_width
            if hasattr(r["start"]["road"], "name"):
                start_name = r["start"]["road"].name.lower().replace(" ", "")
                if conf != None:
                    if start_name in conf.keys():
                        if conf[start_name][1] != None:
                            start_width = conf[start_name][1]

            if hasattr(r["end"]["road"], "name") :
                end_name = r["end"]["road"].name.lower().replace(" ", "")
                if conf != None:
                    if end_name in conf.keys():
                        if conf[end_name][1] != None:
                            end_width = conf[end_name][1]

            left_boundary_points = find_parallel(points, True, start_width/2, end_width/2)
            right_boundary_points = find_parallel(points, False, start_width/2, end_width/2)

            ls_right_boundary = etree.SubElement(lane_sec, "boundaries")
            ls_right_boundary.set("type", "rightBoundary")

            ls_right_boundary_geo = etree.SubElement(ls_right_boundary, "geometry")
            lslb_geo_ps = etree.SubElement(ls_right_boundary_geo, "pointSet")

            for p in right_boundary_points:
                ps_point = etree.SubElement(lslb_geo_ps, "point")
                ps_point.set("x", format_coord(p[1]))
                ps_point.set("y", format_coord(p[0]))
                ps_point.set("z", format_coord(0.0))

            ls_left_boundary = etree.SubElement(lane_sec, "boundaries")
            ls_left_boundary.set("type", "leftBoundary")

            ls_left_boundary_geo = etree.SubElement(ls_left_boundary, "geometry")
            lslb_geo_ps = etree.SubElement(ls_left_boundary_geo, "pointSet")

            for p in left_boundary_points:
                ps_point = etree.SubElement(lslb_geo_ps, "point")
                ps_point.set("x", format_coord(p[1]))
                ps_point.set("y", format_coord(p[0]))
                ps_point.set("z", format_coord(0.0))

            center = etree.SubElement(lane_sec, "center")
            center_lane = etree.SubElement(center, "lane")
            center_lane.set("id", str(0))
            center_lane.set("uid", "{}_0".format(road_id))
            center_lane.set("type", "none")

            center_lane_border = etree.SubElement(center_lane, "border")
            center_lane_border.set("virtual", "TRUE")

            cborder_type = etree.SubElement(center_lane_border, "borderType")
            cborder_type.set("sOffset", "0")
            cborder_type.set("type", "none")
            cborder_type.set("color", "none")

            center_geo = etree.SubElement(center_lane_border, "geometry")
            center_geo.set("sOffset", str(0))
            center_geo.set("x", format_coord(left_boundary_points[0][1]))
            center_geo.set("y", format_coord(left_boundary_points[0][0]))
            center_geo.set("z", format_coord(0.0))
            center_geo.set("length", str(road_length(left_boundary_points)))
            
            center_geo_ps = etree.SubElement(center_geo, "pointSet")

            for p in left_boundary_points:
                cg_point = etree.SubElement(center_geo_ps, "point")
                cg_point.set("x", format_coord(p[1]))
                cg_point.set("y", format_coord(p[0]))
                cg_point.set("z", format_coord(0.0))

            right = etree.SubElement(lane_sec, "right")
            right_lane = etree.SubElement(right, "lane")
            right_lane.set("id", str(-1))
            right_lane.set("uid", "{}_11".format(road_id))
            right_lane.set("type", "driving")
            right_lane.set("direction", "bidirection")
            right_lane.set("turnType", "noTurn")

            right_lane.insert(1, conn_link)

            right_lane_cl = etree.SubElement(right_lane, "centerLine")

            right_geo = etree.SubElement(right_lane_cl, "geometry")
            right_geo.set("sOffset", str(0))
            right_geo.set("x", format_coord(points[0][1]))
            right_geo.set("y", format_coord(points[0][0]))
            right_geo.set("z", format_coord(0.0))
            right_geo.set("length", str(road_length(points)))
            
            right_geo_ps = etree.SubElement(right_geo, "pointSet")

            for p in points:
                rg_point = etree.SubElement(right_geo_ps, "point")
                rg_point.set("x", format_coord(p[1]))
                rg_point.set("y", format_coord(p[0]))
                rg_point.set("z", format_coord(0.0))

            right_lane_border = etree.SubElement(right_lane, "border")
            right_lane_border.set("virtual", "TRUE")

            rborder_type = etree.SubElement(right_lane_border, "borderType")
            rborder_type.set("sOffset", "0")
            rborder_type.set("type", "none")
            rborder_type.set("color", "none")

            right_border_geo = etree.SubElement(right_lane_border, "geometry")
            right_border_geo.set("sOffset", str(0))
            right_border_geo.set("x", format_coord(right_boundary_points[0][1]))
            right_border_geo.set("y", format_coord(right_boundary_points[0][0]))
            right_border_geo.set("z", format_coord(0.0))
            right_border_geo.set("length", str(road_length(right_boundary_points)))
            
            right_border_geo_ps = etree.SubElement(right_border_geo, "pointSet")

            for p in right_boundary_points:
                rg_point = etree.SubElement(right_border_geo_ps, "point")
                rg_point.set("x", format_coord(p[1]))
                rg_point.set("y", format_coord(p[0]))
                rg_point.set("z", format_coord(0.0))

            right_sample = etree.SubElement(right_lane, "sampleAssociates")
            right_road_sample = etree.SubElement(right_lane, "roadSampleAssociations")

            road_len = road_length(points)
            for s in range(len(points)):
                s_pos = road_len/len(points) * s
                right_samp = etree.SubElement(right_sample, "sampleAssociate")
                right_samp.set("sOffset", str(int(s_pos)))
                right_samp.set("leftWidth", str(lane_width/2))
                right_samp.set("rightWidth", str(lane_width/2))

                right_road_samp = etree.SubElement(right_road_sample, "sampleAssociation")
                right_road_samp.set("sOffset", str(int(s_pos)))
                right_road_samp.set("leftWidth", str(lane_width/2))
                right_road_samp.set("rightWidth", str(lane_width/2))

            conn = etree.SubElement(junc, "connection")
            conn.set("id", str(conns))
            conn.set("incomingRoad", str(r["start"]["road"].id))
            conn.set("connectingRoad", str(road_id))
            conn.set("contactPoint", "start")

            for l in range(math.ceil(r["start"]["road"].lanes/2)):
                conn_s_link = etree.SubElement(conn, "laneLink")
                conn_s_link.set("from", str(-(l+1)))
                conn_s_link.set("to", str(-1))

                if r["start"]["road"].lanes > 1:
                    conn_sl_link = etree.SubElement(conn, "laneLink")
                    conn_sl_link.set("from", str(l+1))
                    conn_sl_link.set("to", str(-1))

            conns += 1

            conn = etree.SubElement(junc, "connection")
            conn.set("id", str(conns))
            conn.set("incomingRoad", str(r["end"]["road"].id))
            conn.set("connectingRoad", str(road_id))
            conn.set("contactPoint", "end")

            for l in range(math.ceil(r["end"]["road"].lanes/2)):
                conn_s_link = etree.SubElement(conn, "laneLink")
                conn_s_link.set("from", str(-(l+1)))
                conn_s_link.set("to", str(-1))

                if r["end"]["road"].lanes > 1:
                    conn_sl_link = etree.SubElement(conn, "laneLink")
                    conn_sl_link.set("from", str(l+1))
                    conn_sl_link.set("to", str(-1))

            conns += 1

    header.set("north", format_coord(max_coord[0]))
    header.set("south", format_coord(max_coord[1]))
    header.set("east", format_coord(max_coord[2]))
    header.set("west", format_coord(max_coord[3]))

    print("XML successfully generated, writing to '{}'".format(filename))

    tree.write(filename, xml_declaration=True, pretty_print=pretty, encoding='UTF-8')

# Calculate road length
def road_length(road):
    length = 0
    for i in range(len(road)-1):
        p1 = road[i]
        p2 = road[i+1]
        
        if isinstance(p1, Node):
            length += distance.distance((p1.lat, p1.lng), (p2.lat, p2.lng)).m
        else:
            length += distance.distance(p1, p2).m

    return length
    
def vector_angle(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)

    dot = np.dot(v1_u, v2_u)
    det = v1_u[0]*v2_u[1] - v1_u[1]*v2_u[0]

    return np.arctan2(det, dot)

def rotate_vector(vector, angle):
    v_x = math.cos(angle) * vector[0] - math.sin(angle) * vector[1]
    v_y = math.sin(angle) * vector[0] + math.cos(angle) * vector[1]
    return [v_x, v_y]

def curve (A, B, C, t):
    P0 = A * t + (1 - t) * B
    P1 = B * t + (1 - t) * C
    return P0 * t + (1 - t) * P1

def make_curve(p1, p2, p3):
    crv_line = []
    for x in np.linspace(0,1,10):
        crv_line.append(curve(p1, p2, p3, x))
    return crv_line

def get_border_type(type_stat):
    main_type = max(type_stat, key=type_stat.get)
    secondary_type = max([t for t in type_stat if t != main_type], default = None)
    if secondary_type is not None and type_stat[main_type] != type_stat[secondary_type]:
        secondary_type = None

    if secondary_type is not None:
        print(main_type, secondary_type, type_stat)
        
    if main_type in ['virtual']:
        pass


def find_parallel(road, left, start_width, end_width):
    points = []
    lanelet_node_type = []

    for n in road:
        if isinstance(n, Node):
            points.append((n.lat, n.lng))
            lanelet_node_type.append(n.lanelet_node_type)
        else:
            points.append(n)
    
    type_stat = dict((i, lanelet_node_type.count(i)) for i in lanelet_node_type)
    get_border_type(type_stat)

    points = np.array(points)
    vectors = []

    parallel = []
    for i in range(len(points)-1):
        # Convert the points to UTM coordinates
        p1 = utm.from_latlon(*points[i])
        p2 = utm.from_latlon(*points[i + 1])

        # Vector between the current and the next point
        v = np.array([p2[0] - p1[0], p2[1] - p1[1]])

        widths = np.linspace(0, 1, len(points))[0:-1]
        if i != 0:
            # If the point is not the first or last point, use both the previous and the next
            # points to calculate the new point
            p0 = utm.from_latlon(*points[i-1])
            v0 = np.array([p1[0] - p0[0], p1[1] - p0[1]])
            
            # Find  angle between vectors
            angle = vector_angle(v0, v)
            angle = math.pi + angle
            angle = -angle / 2.0

            # Make a new point based on the second vector and the calculated angle
            lv = np.array(rotate_vector(v, angle))

            width = start_width * widths[(i)] + end_width * widths[-(i)]

            # Scale width to maintain the lane width at sharp angles
            scaled_width = abs(width / np.sin(angle))
        else:
            # If the point is the first point, only use the next point to calculate
            lv = np.array([v[1], -v[0]])
            scaled_width = end_width

        # Move the new point correctly represent the road's width
        l = scaled_width * lv / np.linalg.norm(lv)
        if left:
            lp = (p1[0] - l[0], p1[1] - l[1])
        else:
            lp = (p1[0] + l[0], p1[1] + l[1])

        # Convert back to lat/long and append to the line
        lp = utm.to_latlon(lp[0], lp[1], utmz["zone"], utmz["letter"])
        parallel.append(lp)

        # If this is the last iteration, add a point for the final point by using the two last points
        if i == len(points) - 2:
            lv = np.array([-v[1], v[0]]) if left else np.array([v[1], -v[0]])
            lv = lv / np.linalg.norm(v)
            l = start_width * lv/np.linalg.norm(lv)
            lp = (p2[0] + l[0], p2[1] + l[1])

            lp = utm.to_latlon(lp[0], lp[1], utmz["zone"], utmz["letter"])
            parallel.append(lp)
    
    return parallel

def main():
    global utmz

    parser = argparse.ArgumentParser()

    parser.add_argument('file', help="Input filename")
    parser.add_argument('-c', '--config', help="Manually set lane numbers and widths based on road names")
    parser.add_argument('-z', '--zone', action="store", type=str, help="UTM zone, example: -z 32V")
    parser.add_argument('-p', '--pretty', action='store_true', help="Prettify output")
    parser.set_defaults(pretty=False)

    args = parser.parse_args()

    if args.file:
        filename = args.file

    if args.zone:
        try:
            gz = args.zone
            utmz["zone"] = int(gz[0:-1])
            utmz["letter"] = str(gz[-1]).upper()
            utmz["full"] = gz

            if utmz["zone"] > 60 or utmz["zone"] < 1:
                raise ValueError("Zone number out of range, must be between 1 and 60")
            
            if not utmz["letter"].isalpha() or utmz["letter"] in ["A", "B", "Y", "Z"]:
                raise ValueError("Zone letter out of range, must be between C and X")

        except (TypeError, ValueError) as e:
            print("Erroneous UTM zone \"{}\", using default \"{}\".".format(args.zone, utmz["full"]))

    if args.config:
        conf = read_config(args.config)
    else:
        conf = None
    nodes, roads = readOSM(filename)
    print('nodes', len(nodes))
    print('roads', len(roads))
    buildTxt(filename, roads)
    # buildXML(filename, roads, args.pretty, conf)

if __name__ == "__main__":
    main()
