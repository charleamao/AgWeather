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
from time import sleep
from agweather_package import xml_parser as parse

"""
Purpose: user_in() serves as the user interface for AgAuto. The function
will first print a list of choices that are available. Typing out the 
explicit name of a possible choice will either run a program or quit,
if the choice is 'q'.
"""


def user_in():

    rendered_text = Figlet(font='slant')
    print rendered_text.renderText('AgAuto')

    choices = ["dailyUpload", "mawpCleaner", "debug", "calcPotatoDSV", "q"]
    print "[1] dailyUpload\n[2] mawpCleaner \n[3] calcPotatoDSV\n[4] debug\n[q] Quit"
    choice = ''

    # Program will keep asking for which programs to run until user inputs 'q'.
    while choice != 'q':
        choice = raw_input("Which program do you want to run?:")

        if choice.strip() == 'dailyUpload' or choice.strip() == '1':
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
        elif choice.strip() == 'debug' or choice.strip() == '4':
            debug()
        elif choice not in choices:
            print "Input error. Please pick from list of commands.\n"
        print '\n'


def debug():
    all_data = parse.grab_desired_xml_data('hourly')
    print parse.gen_string_rep(all_data.get_data('PBO'))


def main():
    # update_dailyEC()
    user_in()
    

main()
