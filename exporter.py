from pwx_importer import *
from tcx_creator import *
from xml.etree import ElementTree as et
from xml.dom import minidom
import os, sys
import datetime

input_path=r'C:\Users\Maciek\PycharmProjects\PWX_2_TCX_Parser\pwx'
output_path=r'C:\Users\Maciek\PycharmProjects\PWX_2_TCX_Parser\tcx'

def export_tcx_file(pwx_path, tcx_path):
    files = get_new_files(pwx_path, tcx_path)
    if files.__len__():
        for file in files:
            pwx = open_pwx_and_fix_tags(os.path.join(pwx_path, file + '.pwx'))
            start_time = str(get_start_time(pwx))
            workout_data = get_workout_data(pwx)
            activity_type = get_activity_type(pwx)
            total_time = get_duration(pwx)
            total_dist = get_dist(pwx)
            avg_hr = get_avg_heart_rate(workout_data)
            max_hr = get_max_heart_rate(workout_data)
            
            tcx = generate_tcx_content(file, activity_type, start_time, total_time, total_dist, avg_hr, max_hr, workout_data)
            tcx = minidom.parseString(et.tostring(tcx)).toprettyxml(indent="   ")
            with open(os.path.join(tcx_path, file + '.tcx'), "wb") as f:
                f.write(tcx.encode('utf-8'))
                f.close()
            print("File {0} exported at {1}".format(file, datetime.datetime.now()))
    else:
        print("No new Files found.")
        

def get_new_files(pwx_path, tcx_path):
    pwx_files = get_file_list(pwx_path, '.pwx')
    tcx_files = get_file_list(tcx_path, '.tcx')
    new_file = [file for file in pwx_files if file not in tcx_files]
    return new_file

def get_file_list(path, extension):
    file_list = []
    for files in os.listdir(path):
        if os.path.isfile(os.path.join(path, files)):
            item_no_extension = str.replace(files, extension,'')
            file_list.append(item_no_extension)
    return file_list
    
export_tcx_file(input_path, output_path)