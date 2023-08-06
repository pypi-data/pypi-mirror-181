"""The report module is designed to display a report on the lap time by drivers.

A report on the lap time by drivers in ascending or descending order, or to display statistics for one specific driver.
The module needs a directory with 3 files to work:
- this file contains abbreviations and their decryption,
for example 'DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER'
- the log file contains the start logs for each and the drivers with their abbreviations,
for example 'MES2018-05-24_12:05:58.778'
- the log file contains the end logs for each and the drivers with their abbreviations,
for example 'MES2018-05-24_12:04:45.513'
The processing of the directory with files is carried out in a function build_report,
it takes 2 parameters, the directory itself and the order (by default, it is set by increment).
This function outputs a sheet with a ready-made list of drivers and their lap times (ascending by default).
Next, the data is transmitted to the function 'print_report',
the numbering of drivers takes place in it and the delimiter divides the name of the rider,
the team, the lap time, also the delimiter separates the first 15 drivers and is displayed on the screen
In the function, control of the output of the necessary data from the command line is implemented:
'--files' command and specify the directory, for example --files <folder_path> [--asc | --desc
we will get the statistics on drivers displayed on the screen in ascending order
'--files' command and specify the directory, for example --files <folder_path> --desc
we will get the statistics on drivers displayed on the screen in descending  order
'--driver' of the command and specify the directory, for example --files <folder_path> --driver “Sebastian Vettel”,
we will get statistics displayed on the screen for a specific driver
"""
import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

from src.models import *

ABBR_FILENAME = 'abbreviations.txt'
START_FILENAME = 'start.log'
END_FILENAME = 'end.log'
DELIMITER_POSITION = 15
LINE_WIDTH = 72


def read_file(filepath):
    """Function accepts filepath and in read lines the file"""
    with open(filepath) as f:
        return f.readlines()


def parse_abbr_lines(row_strings):
    """Function accepts row strings with abbreviations.txt, separates them and collects them into a list"""
    parsed_lines = []
    for line in row_strings:
        parsed_line = line.rstrip().split('_')
        parsed_lines.append(parsed_line)
    return parsed_lines


def parsed_start_end_lines(row_strings):
    """Function accepts row strings with start.log or end.log, separates them into abbr and data time,
    after which collects them into a list
    """
    parsed_lines = []
    for line in row_strings:
        abbr, date_time = line[:3], line[3:].replace('_', ' ').rstrip()
        parsed_lines.append((abbr, datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f')))
    return parsed_lines


def create_database(dir_):
    """
     Create database and fill it.
    """
    try:
        path_dir = Path(dir_).resolve()
        drivers = parse_abbr_lines(read_file(path_dir / ABBR_FILENAME))
        start_times = parsed_start_end_lines(read_file(path_dir / START_FILENAME))
        end_times = parsed_start_end_lines(read_file(path_dir / END_FILENAME))
        db = SqliteDatabase('database.db')
        db.drop_tables([Driver, StartLog, EndLog])
        with db.atomic() as transaction:
            db.create_tables([Driver, StartLog, EndLog])
            Driver.insert_many(drivers).execute()
            StartLog.insert_many(start_times).execute()
            EndLog.insert_many(end_times).execute()
    except FileNotFoundError:
        print(dir_, 'No such file or directory. Please, input the correct path')


def get_data_from_db():
    """
    Get data from database.
    Return list data.
    List data have into: abbr, name, team, time, time_start, time_finish.
    """
    with sqlite3.connect('database.db') as db:
        list_data = []
        cursor = db.cursor()
        query = """ SELECT abbr, name, team, time_start, time_finish FROM drivers
                    JOIN start_logs ON start_logs.abbr_id = drivers.abbr
                     JOIN end_logs ON end_logs.abbr_id = drivers.abbr"""
        cursor.execute(query)
        for data in cursor:
            abbr = data[0]
            name = data[1]
            team = data[2]
            time_start = datetime.strptime(data[3], '%H:%M:%S') if len(data[3]) < 9 \
                else datetime.strptime(data[3], '%H:%M:%S.%f')
            time_finish = datetime.strptime(data[4], '%H:%M:%S') if len(data[4]) < 9 \
                else datetime.strptime(data[4], '%H:%M:%S.%f')
            list_data.append((abbr, name, team, time_start, time_finish))
        return list_data


def build_report(data, desc=False):
    """Construction report based on data.

    The function accepts the data, and desc.
    The calculation of the lap time of each driver takes place,
    if the data on the start and end times of the lap are mixed up,
    the function will replace them with places. As a result,
    we will get a list of drivers with the default lap time in ascending order,
    or if a parameter is specified desc=True, in descending order.

    """
    list_item = []
    for item in data:
        abbr = item[0]
        name = item[1]
        team = item[2]
        time_lap = str(item[3] - item[4]) if item[3] > item[4] else str(item[4] - item[3])
        list_item.append((abbr, name, team, time_lap))
        list_item.sort(key=lambda x: x[3])
    return list_item if not desc else sorted(list_item, key=lambda x: x[3], reverse=True)


def print_report(data):
    """Function print result data.
    
    The print function takes the date and numbers the drivers sequentially,
     and divides the driver's name, team and time with a delimiter. also,
      the delimitor separated the 15 first drivers from the subsequent ones.
    """
    for index, item in enumerate(data, start=1):
        print(f'{index}. {item}'.replace(',', ' | '))
        if index == DELIMITER_POSITION:
            print('-' * LINE_WIDTH)


def find_driver(data, driver):
    """Function takes two arguments date and driver.

    It filters the drivers available in the date, finding the right one displays statistics.
    If the driver's name was entered incorrectly, an error appears NameError.
    """
    filterated_date = list(filter(lambda item: item[0] == driver, data)) \
                      or list(filter(lambda item: str("".join(e[0]
                                                              for e in str(item[0]).split()) + "".join(e[0]
                                                                                                       for e in str(
        item[1]).split()))[0:3] == driver, data))
    if not filterated_date:
        raise NameError("Please, check the name of the pilot, enter a valid name. Example 'Sebastian Vettel' or 'SVF' ")
    return filterated_date[0]


def main():
    """Management is assembled here CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='?', type=str, const='build_report', required=True, help='folder path')
    parser.add_argument('--driver', nargs='?', type=str, help='statistic about driver')
    parser.add_argument('--desc', default=False, action="store_true", help='list of drivers order is desc')
    args = parser.parse_args()
    create_data = create_database(args.files)
    data = get_data_from_db()
    result = build_report(data, args.desc)
    if args.driver:
        print(find_driver(result, args.driver))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
