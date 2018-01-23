from xml.etree import ElementTree as et
from ast import literal_eval
import datetime
import dateutil.parser

def open_pwx_and_fix_tags(file_path):
    root = et.parse(file_path).getroot()
    for child in root.getiterator():
        child.tag = fix_tag_name(child.tag)        
    return root

def fix_tag_name(input_tag):
    output_tag = str.replace(input_tag,'{http://www.peaksware.com/PWX/1/0}', '')
    return output_tag

def get_start_time(pwx):
    start_time = dateutil.parser.parse(pwx.find('workout').find('time').text)
    return start_time

def increment_dates(input_date, seconds_incrementor):
    output_date = (input_date + datetime.timedelta(seconds=seconds_incrementor)).isoformat()
    return output_date

def get_workout_data(pwx, start_time):
    sample_params_list =[]
    sample_params_dict={}
    for sample in pwx.find('workout').findall('sample'):        
        if sample_params_dict.__len__() >0:
            sample_params_list.append(sample_params_dict.copy())
            sample_params_dict.clear()
        for child in sample:     
            if child.tag == 'timeoffset':
                sample_params_dict[child.tag] = increment_dates(start_time, literal_eval(child.text))
            elif child.tag != 'extension':
                sample_params_dict[child.tag] = literal_eval(child.text)
    return sample_params_list

def get_activity_type(pwx):
    activity_type = pwx.find('workout').find('sportType').text
    if activity_type in ["Bike","Mountain Bike"]:
        activity_type = "Biking"
    elif activity_type == "Run":
        activity_type = "Running"
    else:
        activity_type = "Other"
    return activity_type

def get_duration(pwx):
    duration = pwx.find('workout').find('summarydata').find('duration').text
    return duration

def get_dist(pwx):
    dist = pwx.find('workout').find('summarydata').find('dist').text
    return dist

def get_avg_heart_rate(list):
    avg_hr = int(sum(hr['hr'] for hr in list) / len(list))
    return avg_hr

def get_max_heart_rate(list):
    max_hr = int(max(hr['hr'] for hr in list))
    return max_hr

def get_activity_start_time(list):
    activity_start_time = min(timeoffset['timeoffset'] for timeoffset in list)
    return activity_start_time