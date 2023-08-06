from main import execute


if __name__ == "__main__":
    src_path = 'data/maptiler-osm-2017-07-03-v3.6.1-us_virginia.mbtiles'
    temp_folder = 'tileset_analyzer/static/data'
    execute(src_path, temp_folder)
