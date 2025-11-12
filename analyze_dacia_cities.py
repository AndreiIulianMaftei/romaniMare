"""
Analyze Dacia Cities Data and Generate Statistics and Visualizations
Creates pie charts, bar charts, and comprehensive statistics reports
"""

import csv
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from collections import defaultdict
import json

# Use a non-interactive backend for saving figures
matplotlib.use('Agg')

class DaciaCitiesAnalyzer:
    """Analyze and visualize Dacia cities data"""
    
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.cities = []
        self.stats = {}
        
    def load_data(self):
        """Load cities data from CSV"""
        print(f"Loading data from {self.csv_file}...")
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                try:
                    row['population'] = int(row['population']) if row['population'] else 0
                    row['latitude'] = float(row['latitude'])
                    row['longitude'] = float(row['longitude'])
                    row['elevation'] = int(row['elevation']) if row['elevation'] else 0
                except (ValueError, KeyError):
                    continue
                
                self.cities.append(row)
        
        print(f"Loaded {len(self.cities):,} cities")
        
    def calculate_statistics(self):
        """Calculate comprehensive statistics"""
        print("\nCalculating statistics...")
        
        # Group by country
        by_country = defaultdict(list)
        for city in self.cities:
            by_country[city['country_code']].append(city)
        
        # Calculate statistics
        self.stats = {
            'total_cities': len(self.cities),
            'total_population': sum(c['population'] for c in self.cities),
            'countries': {}
        }
        
        # Country-level statistics
        for country, cities in by_country.items():
            populations = [c['population'] for c in cities]
            elevations = [c['elevation'] for c in cities if c['elevation'] > 0]
            
            self.stats['countries'][country] = {
                'city_count': len(cities),
                'total_population': sum(populations),
                'avg_population': int(np.mean(populations)) if populations else 0,
                'median_population': int(np.median(populations)) if populations else 0,
                'max_population': max(populations) if populations else 0,
                'min_population': min(populations) if populations else 0,
                'avg_elevation': int(np.mean(elevations)) if elevations else 0,
                'max_elevation': max(elevations) if elevations else 0,
                'largest_city': max(cities, key=lambda x: x['population'])['name'] if cities else 'N/A'
            }
        
        # Overall statistics
        all_populations = [c['population'] for c in self.cities]
        all_elevations = [c['elevation'] for c in self.cities if c['elevation'] > 0]
        
        self.stats['overall'] = {
            'avg_population': int(np.mean(all_populations)) if all_populations else 0,
            'median_population': int(np.median(all_populations)) if all_populations else 0,
            'avg_elevation': int(np.mean(all_elevations)) if all_elevations else 0,
            'max_elevation': max(all_elevations) if all_elevations else 0,
            'cities_over_100k': sum(1 for c in self.cities if c['population'] > 100000),
            'cities_over_50k': sum(1 for c in self.cities if c['population'] > 50000),
            'cities_over_10k': sum(1 for c in self.cities if c['population'] > 10000),
        }
        
        return self.stats
    
    def create_pie_chart_cities_by_country(self, output_file='pie_cities_by_country.png'):
        """Create pie chart of cities distribution by country"""
        print(f"Creating pie chart: {output_file}")
        
        # Count cities by country
        country_counts = {}
        for country, data in self.stats['countries'].items():
            country_counts[country] = data['city_count']
        
        # Sort by count
        sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
        labels = [f"{c[0]} ({c[1]:,})" for c in sorted_countries]
        sizes = [c[1] for c in sorted_countries]
        
        # Create color palette
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        
        # Create pie chart
        plt.figure(figsize=(12, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        plt.title('Distribution of Cities by Country\nDacia Region', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved: {output_file}")
    
    def create_pie_chart_population_by_country(self, output_file='pie_population_by_country.png'):
        """Create pie chart of population distribution by country"""
        print(f"Creating pie chart: {output_file}")
        
        # Get population by country
        country_pops = {}
        for country, data in self.stats['countries'].items():
            country_pops[country] = data['total_population']
        
        # Sort by population
        sorted_countries = sorted(country_pops.items(), key=lambda x: x[1], reverse=True)
        labels = [f"{c[0]} ({c[1]:,})" for c in sorted_countries]
        sizes = [c[1] for c in sorted_countries]
        
        # Create color palette
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(labels)))
        
        # Create pie chart
        plt.figure(figsize=(12, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        plt.title('Distribution of Total Population by Country\nDacia Region', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved: {output_file}")
    
    def create_bar_chart_cities_by_country(self, output_file='bar_cities_by_country.png'):
        """Create bar chart of cities by country"""
        print(f"Creating bar chart: {output_file}")
        
        # Get data
        country_counts = {c: d['city_count'] for c, d in self.stats['countries'].items()}
        sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
        
        countries = [c[0] for c in sorted_countries]
        counts = [c[1] for c in sorted_countries]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(countries, counts, color=plt.cm.Set2(np.linspace(0, 1, len(countries))))
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Country', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Cities', fontsize=12, fontweight='bold')
        plt.title('Number of Cities by Country - Dacia Region', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved: {output_file}")
    
    def create_bar_chart_population_by_country(self, output_file='bar_population_by_country.png'):
        """Create bar chart of total population by country"""
        print(f"Creating bar chart: {output_file}")
        
        # Get data
        country_pops = {c: d['total_population'] for c, d in self.stats['countries'].items()}
        sorted_countries = sorted(country_pops.items(), key=lambda x: x[1], reverse=True)
        
        countries = [c[0] for c in sorted_countries]
        pops = [c[1] for c in sorted_countries]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(countries, pops, color=plt.cm.Spectral(np.linspace(0, 1, len(countries))))
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.xlabel('Country', fontsize=12, fontweight='bold')
        plt.ylabel('Total Population', fontsize=12, fontweight='bold')
        plt.title('Total Population by Country - Dacia Region', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved: {output_file}")
    
    def create_population_size_distribution(self, output_file='histogram_population_distribution.png'):
        """Create histogram of population size distribution"""
        print(f"Creating histogram: {output_file}")
        
        # Define population categories
        categories = {
            '< 1K': (0, 1000),
            '1K-5K': (1000, 5000),
            '5K-10K': (5000, 10000),
            '10K-50K': (10000, 50000),
            '50K-100K': (50000, 100000),
            '100K-500K': (100000, 500000),
            '500K+': (500000, float('inf'))
        }
        
        # Count cities in each category
        counts = {}
        for label, (min_pop, max_pop) in categories.items():
            counts[label] = sum(1 for c in self.cities if min_pop <= c['population'] < max_pop)
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        labels = list(counts.keys())
        values = list(counts.values())
        
        bars = plt.bar(labels, values, color=plt.cm.viridis(np.linspace(0, 1, len(labels))))
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Population Range', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Cities', fontsize=12, fontweight='bold')
        plt.title('Cities by Population Size - Dacia Region', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved: {output_file}")
    
    def create_elevation_distribution(self, output_file='histogram_elevation_distribution.png'):
        """Create histogram of elevation distribution"""
        print(f"Creating histogram: {output_file}")
        
        # Get elevations (filter out 0 values)
        elevations = [c['elevation'] for c in self.cities if c['elevation'] > 0]
        
        if not elevations:
            print("  Skipped: No elevation data available")
            return
        
        # Create histogram
        plt.figure(figsize=(12, 6))
        plt.hist(elevations, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        
        plt.xlabel('Elevation (meters)', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Cities', fontsize=12, fontweight='bold')
        plt.title('Elevation Distribution - Dacia Region', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved: {output_file}")
    
    def create_top_cities_chart(self, top_n=20, output_file='bar_top_cities.png'):
        """Create bar chart of top N cities by population"""
        print(f"Creating bar chart: {output_file}")
        
        # Get top cities
        top_cities = sorted(self.cities, key=lambda x: x['population'], reverse=True)[:top_n]
        
        # Prepare data
        names = [f"{c['name']} ({c['country_code']})" for c in top_cities]
        pops = [c['population'] for c in top_cities]
        
        # Create horizontal bar chart
        plt.figure(figsize=(12, 10))
        y_pos = np.arange(len(names))
        
        colors = plt.cm.rainbow(np.linspace(0, 1, len(names)))
        bars = plt.barh(y_pos, pops, color=colors)
        
        # Add value labels
        for i, (bar, pop) in enumerate(zip(bars, pops)):
            plt.text(pop, i, f' {pop:,}', va='center', fontweight='bold')
        
        plt.yticks(y_pos, names)
        plt.xlabel('Population', fontsize=12, fontweight='bold')
        plt.title(f'Top {top_n} Cities by Population - Dacia Region', fontsize=14, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved: {output_file}")
    
    def create_avg_population_by_country(self, output_file='bar_avg_population_by_country.png'):
        """Create bar chart of average population by country"""
        print(f"Creating bar chart: {output_file}")
        
        # Get data
        country_avg_pops = {c: d['avg_population'] for c, d in self.stats['countries'].items()}
        sorted_countries = sorted(country_avg_pops.items(), key=lambda x: x[1], reverse=True)
        
        countries = [c[0] for c in sorted_countries]
        avg_pops = [c[1] for c in sorted_countries]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(countries, avg_pops, color=plt.cm.coolwarm(np.linspace(0, 1, len(countries))))
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Country', fontsize=12, fontweight='bold')
        plt.ylabel('Average Population per City', fontsize=12, fontweight='bold')
        plt.title('Average City Population by Country - Dacia Region', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved: {output_file}")
    
    def save_statistics_report(self, output_file='statistics_report.txt'):
        """Save comprehensive statistics report to text file"""
        print(f"\nSaving statistics report: {output_file}")
        
        report = []
        report.append("="*80)
        report.append("DACIA REGION CITIES - COMPREHENSIVE STATISTICS REPORT")
        report.append("="*80)
        report.append("")
        
        # Overall statistics
        report.append("-"*80)
        report.append("OVERALL STATISTICS")
        report.append("-"*80)
        report.append(f"Total Cities:              {self.stats['total_cities']:,}")
        report.append(f"Total Population:          {self.stats['total_population']:,}")
        report.append(f"Average Population:        {self.stats['overall']['avg_population']:,}")
        report.append(f"Median Population:         {self.stats['overall']['median_population']:,}")
        report.append(f"Average Elevation:         {self.stats['overall']['avg_elevation']:,} meters")
        report.append(f"Maximum Elevation:         {self.stats['overall']['max_elevation']:,} meters")
        report.append(f"Cities > 100K population:  {self.stats['overall']['cities_over_100k']:,}")
        report.append(f"Cities > 50K population:   {self.stats['overall']['cities_over_50k']:,}")
        report.append(f"Cities > 10K population:   {self.stats['overall']['cities_over_10k']:,}")
        report.append("")
        
        # Country statistics
        report.append("-"*80)
        report.append("STATISTICS BY COUNTRY")
        report.append("-"*80)
        
        sorted_countries = sorted(self.stats['countries'].items(), 
                                 key=lambda x: x[1]['total_population'], 
                                 reverse=True)
        
        for country, data in sorted_countries:
            report.append("")
            report.append(f"Country: {country}")
            report.append(f"  Number of Cities:        {data['city_count']:,}")
            report.append(f"  Total Population:        {data['total_population']:,}")
            report.append(f"  Average Population:      {data['avg_population']:,}")
            report.append(f"  Median Population:       {data['median_population']:,}")
            report.append(f"  Max Population:          {data['max_population']:,}")
            report.append(f"  Min Population:          {data['min_population']:,}")
            report.append(f"  Average Elevation:       {data['avg_elevation']:,} meters")
            report.append(f"  Max Elevation:           {data['max_elevation']:,} meters")
            report.append(f"  Largest City:            {data['largest_city']}")
            
            # Calculate percentage
            pct_cities = (data['city_count'] / self.stats['total_cities']) * 100
            pct_pop = (data['total_population'] / self.stats['total_population']) * 100
            report.append(f"  % of Total Cities:       {pct_cities:.1f}%")
            report.append(f"  % of Total Population:   {pct_pop:.1f}%")
        
        report.append("")
        report.append("="*80)
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"  Saved: {output_file}")
        
        # Also print to console
        print('\n'.join(report))
    
    def save_statistics_json(self, output_file='statistics.json'):
        """Save statistics as JSON"""
        print(f"\nSaving statistics JSON: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"  Saved: {output_file}")
    
    def generate_all_visualizations(self):
        """Generate all visualizations and reports"""
        print("\n" + "="*80)
        print("GENERATING VISUALIZATIONS AND REPORTS")
        print("="*80)
        
        # Create visualizations
        self.create_pie_chart_cities_by_country()
        self.create_pie_chart_population_by_country()
        self.create_bar_chart_cities_by_country()
        self.create_bar_chart_population_by_country()
        self.create_avg_population_by_country()
        self.create_population_size_distribution()
        self.create_elevation_distribution()
        self.create_top_cities_chart(top_n=20)
        
        # Create reports
        self.save_statistics_report()
        self.save_statistics_json()
        
        print("\n" + "="*80)
        print("ALL VISUALIZATIONS AND REPORTS COMPLETED")
        print("="*80)


def main():
    """Main function"""
    print("="*80)
    print("DACIA CITIES DATA ANALYZER")
    print("="*80)
    
    # Input file
    csv_file = 'dacia_cities_all.csv'
    
    # Create analyzer
    analyzer = DaciaCitiesAnalyzer(csv_file)
    
    # Load data
    analyzer.load_data()
    
    # Calculate statistics
    analyzer.calculate_statistics()
    
    # Generate all visualizations and reports
    analyzer.generate_all_visualizations()


if __name__ == '__main__':
    main()
