#!/usr/bin/env python3
"""
Example usage of the Business Lead Scraper
Demonstrates different ways to use the scraper programmatically
"""

import os
import sys
from datetime import datetime
from business_lead_scraper import GoogleMapsScraper, YelpScraper, DataExporter, BusinessLead

def example_basic_scraping():
    """Basic example of scraping business leads"""
    print("Example 1: Basic Scraping")
    print("-" * 30)
    
    # Initialize scraper
    scraper = GoogleMapsScraper(headless=True)
    
    try:
        # Search for restaurants in New York
        leads = scraper.search_businesses(
            keyword="restaurant",
            location="New York",
            max_results=10
        )
        
        print(f"Found {len(leads)} leads:")
        for i, lead in enumerate(leads[:5], 1):  # Show first 5
            print(f"{i}. {lead.name}")
            print(f"   Address: {lead.address}")
            print(f"   Phone: {lead.phone}")
            print(f"   Rating: {lead.rating}")
            print()
        
        # Export to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"example_restaurants_{timestamp}.csv"
        DataExporter.to_csv(leads, filename)
        print(f"Results exported to {filename}")
        
    finally:
        scraper.close()

def example_multi_source_scraping():
    """Example of scraping from multiple sources"""
    print("\nExample 2: Multi-Source Scraping")
    print("-" * 35)
    
    all_leads = []
    
    # Scrape from Google Maps
    print("Scraping Google Maps...")
    google_scraper = GoogleMapsScraper(headless=True)
    try:
        google_leads = google_scraper.search_businesses("coffee shop", "San Francisco", 5)
        all_leads.extend(google_leads)
        print(f"Google Maps: {len(google_leads)} leads")
    finally:
        google_scraper.close()
    
    # Scrape from Yelp
    print("Scraping Yelp...")
    yelp_scraper = YelpScraper(headless=True)
    try:
        yelp_leads = yelp_scraper.search_businesses("coffee shop", "San Francisco", 5)
        all_leads.extend(yelp_leads)
        print(f"Yelp: {len(yelp_leads)} leads")
    finally:
        yelp_scraper.close()
    
    # Remove duplicates
    seen = set()
    unique_leads = []
    for lead in all_leads:
        identifier = f"{lead.name}|{lead.address}"
        if identifier not in seen:
            seen.add(identifier)
            unique_leads.append(lead)
    
    print(f"Total unique leads: {len(unique_leads)}")
    
    # Export results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    DataExporter.to_json(unique_leads, f"multi_source_coffee_{timestamp}.json")

def example_custom_data_processing():
    """Example of custom data processing"""
    print("\nExample 3: Custom Data Processing")
    print("-" * 37)
    
    # Create some sample leads
    sample_leads = [
        BusinessLead(
            name="Joe's Pizza",
            address="123 Main St, New York, NY",
            phone="(555) 123-4567",
            website="https://joespizza.com",
            source="Google Maps",
            rating="4.5",
            review_count="150"
        ),
        BusinessLead(
            name="Maria's Tacos",
            address="456 Oak Ave, Los Angeles, CA",
            phone="(555) 987-6543",
            website="https://mariastacos.com",
            source="Yelp",
            rating="4.8",
            review_count="89"
        )
    ]
    
    # Filter leads by rating
    high_rated = [lead for lead in sample_leads if lead.rating and float(lead.rating) >= 4.5]
    print(f"High-rated businesses (4.5+): {len(high_rated)}")
    
    # Group by source
    by_source = {}
    for lead in sample_leads:
        if lead.source not in by_source:
            by_source[lead.source] = []
        by_source[lead.source].append(lead)
    
    for source, leads in by_source.items():
        print(f"{source}: {len(leads)} leads")
    
    # Export filtered results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    DataExporter.to_csv(high_rated, f"high_rated_businesses_{timestamp}.csv")

def example_error_handling():
    """Example of proper error handling"""
    print("\nExample 4: Error Handling")
    print("-" * 26)
    
    scraper = None
    try:
        scraper = GoogleMapsScraper(headless=True)
        
        # Try to scrape with invalid parameters
        leads = scraper.search_businesses("", "", 5)  # Empty search terms
        
        if not leads:
            print("No leads found - this is expected with empty search terms")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        print("This demonstrates proper error handling")
    
    finally:
        if scraper:
            scraper.close()
            print("Scraper closed properly")

def example_batch_processing():
    """Example of processing multiple search queries"""
    print("\nExample 5: Batch Processing")
    print("-" * 28)
    
    # Define multiple search queries
    search_queries = [
        ("pizza", "Chicago"),
        ("sushi", "Los Angeles"),
        ("coffee", "Seattle")
    ]
    
    all_results = {}
    
    scraper = GoogleMapsScraper(headless=True)
    try:
        for keyword, location in search_queries:
            print(f"Searching for {keyword} in {location}...")
            
            leads = scraper.search_businesses(keyword, location, 3)
            all_results[f"{keyword}_{location}"] = leads
            
            print(f"Found {len(leads)} leads for {keyword} in {location}")
    
    finally:
        scraper.close()
    
    # Export all results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for query_name, leads in all_results.items():
        filename = f"batch_{query_name}_{timestamp}.csv"
        DataExporter.to_csv(leads, filename)
        print(f"Exported {query_name} to {filename}")

def main():
    """Run all examples"""
    print("Business Lead Scraper - Usage Examples")
    print("=" * 40)
    
    # Create output directory
    os.makedirs("examples_output", exist_ok=True)
    os.chdir("examples_output")
    
    try:
        # Run examples
        example_basic_scraping()
        example_multi_source_scraping()
        example_custom_data_processing()
        example_error_handling()
        example_batch_processing()
        
        print("\n" + "=" * 40)
        print("All examples completed successfully!")
        print("Check the 'examples_output' directory for generated files.")
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"\nError running examples: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
