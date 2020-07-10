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
image_metadata_dir = os.path.join(os.path.dirname(os.getcwd()), r'image_metadata')
output_geojson_path = os.path.join(
    os.path.dirname(os.getcwd()), r'output_geojson', r'geohash_density_08200821.geojson')
START_TIME = "2018-08-20 00:00:00 UTC"
END_TIME = "2018-08-21 00:00:00 UTC"

# create a logger to report
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    logger.info("Reading GeoJSON metadata files...")

    # Convert start and end times to epoch
    start_epoch = (datetime.strptime(START_TIME, "%Y-%m-%d %H:%M:%S %Z")
                   - datetime(1970, 1, 1)).total_seconds()
    end_epoch = (datetime.strptime(END_TIME, "%Y-%m-%d %H:%M:%S %Z")
                 - datetime(1970, 1, 1)).total_seconds()

    metadata_path = []

    for filename in os.listdir(image_metadata_dir):
        # 'file_start_time' is 'naive' datetime object that'll use local time.
        # Run from Pacific region it should match SF AOI timezone.
        # GeoJSON file names are assumed to be in Pacific timezone.
        # To convert to 'aware', use 'tzinfo'.
        file_start_time = datetime.strptime(filename.split('.')[0], "%Y%m%d").timestamp()
        if (start_epoch < file_start_time + 86400) and (file_start_time < end_epoch):
            metadata_path.append(os.path.join(image_metadata_dir, filename))

    prod_inp = partial(read_geojson_metadata, start_epoch=start_epoch, end_epoch=end_epoch)

    # create a process pool and pass list of files to read geoJSON metadata function
    pool = Pool(processes=cpu_count())
    wkt_list = pool.map(prod_inp, metadata_path)
    pool.close()
    pool.join()

    # flatten the wkt list returned from each file
    flat_wkt_list = [item for sublist in wkt_list for item in sublist]
    logger.info("Reading GeoJSON metadata files...done")

    # Create geohash densities
    polygon_gdf = density_geohash(flat_wkt_list)
    polygon_gdf.to_file(output_geojson_path, driver='GeoJSON')
    logger.info("completed geohashing and counting points, output created...done")
