"""Read point metadata and create a geohash density heat map as a GeoJSON Feature Collection
"""

import os

from collections import Counter
import logging
from multiprocessing import current_process
from datetime import datetime
import geohash
import pandas as pd
import geopandas as gpd
from shapely import geometry
import seaborn as sns
logger = logging.getLogger(__name__)


def read_geojson_metadata(geojson_file, start_epoch, end_epoch, date_field, date_format):
    """Reads metadata from geojson file from an input directory
    and returns a list of wkt strings for points within the given time range
        :param geojson_file: input geojson file
        :param start_epoch: start of time range in epoch
        :param end_epoch: end of time range in epoch
        :param date_field: The field in the geojson file that represents the date
        :param date_format: The date format of the date field
        :return: list of wkt strings for points within the given time range
    """

    logger.info("Reading metadata for file {}: {} with PID {}"
                .format(os.path.basename(geojson_file), current_process().name, os.getpid()))

    point_wkt_list = []

    point_metadata = gpd.read_file(geojson_file)

    # Convert date to epoch time in local timezone, use 'tzinfo' if 'Aware' timezones are desired
    point_date = [datetime.strptime(point_metadata[date_field][i], date_format).timestamp()
                  for i in range(len(point_metadata[date_field]))]

    point_metadata['captured_on_epoch'] = point_date

    filter_geom = point_metadata[point_metadata['captured_on_epoch'] <= end_epoch]\
        [point_metadata['captured_on_epoch'] >= start_epoch]['geometry']
    for pnt in filter_geom:
        point_wkt_list.append('{lat} {lon}'.format(lat=pnt.y, lon=pnt.x))

    return point_wkt_list


def density_geohash(input_point_collections, precision=8):
    """
    :param input_point_collections: list of wkt strings for points that need to be aggregated
    :param precision: precision for the geohash encoder. Default is 8.
    :return: a Geopandas Dataframe of geohash mapping a count and color to each hash polygon
    """
    logger.info("Counting points for geohash regions within time range...")

    # create a geohash dictionary with unique geohash and their counts
    geohash_dict = Counter([
        geohash.encode(
            float(input_point.split(" ")[0]),
            float(input_point.split(" ")[1]), precision
        )
        for input_point in input_point_collections
    ])

    # map a color to count value using a palette
    count_max = max(geohash_dict.values())
    color_ramp = sns.cubehelix_palette(count_max).as_hex()
    colors = {count: color_ramp[count - 1] for count in set(geohash_dict.values())}

    # Create data frame with geohash strings, counts and associated colors
    geohash_df = pd.DataFrame([[geohash_str for geohash_str in geohash_dict.keys()],
                               [colors[ct] for ct in geohash_dict.values()],
                               [ct for ct in geohash_dict.values()]],
                              ).T
    geohash_df.columns = ['geohash', 'color', 'count']

    def geohash_to_bounds(geohash_string):
        """
        :param geohash_string: String that represents the geohash.
        :return: Returns a shapely Polygon for a given geohash.
        """
        lat, lon, lat_err, lon_err = geohash.decode_exactly(geohash_string)

        edge1 = (lat - lat_err, lon - lon_err)[::-1]
        edge2 = (lat - lat_err, lon + lon_err)[::-1]
        edge3 = (lat + lat_err, lon + lon_err)[::-1]
        edge4 = (lat + lat_err, lon - lon_err)[::-1]

        return geometry.Polygon([edge1, edge2, edge3, edge4, edge1])

    # get polygon representation for each geohash
    bbox_polygons = [geohash_to_bounds(geohash_val) for geohash_val in geohash_dict.keys()]
    polygon_gdf = gpd.GeoDataFrame(geohash_df, geometry=bbox_polygons)

    return polygon_gdf
