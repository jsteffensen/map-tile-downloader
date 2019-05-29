package com.c2_systems.maptiles;

import java.net.URL;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.FailingHttpStatusCodeException;
import com.gargoylesoftware.htmlunit.WebClient;

public class TileClient {

	public static WebClient webClient = new WebClient(BrowserVersion.CHROME);
	
	public static void saveTileJavaIO(int x, int y, int z) {

		if(!Files.exists( Paths.get("C:/MapTileDownloader/openstreetmap/" + x + "/" + y + "/" + z + App.filetype) )) {
			
			try(InputStream in = new URL(App.base + x + "/" + y + "/" + z + App.filetype).openStream()){
				Path dir = Paths.get("C:/MapTileDownloader/openstreetmap/" + x + "/" + y);
				Files.createDirectories(dir);
	
			    Files.copy(in, Paths.get("C:/MapTileDownloader/openstreetmap/" + x + "/" + y + "/" + z + App.filetype));
			} catch (IOException e) {
				if (e instanceof FileNotFoundException) {
					System.out.println("not found.");
				} else {
					e.printStackTrace();
				}
				System.exit(1);
			}
		}
	}
	
	public static void saveTileHtmlUnit(int x, int y, int z) {
		
		if(!Files.exists( Paths.get("C:/MapTileDownloader/openstreetmap/" + x + "/" + y + "/" + z + App.filetype) )) {
			
			try {
				URL url = new URL(App.base + x + "/" + y + "/" + z + App.filetype);
				webClient.getPage(url);
			} catch (Exception e) {
				if(e instanceof FailingHttpStatusCodeException) {
					e.printStackTrace();
				} else if(e instanceof IOException) {
					e.printStackTrace();
				} else {
					e.printStackTrace();
				}
				
				System.exit(1);
			}

		}
	}
	
}
