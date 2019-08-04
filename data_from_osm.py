# python 3


import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import pandas as pd

import schema

OSM_PATH = 'map_data.osm'

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')


# Fields order here is different than the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    if element.tag == 'node':
        for i in node_attr_fields:
            node_attribs[i] = element.attrib[i]

        for j in element.findall('./tag'):
            m2 = LOWER_COLON.search(j.attrib['k'])
            d={}
            #if m1:
            #    d={}
            if m2:
                a = j.attrib['k'].split(':',1)
                d['type'] = a[0]
                d['id'] = element.attrib['id']
                d['key'] = a[1]
                d['value'] = j.attrib['v']
            else:
                d['type'] = default_tag_type
                d['id'] = element.attrib['id']
                d['key'] = j.attrib['k']
                d['value'] = j.attrib['v']
            tags.append(d)
    
    if element.tag == 'way':
        for i in way_attr_fields:
            way_attribs[i] = element.attrib[i]
        
        t1 = element.findall('./tag')
        
        for j in t1:
            m2 = LOWER_COLON.search(j.attrib['k'])
            d={}
            #if m1:
            #    d={}
            if m2:
                a = j.attrib['k'].split(':',1)
                d['type'] = a[0]
                d['id'] = element.attrib['id']
                d['key'] = a[1]
                d['value'] = j.attrib['v']
            else:
                d['type'] = default_tag_type
                d['id'] = element.attrib['id']
                d['key'] = j.attrib['k']
                d['value'] = j.attrib['v']
            tags.append(d)
        
        t2 = element.findall('./nd')
        count = 0
        d2={}
        for j in t2:
            d2['id'] = element.attrib['id']
            d2['node_id'] = j.attrib['ref']
            d2['position'] = count
            count = count + 1
            way_nodes.append(d2)
            d2={}
    
    if element.tag == 'node':
        #pprint.pprint({'node': node_attribs, 'node_tags': tags})
        #print(node_attribs.keys)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        #pprint.pprint({'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags})
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
     
            
            

# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in):
    """Iteratively process each XML element"""

    for element in get_element(file_in, tags=('node', 'way')):
        el = shape_element(element)
        if el:

            if element.tag == 'node':
                n.append(el['node'])
                n_tags.append(el['node_tags'])

            elif element.tag == 'way':
                w.append(el['way'])
                w_nodes.append(el['way_nodes'])
                w_tags.append(el['way_tags'])



n = []
n_tags = []
w = []
w_nodes = []
w_tags = []
process_map(OSM_PATH)

#nodes
n_pd = pd.DataFrame(n)
#ways
w_pd = pd.DataFrame(w)

n_tags1=[]
for i in n_tags:
    for j in i:
        n_tags1.append(j)
#nodes_tags
n_tags_pd = pd.DataFrame(n_tags1)

w_nodes1=[]
for i in w_nodes:
    for j in i:
        w_nodes1.append(j)
#ways_nodes
w_nodes_pd = pd.DataFrame(w_nodes1)

w_tags1=[]
for i in w_tags:
    for j in i:
        w_tags1.append(j)
#ways_tags
w_tags_pd = pd.DataFrame(w_tags1)


#To run the auditing and cleaning file uncomment it
#exec(open('auditing_and_cleaning.py').read())


#Saving to csv uncomment below

#n_pd.to_csv('nodes.csv', sep=',', encoding='utf-8', index=False)
#n_tags_pd.to_csv('nodes_tags.csv', sep=',', encoding='utf-8', index=False)
#w_pd.to_csv('ways.csv', sep=',', encoding='utf-8', index=False)
#w_nodes_pd.to_csv('ways_nodes.csv', sep=',', encoding='utf-8', index=False)
#w_tags_pd.to_csv('ways_tags.csv', sep=',', encoding='utf-8', index=False)
