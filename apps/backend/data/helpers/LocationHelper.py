'''
    BarcelonaNow (c) Copyright 2018 by the Eurecat - Technology Centre of Catalonia

    This source code is free software; you can redistribute it and/or
    modify it under the terms of the GNU Public License as published
    by the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This source code is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Please refer to the GNU Public License for more details.

    You should have received a copy of the GNU Public License along with
    this source code; if not, write to:
    Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
'''

import json

import pyproj as pyproj
from shapely.geometry import shape, Point

from apps.backend.data.helpers.GeneralHelper import GeneralHelper
from config.Config import Config

cfg = Config().get()

# This class defines a set of utilities methods to manage geographic locations.
class LocationHelper:

    def __init__(self):
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/assets/barcelona.geojson') as f:
            self.neighbourhoods = json.load(f)
            
    # This method translates the Barcelona City Council latitude and longitude format into standard WGS84 format
    def toWGS84(self, latitude, longitude, coordinates='EPSG:23031'):
        if GeneralHelper().check(latitude) and GeneralHelper().check(longitude):
            FROM = pyproj.Proj('+init=' + coordinates)
            WGS84 = pyproj.Proj('+init=EPSG:4326')
            long_from = float(longitude) / 1000 + 400000
            lat_from = float(latitude) / 1000 + 4500000
            long_wgs84, lat_wgs84 = pyproj.transform(FROM, WGS84, long_from, lat_from)
            return long_wgs84, lat_wgs84
        return GeneralHelper().default(longitude), GeneralHelper().default(latitude)

    # This method returns the Barcelona district and neighbourhood in which the point (latitude, longitude) is included
    def getLocationAreas(self, latitude, longitude):
        district = ''
        neighbourhood = ''
        for feature in self.neighbourhoods['features']:
            if shape(feature['geometry']).contains(Point(float(longitude), float(latitude))):
                neighbourhood = feature['properties']['neighbourhood']
                district = feature['properties']['neighbourhood_group']
        return district, neighbourhood

    def toWGS84Geometry(self, geometry, coordinates='EPSG:23031', isNested=False):
        FROM = pyproj.Proj('+init=' + coordinates)
        WGS84 = pyproj.Proj('+init=' + 'EPSG:4326')
        wgs84_coordinates = []
        if (isNested == True):
            old_coordinates = geometry['coordinates'][0]
        else:
            old_coordinates = geometry['coordinates']
        for coord in old_coordinates:
            wgs84_long, wgs84_lat = pyproj.transform(FROM, WGS84, coord[0], coord[1])
            wgs84_coordinates.append([wgs84_long, wgs84_lat, 0.0])
        if (isNested == True):
            wgs84_coordinates = [wgs84_coordinates]
        geometry['coordinates'] = wgs84_coordinates

        return geometry
