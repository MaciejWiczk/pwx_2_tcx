from pwx_importer import *
from tcx_creator import *
from progress.bar import IncrementalBar
import concurrent.futures
import os
from pathlib import Path
from xml.etree.ElementTree import tostring
import argparse


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
    p = Path(tcx_path)
    with open(str(p / f'{file}.tcx'), "wb") as f:
        f.write(tostring(tcx))
        f.close()


def get_new_files(pwx_path, tcx_path):
    pwx_files = get_file_list(pwx_path, '.pwx')
    tcx_files = get_file_list(tcx_path, '.tcx')
    return pwx_files - tcx_files


def get_file_list(path, extension):
    return {str.replace(file, extension, '') for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))}


def main():
    Path(output_path).mkdir(parents=True, exist_ok=True)
    files = get_new_files(input_path, output_path)
    if files:
        progress_bar = IncrementalBar('Processing', max=len(files), suffix='%(percent).1f%% - %(eta)ds, elapsed: %(elapsed)ds')
        with concurrent.futures.ProcessPoolExecutor() as exe:
            futures = {exe.submit(convert_pwx_2_tcx, input_path, output_path, file): file for file in files}
            for future in concurrent.futures.as_completed(futures):
                progress_bar.next()
    else:
        print("No new Files found.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Processing .pwx into .tcx files. Please provide input and output paths.')
    parser.add_argument('-i','--input-path')
    parser.add_argument('-o', '--output-path')
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    main()

