from tileset_analyzer.api.main_api import start_api
from tileset_analyzer.data_source.tile_source_factory import TilesetSourceFactory
from tileset_analyzer.utils.json_utils import write_json_file
import sys
import os
import argparse


def execute(src_path, scheme, temp_folder, actions):
    print('started...')
    print('src_path:', src_path)
    print('scheme:', scheme)
    print('temp_folder:', temp_folder)
    print('actions', actions)

    if 'process' in actions:
        print('processing started')
        data_source = TilesetSourceFactory.get_tileset_source(src_path, scheme)
        result = data_source.analyze()

        output_json = os.path.join(temp_folder, 'analysis_result.json')

        write_json_file(result.get_json(), output_json)
        print('processing completed')

    if 'serve' in actions:
        print('Web UI started')
        start_api(temp_folder)
        print('Web UI stopped')

    print('completed')


def get_arg(param):
    source_index = sys.argv.index(param)
    val = sys.argv[source_index + 1]
    return val


def cli():
    parser = argparse.ArgumentParser(prog='tileset_analyzer')
    parser.add_argument('--source', help='source', required=True)
    parser.add_argument('--scheme', help='scheme', default='XYZ')
    parser.add_argument('--temp_folder', help='temp_folder', required=True)
    parser.add_argument('--actions', help='actions', default='process,serve')
    args = parser.parse_args()
    actions = args.actions.split(',')
    execute(args.source, args.scheme, args.temp_folder, actions)


'''
if __name__ == "__main__":
   cli()
'''
