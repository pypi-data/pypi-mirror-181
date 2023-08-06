from tileset_analyzer.api.main_api import start_api
from tileset_analyzer.data_source.tile_source_factory import TilesetSourceFactory
from tileset_analyzer.utils.json_utils import write_json_file
import sys
import os


def execute(src_path, temp_folder):
    print('src_path', src_path)
    print('temp_folder', temp_folder)
    print('processing started')

    data_source = TilesetSourceFactory.get_tileset_source(src_path)
    result = data_source.analyze()

    output_json = os.path.join(temp_folder, 'analysis_result.json')

    write_json_file(result.get_json(), output_json)
    print('processing completed')

    print('Web UI started')
    start_api(temp_folder)
    print('Web UI stopped')


def get_arg(param):
    source_index = sys.argv.index(param)
    val = sys.argv[source_index + 1]
    return val


def cli():
    
    print('input:')
    print(sys.argv)
    print('------------------')
    src_path = None
    if '--source' in sys.argv[1:]:
        src_path = get_arg('--source')
    else:
        print('invalid Input.. Missing --source argument')
        exit(0)

    temp_folder = None
    if '--temp_folder' in sys.argv[1:]:
        temp_folder = get_arg('--temp_folder')
    else:
        print('invalid Input.. Missing --temp_folder argument')
        exit(0)

    execute(src_path, temp_folder)


'''
if __name__ == "__main__":
   cli()
'''
