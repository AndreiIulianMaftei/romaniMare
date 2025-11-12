# Dacia Cities Filter

This script filters cities from the GeoNames cities500.txt database that fall within the historical Dacia border polygon.

## Features

- ✅ Loads Dacia border polygon from JSON
- ✅ Filters 185,000+ cities from cities500.txt
- ✅ Uses point-in-polygon algorithm to identify cities within Dacia
- ✅ Categorizes cities by country code
- ✅ Generates comprehensive statistics
- ✅ Saves results to CSV files

## Output Files

1. **dacia_cities_all.csv** - All cities within Dacia border, sorted by country and population
2. **dacia_cities_XX.csv** - Separate CSV for each country (e.g., dacia_cities_RO.csv for Romania)

## Installation

Install the required dependencies:
```powershell
pip install shapely
```

Or install all dependencies:
```powershell
pip install -r requirements.txt
```

## Usage

```powershell
python filter_dacia_cities.py
```

## CSV Output Format

The output CSV files contain these columns:
- `geonameid` - Unique ID
- `name` - City name
- `asciiname` - ASCII version
- `alternatenames` - Alternate names
- `latitude` - Latitude coordinate
- `longitude` - Longitude coordinate
- `feature_class` - Feature type (P for populated place)
- `feature_code` - Specific feature code
- `country_code` - ISO 2-letter country code
- `cc2` - Alternate country codes
- `admin1_code` - 1st level admin division
- `admin2_code` - 2nd level admin division
- `admin3_code` - 3rd level admin division
- `admin4_code` - 4th level admin division
- `population` - Population count
- `elevation` - Elevation in meters
- `dem` - Digital elevation model
- `timezone` - IANA timezone
- `modification_date` - Last update date

## Summary Report

The script generates a summary showing:
- Total cities found in Dacia region
- Number of countries represented
- Top 20 cities by population
- Statistics by country (city count, total population, largest city)

## Expected Countries

Historically, Dacia covered parts of modern-day:
- Romania (RO)
- Moldova (MD)
- Ukraine (UA)
- Serbia (RS)
- Bulgaria (BG)
- Hungary (HU)
