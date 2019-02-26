# map-tile-downloader
Crude tool to download maptiles from ArcGIS and save them as imagefiles (for LeafletJS usage)

Can be imported into Eclipse, and exported as runnable Jar.

Set this section in /src/GoGetter.java:
```
		// CHANGE THESE ////////////
		base = "https://basemaps.arcgis.com/arcgis/rest/services/World_Basemap_v2/VectorTileServer/tile/";
		filetype = ".pbf";
		
		zoom1 = 11;
		zoom2 = 19;

		lat1 = 53.67d;
		lon1 = 4.2d;

		lat2 = 58.12d;
		lon2 = 16.3d;
		////////////////////////////
    
```
