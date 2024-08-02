"""
/***************************************************************************
 PublicTransitAnalysis
                                 A QGIS plugin
 Using OpenTripPlanner to calculate public transport reachability from a
    starting point to all stops in a GTFS feed.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-05-14
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Julek Weck
        email                : j.weck@tu-braunschweig.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


from datetime import time, date, datetime
class ReferencePoint:
    """
    There is always only one object of this class. It contains all parameters set in the GUI.
    Additional variables, derived from the GUI parameters, are also present.
    """

    def __init__(self, lat, lon, day, time_start, time_end, walk_speed, max_walking_time, layer_name, filepath):
        self.__incorrect_input = False
        self.__error_message = ""
        self.lat = lat
        self.lon = lon
        self.day = day
        self.time_start = time_start
        self.time_end = time_end
        self.walk_speed = walk_speed
        self.max_walking_time = max_walking_time
        self.catchment_area = self.calculate_distance(self.walk_speed, self.max_walking_time)
        #collection of all stops in the catchment area of the reference point. Find them step-by-step over the itineraries.
        self.__first_possible_stops = []
        self.search_window = self.calculate_search_window()

        self.layer_name = layer_name #I dind't make a property and setter method
        self.filepath = filepath #I dind't make a property and setter method
    @property
    def lat(self):
        return self.__lat

    @lat.setter
    def lat(self, lat):
        try:
            self.__lat = float(lat)
        except ValueError:
            self.__incorrect_input = True
            self.__error_message += "The lat text field has to contain only numbers" + "\n"

    @property
    def lon(self):
        return self.__lon

    @lon.setter
    def lon(self, lon):
        try:
            self.__lon = float(lon)
        except ValueError:
            self.__incorrect_input = True
            self.__error_message += "The lon text field has to contain only numbers" + "\n"

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        try:
            self.__day = date.fromisoformat(day)
        except ValueError:
            self.__incorrect_input = True
            self.__error_message += "The date has to be given in YYYY-MM-DD" + "\n"

    @property
    def time_start(self):
        return self.__time_start

    @time_start.setter
    def time_start(self, begin):
        try:
            self.__time_start = time.fromisoformat(begin)
        except ValueError:
            self.__incorrect_input = True
            self.__error_message += "The time_start has to be given in hh:mm" + "\n"


    @property
    def time_end(self):
        return self.__time_end

    @time_end.setter
    def time_end(self, end):
        try:
            self.__time_end = time.fromisoformat(end)
        except ValueError:
            self.__incorrect_input = True
            self.__error_message += "The time_end has to be given in hh:mm" + "\n"


    @property
    def search_window(self):
        return self.__search_window

    @search_window.setter
    def search_window(self, search_window):
        try:
            self.__search_window = int(search_window)
            print(self.__search_window)
        except ValueError:
            self.__incorrect_input = True
            self.__error_message += "The search window text field has to contain only numbers" + "\n"

    @property
    def walk_speed(self):
        return self.__walk_speed

    @walk_speed.setter
    def walk_speed(self, speed):
        self.__walk_speed = speed

    @property
    def max_walking_time(self):
        return self.__max_walking_time

    @max_walking_time.setter
    def max_walking_time(self, duration):
        self.__max_walking_time = duration


    @property
    def catchment_area(self):
        return self.__catchment_area

    @catchment_area.setter
    def catchment_area(self, catchment_area):
        try:
            self.__catchment_area = float(catchment_area)
        except ValueError:
            self.__incorrect_input = True
            self.__error_message += "The catchment area text field has to contain only numbers" + "\n"

    @property
    def incorrect_input(self):
        return self.__incorrect_input

    @property
    def error_message(self):
        return self.__error_message

    def calculate_search_window(self):
        diff = datetime.combine(self.day, self.time_end) - datetime.combine(self.day, self.time_start)
        diff = diff.total_seconds()
        if diff >= 0:
            print(f"diff: {diff}")
            return diff

        else:
            self.__incorrect_input = True
            self.__error_message += "time_start is later than time_end" + "\n"

    def calculate_distance(self, speed, duration):
        distance = speed*duration
        return distance


    def get_first_possible_stops(self):
        return self.__first_possible_stops

    def add_first_possible_stop(self, start_station:str):
        if self.__first_possible_stops.count(start_station) == 0:
            self.__first_possible_stops.append(start_station)

    def remove_empty_entries_in_first_possible_stops(self):
        while "" in self.__first_possible_stops:
            self.__first_possible_stops.remove("")  # because of the declaration of stat_station, there can be empty strings in possible_start_station

