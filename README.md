# Wikipedia City Data Extractor

This script extracts demographic and economic data about cities from Wikipedia.

## Features

The script extracts the following information for each city:
- **Population**: Total population, metro population, population density
- **Demographics**: Demographic summary and demonym
- **Economy**: GDP total and GDP per capita
- **Industries**: Major industries in the city
- **Area**: Total area
- **Wikipedia URL**: Link to the source page

## Installation

1. Install the required dependencies:
```powershell
pip install -r requirements.txt
```

## Usage

1. Edit `cities.csv` to include the cities you want to extract data for:
```csv
city,country
London,United Kingdom
Paris,France
Berlin,Germany
```

2. Run the script:
```powershell
python extract_city_data.py
```

3. The data will be saved to `cities_data.json` in a structured format.

## Output Format

The script generates a JSON file with the following structure:
```json
[
  {
    "city": "London",
    "country": "United Kingdom",
    "status": "success",
    "wikipedia_url": "https://en.wikipedia.org/wiki/London",
    "population": "8,961,989",
    "metro_population": "14,257,962",
    "population_density": "5,701/km²",
    "area": "1,572 km²",
    "gdp_total": "$978 billion",
    "gdp_per_capita": "$109,190",
    "demographics": "...",
    "economy": "...",
    "industries": ["Finance", "Technology", "Tourism"],
    "demonym": "Londoner"
  }
]
```

## Notes

- The script includes a 1-second delay between requests to be respectful to Wikipedia's servers
- Not all data may be available for every city
- The script uses Wikipedia's API for searching and web scraping for data extraction
