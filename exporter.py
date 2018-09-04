from pwx_importer import *
from tcx_creator import *
from progress.bar import IncrementalBar
from concurrent.futures import ProcessPoolExecutor as Executor
import os

input_path = r'C:\Users\Maciek\PycharmProjects\PWX_2_TCX_Parser\pwx'
output_path = r'C:\Users\Maciek\PycharmProjects\PWX_2_TCX_Parser\tcx'


def convert_pwx_2_tcx(pwx_path, tcx_path, file):
    pwx = open_pwx_and_fix_tags(os.path.join(pwx_path, file + '.pwx'))
    start_time = str(get_start_time(pwx))
    workout_data = get_workout_data(pwx)
    activity_type = get_activity_type(pwx)
    total_time = get_duration(pwx)
    total_dist = get_dist(pwx)
    avg_hr = get_avg_heart_rate(workout_data)
    max_hr = get_max_heart_rate(workout_data)
    tcx = generate_tcx_content(file, activity_type, start_time, total_time, total_dist, avg_hr, max_hr,
                               workout_data)
    with open(os.path.join(tcx_path, file + '.tcx'), "wb") as f:
        f.write(tostring(tcx))
        f.close()
    progress_bar.next()


def get_new_files(pwx_path, tcx_path):
    pwx_files = get_file_list(pwx_path, '.pwx')
    tcx_files = get_file_list(tcx_path, '.tcx')
    return pwx_files - tcx_files


def get_file_list(path, extension):
    return {str.replace(file, extension, '') for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))}


if __name__ == '__main__':
    files = get_new_files(input_path, output_path)
    if files.__len__():
        progress_bar = IncrementalBar('Processing', max=files.__len__(), suffix='%(percent).1f%% - %(eta)ds')
        with Executor(max_workers=8) as exe:
            for file in files:
                exe.submit(convert_pwx_2_tcx(input_path, output_path, file))
    else:
        print("No new Files found.")
