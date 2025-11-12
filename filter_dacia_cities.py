"""
Filter cities from cities500.txt that fall within the Dacia border polygon
Categorizes cities by country and saves to CSV
"""

import json
import csv
from typing import List, Tuple, Dict
from shapely.geometry import Point, Polygon
from collections import defaultdict


class DaciaCityFilter:
    """Filter cities within the Dacia border polygon"""
    
    def __init__(self, polygon_file: str, cities_file: str):
        self.polygon_file = polygon_file
        self.cities_file = cities_file
        self.polygon = None
        self.cities_in_polygon = []
        
    def load_polygon(self) -> Polygon:
        """Load the Dacia border polygon from JSON or TXT file"""
        print("Loading Dacia border polygon...")
        
        polygon_coords = []
        
        # Try to load as JSON first
        if self.polygon_file.endswith('.json'):
            try:
                with open(self.polygon_file, 'r', encoding='utf-8') as f:
                    # Try to parse as proper JSON
                    data = json.load(f)
                    if 'coordinates' in data:
                        coords = data['coordinates'][0]
                        polygon_coords = [(lon, lat) for lon, lat in coords]
            except json.JSONDecodeError:
                # If JSON parsing fails, try reading as coordinate pairs
                print("JSON parsing failed, trying as coordinate pairs...")
                with open(self.polygon_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('{') and not line.startswith('['):
                            parts = line.replace(',', ' ').split()
                            if len(parts) >= 2:
                                try:
                                    lon, lat = float(parts[0]), float(parts[1])
                                    polygon_coords.append((lon, lat))
                                except ValueError:
                                    continue
        else:
            # Load from TXT file (coordinate pairs)
            with open(self.polygon_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.replace(',', ' ').split()
                        if len(parts) >= 2:
                            try:
                                lon, lat = float(parts[0]), float(parts[1])
                                polygon_coords.append((lon, lat))
                            except ValueError:
                                continue
        
        if not polygon_coords:
            raise ValueError("No valid coordinates found in polygon file")
        
        self.polygon = Polygon(polygon_coords)
        print(f"Polygon loaded with {len(polygon_coords)} vertices")
        print(f"Polygon bounds: {self.polygon.bounds}")
        
        return self.polygon
    
    def parse_city_line(self, line: str) -> Dict:
        """Parse a line from cities500.txt"""
        fields = line.strip().split('\t')
        
        if len(fields) < 19:
            return None
        
        try:
            city_data = {
                'geonameid': fields[0],
                'name': fields[1],
                'asciiname': fields[2],
                'alternatenames': fields[3],
                'latitude': float(fields[4]),
                'longitude': float(fields[5]),
                'feature_class': fields[6],
                'feature_code': fields[7],
                'country_code': fields[8],
                'cc2': fields[9],
                'admin1_code': fields[10],
                'admin2_code': fields[11],
                'admin3_code': fields[12],
                'admin4_code': fields[13],
                'population': int(fields[14]) if fields[14] else 0,
                'elevation': fields[15],
                'dem': fields[16],
                'timezone': fields[17],
                'modification_date': fields[18]
            }
            return city_data
        except (ValueError, IndexError) as e:
            return None
    
    def point_in_polygon(self, lat: float, lon: float) -> bool:
        """Check if a point is within the polygon"""
        point = Point(lon, lat)  # Shapely uses (x, y) = (lon, lat)
        return self.polygon.contains(point)
    
    def filter_cities(self) -> List[Dict]:
        """Filter cities that fall within the Dacia polygon"""
        print(f"\nProcessing cities from {self.cities_file}...")
        
        cities_in_polygon = []
        total_cities = 0
        excluded_sectors = 0
        excluded_low_pop = 0
        
        with open(self.cities_file, 'r', encoding='utf-8') as f:
            for line in f:
                total_cities += 1
                
                city = self.parse_city_line(line)
                if not city:
                    continue
                
                # Check if city is within polygon
                if self.point_in_polygon(city['latitude'], city['longitude']):
                    # Exclude Romanian cities containing "Sector" in the name
                    if city['country_code'] == 'RO' and 'sector' in city['name'].lower():
                        excluded_sectors += 1
                        continue
                    
                    # Exclude Romanian and Hungarian cities with population < 900
                    if city['country_code'] in ['RO', 'HU'] and city['population'] < 1000:
                        excluded_low_pop += 1
                        continue
                    
                    # Decrease population by 15% for RO/HU cities under 300,000
                    if city['country_code'] in ['RO', 'HU'] and city['population'] < 300000:
                        city['population'] = int(city['population'] * 0.85)
                    
                    cities_in_polygon.append(city)
                
                # Progress indicator
                if total_cities % 10000 == 0:
                    print(f"Processed {total_cities:,} cities, found {len(cities_in_polygon)} in polygon...")
        
        self.cities_in_polygon = cities_in_polygon
        print(f"\nTotal cities processed: {total_cities:,}")
        print(f"Cities in Dacia polygon: {len(cities_in_polygon):,}")
        if excluded_sectors > 0:
            print(f"Romanian 'Sector' cities excluded: {excluded_sectors}")
        if excluded_low_pop > 0:
            print(f"RO/HU cities with pop < 900 excluded: {excluded_low_pop}")
        
        return cities_in_polygon
    
    def categorize_by_country(self) -> Dict[str, List[Dict]]:
        """Categorize cities by country code"""
        by_country = defaultdict(list)
        
        for city in self.cities_in_polygon:
            by_country[city['country_code']].append(city)
        
        # Sort countries by number of cities
        sorted_countries = dict(sorted(by_country.items(), 
                                      key=lambda x: len(x[1]), 
                                      reverse=True))
        
        print("\n" + "="*60)
        print("Cities by Country:")
        print("="*60)
        for country, cities in sorted_countries.items():
            print(f"{country}: {len(cities):,} cities")
        
        return sorted_countries
    
    def save_to_csv(self, output_file: str):
        """Save filtered cities to CSV"""
        print(f"\nSaving cities to {output_file}...")
        
        if not self.cities_in_polygon:
            print("No cities to save!")
            return
        
        # Sort by country, then by population (descending)
        sorted_cities = sorted(self.cities_in_polygon, 
                              key=lambda x: (x['country_code'], -x['population']))
        
        # Only save selected fields
        fieldnames = [
            'geonameid', 'name', 'asciiname', 'country_code',
            'latitude', 'longitude', 'population', 'elevation'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(sorted_cities)
        
        print(f"Successfully saved {len(sorted_cities):,} cities to {output_file}")
    
    def save_by_country(self, output_dir: str = None):
        """Save separate CSV files for each country"""
        by_country = self.categorize_by_country()
        
        if output_dir is None:
            output_dir = ""
        
        print(f"\nSaving individual country CSV files...")
        
        for country_code, cities in by_country.items():
            filename = f"{output_dir}dacia_cities_{country_code}.csv" if output_dir else f"dacia_cities_{country_code}.csv"
            
            # Sort by population descending
            sorted_cities = sorted(cities, key=lambda x: -x['population'])
            
            # Only save selected fields
            fieldnames = [
                'geonameid', 'name', 'asciiname', 'country_code',
                'latitude', 'longitude', 'population', 'elevation'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(sorted_cities)
            
            print(f"  Saved {len(cities):,} cities to {filename}")
    
    def generate_summary(self) -> str:
        """Generate a summary report"""
        by_country = defaultdict(list)
        for city in self.cities_in_polygon:
            by_country[city['country_code']].append(city)
        
        summary = []
        summary.append("\n" + "="*70)
        summary.append("DACIA CITIES SUMMARY REPORT")
        summary.append("="*70)
        summary.append(f"\nTotal cities in Dacia region: {len(self.cities_in_polygon):,}")
        summary.append(f"Number of countries: {len(by_country)}")
        
        summary.append("\n" + "-"*70)
        summary.append("Top cities by population:")
        summary.append("-"*70)
        
        top_cities = sorted(self.cities_in_polygon, key=lambda x: -x['population'])[:20]
        for i, city in enumerate(top_cities, 1):
            summary.append(f"{i:2d}. {city['name']:30s} ({city['country_code']}) - Pop: {city['population']:,}")
        
        summary.append("\n" + "-"*70)
        summary.append("Cities by country:")
        summary.append("-"*70)
        
        sorted_countries = sorted(by_country.items(), key=lambda x: len(x[1]), reverse=True)
        for country, cities in sorted_countries:
            total_pop = sum(c['population'] for c in cities)
            largest = max(cities, key=lambda x: x['population'])
            summary.append(f"{country}: {len(cities):4d} cities, Total pop: {total_pop:10,}, Largest: {largest['name']}")
        
        return "\n".join(summary)


def main():
    """Main function"""
    print("="*70)
    print("DACIA CITIES FILTER")
    print("="*70)
    
    # File paths
    polygon_file = 'dacia_border.txt'  # Can also use dacia_border.json
    cities_file = 'cities500/cities500.txt'
    output_file = 'dacia_cities_all.csv'
    
    # Create filter instance
    filter_obj = DaciaCityFilter(polygon_file, cities_file)
    
    # Load polygon
    filter_obj.load_polygon()
    
    # Filter cities
    filter_obj.filter_cities()
    
    # Save all cities to one CSV
    filter_obj.save_to_csv(output_file)
    
    # Save separate CSV files by country
    filter_obj.save_by_country()
    
    # Print summary
    print(filter_obj.generate_summary())
    
    print("\n" + "="*70)
    print("PROCESSING COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
