# Dacia Region - Cities Analysis Project

Comprehensive analysis of cities within the historical Dacia border region, covering 9 countries across Central and Eastern Europe.

---

## 📊 STATISTICS REPORT

### Overall Statistics

| Metric | Value |
|--------|-------|
| **Total Cities** | 6,710 |
| **Total Population** | 40,984,505 |
| **Average Population** | 6,107 |
| **Median Population** | 2,239 |
| **Average Elevation** | 179 meters |
| **Maximum Elevation** | 1,183 meters |
| **Cities > 100K** | 42 |
| **Cities > 50K** | 104 |
| **Cities > 10K** | 473 |

---

### Statistics by Country

#### 🇷🇴 Romania (RO)
- **Cities**: 4,296 (64.0% of total)
- **Population**: 19,258,537 (47.0% of total)
- **Average Population**: 4,482
- **Median Population**: 2,137
- **Largest City**: Bucharest (1,877,155)
- **Average Elevation**: 324 meters

#### 🇭🇺 Hungary (HU)
- **Cities**: 941 (14.0% of total)
- **Population**: 9,632,830 (23.5% of total)
- **Average Population**: 10,236
- **Median Population**: 2,992
- **Largest City**: Budapest (1,741,041)
- **Average Elevation**: 124 meters

#### 🇺🇦 Ukraine (UA)
- **Cities**: 837 (12.5% of total)
- **Population**: 4,389,286 (10.7% of total)
- **Average Population**: 5,244
- **Median Population**: 1,831
- **Largest City**: Odesa (1,015,826)
- **Average Elevation**: 178 meters

#### 🇷🇸 Serbia (RS)
- **Cities**: 287 (4.3% of total)
- **Population**: 3,750,853 (9.2% of total)
- **Average Population**: 13,069
- **Median Population**: 2,280
- **Largest City**: Belgrade (1,273,651)
- **Average Elevation**: 202 meters

#### 🇲🇩 Moldova (MD)
- **Cities**: 80 (1.2% of total)
- **Population**: 1,865,898 (4.6% of total)
- **Average Population**: 23,323
- **Median Population**: 9,631
- **Largest City**: Chisinau (635,994)
- **Average Elevation**: 90 meters

#### 🇧🇬 Bulgaria (BG)
- **Cities**: 122 (1.8% of total)
- **Population**: 1,483,824 (3.6% of total)
- **Average Population**: 12,162
- **Median Population**: 3,612
- **Largest City**: Varna (312,770)
- **Average Elevation**: 102 meters

#### 🇸🇰 Slovakia (SK)
- **Cities**: 114 (1.7% of total)
- **Population**: 562,659 (1.4% of total)
- **Average Population**: 4,935
- **Median Population**: 1,911
- **Largest City**: Nitra (86,329)
- **Average Elevation**: 121 meters

#### 🇭🇷 Croatia (HR)
- **Cities**: 28 (0.4% of total)
- **Population**: 34,557 (0.1% of total)
- **Average Population**: 1,234
- **Largest City**: Beli Manastir (6,327)

#### 🇸🇮 Slovenia (SI)
- **Cities**: 5 (0.1% of total)
- **Population**: 6,061 (0.0% of total)
- **Average Population**: 1,212
- **Largest City**: Lendava (3,129)

---

### Top 20 Cities by Population

| Rank | City | Country | Population |
|------|------|---------|------------|
| 1 | Bucharest | RO | 1,877,155 |
| 2 | Budapest | HU | 1,741,041 |
| 3 | Belgrade | RS | 1,273,651 |
| 4 | Odesa | UA | 1,015,826 |
| 5 | Chisinau | MD | 635,994 |
| 6 | Iaşi | RO | 378,954 |
| 7 | Constanţa | RO | 317,832 |
| 8 | Varna | BG | 312,770 |
| 9 | Chernivtsi | UA | 265,471 |
| 10 | Niš | RS | 250,000 |
| 11 | Cluj-Napoca | RO | 243,608 |
| 12 | Ivano-Frankivsk | UA | 238,196 |
| 13 | Novi Sad | RS | 215,400 |
| 14 | Braşov | RO | 215,220 |
| 15 | Timişoara | RO | 213,221 |
| 16 | Craiova | RO | 199,019 |
| 17 | Galaţi | RO | 185,173 |
| 18 | Târgu Mureş | RO | 180,839 |
| 19 | Debrecen | HU | 172,041 |
| 20 | Tiraspol | MD | 157,000 |

---

## 📁 Project Files

### Data Files
- **`dacia_cities_all.csv`** - All 6,710 cities in the Dacia region
- **`dacia_cities_RO.csv`** - 4,296 Romanian cities
- **`dacia_cities_HU.csv`** - 941 Hungarian cities
- **`dacia_cities_UA.csv`** - 837 Ukrainian cities
- **`dacia_cities_RS.csv`** - 287 Serbian cities
- **`dacia_cities_BG.csv`** - 122 Bulgarian cities
- **`dacia_cities_SK.csv`** - 114 Slovakian cities
- **`dacia_cities_MD.csv`** - 80 Moldovan cities
- **`dacia_cities_HR.csv`** - 28 Croatian cities
- **`dacia_cities_SI.csv`** - 5 Slovenian cities

### Visualization Files
- **`pie_cities_by_country.png`** - Pie chart: City distribution by country
- **`pie_population_by_country.png`** - Pie chart: Population distribution by country
- **`bar_cities_by_country.png`** - Bar chart: Number of cities per country
- **`bar_population_by_country.png`** - Bar chart: Total population per country
- **`bar_avg_population_by_country.png`** - Bar chart: Average city population
- **`histogram_population_distribution.png`** - Population size distribution
- **`histogram_elevation_distribution.png`** - Elevation distribution
- **`bar_top_cities.png`** - Top 20 cities by population

### Scripts
- **`filter_dacia_cities.py`** - Filters cities within Dacia border polygon
- **`analyze_dacia_cities.py`** - Generates statistics and visualizations
- **`extract_city_data.py`** - Wikipedia data extractor (optional)

---

## 🚀 Usage

### 1. Filter Cities
```powershell
python filter_dacia_cities.py
```
Filters cities from GeoNames database within the Dacia polygon.

### 2. Generate Statistics and Visualizations
```powershell
python analyze_dacia_cities.py
```
Creates charts, graphs, and comprehensive reports.

### 3. Extract Wikipedia Data (Optional)
```powershell
python extract_city_data.py
```
Extracts demographic and economic data from Wikipedia.

---

## 📦 Installation

```powershell
pip install -r requirements.txt
```

**Requirements:**
- shapely
- matplotlib
- numpy
- requests
- beautifulsoup4

---

## 📝 Data Notes

- **Data Source**: GeoNames cities500 database
- **Population Adjustments**: Romanian and Hungarian cities under 300,000 have populations reduced by 15%
- **Filters Applied**:
  - Excluded Romanian "Sector" administrative divisions
  - Excluded RO/HU cities with population < 1,000
- **Polygon**: Historical Dacia border region

---

## 📄 License

Open source project for historical and demographic analysis.
