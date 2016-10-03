import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class GoGetter {

	public static void saveTile(int x, int y, int z) {

		//String base = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/";
		String base = "https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/";

		try(InputStream in = new URL(base + x + "/" + y + "/" + z + ".png").openStream()){
			Path dir = Paths.get("C:/MapTileDownloader/aal/" + x + "/" + y);
			Files.createDirectories(dir);

		    Files.copy(in, Paths.get("C:/MapTileDownloader/aal/" + x + "/" + y + "/" + z + ".png"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	 public static int[] getTileNumber(final double lat, final double lon, final int zoom) {
		   int xtile = (int)Math.floor( (lon + 180) / 360 * (1<<zoom) ) ;
		   int ytile = (int)Math.floor( (1 - Math.log(Math.tan(Math.toRadians(lat)) + 1 / Math.cos(Math.toRadians(lat))) / Math.PI) / 2 * (1<<zoom) ) ;
		    if (xtile < 0)
		     xtile=0;
		    if (xtile >= (1<<zoom))
		     xtile=((1<<zoom)-1);
		    if (ytile < 0)
		     ytile=0;
		    if (ytile >= (1<<zoom))
		     ytile=((1<<zoom)-1);
		    int[] arr = {xtile, ytile};
		    return arr;

	}

	public static void main(String[] args) {

		int zoom, y1, y2, z1, z2, m, t;
		double lat1, lat2, lon1, lon2;

		// CHANGE THESE ////////////
		zoom = 19;

		lat1 = 57.077372d;
		lon1 = 9.814816d;

		lat2 = 57.111579d;
		lon2 = 9.890497d;
		////////////////////////////

		int[] startTile = getTileNumber(lat1, lon1, zoom);
		int[] stopTile = getTileNumber(lat2, lon2, zoom);

		y1 = stopTile[1];
		y2 = startTile[1];

		z1 = startTile[0];
		z2 = stopTile[0];

		m = 1;
		t = (y2-y1+1) * (z2-z1+1);

		for(int j = y1; j <= y2; j++) {
			for(int k = z1 ; k <= z2; k++, m++) {
				saveTile(zoom, j, k);
				System.out.println("Tile " + m + " of " + t);
			}

		}


	}

}
