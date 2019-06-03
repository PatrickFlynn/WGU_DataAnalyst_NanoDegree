import xml.etree.ElementTree as ET
#import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

filepath = r'S:\Code\School\WGU_DataAnalyst_NanoDegree\02 - Data Wrangling with MongoDB'

def xml_retrieve_to_dataframe(search_tag):
    with open(os.path.join(filepath, 'Cleaned_Henderson.osm'),encoding="utf8") as osm_file:
        nodes = []
        node_tags = []
        for event, elem in ET.iterparse(osm_file):
            for items in elem:
                    if items.tag == search_tag:
                        nodes.append(items.attrib)
                        if list(items):
                            for x in list(items):
                                temp_dict = {}
                                temp_dict.update(x.attrib)
                                temp_dict['type'] = x.tag
                                temp_dict['id'] = items.attrib['id']
                                node_tags.append(temp_dict)
        df = pd.DataFrame(nodes)
        tag_df = pd.DataFrame(node_tags)
        return df, tag_df
    
nodes, nodes_tags = xml_retrieve_to_dataframe('node')
ways, ways_tags = xml_retrieve_to_dataframe('way')

ways_nodes = ways_tags.loc[ways_tags['type'] == 'nd', :]
ways_tags = ways_tags.loc[ways_tags['type'] != 'nd', :]

ways_nodes.drop(columns=['k', 'type', 'v'], inplace=True)

ways_tags.drop(columns=['ref'], inplace=True)

yes_no_dict = {'yes':'True', 'no':'False', 'YES':'True', 'Yes':'True', 'NO':'False', 'No':'False'}
ways_tags['v'].replace(yes_no_dict, inplace=True)

nodes['id'] = nodes['id'].astype(float)
nodes['lat'] = nodes['lat'].astype(float)
nodes['lon'] = nodes['lon'].astype(float)
nodes['uid'] = nodes['uid'].astype(float)
nodes['changeset'] = nodes['changeset'].astype(float)
nodes['version'] = nodes['version'].astype(int)
nodes.fillna('', inplace=True)
nodes = nodes[['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']]

nodes_tags['id'] = nodes_tags['id'].astype(float)
nodes_tags.fillna('', inplace=True)
nodes_tags = nodes_tags[['id', 'k', 'v', 'type']]

ways['id'] = ways['id'].astype(float)
ways['uid'] = ways['uid'].astype(float)
ways['changeset'] = ways['changeset'].astype(float)
ways.fillna('', inplace=True)
ways = ways[['id', 'user', 'uid', 'version', 'changeset', 'timestamp']]

ways_tags['id'] = ways_tags['id'].astype(float)
ways_tags.fillna('', inplace=True)
ways_tags = ways_tags[['id', 'k', 'v', 'type']]

ways_nodes['id'] = ways_nodes['id'].astype(float)
ways_nodes['ref'] = ways_nodes['ref'].astype(float)
ways_nodes.fillna('', inplace=True)
ways_nodes = ways_nodes[['id', 'ref']]

nodes.to_csv(os.path.join(filepath, 'nodes.csv'), index=False)
nodes_tags.to_csv(os.path.join(filepath, 'nodes_tags.csv'), index=False)
ways.to_csv(os.path.join(filepath, 'ways.csv'), index=False)
ways_tags.to_csv(os.path.join(filepath, 'ways_tags.csv'), index=False)
ways_nodes.to_csv(os.path.join(filepath, 'ways_nodes.csv'), index=False)