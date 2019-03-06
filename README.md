# map-tile-downloader
Crude tool to download maptiles from ArcGIS and save them as imagefiles on a local drive (e.g. for offline LeafletJS usage).

Can be imported into Eclipse, and exported as runnable Jar.

Set this section in [/src/GoGetter.java](https://github.com/jsteffensen/map-tile-downloader/blob/master/src/GoGetter.java):
```
// CHANGE THESE ////////////
base = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/";
//base = "https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/";
filetype = ".png";

zoom1 = 6;
zoom2 = 10;

lat1 = 53.67d;
lon1 = 4.2d;

lat2 = 58.12d;
lon2 = 16.3d;
////////////////////////////
    
```
