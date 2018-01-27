from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from ast import literal_eval
from pprint import pprint
import abc

def generate_tcx_file():
    abc

def begin_tcx():
    tcx = Element('TrainingCenterDatabase', attrib = {'xmlns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'})
    return tcx

def populate_tcx_header(tcx, activity_type):    
    activities = SubElement(tcx, 'Activities')
    activity = SubElement(activities, 'Activity', attrib = {'Sport':activity_type})

def populate_tcx_start_time(tcx, start_time):
    SubElement(tcx.find('Activities').find('Activity'), 'Lap', attrib = {'StartTime': start_time})

def populate_tcx_summary(tcx, total_time, total_dist, avg_hr, max_hr):
    lap = tcx.find('Activities').find('Activity').find('Lap')
    tot = SubElementWithText(lap, 'TotalTimeSeconds', total_time)
    dist = SubElementWithText(lap, 'DistanceMeters', total_dist)  
    cal = SubElementWithText(lap, 'Calories', text = '0')
    avg = SubElementWithSubValue(lap, 'AverageHeartRateBpm', avg_hr)
    max = SubElementWithSubValue(lap, 'MaximumHeartRateBpm', max_hr)
    intensity = SubElementWithText(lap, 'Intensity', 'Active')
    trigger = SubElementWithText(lap, 'TriggerMethod', 'Manual')

def populate_tcx_track(tcx, data_list):
    lap = tcx.find('Activities').find('Activity').find('Lap')
    track = SubElement(lap, 'Track')
    #LOOOOOOOOOOP
    for d in data_list:
        for key, value in d:
            trackpoint = SubElement(track, 'Trackpoint')
            if key == 'lat':
                position = SubElement(trackpoint, 'Position')
                latitude = SubElementWithText(position, 'LatitudeDegrees', value)
            elif key == 'lon':
                longtitude = SubElementWithText(position, 'LongtitudeDegrees', value)
            elif key == 'alt':
                altitude = SubElementWithText(trackpoint, 'AltitudeMeters', value)
            elif key == 'hr':
                
                                      
            
        
    
def SubElementWithText(parent, tag, text):
    element = parent.makeelement(tag, {})
    parent.append(element)
    element.text = text
    return element

def SubElementWithSubValue(parent, tag, text):
    element = parent.makeelement(tag, {})
    parent.append(element)
    sub = element.makeelement('Value', {})
    element.append(sub)
    sub.text = text
    return sub

a = begin_tcx()
populate_tcx_header(a, 'Biking')
populate_tcx_start_time(a, '2017-05-28T11:31:31')
populate_tcx_summary(a, '9236.3', '30463', '140', '178')
populate_tcx_track(a, [{'timeoffset': '2017-05-28T11:31:31', 'hr': 116, 'lat': 54.336777, 'lon': 18.571527, 'alt': 123.0}])
print(tostring(a))