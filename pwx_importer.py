from xml.etree import ElementTree as et
from ast import literal_eval
import datetime
import dateutil.parser

def open_pwx_and_fix_tags(file_path):
    root = et.parse(file_path).getroot()
    def fix_tag_name(input_tag):
        return str.replace(input_tag,'{http://www.peaksware.com/PWX/1/0}', '')
    for child in root.getiterator():
        child.tag = fix_tag_name(child.tag)        
    return root

def get_start_time(pwx):
    return dateutil.parser.parse(pwx.find('workout').find('time').text)    

def get_workout_data(pwx):    
    def increment_dates(input_date, seconds_incrementor):
        return (input_date + datetime.timedelta(seconds=seconds_incrementor)).isoformat()
    start_time = get_start_time(pwx)
    sample_params_list =[]
    sample_params_dict={}
    for sample in pwx.find('workout').findall('sample'):        
        if sample_params_dict.__len__():
            sample_params_list.append(sample_params_dict.copy())
            sample_params_dict.clear()
        for child in sample:     
            if child.tag == 'timeoffset':
                sample_params_dict[child.tag] = str(increment_dates(start_time, literal_eval(child.text)))
            elif child.tag != 'extension':
                sample_params_dict[child.tag] = str(literal_eval(child.text))
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
    return pwx.find('workout').find('summarydata').find('duration').text

def get_dist(pwx):
    return pwx.find('workout').find('summarydata').find('dist').text

def get_avg_heart_rate(list):
    return str(int(sum(int(hr['hr']) for hr in list) / len(list)))

def get_max_heart_rate(list):
    return str(max(int(hr['hr']) for hr in list))