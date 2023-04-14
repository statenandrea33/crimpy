"""Folium module."""

import folium

class Map(folium.Map):
    """Create a folium map object.
    
    Args:
        folium (_type_): The folium map object.
    """
# Init Function    
    def __init__(self, center=[20,0], zoom=2, **kwargs) -> None:
        """Initializes the map object.
       
        Agrs:
            center (list, optional): The center of the map. Defaults to [20,0].
            zoom (int, optional): The zoom level of the map. Defaults to 2.
        """
        super().__init__(location=center, zoom_start=zoom, **kwargs)

# Add Tile Layer Function
    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Add a tile layer to the map.

        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = folium.TileLayer(
            tiles=url, 
            name=name, 
            attr=attribution, 
            **kwargs
        )
        self.add_child(tile_layer)

# Add GeoJSON Function
    def add_geojson(self, data, name = 'GeoJSON', **kwargs):
        """Add a geojson file to the map (folium version).

        Args:
            data (str): A name of the geojson file.
            name (str, optional): A layer name of the geojson file to be displayed on the map. Defaults to 'GeoJSON'.
        """     
        geojson_layer = folium.GeoJson(
            data,
            name=name,
            **kwargs
        )
        self.add_child(geojson_layer)

# Add a Shapefile Function
    def add_shp(self, data, name='Shapefile', **kwargs):
        """Add a Shapefile layer to the map.

        Args:
            data (str): The path to the Shapefile.
            name (str, optional): The name of the Shapefile layer. Defaults to 'Shapefile'.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)