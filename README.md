
Geohash Mapper Module
=====================

This project can be used to create a heatmap of spatial point data. Geohash polygons are used to represent heatmaps and are stored as a GeoJSON collection file. Input spatial point in GeoJSON format can be used by this module. Input points that lie within a geohash polygon's spatial extents are counted and used to create these heatmaps. A temporal filter can be applied to the heatmap creation process, if the point data has a date field associated to it. The date field is usually stored in the point metadata (see sample data provided with this module in the 'sample_data/' folder). Multiprocessing is leveraged to process multiple input files parallely improving overall processing time. 

---------------


## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

## Sample data
Sample input and output datasets are provided to demonstrate this functionality. This is a good starting point to understand the modules and how to prepare your own input datasets. 

The sample includes:
1) Two input point files - _LACollisions2012.geojson_ and _LACollisions2013.geojson_
Credits - These datasets were derived from point features acquired from Los Angeles GeoHub Open Data. 
The source dataset is named 'Collisions 2009-2013 (SWITRS)' and can be found in the GeoHub Open Data platform here: http://geohub.lacity.org/ 
2) Output heatmap geohash polygon collection file - _geohash_density.geojson_

---------------
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
  - Input geojson point files are in a folder called 'sample_data'
  - Output geohash heatmap file path is created with a file name 'geohash_density.geojson' in the 'sample_data' directory
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
B. Run main.py. 
This will kickstart the aggregration process from input point files and create an output geohash collection file.
```
$ python main.py
```
---------------

## Accessing doc
Doc for the modules is located from this path as an html file. Open this file from a web browser.
```
geohash_mapper/docs/_build/html/index.html
```

---------------

## Visualizing the output

- Quickest way to visualize the output is using HERE's GeoJSON web mapper that can be found here: http://geojson.tools/
- Copy paste the contents of the output geojson file to the 'Editor' or upload the GeoJSON file. 
You can try it out with the sample output data from this file in this repo: '/sample_data/geohash_density.geojson'

![alt text](https://github.com/neerubhai/geohash_heatmapper/blob/master/sample_data/geohash_heatmap_sampledata.png)
---------------

