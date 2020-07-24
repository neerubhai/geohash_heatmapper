Geohash Mapper Module
=====================

This project is used to create a geohash heatmap GeoJSON collection file from input GeoJSON files that represent points 
Points with a datestamp are supported and can be used to filter the heatmap aggregation temporally.

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

A. Modify paths, query date ranges, geojson date field and formats in **main.py**
- For example
  - Input geojson files are in a folder called 'sample_data'
  - Output target file path is a file names 'geohash_denisty.geojson' in the 'sample_data' directory
  - Start of date range is "2012-01-20 UTC"
  - End of date range is "2013-10-20 UTC"
  - Input date field is "COLLISION_"
  - Input date format is "%Y-%m-%d" 
- These are set as follows:
```
input_geojson_dir = os.path.join(os.getcwd(), r'sample_data')
output_geojson_path = os.path.join(os.getcwd(), r'sample_data', r'geohash_density.geojson')
START_DATE = "2012-01-20 UTC" 
END_DATE = "2013-10-20 UTC" 
INPUT_DATE_FIELD = "COLLISION_" 
INPUT_DATE_FORMAT = "%Y-%m-%d" 
```
B. Run main.py
```
$ python main.py
```

## Accessing doc
Doc is located from this path as html. Open this file from a browser.
```
geohash_mapper/docs/_build/html/index.html
```

## Visualizing the output

- Quickest way to visualize the output is using HERE's GeoJSON web mapper that can be found here: http://geojson.tools/
- Copy paste the contents of the output geojson file to the 'Editor' or upload the GeoJSON file.
