import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class GoGetter {
	
	private static String base, filetype;
	private static int zoom1, zoom2;
	private static double lat1, lon1, lat2, lon2;
	
	public static void main(String[] args) {
		
		// CHANGE THESE ////////////
		
		//base = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/";
		base = "https://b.tile.openstreetmap.org/";
		filetype = ".png";
		
		zoom1 = 1;
		zoom2 = 14;

		// south-west corner
		lat1 = 53.67d;
		lon1 = 4.2d;

		// north-west corner
		lat2 = 58.17d;
		lon2 = 18.7d;
		////////////////////////////
		
		downloadSet();

	}
	
	private static void downloadSet() {
		int[] startTile = getTileNumber(lat1, lon1, zoom1);
		int[] stopTile = getTileNumber(lat2, lon2, zoom1);

		int y1 = stopTile[1];
		int y2 = startTile[1];

		int z1 = startTile[0];
		int z2 = stopTile[0];

		int m = 1;
		int t = (y2-y1+1) * (z2-z1+1);

		for(int j = y1; j <= y2; j++) {
			for(int k = z1 ; k <= z2; k++, m++) {
				saveTile(zoom1, j, k);
				System.out.println("Tile " + m + " of " + t + " (" + zoom1 + "/" + j + "/" + k + filetype + ")");
			}

		}
		if(zoom1<zoom2) {
			zoom1++;
			downloadSet();
		} else {
			System.out.println("Done downloading");
		}
	}
	
	 private static int[] getTileNumber(final double lat, final double lon, final int zoom) {
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
	 
	public static void saveTile(int x, int y, int z) {

		if(!Files.exists( Paths.get("C:/MapTileDownloader/openstreetmap/" + x + "/" + y + "/" + z + filetype) )) {
			
			try(InputStream in = new URL(base + x + "/" + y + "/" + z + filetype).openStream()){
				Path dir = Paths.get("C:/MapTileDownloader/openstreetmap/" + x + "/" + y);
				Files.createDirectories(dir);
	
			    Files.copy(in, Paths.get("C:/MapTileDownloader/openstreetmap/" + x + "/" + y + "/" + z + filetype));
			} catch (IOException e) {
				if (e instanceof FileNotFoundException) {
					System.out.println("not found.");
				} else {
					e.printStackTrace();
				}
			}
		}
	}

}
