from typing import Final

SQL_COUNT_TILES: Final[str] = 'select count(*) as count from tiles;'
SQL_COUNT_TILES_BY_Z: Final[str] = 'select zoom_level as zoom_level, count(*) as count from tiles group by zoom_level order by zoom_level ASC;'
SQL_SUM_TILE_SIZES_BY_Z: Final[str] = 'select zoom_level as zoom_level, sum(LENGTH(tile_data)) as size from tiles group by zoom_level order by zoom_level ASC ;'
SQL_MIN_TILE_SIZES_BY_Z: Final[str] = 'select zoom_level as zoom_level, min(LENGTH(tile_data)) as size from tiles group by zoom_level order by zoom_level ASC;'
SQL_MAX_TILE_SIZES_BY_Z: Final[str] = 'select zoom_level as zoom_level, max(LENGTH(tile_data)) as size from tiles group by zoom_level order by zoom_level ASC;'
SQL_AVG_TILE_SIZES_BY_Z: Final[str] = 'select zoom_level as zoom_level, ROUND(avg(LENGTH(tile_data))) as size from tiles group by zoom_level order by zoom_level ASC;'
SQL_LIST_TILE_SIZES_BY_Z: Final[str] = 'select zoom_level as zoom_level, LENGTH(tile_data) as size from tiles order by zoom_level asc, LENGTH(tile_data) asc;'
SQL_ALL_TILES: Final[str] = 'select tile_row as x, tile_column as y, zoom_level as z, tile_data as tile_data from tiles order by zoom_level asc, x asc, y asc;'

