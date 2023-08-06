from typing import List
import json

from tileset_analyzer.entities.layer_level_size import LayerLevelSize
from tileset_analyzer.entities.level_count import LevelCount
from tileset_analyzer.entities.level_size import LevelSize
from tileset_analyzer.entities.tileset_info import TilesetInfo


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return sorted(o)
        return o.__dict__


class TilesetAnalysisResult:
    def __init__(self):
        self.count_tiles_total: int = None
        self.count_tiles_by_z: List[LevelCount] = None
        self.tiles_size_agg_sum_by_z: List[LevelSize] = None
        self.tiles_size_agg_min_by_z: List[LevelSize] = None
        self.tiles_size_agg_max_by_z: List[LevelSize] = None
        self.tiles_size_agg_avg_by_z: List[LevelSize] = None
        self.tiles_size_agg_50p_by_z: List[LevelSize] = None
        self.tiles_size_agg_85p_by_z: List[LevelSize] = None
        self.tiles_size_agg_90p_by_z: List[LevelSize] = None
        self.tiles_size_agg_95p_by_z: List[LevelSize] = None
        self.tiles_size_agg_99p_by_z: List[LevelSize] = None

        self.tileset_info: TilesetInfo = None

    def set_count_tiles_total(self, num: int):
        self.count_tiles_total = num

    def set_count_tiles_by_z(self, level_counts: List[LevelCount]):
        self.count_tiles_by_z = level_counts

    def set_tiles_size_agg_sum_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_sum_by_z = level_sizes

    def set_tiles_size_agg_min_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_min_by_z = level_sizes

    def set_tiles_size_agg_max_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_max_by_z = level_sizes

    def set_tiles_size_agg_avg_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_avg_by_z = level_sizes

    def set_tiles_size_agg_50p_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_50p_by_z = level_sizes

    def set_tiles_size_agg_85p_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_85p_by_z = level_sizes

    def set_tiles_size_agg_90p_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_90p_by_z = level_sizes

    def set_tiles_size_agg_95p_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_95p_by_z = level_sizes

    def set_tiles_size_agg_99p_by_z(self, level_sizes: List[LevelSize]):
        self.tiles_size_agg_99p_by_z = level_sizes

    def set_tileset_info(self, tileset_info: TilesetInfo):
        self.tileset_info = tileset_info

    def set_tiles_size_agg_sum_by_z_layer(self, level_sizes: List[LayerLevelSize]):
        self.tiles_size_agg_sum_by_z_layer = level_sizes

    def get_json(self):
        return json.dumps(
            self.__dict__,
            indent=4,
            cls=CustomEncoder,
            sort_keys=True,
            separators=(',', ': '),
            ensure_ascii=False
        )
