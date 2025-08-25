#!/usr/bin/env python3
"""
Business Lead Scraper
A comprehensive tool for scraping business leads from Google Maps and Yelp
"""

import argparse
import csv
import json
import time
import random
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class BusinessLead:
    """Data class for storing business lead information"""
    name: str
    address: str
    phone: str
    website: str = ""
    email: str = ""
    source: str = ""
    rating: str = ""
    review_count: str = ""

class RateLimiter:
    """Simple rate limiter to prevent overwhelming servers"""
    
    def __init__(self, min_delay=1, max_delay=3):
        self.min_delay = min_delay
        self.max_delay = max_delay
    
    def wait(self):
        """Wait for a random time between min_delay and max_delay seconds"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)

class GoogleMapsScraper:
    """Scraper for Google Maps business listings"""
    
    def __init__(self, headless=True):
        self.rate_limiter = RateLimiter()
        self.setup_driver(headless)
    
    def setup_driver(self, headless):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {e}")
            raise
    
    def search_businesses(self, keyword: str, location: str, max_results: int = 50) -> List[BusinessLead]:
        """Search for businesses on Google Maps"""
        leads = []
        search_query = f"{keyword} in {location}"
        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
        
        try:
            logger.info(f"Searching Google Maps for: {search_query}")
            self.driver.get(url)
            self.rate_limiter.wait()
            
            # Wait for search results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-result-index]"))
            )
            
            # Scroll to load more results
            self.scroll_to_load_results()
            
            # Get business listings
            business_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-result-index]")
            logger.info(f"Found {len(business_elements)} potential business listings")
            
            for idx, element in enumerate(business_elements[:max_results]):
                try:
                    lead = self.extract_business_info(element)
                    if lead and lead.name:
                        lead.source = "Google Maps"
                        leads.append(lead)
                        logger.info(f"Extracted lead {idx + 1}: {lead.name}")
                    
                    self.rate_limiter.wait()
                    
                except Exception as e:
                    logger.warning(f"Error extracting business {idx + 1}: {e}")
                    continue
            
        except TimeoutException:
            logger.error("Timeout waiting for Google Maps results")
        except Exception as e:
            logger.error(f"Error searching Google Maps: {e}")
        
        return leads
    
    def scroll_to_load_results(self):
        """Scroll to load more search results"""
        scroll_pause_time = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(3):  # Scroll 3 times to load more results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def extract_business_info(self, element) -> Optional[BusinessLead]:
        """Extract business information from a Google Maps listing element"""
        try:
            # Click on the business listing
            element.click()
            time.sleep(3)  # Wait for details panel to load
            
            # Extract business name
            name_elem = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            name = name_elem.text.strip()
            
            # Extract address
            address = self.extract_text_by_aria_label("Address")
            
            # Extract phone
            phone = self.extract_text_by_aria_label("Phone")
            
            # Extract website
            website = self.extract_website()
            
            # Extract rating and review count
            rating = self.extract_rating()
            review_count = self.extract_review_count()
            
            return BusinessLead(
                name=name,
                address=address,
                phone=phone,
                website=website,
                rating=rating,
                review_count=review_count
            )
            
        except Exception as e:
            logger.warning(f"Error extracting business info: {e}")
            return None
    
    def extract_text_by_aria_label(self, aria_label: str) -> str:
        """Extract text using aria-label attribute"""
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, f"[aria-label*='{aria_label}']")
            for elem in elements:
                text = elem.text.strip()
                if text and text != aria_label:
                    return text
        except:
            pass
        return ""
    
    def extract_website(self) -> str:
        """Extract website URL"""
        try:
            website_elem = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='authority']")
            return website_elem.text.strip()
        except:
            return ""
    
    def extract_rating(self) -> str:
        """Extract business rating"""
        try:
            rating_elem = self.driver.find_element(By.CSS_SELECTOR, "span[role='img']")
            return rating_elem.get_attribute("aria-label").split()[0]
        except:
            return ""
    
    def extract_review_count(self) -> str:
        """Extract review count"""
        try:
            review_elem = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='review']")
            return review_elem.text.strip()
        except:
            return ""
    
    def close(self):
        """Close the WebDriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

class YelpScraper:
    """Scraper for Yelp business listings"""
    
    def __init__(self, headless=True):
        self.rate_limiter = RateLimiter()
        self.setup_driver(headless)
    
    def setup_driver(self, headless):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {e}")
            raise
    
    def search_businesses(self, keyword: str, location: str, max_results: int = 50) -> List[BusinessLead]:
        """Search for businesses on Yelp"""
        leads = []
        search_query = f"{keyword} in {location}"
        url = f"https://www.yelp.com/search?find_desc={keyword.replace(' ', '+')}&find_loc={location.replace(' ', '+')}"
        
        try:
            logger.info(f"Searching Yelp for: {search_query}")
            self.driver.get(url)
            self.rate_limiter.wait()
            
            # Wait for search results
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='serp-ia-card']"))
            )
            
            # Get business listings
            business_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='serp-ia-card']")
            logger.info(f"Found {len(business_elements)} potential business listings")
            
            for idx, element in enumerate(business_elements[:max_results]):
                try:
                    lead = self.extract_yelp_business_info(element)
                    if lead and lead.name:
                        lead.source = "Yelp"
                        leads.append(lead)
                        logger.info(f"Extracted lead {idx + 1}: {lead.name}")
                    
                    self.rate_limiter.wait()
                    
                except Exception as e:
                    logger.warning(f"Error extracting Yelp business {idx + 1}: {e}")
                    continue
        
        except TimeoutException:
            logger.error("Timeout waiting for Yelp results")
        except Exception as e:
            logger.error(f"Error searching Yelp: {e}")
        
        return leads
    
    def extract_yelp_business_info(self, element) -> Optional[BusinessLead]:
        """Extract business information from a Yelp listing element"""
        try:
            # Extract business name
            name_elem = element.find_element(By.CSS_SELECTOR, "[data-testid='business-name']")
            name = name_elem.text.strip()
            
            # Extract address
            address_elem = element.find_element(By.CSS_SELECTOR, "[data-testid='business-address']")
            address = address_elem.text.strip()
            
            # Extract phone
            phone_elem = element.find_element(By.CSS_SELECTOR, "[data-testid='business-phone-number']")
            phone = phone_elem.text.strip()
            
            # Extract rating
            rating_elem = element.find_element(By.CSS_SELECTOR, "[role='img']")
            rating = rating_elem.get_attribute("aria-label").split()[0]
            
            # Extract review count
            review_elem = element.find_element(By.CSS_SELECTOR, "[data-testid='review-count']")
            review_count = review_elem.text.strip()
            
            # Extract website (may need to visit business page)
            website = self.extract_website_from_business_page(name_elem)
            
            return BusinessLead(
                name=name,
                address=address,
                phone=phone,
                website=website,
                rating=rating,
                review_count=review_count
            )
            
        except Exception as e:
            logger.warning(f"Error extracting Yelp business info: {e}")
            return None
    
    def extract_website_from_business_page(self, name_elem) -> str:
        """Extract website by visiting the business page"""
        try:
            # Click on business name to go to business page
            name_elem.click()
            time.sleep(3)
            
            # Look for website link
            website_elem = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Business website']")
            return website_elem.get_attribute("href") or ""
        except:
            return ""
    
    def close(self):
        """Close the WebDriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

class DataExporter:
    """Export scraped data to various formats"""
    
    @staticmethod
    def to_csv(leads: List[BusinessLead], filename: str):
        """Export leads to CSV format"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'address', 'phone', 'website', 'email', 'source', 'rating', 'review_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for lead in leads:
                writer.writerow({
                    'name': lead.name,
                    'address': lead.address,
                    'phone': lead.phone,
                    'website': lead.website,
                    'email': lead.email,
                    'source': lead.source,
                    'rating': lead.rating,
                    'review_count': lead.review_count
                })
        
        logger.info(f"Exported {len(leads)} leads to {filename}")
    
    @staticmethod
    def to_json(leads: List[BusinessLead], filename: str):
        """Export leads to JSON format"""
        data = []
        for lead in leads:
            data.append({
                'name': lead.name,
                'address': lead.address,
                'phone': lead.phone,
                'website': lead.website,
                'email': lead.email,
                'source': lead.source,
                'rating': lead.rating,
                'review_count': lead.review_count
            })
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(leads)} leads to {filename}")

def main():
    """Main function to run the business lead scraper"""
    parser = argparse.ArgumentParser(description='Scrape business leads from Google Maps and Yelp')
    parser.add_argument('--keyword', required=True, help='Business keyword to search for')
    parser.add_argument('--location', required=True, help='Location to search in')
    parser.add_argument('--source', choices=['google', 'yelp', 'both'], default='both', 
                       help='Source to scrape from (default: both)')
    parser.add_argument('--max-results', type=int, default=50, help='Maximum results per source (default: 50)')
    parser.add_argument('--output-format', choices=['csv', 'json', 'both'], default='both',
                       help='Output format (default: both)')
    parser.add_argument('--output-dir', default='./output', help='Output directory (default: ./output)')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode (default: True)')
    
    args = parser.parse_args()
    
    # Create output directory
    import os
    os.makedirs(args.output_dir, exist_ok=True)
    
    all_leads = []
    
    try:
        # Scrape from Google Maps
        if args.source in ['google', 'both']:
            logger.info("Starting Google Maps scraping...")
            google_scraper = GoogleMapsScraper(headless=args.headless)
            try:
                google_leads = google_scraper.search_businesses(
                    args.keyword, args.location, args.max_results
                )
                all_leads.extend(google_leads)
                logger.info(f"Scraped {len(google_leads)} leads from Google Maps")
            finally:
                google_scraper.close()
        
        # Scrape from Yelp
        if args.source in ['yelp', 'both']:
            logger.info("Starting Yelp scraping...")
            yelp_scraper = YelpScraper(headless=args.headless)
            try:
                yelp_leads = yelp_scraper.search_businesses(
                    args.keyword, args.location, args.max_results
                )
                all_leads.extend(yelp_leads)
                logger.info(f"Scraped {len(yelp_leads)} leads from Yelp")
            finally:
                yelp_scraper.close()
        
        # Remove duplicates based on name and address
        seen = set()
        unique_leads = []
        for lead in all_leads:
            identifier = f"{lead.name}|{lead.address}"
            if identifier not in seen:
                seen.add(identifier)
                unique_leads.append(lead)
        
        logger.info(f"Total unique leads found: {len(unique_leads)}")
        
        # Export results
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        base_filename = f"{args.keyword}_{args.location}_{timestamp}"
        
        if args.output_format in ['csv', 'both']:
            csv_filename = os.path.join(args.output_dir, f"{base_filename}.csv")
            DataExporter.to_csv(unique_leads, csv_filename)
        
        if args.output_format in ['json', 'both']:
            json_filename = os.path.join(args.output_dir, f"{base_filename}.json")
            DataExporter.to_json(unique_leads, json_filename)
        
        logger.info("Scraping completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise

if __name__ == "__main__":
    main()
