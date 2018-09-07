from xml.etree.ElementTree import Element, SubElement


def generate_tcx_content(file, activity_type, start_time, total_time, total_dist, avg_hr, max_hr, data_list):
    tcx = begin_tcx()
    populate_tcx_header(tcx, activity_type)
    populate_tcx_start_time(tcx, start_time)
    populate_tcx_summary(tcx, total_time, total_dist, avg_hr, max_hr)
    populate_tcx_track(tcx, data_list)
    indent(tcx, 1)
    return tcx


def begin_tcx():
    tcx = Element('TrainingCenterDatabase', attrib={'xmlns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'})
    return tcx


def populate_tcx_header(tcx, activity_type):    
    activities = SubElement(tcx, 'Activities')
    activity = SubElement(activities, 'Activity', attrib={'Sport': activity_type})


def populate_tcx_start_time(tcx, start_time):
    SubElement(tcx.find('Activities').find('Activity'), 'Lap', attrib={'StartTime': start_time})
    SubElementWithText(tcx.find('Activities').find('Activity'), 'Id', start_time)


def populate_tcx_summary(tcx, total_time, total_dist, avg_hr, max_hr):
    lap = tcx.find('Activities').find('Activity').find('Lap')
    tot = SubElementWithText(lap, 'TotalTimeSeconds', total_time)
    dist = SubElementWithText(lap, 'DistanceMeters', total_dist)  
    cal = SubElementWithText(lap, 'Calories', text='0')
    avg = SubElementWithSubValue(lap, 'AverageHeartRateBpm', avg_hr)
    max = SubElementWithSubValue(lap, 'MaximumHeartRateBpm', max_hr)
    intensity = SubElementWithText(lap, 'Intensity', 'Active')
    trigger = SubElementWithText(lap, 'TriggerMethod', 'Manual')


def populate_tcx_track(tcx, data_list):
    lap = tcx.find('Activities').find('Activity').find('Lap')
    track = SubElement(lap, 'Track')
    for d in data_list:        
        trackpoint = SubElement(track, 'Trackpoint')
        if {'lat', 'lon'} <= set(d):
            position = SubElement(trackpoint, 'Position')
            latitude = SubElementWithText(position, 'LatitudeDegrees', str(d['lat']))
            longtitude = SubElementWithText(position, 'LongitudeDegrees', str(d['lon']))
        if 'alt' in d:
            altitude = SubElementWithText(trackpoint, 'AltitudeMeters', str(int(float(d['alt']))))
        if 'hr' in d:
            hr = SubElementWithSubValue(trackpoint, 'HeartRateBpm', str(d['hr']))
        time_offset = SubElementWithText(trackpoint, 'Time', str(d['timeoffset']))


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


def indent(elem, level=0):
    """
    Shamelessly copied from StackOverflow:
    https://stackoverflow.com/questions/6039949/python-elementtree-error-trying-to-implement-a-pretty-print
    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
