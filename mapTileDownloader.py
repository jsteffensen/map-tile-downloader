#!/usr/bin/env python3
"""
Same thing ...
Map Tile Downloader - Python version
Downloads map tiles from ArcGIS or other tile servers
Uses only standard library (urllib) - no external dependencies required
"""

import urllib.request
import urllib.error
import os
import math
from pathlib import Path


class MapTileDownloader:
    """Downloads map tiles from tile servers like ArcGIS"""
    
    def __init__(self, base_url, filetype=".png", output_dir="tiles"):
        """
        Initialize the downloader
        
        Args:
            base_url: Base URL for tiles (e.g., "https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/")
            filetype: File extension for tiles (e.g., ".png", ".jpg")
            output_dir: Directory to save tiles
        """
        self.base_url = base_url
        self.filetype = filetype
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def lat_lon_to_tile(self, lat, lon, zoom):
        """
        Convert latitude/longitude to tile coordinates
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            zoom: Zoom level
            
        Returns:
            tuple: (x, y) tile coordinates
        """
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        x = int((lon + 180.0) / 360.0 * n)
        y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (x, y)
    
    def download_tile(self, zoom, x, y, current=None, total=None):
        """
        Download a single tile
        
        Args:
            zoom: Zoom level
            x: Tile X coordinate
            y: Tile Y coordinate
            current: Current tile number (for progress tracking)
            total: Total number of tiles (for progress tracking)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Construct URL (format: base_url/zoom/y/x.filetype)
        url = f"{self.base_url}{zoom}/{y}/{x}{self.filetype}"
        
        # Create directory structure
        tile_dir = os.path.join(self.output_dir, str(zoom), str(y))
        Path(tile_dir).mkdir(parents=True, exist_ok=True)
        
        # File path
        filepath = os.path.join(tile_dir, f"{x}{self.filetype}")
        
        # Progress string
        progress_str = ""
        if current is not None and total is not None:
            percentage = (current / total) * 100
            progress_str = f" ({current}/{total} - {percentage:.1f}%)"
        
        # Skip if already downloaded
        if os.path.exists(filepath):
            print(f"Skipping (already exists): {zoom}/{y}/{x}{progress_str}")
            return True
        
        try:
            # Download tile
            print(f"Downloading: {zoom}/{y}/{x}{progress_str}")
            with urllib.request.urlopen(url, timeout=10) as response:
                data = response.read()
                
            # Save tile
            with open(filepath, 'wb') as f:
                f.write(data)
                
            return True
            
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code} for tile {zoom}/{y}/{x}: {e.reason}{progress_str}")
            return False
        except urllib.error.URLError as e:
            print(f"URL Error for tile {zoom}/{y}/{x}: {e.reason}{progress_str}")
            return False
        except Exception as e:
            print(f"Error downloading tile {zoom}/{y}/{x}: {str(e)}{progress_str}")
            return False
    
    def calculate_tile_count(self, lat1, lon1, lat2, lon2, zoom_min, zoom_max):
        """
        Calculate how many tiles will be downloaded without actually downloading
        
        Args:
            lat1: Bottom-left latitude
            lon1: Bottom-left longitude
            lat2: Top-right latitude
            lon2: Top-right longitude
            zoom_min: Minimum zoom level
            zoom_max: Maximum zoom level
            
        Returns:
            dict: Statistics about tiles per zoom level and total
        """
        stats = {
            'zoom_levels': {},
            'total_tiles': 0
        }
        
        for zoom in range(zoom_min, zoom_max + 1):
            # Get tile coordinates for corners
            x1, y1 = self.lat_lon_to_tile(lat1, lon1, zoom)
            x2, y2 = self.lat_lon_to_tile(lat2, lon2, zoom)
            
            # Ensure correct order
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            
            # Calculate tiles for this zoom level
            tiles_in_zoom = (x_max - x_min + 1) * (y_max - y_min + 1)
            
            stats['zoom_levels'][zoom] = {
                'tile_count': tiles_in_zoom,
                'x_range': (x_min, x_max),
                'y_range': (y_min, y_max)
            }
            stats['total_tiles'] += tiles_in_zoom
        
        return stats
    
    def download_region(self, lat1, lon1, lat2, lon2, zoom_min, zoom_max):
        """
        Download all tiles for a geographic region across multiple zoom levels
        
        Args:
            lat1: Bottom-left latitude
            lon1: Bottom-left longitude
            lat2: Top-right latitude
            lon2: Top-right longitude
            zoom_min: Minimum zoom level
            zoom_max: Maximum zoom level
        """
        # Calculate and display tile count before downloading
        print("=== Calculating tile count ===")
        stats = self.calculate_tile_count(lat1, lon1, lat2, lon2, zoom_min, zoom_max)
        
        print(f"\nTiles per zoom level:")
        for zoom, info in stats['zoom_levels'].items():
            x_min, x_max = info['x_range']
            y_min, y_max = info['y_range']
            print(f"  Zoom {zoom}: {info['tile_count']:,} tiles (X: {x_min}-{x_max}, Y: {y_min}-{y_max})")
        
        print(f"\n** TOTAL TILES TO DOWNLOAD: {stats['total_tiles']:,} **")
        
        # Estimate download size (assuming ~50KB per tile on average)
        estimated_size_mb = (stats['total_tiles'] * 50) / 1024
        if estimated_size_mb > 1024:
            print(f"** ESTIMATED SIZE: ~{estimated_size_mb/1024:.1f} GB **")
        else:
            print(f"** ESTIMATED SIZE: ~{estimated_size_mb:.0f} MB **")
        
        # Ask for confirmation
        print("\nPress Enter to start downloading, or Ctrl+C to cancel...")
        try:
            input()
        except KeyboardInterrupt:
            print("\n\nDownload cancelled by user.")
            return
        
        total_tiles = 0
        successful_tiles = 0
        overall_tile_count = 0
        
        for zoom in range(zoom_min, zoom_max + 1):
            print(f"\n=== Processing Zoom Level {zoom} ===")
            
            # Get tile coordinates for corners
            x1, y1 = self.lat_lon_to_tile(lat1, lon1, zoom)
            x2, y2 = self.lat_lon_to_tile(lat2, lon2, zoom)
            
            # Ensure correct order
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            
            # Download all tiles in the region
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    total_tiles += 1
                    overall_tile_count += 1
                    if self.download_tile(zoom, x, y, overall_tile_count, stats['total_tiles']):
                        successful_tiles += 1
        
        print(f"\n=== Download Complete ===")
        print(f"Total tiles processed: {total_tiles}")
        print(f"Successfully downloaded: {successful_tiles}")
        print(f"Failed: {total_tiles - successful_tiles}")
        print(f"Output directory: {self.output_dir}")


def main():
    """Example usage"""
    
    # Configuration - CHANGE THESE VALUES
    base_url = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/"
    filetype = ".png"
    
    # Zoom levels
    zoom_min = 6
    zoom_max = 8
    
    # Geographic region (example: area around Denmark/Netherlands)
    lat1 = 53.67  # Bottom latitude
    lon1 = 4.2    # Left longitude
    lat2 = 58.12  # Top latitude
    lon2 = 16.3   # Right longitude
    
    output_dir = "downloaded_tiles"
    
    # Create downloader and start downloading
    downloader = MapTileDownloader(base_url, filetype, output_dir)
    downloader.download_region(lat1, lon1, lat2, lon2, zoom_min, zoom_max)


if __name__ == "__main__":
    main()
