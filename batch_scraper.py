#!/usr/bin/env python3
"""
Batch Business Lead Scraper
Process multiple search queries from a CSV file
"""

import csv
import json
import os
import sys
import argparse
from datetime import datetime
from typing import List, Dict
import logging
from business_lead_scraper import GoogleMapsScraper, YelpScraper, DataExporter, BusinessLead

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BatchScraper:
    """Batch processor for multiple scraping queries"""
    
    def __init__(self, headless=True, max_results_per_query=50):
        self.headless = headless
        self.max_results_per_query = max_results_per_query
        self.results = {}
        
    def load_queries_from_csv(self, filename: str) -> List[Dict]:
        """Load search queries from CSV file"""
        queries = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Validate required columns
                required_columns = ['keyword', 'location']
                if not all(col in reader.fieldnames for col in required_columns):
                    raise ValueError(f"CSV must contain columns: {required_columns}")
                
                for row in reader:
                    if row['keyword'].strip() and row['location'].strip():
                        query = {
                            'keyword': row['keyword'].strip(),
                            'location': row['location'].strip(),
                            'source': row.get('source', 'both').strip(),
                            'max_results': int(row.get('max_results', self.max_results_per_query))
                        }
                        queries.append(query)
                
                logger.info(f"Loaded {len(queries)} queries from {filename}")
                
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
            raise
        except Exception as e:
            logger.error(f"Error loading queries from CSV: {e}")
            raise
        
        return queries
    
    def create_sample_queries_csv(self, filename: str):
        """Create a sample queries CSV file"""
        sample_queries = [
            {'keyword': 'restaurant', 'location': 'New York', 'source': 'both', 'max_results': 20},
            {'keyword': 'pizza', 'location': 'Chicago', 'source': 'google', 'max_results': 15},
            {'keyword': 'coffee shop', 'location': 'San Francisco', 'source': 'yelp', 'max_results': 25},
            {'keyword': 'plumber', 'location': 'Los Angeles', 'source': 'both', 'max_results': 30},
            {'keyword': 'dentist', 'location': 'Miami', 'source': 'google', 'max_results': 10}
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['keyword', 'location', 'source', 'max_results']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(sample_queries)
        
        logger.info(f"Sample queries CSV created: {filename}")
    
    def process_queries(self, queries: List[Dict]) -> Dict:
        """Process multiple search queries"""
        all_results = {}
        
        for i, query in enumerate(queries, 1):
            query_id = f"{query['keyword']}_{query['location']}"
            logger.info(f"Processing query {i}/{len(queries)}: {query_id}")
            
            try:
                leads = self.scrape_single_query(query)
                all_results[query_id] = {
                    'query': query,
                    'leads': leads,
                    'count': len(leads)
                }
                
                logger.info(f"Query {i} completed: {len(leads)} leads found")
                
            except Exception as e:
                logger.error(f"Error processing query {i} ({query_id}): {e}")
                all_results[query_id] = {
                    'query': query,
                    'leads': [],
                    'count': 0,
                    'error': str(e)
                }
        
        return all_results
    
    def scrape_single_query(self, query: Dict) -> List[BusinessLead]:
        """Scrape a single query"""
        all_leads = []
        
        # Scrape from Google Maps
        if query['source'] in ['google', 'both']:
            logger.info(f"Scraping Google Maps for: {query['keyword']} in {query['location']}")
            
            scraper = GoogleMapsScraper(headless=self.headless)
            try:
                leads = scraper.search_businesses(
                    query['keyword'], 
                    query['location'], 
                    query['max_results']
                )
                all_leads.extend(leads)
                logger.info(f"Google Maps: {len(leads)} leads")
                
            finally:
                scraper.close()
        
        # Scrape from Yelp
        if query['source'] in ['yelp', 'both']:
            logger.info(f"Scraping Yelp for: {query['keyword']} in {query['location']}")
            
            scraper = YelpScraper(headless=self.headless)
            try:
                leads = scraper.search_businesses(
                    query['keyword'], 
                    query['location'], 
                    query['max_results']
                )
                all_leads.extend(leads)
                logger.info(f"Yelp: {len(leads)} leads")
                
            finally:
                scraper.close()
        
        # Remove duplicates
        seen = set()
        unique_leads = []
        for lead in all_leads:
            identifier = f"{lead.name}|{lead.address}"
            if identifier not in seen:
                seen.add(identifier)
                unique_leads.append(lead)
        
        return unique_leads
    
    def export_results(self, results: Dict, output_dir: str, format_type: str = 'both'):
        """Export batch results"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export individual query results
        for query_id, result in results.items():
            if result['leads']:
                base_filename = f"{query_id}_{timestamp}"
                
                if format_type in ['csv', 'both']:
                    csv_filename = os.path.join(output_dir, f"{base_filename}.csv")
                    DataExporter.to_csv(result['leads'], csv_filename)
                
                if format_type in ['json', 'both']:
                    json_filename = os.path.join(output_dir, f"{base_filename}.json")
                    DataExporter.to_json(result['leads'], json_filename)
        
        # Export summary report
        self.export_summary_report(results, output_dir, timestamp)
        
        # Export combined results
        self.export_combined_results(results, output_dir, timestamp, format_type)
    
    def export_summary_report(self, results: Dict, output_dir: str, timestamp: str):
        """Export a summary report of all queries"""
        summary_filename = os.path.join(output_dir, f"batch_summary_{timestamp}.csv")
        
        with open(summary_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['query_id', 'keyword', 'location', 'source', 'leads_found', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for query_id, result in results.items():
                writer.writerow({
                    'query_id': query_id,
                    'keyword': result['query']['keyword'],
                    'location': result['query']['location'],
                    'source': result['query']['source'],
                    'leads_found': result['count'],
                    'status': 'Error' if 'error' in result else 'Success'
                })
        
        logger.info(f"Summary report exported: {summary_filename}")
    
    def export_combined_results(self, results: Dict, output_dir: str, timestamp: str, format_type: str):
        """Export all results combined into single files"""
        all_leads = []
        
        for result in results.values():
            all_leads.extend(result['leads'])
        
        if all_leads:
            # Remove duplicates across all queries
            seen = set()
            unique_leads = []
            for lead in all_leads:
                identifier = f"{lead.name}|{lead.address}"
                if identifier not in seen:
                    seen.add(identifier)
                    unique_leads.append(lead)
            
            base_filename = f"batch_combined_{timestamp}"
            
            if format_type in ['csv', 'both']:
                csv_filename = os.path.join(output_dir, f"{base_filename}.csv")
                DataExporter.to_csv(unique_leads, csv_filename)
            
            if format_type in ['json', 'both']:
                json_filename = os.path.join(output_dir, f"{base_filename}.json")
                DataExporter.to_json(unique_leads, json_filename)
            
            logger.info(f"Combined results exported: {len(unique_leads)} unique leads")

def main():
    """Main function for batch scraper"""
    parser = argparse.ArgumentParser(description='Batch Business Lead Scraper')
    parser.add_argument('--queries-file', required=True, 
                       help='CSV file containing search queries')
    parser.add_argument('--output-dir', default='./batch_output', 
                       help='Output directory (default: ./batch_output)')
    parser.add_argument('--format', choices=['csv', 'json', 'both'], default='both',
                       help='Output format (default: both)')
    parser.add_argument('--max-results', type=int, default=50,
                       help='Default max results per query (default: 50)')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode (default: True)')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create a sample queries CSV file')
    
    args = parser.parse_args()
    
    # Create sample file if requested
    if args.create_sample:
        sample_filename = 'sample_queries.csv'
        batch_scraper = BatchScraper()
        batch_scraper.create_sample_queries_csv(sample_filename)
        print(f"Sample queries file created: {sample_filename}")
        print("Edit this file with your search queries and run:")
        print(f"python batch_scraper.py --queries-file {sample_filename}")
        return
    
    # Validate queries file
    if not os.path.exists(args.queries_file):
        logger.error(f"Queries file not found: {args.queries_file}")
        sys.exit(1)
    
    try:
        # Initialize batch scraper
        batch_scraper = BatchScraper(
            headless=args.headless,
            max_results_per_query=args.max_results
        )
        
        # Load queries
        queries = batch_scraper.load_queries_from_csv(args.queries_file)
        
        if not queries:
            logger.error("No valid queries found in the CSV file")
            sys.exit(1)
        
        logger.info(f"Starting batch processing of {len(queries)} queries...")
        
        # Process queries
        results = batch_scraper.process_queries(queries)
        
        # Export results
        batch_scraper.export_results(results, args.output_dir, args.format)
        
        # Print summary
        total_leads = sum(result['count'] for result in results.values())
        successful_queries = sum(1 for result in results.values() if 'error' not in result)
        
        logger.info("Batch processing completed!")
        logger.info(f"Processed queries: {len(queries)}")
        logger.info(f"Successful queries: {successful_queries}")
        logger.info(f"Total leads found: {total_leads}")
        logger.info(f"Results saved to: {args.output_dir}")
        
    except KeyboardInterrupt:
        logger.info("Batch processing interrupted by user")
    except Exception as e:
        logger.error(f"Error during batch processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
