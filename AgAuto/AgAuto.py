# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:27:19 2019

@author: CAmao

Purpose: AgAuto serves as the main program that allows you to interface with
the different automation programs for AgWeather.

Date modified: Tue May 21 2019
"""

from agweather_package import PotatoBlight as potato
from agweather_package import DailyUpload as daily
from pyfiglet import Figlet
from subprocess import call
from os import getcwd, path
from time import sleep, time
from agweather_package import write_list_to_csv
from agweather_package import FHBRisk as FHB
from agweather_package import get_path_dir

"""
Purpose: user_in() serves as the user interface for AgAuto. The function
will first print a list of choices that are available. Typing out the 
explicit name of a possible choice will either run a program or quit,
if the choice is 'q'.
"""


def user_in():

    rendered_text = Figlet(font='slant')
    print(rendered_text.renderText('AgAuto'))

    choices = ["dailyUpload", "mawpCleaner", "debug", "calcPotatoDSV", 'FHBRisk', "q"]
    print("[1] dailyUpload\n[2] mawpCleaner \n[3] calcPotatoDSV\n[4] FHBRisk\n[d] debug\n[q] Quit")
    choice = ''

    # Program will keep asking for which programs to run until user inputs 'q'.
    while choice != 'q':
        choice = input("Which program do you want to run?:")

        if choice.strip() == 'dailyUpload' or choice.strip() == '1':
            time1 = time()
            print("Downloading data....")
            contents_to_write = daily.back_fill_daily_ec()
            if len(contents_to_write) > 1:
                write_list_to_csv('DailyEC.csv', contents_to_write)
                time2 = time()
                print("Time Elapsed: %is" % (time2 - time1))

            daily.update_dailyEC()
            file_24 = "mawp24raw.txt"
            file_60 = "mawp60raw.txt"
            daily.cleanData(file_24)
            daily.cleanData(file_60)
            daily.gen_Bat_file()
            in_me = False
            while not in_me:
                in_me = daily.in_managed_environment()
                sleep(4)
            if in_me:
                call(path.join(getcwd(), 'AgAuto_batch.bat'))

        elif choice.strip() == 'mawpCleaner' or choice.strip() == '2':
            file_24 = "mawp24raw.txt"
            file_60 = "mawp60raw.txt"
            daily.cleanData(file_24)
            daily.cleanData(file_60)
        elif choice.strip() == 'calcPotatoDSV' or choice.strip() == '3':
            potato.show_all_stations_dsv()
        elif choice.strip() == 'FHBRisk' or choice.strip() == '4':
            fhb_results = FHB.show_all_fhb_risks()
            write_list_to_csv(get_path_dir('output_files', 'FHB_Calculation_results.csv'), fhb_results)
        elif choice.strip() == 'debug' or choice.strip() == 'd':
            debug()
        elif choice not in choices:
            print("Input error. Please pick from list of commands.\n")
        print('\n')


def debug():
    """
    with open(get_path_dir('config_files', 'mbag_stations.csv'), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        ids = []
        data = []
        for each_row in list(csv_reader)[1:]:
            ids.append(int(each_row[0]))
            data.append(each_row[1])

        initialize_yaml_text(ids, 'desc', data, 'mbag_stations.yaml')
    """
    FHB.show_all_fhb_risks()


def main():
    # update_dailyEC()
    user_in()


main()
