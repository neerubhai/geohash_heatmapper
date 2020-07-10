Geohash Mapper Module
=====================

This project is used to create a geohash heatmap GeoJSON collection from image metadata.

---------------


## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Setup

1. Install Python 3.6+ 
Latest version of 3.6.x can be downloaded here: https://www.python.org/downloads/release/python-3610/

2. Install Pip

3. Install the required packages. Run the following command in your terminal: 
```
$ cd geohash_mapper
$ pip install -r requirements.txt
```

### Running the code

A. Modify paths and time ranges in **main.py**
- For example
  - Input geojson files are in a folder called 'image_metadata'
  - Output target file path is a file names 'geohash_denisty.geojson' in the 'output geojson' directory
  - Start of time range is "2018-08-17 00:00:00 UTC"
  - End of time range is "2018-08-20 00:00:00 UTC" 
- Set the paths and time range as follows:
```
image_metadata_dir = os.path.join(os.path.dirname(os.getcwd()), r'image_metadata')
output_geojson_path = os.path.join(
    os.path.dirname(os.getcwd()), r'output_geojson', r'geohash_density.geojson')
START_TIME = "2018-08-20 00:00:00 UTC"
END_TIME = "2018-08-21 00:00:00 UTC"
```
B. Run main.py
```
$ python main.py
```

## Running the tests

Run the unit tests that test the functionality of this module
```
$ python sanity_test.py
```

## Accessing doc
Doc is located from this path as html. Open this file from a browser.
```
geohash_mapper/docs/_build/html/index.html
```

## Visualizing the output

- Quickest way to visualize the output is using HERE's GeoJSON web mapper that can be found here: http://geojson.tools/
- Copy paste the contents of the output geojson file to the 'Editor' or upload the GeoJSON file.
