"""
Unit tests for geohash mapper module
"""

import unittest
from datetime import datetime
import os
from geohash_mapper import geohash_mapper


def epoch_converter(start_time, end_time):
    """
    Convert time in a formatted string to epoch time
    :param start_time: start time string
    :param end_time: end time string
    :return: start_epoch, end_epoch
    """
    start_epoch = (datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S %Z")
                   - datetime(1970, 1, 1)).total_seconds()
    end_epoch = (datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S %Z")
                 - datetime(1970, 1, 1)).total_seconds()
    return start_epoch, end_epoch


class GeohashMapperTests(unittest.TestCase):
    """
    class for unit tests that test geohash mapper
    """
    test_file_1 = os.path.join(os.getcwd(), r'test_data/20180815.geojson')
    test_file_2 = os.path.join(os.getcwd(), r'test_data/20180817.geojson')

    def test_file_access(self):
        """
        Check for a given time range that falls within and outside a file date range
        """
        # TestCase1: positive test, return some wkt strings from the file
        start_time = "2018-08-17 00:00:00 UTC"
        end_time = "2018-08-18 00:00:00 UTC"
        start_epoch, end_epoch = epoch_converter(start_time, end_time)
        wkt_strings = geohash_mapper.read_geojson_metadata(self.test_file_2, start_epoch, end_epoch)
        self.assertTrue(len(wkt_strings) > 0)

        # TestCase2: negative test, outside time range so returns no values
        start_time = "2018-08-20 00:00:00 UTC"
        end_time = "2018-08-21 00:00:00 UTC"
        start_epoch, end_epoch = epoch_converter(start_time, end_time)
        expected_value = 0
        wkt_strings = geohash_mapper.read_geojson_metadata(self.test_file_2, start_epoch, end_epoch)
        self.assertTrue(len(wkt_strings) == expected_value)

        # TestCase3: exact test, expect all value from '20180815.geojson' for a given time range
        start_time = "2018-08-15 07:00:00 UTC"
        end_time = "2018-08-16 07:00:00 UTC"
        start_epoch, end_epoch = epoch_converter(start_time, end_time)
        expected_value = 8
        wkt_strings = geohash_mapper.read_geojson_metadata(self.test_file_1, start_epoch, end_epoch)
        self.assertTrue(len(wkt_strings) == expected_value)

        # TestCase4: subset test, expect a subset of values from '20180815.geojson' for a given time range
        start_time = "2018-08-15 15:00:00 UTC"
        end_time = "2018-08-15 16:00:00 UTC"
        start_epoch, end_epoch = epoch_converter(start_time, end_time)
        expected_value = 3
        wkt_strings = geohash_mapper.read_geojson_metadata(self.test_file_1, start_epoch, end_epoch)
        self.assertTrue(len(wkt_strings) == expected_value)

    def test_density_geohasher(self):
        """
        Tests for density_geohash function
        """

        # TestCase5: Sanity tests to check geohash, count, colors and bounds.
        start_time = "2018-08-15 15:00:00 UTC"
        end_time = "2018-08-15 16:00:00 UTC"
        start_epoch, end_epoch = epoch_converter(start_time, end_time)
        wkt_list = geohash_mapper.read_geojson_metadata(self.test_file_1, start_epoch, end_epoch)
        polygon_gdf = geohash_mapper.density_geohash(wkt_list)
        self.assertListEqual(list1=['9q8yyxuu', '9q8yyxv4', '9q8yyxvx'],
                             list2=polygon_gdf['geohash'].to_list())
        self.assertListEqual(list1=['#edd1cb', '#edd1cb', '#edd1cb'],
                             list2=polygon_gdf['color'].to_list())
        self.assertListEqual(list1=[1, 1, 1],
                             list2=polygon_gdf['count'].to_list())
        self.assertTupleEqual(tuple1=(-122.40314483642578, 37.79228210449219,
                                      -122.40280151367188, 37.79245376586914),
                              tuple2=polygon_gdf['geometry'][0].bounds)


if __name__ == '__main__':
    unittest.main()
