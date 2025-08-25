#!/usr/bin/env python3
"""
Demo script for Business Lead Scraper
Demonstrates all features and capabilities
"""

import os
import sys
import time
from datetime import datetime
from business_lead_scraper import GoogleMapsScraper, YelpScraper, DataExporter, BusinessLead

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{title}")
    print("-" * len(title))

def demo_basic_scraping():
    """Demonstrate basic scraping functionality"""
    print_header("DEMO: Basic Business Lead Scraping")
    
    print("This demo will scrape a few business leads to show the basic functionality.")
    print("We'll search for 'coffee shop' in 'San Francisco' using Google Maps.")
    
    input("\nPress Enter to continue...")
    
    # Initialize scraper
    print("\n1. Initializing Google Maps scraper...")
    scraper = GoogleMapsScraper(headless=True)
    
    try:
        # Search for businesses
        print("2. Searching for coffee shops in San Francisco...")
        leads = scraper.search_businesses("coffee shop", "San Francisco", 5)
        
        print(f"3. Found {len(leads)} business leads:")
        
        # Display results
        for i, lead in enumerate(leads, 1):
            print(f"\n   Lead {i}:")
            print(f"   Name: {lead.name}")
            print(f"   Address: {lead.address}")
            print(f"   Phone: {lead.phone}")
            print(f"   Website: {lead.website}")
            print(f"   Rating: {lead.rating}")
            print(f"   Source: {lead.source}")
        
        # Export results
        if leads:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"demo_coffee_shops_{timestamp}.csv"
            DataExporter.to_csv(leads, filename)
            print(f"\n4. Results exported to: {filename}")
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    
    finally:
        scraper.close()
        print("5. Scraper closed successfully")

def demo_data_structures():
    """Demonstrate data structures and export formats"""
    print_header("DEMO: Data Structures and Export Formats")
    
    # Create sample data
    sample_leads = [
        BusinessLead(
            name="Joe's Pizza Palace",
            address="123 Main Street, New York, NY 10001",
            phone="(555) 123-4567",
            website="https://joespizza.com",
            email="info@joespizza.com",
            source="Google Maps",
            rating="4.5",
            review_count="234 reviews"
        ),
        BusinessLead(
            name="Maria's Authentic Tacos",
            address="456 Oak Avenue, Los Angeles, CA 90210",
            phone="(555) 987-6543",
            website="https://mariastacos.com",
            source="Yelp",
            rating="4.8",
            review_count="89 reviews"
        ),
        BusinessLead(
            name="Seattle Coffee Roasters",
            address="789 Pine Street, Seattle, WA 98101",
            phone="(555) 555-0123",
            website="https://seattlecoffee.com",
            source="Google Maps",
            rating="4.2",
            review_count="156 reviews"
        )
    ]
    
    print("Sample business leads created:")
    for i, lead in enumerate(sample_leads, 1):
        print(f"\n{i}. {lead.name}")
        print(f"   Location: {lead.address}")
        print(f"   Contact: {lead.phone}")
        print(f"   Rating: {lead.rating} ({lead.review_count})")
    
    # Export to different formats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print_section("Exporting to CSV format")
    csv_filename = f"demo_sample_leads_{timestamp}.csv"
    DataExporter.to_csv(sample_leads, csv_filename)
    print(f"✓ CSV exported: {csv_filename}")
    
    print_section("Exporting to JSON format")
    json_filename = f"demo_sample_leads_{timestamp}.json"
    DataExporter.to_json(sample_leads, json_filename)
    print(f"✓ JSON exported: {json_filename}")
    
    # Show file contents
    print_section("CSV file preview")
    try:
        with open(csv_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:4]  # Show first 4 lines
            for line in lines:
                print(f"   {line.strip()}")
            if len(lines) == 4:
                print("   ...")
    except Exception as e:
        print(f"Error reading CSV: {e}")

def demo_configuration():
    """Demonstrate configuration options"""
    print_header("DEMO: Configuration and Customization")
    
    try:
        from config import get_config, update_config
        
        print("Loading default configuration...")
        config = get_config()
        
        print_section("Browser Configuration")
        browser_config = config['browser']
        for key, value in browser_config.items():
            print(f"   {key}: {value}")
        
        print_section("Rate Limiting Configuration")
        rate_config = config['rate_limit']
        for key, value in rate_config.items():
            print(f"   {key}: {value}")
        
        print_section("Output Configuration")
        output_config = config['output']
        for key, value in output_config.items():
            print(f"   {key}: {value}")
        
        print_section("Customizing Configuration")
        custom_config = update_config(
            browser={'headless': False, 'window_size': '1280x720'},
            rate_limit={'min_delay': 2, 'max_delay': 5}
        )
        
        print("Updated browser settings:")
        for key, value in custom_config['browser'].items():
            print(f"   {key}: {value}")
        
        print("Updated rate limiting:")
        for key, value in custom_config['rate_limit'].items():
            print(f"   {key}: {value}")
        
    except ImportError:
        print("Configuration module not available")

def demo_error_handling():
    """Demonstrate error handling capabilities"""
    print_header("DEMO: Error Handling and Robustness")
    
    print("Testing error handling with invalid inputs...")
    
    # Test with empty search terms
    print_section("Test 1: Empty search terms")
    scraper = GoogleMapsScraper(headless=True)
    try:
        leads = scraper.search_businesses("", "", 5)
        print(f"Result: {len(leads)} leads found (expected: 0)")
    except Exception as e:
        print(f"Handled error: {e}")
    finally:
        scraper.close()
    
    # Test with invalid data export
    print_section("Test 2: Export with empty data")
    try:
        empty_leads = []
        DataExporter.to_csv(empty_leads, "test_empty.csv")
        print("✓ Empty data export handled successfully")
        
        # Check if file was created
        if os.path.exists("test_empty.csv"):
            with open("test_empty.csv", 'r') as f:
                content = f.read()
                print(f"   File content: {len(content)} characters")
            os.remove("test_empty.csv")  # Cleanup
    except Exception as e:
        print(f"Export error handled: {e}")
    
    # Test data validation
    print_section("Test 3: Data validation")
    try:
        # Create lead with minimal data
        minimal_lead = BusinessLead(name="Test Business", address="", phone="")
        leads = [minimal_lead]
        
        DataExporter.to_csv(leads, "test_minimal.csv")
        print("✓ Minimal data export successful")
        
        if os.path.exists("test_minimal.csv"):
            os.remove("test_minimal.csv")  # Cleanup
            
    except Exception as e:
        print(f"Validation error: {e}")

def demo_batch_processing():
    """Demonstrate batch processing capabilities"""
    print_header("DEMO: Batch Processing")
    
    print("Creating sample batch queries...")
    
    # Create sample queries
    sample_queries = [
        {"keyword": "pizza", "location": "New York", "max_results": 3},
        {"keyword": "sushi", "location": "Los Angeles", "max_results": 3},
        {"keyword": "coffee", "location": "Seattle", "max_results": 3}
    ]
    
    print("Sample queries:")
    for i, query in enumerate(sample_queries, 1):
        print(f"   {i}. {query['keyword']} in {query['location']} (max: {query['max_results']})")
    
    print("\nNote: In a real batch process, these would be loaded from a CSV file")
    print("and processed using the batch_scraper.py script:")
    print("\n   python batch_scraper.py --queries-file queries.csv")
    
    # Show what the CSV would look like
    print_section("Sample batch queries CSV format")
    print("keyword,location,source,max_results")
    for query in sample_queries:
        print(f"{query['keyword']},{query['location']},both,{query['max_results']}")

def demo_gui_features():
    """Demonstrate GUI features"""
    print_header("DEMO: Graphical User Interface")
    
    print("The GUI version provides:")
    print("   • Easy-to-use interface")
    print("   • Real-time progress tracking")
    print("   • Live results display")
    print("   • One-click CSV export")
    print("   • Configurable search options")
    
    print("\nTo start the GUI:")
    print("   python gui_scraper.py")
    
    print("\nGUI Features:")
    print("   1. Input fields for keyword and location")
    print("   2. Source selection (Google Maps, Yelp, or both)")
    print("   3. Maximum results configuration")
    print("   4. Progress bar and status updates")
    print("   5. Results table with live updates")
    print("   6. Export button for saving results")
    print("   7. Clear button for resetting")

def demo_summary():
    """Show demo summary and next steps"""
    print_header("DEMO COMPLETE - Summary and Next Steps")
    
    print("This demo has shown:")
    print("   ✓ Basic scraping functionality")
    print("   ✓ Data structures and export formats")
    print("   ✓ Configuration options")
    print("   ✓ Error handling capabilities")
    print("   ✓ Batch processing overview")
    print("   ✓ GUI features overview")
    
    print_section("Files created during this demo")
    demo_files = [f for f in os.listdir('.') if f.startswith('demo_')]
    if demo_files:
        for file in demo_files:
            print(f"   • {file}")
    else:
        print("   No demo files found")
    
    print_section("Next steps")
    print("1. Try the command-line interface:")
    print('   python business_lead_scraper.py --keyword "restaurant" --location "your city"')
    
    print("\n2. Start the GUI application:")
    print("   python gui_scraper.py")
    
    print("\n3. Run batch processing:")
    print("   python batch_scraper.py --create-sample")
    print("   python batch_scraper.py --queries-file sample_queries.csv")
    
    print("\n4. Explore the examples:")
    print("   python example_usage.py")
    
    print("\n5. Run tests to verify everything works:")
    print("   python test_scraper.py")
    
    print_section("Documentation")
    print("• README.md - Main documentation")
    print("• INSTALL.md - Installation guide")
    print("• config.py - Configuration options")

def main():
    """Main demo function"""
    print_header("Business Lead Scraper - Interactive Demo")
    
    print("Welcome to the Business Lead Scraper demo!")
    print("This interactive demo will show you all the features and capabilities.")
    print("\nNote: This demo will perform actual web scraping, so it requires:")
    print("• Internet connection")
    print("• Chrome browser installed")
    print("• All dependencies installed (run 'python setup.py' if needed)")
    
    # Check if user wants to continue
    response = input("\nDo you want to continue with the demo? (y/n): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Demo cancelled. Run 'python demo.py' anytime to try again.")
        return
    
    # Create demo output directory
    demo_dir = f"demo_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(demo_dir, exist_ok=True)
    os.chdir(demo_dir)
    print(f"\nDemo files will be saved to: {demo_dir}")
    
    try:
        # Run demo sections
        demo_basic_scraping()
        
        input("\nPress Enter to continue to the next demo...")
        demo_data_structures()
        
        input("\nPress Enter to continue to the next demo...")
        demo_configuration()
        
        input("\nPress Enter to continue to the next demo...")
        demo_error_handling()
        
        input("\nPress Enter to continue to the next demo...")
        demo_batch_processing()
        
        input("\nPress Enter to continue to the next demo...")
        demo_gui_features()
        
        input("\nPress Enter to see the demo summary...")
        demo_summary()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo error: {e}")
    finally:
        os.chdir('..')  # Go back to parent directory
        print(f"\nDemo completed. Check the '{demo_dir}' folder for generated files.")

if __name__ == "__main__":
    main()
