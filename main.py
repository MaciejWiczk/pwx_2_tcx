from import_pwx import *
from export_tcx import *
import os, sys
from idlelib.replace import replace
input_path=r'C:\Users\Maciek\PycharmProjects\PWX_2_TCX_Parser\pwx'
output_path=r'C:\Users\Maciek\PycharmProjects\PWX_2_TCX_Parser\tcx'

def get_new_files(pwx_path, tcx_path):
    pwx_files = get_file_list(pwx_path, '.pwx')
    tcx_files = get_file_list(tcx_path, '.tcx')
    new_file = [file + '.pwx' for file in pwx_files if file not in tcx_files]
    return new_file

def get_file_list(path, extension):
    file_list = []
    for files in os.listdir(path):
        if os.path.isfile(os.path.join(path, files)):
            item_no_extension = str.replace(files, extension,'')
            file_list.append(item_no_extension)
    return file_list
    
    

# def convert_pwx_to_tcx(input_path):
# 
# def validate_tcx_by_schema(tcx, schema_path):
# 
# def save_tcx_file(tcx, output_path):

start_time_a = datetime.datetime.now()
path_to_file="F:\Docs\Documents\TrainingPeaks\Device Agent\saved\Mezazel\Mezazel_Timex_Cycle_Trainer_2017_05_28_11_31_31.pwx"
a = open_pwx_and_fix_tags(path_to_file)
b = get_start_time(a)
c = get_workout_data(a,b)
d = get_activity_type(a)
e = get_duration(a)
f = get_dist(a)
g = get_avg_heart_rate(c)
h = get_max_heart_rate(c)
i = get_activity_start_time(c)
print(d,e,f,g,h,i, datetime.datetime.now()- start_time_a)
print(i)
print(populate_tcx_header(d))

z = get_new_files(input_path, output_path)
print(z)