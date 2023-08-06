import abc
from collections import namedtuple
from sqlite3 import Connection
from typing import List
from tileset_analyzer.data_source.mbtiles.sqllite_utils import create_connection
from tileset_analyzer.data_source.tile_source import TileSource
from tileset_analyzer.entities.level_size import LevelSize
from tileset_analyzer.entities.tileset_analysis_result import LevelCount, TilesetAnalysisResult
from tileset_analyzer.data_source.mbtiles.sql_queries import SQL_COUNT_TILES, SQL_COUNT_TILES_BY_Z, \
    SQL_SUM_TILE_SIZES_BY_Z, SQL_MIN_TILE_SIZES_BY_Z, SQL_MAX_TILE_SIZES_BY_Z, SQL_AVG_TILE_SIZES_BY_Z, \
    SQL_LIST_TILE_SIZES_BY_Z
import pandas as pd
import numpy as np


class MBTileSource(TileSource):
    def __init__(self, src_path: str):
        self.conn = create_connection(src_path)
        self.tiles_size_z_df = None

    def count_tiles(self) -> int:
        cur = self.conn.cursor()
        cur.execute(SQL_COUNT_TILES)
        count = cur.fetchone()[0]
        return count

    def count_tiles_by_z(self) -> List[LevelCount]:
        cur = self.conn.cursor()
        cur.execute(SQL_COUNT_TILES_BY_Z)
        rows = cur.fetchall()
        result: List[LevelCount] = []
        for row in rows:
            result.append(LevelCount(row[0], row[1]))
        return result

    def _get_agg_tile_size_z(self, agg_type: str) -> List[LevelSize]:
        sql = None
        if agg_type == 'SUM':
            sql = SQL_SUM_TILE_SIZES_BY_Z
        elif agg_type == 'MIN':
            sql = SQL_MIN_TILE_SIZES_BY_Z
        elif agg_type == 'MAX':
            sql = SQL_MAX_TILE_SIZES_BY_Z
        elif agg_type == 'AVG':
            sql = SQL_AVG_TILE_SIZES_BY_Z
        else:
            raise 'UNKNOWN AGG TYPE'

        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        result: List[LevelSize] = []
        for row in rows:
            result.append(LevelSize(row[0], row[1]))
        return result

    def _set_tilesize_z_dataframe(self):
        query = SQL_LIST_TILE_SIZES_BY_Z
        cur = self.conn.cursor()
        self.tiles_size_z_df = pd.read_sql(query, self.conn)
        cur.close()

    def _clear_tilesize_z_dataframe(self):
        self.tiles_size_z_df = None

    def _get_agg_tile_size_percentiles_z(self, percentile_type: str) -> List[LevelSize]:
        quantile = None
        if percentile_type == '50p':
            quantile = 0.5
        elif percentile_type == '85p':
            quantile = 0.85
        elif percentile_type == '90p':
            quantile = 0.9
        elif percentile_type == '95p':
            quantile = 0.95
        elif percentile_type == '99p':
            quantile = 0.99
        else:
            raise 'UNKNOWN PERCENTILE TYPE'

        result_df = self.tiles_size_z_df.groupby('zoom_level').quantile(quantile)
        result: List[LevelSize] = []
        for row in result_df.itertuples():
            result.append(LevelSize(row[0], row[1]))
        return result

    def tiles_size_agg_min_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_z('MIN')

    def tiles_size_agg_max_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_z('MAX')

    def tiles_size_agg_avg_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_z('AVG')

    def tiles_size_agg_sum_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_z('SUM')

    def tiles_size_agg_50p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('50p')

    def tiles_size_agg_85p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('85p')

    def tiles_size_agg_90p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('90p')

    def tiles_size_agg_95p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('95p')

    def tiles_size_agg_99p_by_z(self) -> List[LevelSize]:
        return self._get_agg_tile_size_percentiles_z('99p')

    def analyze(self) -> TilesetAnalysisResult:
        result = TilesetAnalysisResult()
        result.set_count_tiles_total(self.count_tiles())
        result.set_count_tiles_by_z(self.count_tiles_by_z())
        result.set_tiles_size_agg_sum_by_z(self.tiles_size_agg_sum_by_z())
        result.set_tiles_size_agg_min_by_z(self.tiles_size_agg_min_by_z())
        result.set_tiles_size_agg_max_by_z(self.tiles_size_agg_max_by_z())
        result.set_tiles_size_agg_avg_by_z(self.tiles_size_agg_avg_by_z())

        self._set_tilesize_z_dataframe()
        result.set_tiles_size_agg_50p_by_z(self.tiles_size_agg_50p_by_z())
        result.set_tiles_size_agg_85p_by_z(self.tiles_size_agg_85p_by_z())
        result.set_tiles_size_agg_90p_by_z(self.tiles_size_agg_90p_by_z())
        result.set_tiles_size_agg_95p_by_z(self.tiles_size_agg_95p_by_z())
        result.set_tiles_size_agg_99p_by_z(self.tiles_size_agg_99p_by_z())
        self._clear_tilesize_z_dataframe()

        return result

