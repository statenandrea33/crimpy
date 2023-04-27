"""Main module."""

import string
import random
import ipyleaflet

class Map(ipyleaflet.Map):
# Init Function
    def __init__(self, center=[20,0], zoom=2, **kwargs) -> None:
        """Adds the ability to use a mouse to zoom in and out.
        
        Args:
            **kwargs: Keyword arguments passed to the scroll wheel zoom.
        """
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)
        
        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True

        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True

        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()

# Add Search Control Function
    def add_search_control(self, position="topleft", **kwargs):
        """Add a search control to the map.

        Args:
            **kwargs: Keyword arguments passed to the search control.
        """
        if "url" not in kwargs:
            kwargs["url"] = "https://nominatim.openstreetmap.org/search?format=json&q={s}"

        search_control = ipyleaflet.SearchControl(position=position, **kwargs)
        self.add_control(search_control)

# Add Draw Control Function
    def add_draw_control(self, **kwargs):
        """Add a draw control to the map.
        
        Args:
            **kwargs: Keyword arguments passed to the draw control.
        """
        draw_control = ipyleaflet.DrawControl(**kwargs)
        self.add_control(draw_control)

# Add Layers Control Function
    def add_layers_control(self, position='topright'):
        """Add a layers control to the map.

        Args:
            **kwargs: Keyword arguments passed to the layers control.
        """
        layers_control = ipyleaflet.LayersControl(position=position)
        self.add_control(layers_control)

# Add Fullscreen Control Function
    def add_fullscreen_control(self, position='topleft'):
        """Add a fullscreen control to the map.

        Args:
            **kwargs: Keyword arguments passed to the fullscreen control.
        """
        fullscreen_control = ipyleaflet.FullScreenControl(position=position)
        self.add_control(fullscreen_control)

# Add Tile Layer Function
    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Add a tile layer to the map.

        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)

# Basemap Function
    def add_basemap(self, basemap, **kwargs):
        
        import xyzservices.providers as xyz

        if basemap.lower() == "roadmap":
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "satellite":
            url = 'http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"{basemap} is not a valid basemap.")

# Add GeoJSON Function          
    def add_geojson(self, data, name='GeoJSON', **kwargs):
        """Add a GeoJSON layer to the map.

        Args:
            data (dict): The GeoJSON data.
            name (str, optional): The name of the GeoJSON layer. Defaults to 'GeoJSON'.
        """

        if isinstance(data, str):
            import json
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add_layer(geojson)

# Add Shapefile Function
    def add_shp(self, data, name='Shapefile', **kwargs):
        """Add a Shapefile layer to the map.

        Args:
            data (str): The path to the Shapefile.
            name (str, optional): The name of the Shapefile layer. Defaults to 'Shapefile'.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.to_json()
        self.add_geojson(geojson, name=name, **kwargs)

# Add a Vector Function
    def add_vector(self, data, name='Vector', **kwargs):
        """Add a Vector layer to the map.

        Args:
            data (str): The path to the Vector file.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.to_json()
        self.add_geojson(geojson, name=name, **kwargs)

# Add a Raster Function
    def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):
        """Add a raster layer to the map.
        
        Args:
            url (str): The URL of the raster layer.
            name (str, optional): The name of the raster layer. Defaults to 'Raster'.
            fit_bounds (bool, optional): Whether to fit the map bounds to the raster layer. Defaults to True.
        """
        import httpx
        
        titiler_endpoint = "https://titiler.xyz"
        
        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]

        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
            "url": url,
            }
        ).json()

        tile = r["tiles"][0]

        self.add_tile_layer(url=tile, name=name, **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)

# Add an Image Function
    def add_image(self, url, width, height, position = 'bottomleft'):
        """Add an image to the map.

        Args:
            url (str): The URL of the image.
            width (int): The width of the image.
            height (int): The height of the image.
        """
        from ipyleaflet import WidgetControl
        import ipywidgets as widgets

        widget = widgets.HTML(value = f'<img src="{url}" width="{width}" height="{height}">')
        control = WidgetControl(widget=widget, position=position)
        self.add(control)

# Add a Toolbar Function
    def add_toolbar(self, position="topright"):
        """Adds a toolbar with a dropdown menu to change the basemap.
        Args:
            self: The map.
            position (str, optional): The position of the toolbar. Defaults to "topright".
        """
        import ipywidgets as widgets

        widget_width = "250px"
        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )

        toolbar = widgets.HBox([toolbar_button, close_button])

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()
                basemap.close()
                
        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px"))

        icons = ["folder-open", "map", "bluetooth", "area-chart"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(description="", button_style="primary", icon=icons[i*rows+j], 
                                            layout=widgets.Layout(width="28px", padding="0px"))
                
        toolbar = widgets.VBox([toolbar_button])

        basemap = widgets.Dropdown(
            options=['OpenStreetMap', 'ROADMAP', 'SATELLITE'],
            value=None,
            description='Basemap:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='250px')
        )

        basemap_ctrl = ipyleaflet.WidgetControl(widget=basemap, position='topright')

        def change_basemap(change):
            if change['new']:
                self.add_basemap(basemap.value)

        basemap.observe(change_basemap, names='value')

        output = widgets.Output()
        output_ctrl = ipyleaflet.WidgetControl(widget=output, position="bottomright")
        self.add_control(output_ctrl)

        def tool_click(b):
            with output:
                output.clear_output()
                print(f"You clicked the {b.icon} button.")
                if b.icon == 'map':
                    if basemap_ctrl not in self.controls:
                        self.add_control(basemap_ctrl)
        
        for i in range(rows):
            for j in range(cols):
                tool = grid[i, j]
                tool.on_click(tool_click)

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]
                
        toolbar_button.observe(toolbar_click, "value")

        toolbar_ctrl = ipyleaflet.WidgetControl(widget=toolbar, position=position)

        self.add_control(toolbar_ctrl)


# Add Locations to Map Function
    def add_locations_to_map(self, locations):
        """Takes coordinates from a list called locations and creates points on a map.

        Args:
            self : The map to add the locations to.
            locations : A list of locations containing name, latitude, and longitude data. 
        """

        # Create a marker cluster layer to group nearby markers
        marker_cluster = ipyleaflet.MarkerCluster()

        # Loop through the list of locations and add a marker for each one
        for location in locations:
            # Extract the latitude and longitude from the list
            lat, lon = location['latitude'], location['longitude']
       
            # Create a new marker at the location and add it to the layer
            marker = ipyleaflet.Marker(location=(lat,lon))
            self.add_layer(marker)
    
        # Add the marker cluster to the map
        self.add_layer(marker_cluster)
    
        # Find the Center of the markers
        lats = [location['latitude'] for location in locations]
        lons = [location['longitude'] for location in locations]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        # Set the center
        self.center = (center_lat, center_lon)