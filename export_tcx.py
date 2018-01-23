from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from ast import literal_eval
from pprint import pprint

def generate_tcx_file():
    abc

def populate_tcx_header(activity_type):
    root = Element('TrainingCenterDatabase', attrib = {'xmlns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'})
    activities = SubElement(root, 'Activities')
    activity = SubElement(activities, 'Activity', attrib = {'Sport':activity_type})
    return root   # tostring(root)




# a = populate_tcx_header()
# pprint(tostring(a))