"""
Manages configuration settings for the geohash mapper
and initiates a run of the included functions
"""
import os
import logging
from datetime import datetime
from functools import partial
from multiprocessing import Pool, cpu_count
from geohash_mapper.geohash_mapper import read_geojson_metadata, density_geohash

#  Configure these prior to running
input_geojson_dir = os.path.join(os.getcwd(), r'sample_data')
output_geojson_path = os.path.join(os.getcwd(), r'sample_data', r'geohash_density.geojson')
START_DATE = "2012-01-20 UTC" # Start time to aggregate points
END_DATE = "2013-10-20 UTC" # End time to aggregate points
INPUT_DATE_FIELD = "COLLISION_" # Data dependent field representing the date associated to a point
INPUT_DATE_FORMAT = "%Y-%m-%d" # Format of the date field (again data dependant)

# create a logger to report
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    logger.info("Reading input GeoJSON files...")

    # Convert start and end dates to epoch
    start_epoch = (datetime.strptime(START_DATE, "%Y-%m-%d %Z")
                   - datetime(1970, 1, 1)).total_seconds()
    end_epoch = (datetime.strptime(END_DATE, "%Y-%m-%d %Z")
                 - datetime(1970, 1, 1)).total_seconds()

    # Create a list of input file paths
    input_geojson_paths = [os.path.join(os.getcwd(), r'sample_data', f)
                           for f in os.listdir(input_geojson_dir) if f.endswith('.geojson')]

    # Create a partial object with start epoch, end epoch, date field and date format fixed
    prod_inp = partial(read_geojson_metadata, start_epoch=start_epoch,
                       end_epoch=end_epoch, date_field=INPUT_DATE_FIELD,
                       date_format=INPUT_DATE_FORMAT)

    # Create a process pool and pass list of files to read geoJSON metadata function
    pool = Pool(processes=cpu_count())
    wkt_list = pool.map(prod_inp, input_geojson_paths)
    pool.close()
    pool.join()

    # flatten the wkt list returned from each file
    flat_wkt_list = [item for sublist in wkt_list for item in sublist]
    logger.info("Reading GeoJSON metadata files...done")

    # Create geohash densities
    polygon_gdf = density_geohash(flat_wkt_list, precision=6)
    polygon_gdf.to_file(output_geojson_path, driver='GeoJSON')
    logger.info("completed geohashing and counting points, output created...done")
