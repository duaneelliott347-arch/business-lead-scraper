#!/usr/bin/env python3
"""
Test script for Business Lead Scraper
Runs basic tests to verify functionality
"""

import unittest
import tempfile
import os
import json
import csv
from unittest.mock import Mock, patch
from business_lead_scraper import BusinessLead, DataExporter, RateLimiter

class TestBusinessLead(unittest.TestCase):
    """Test BusinessLead data class"""
    
    def test_business_lead_creation(self):
        """Test creating a BusinessLead instance"""
        lead = BusinessLead(
            name="Test Business",
            address="123 Test St",
            phone="555-1234",
            website="https://test.com",
            email="test@test.com",
            source="Test",
            rating="4.5",
            review_count="100"
        )
        
        self.assertEqual(lead.name, "Test Business")
        self.assertEqual(lead.address, "123 Test St")
        self.assertEqual(lead.phone, "555-1234")
        self.assertEqual(lead.website, "https://test.com")
        self.assertEqual(lead.email, "test@test.com")
        self.assertEqual(lead.source, "Test")
        self.assertEqual(lead.rating, "4.5")
        self.assertEqual(lead.review_count, "100")
    
    def test_business_lead_defaults(self):
        """Test BusinessLead with default values"""
        lead = BusinessLead(
            name="Test Business",
            address="123 Test St",
            phone="555-1234"
        )
        
        self.assertEqual(lead.name, "Test Business")
        self.assertEqual(lead.website, "")
        self.assertEqual(lead.email, "")
        self.assertEqual(lead.source, "")

class TestRateLimiter(unittest.TestCase):
    """Test RateLimiter functionality"""
    
    def test_rate_limiter_initialization(self):
        """Test RateLimiter initialization"""
        limiter = RateLimiter(min_delay=1, max_delay=3)
        self.assertEqual(limiter.min_delay, 1)
        self.assertEqual(limiter.max_delay, 3)
    
    @patch('time.sleep')
    def test_rate_limiter_wait(self, mock_sleep):
        """Test RateLimiter wait method"""
        limiter = RateLimiter(min_delay=1, max_delay=2)
        limiter.wait()
        mock_sleep.assert_called_once()
        
        # Check that sleep was called with a value between min and max delay
        call_args = mock_sleep.call_args[0][0]
        self.assertGreaterEqual(call_args, 1)
        self.assertLessEqual(call_args, 2)

class TestDataExporter(unittest.TestCase):
    """Test DataExporter functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.test_leads = [
            BusinessLead(
                name="Business 1",
                address="Address 1",
                phone="Phone 1",
                website="Website 1",
                email="Email 1",
                source="Source 1",
                rating="4.5",
                review_count="100"
            ),
            BusinessLead(
                name="Business 2",
                address="Address 2",
                phone="Phone 2",
                website="Website 2",
                email="Email 2",
                source="Source 2",
                rating="4.0",
                review_count="50"
            )
        ]
    
    def test_csv_export(self):
        """Test CSV export functionality"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_filename = f.name
        
        try:
            DataExporter.to_csv(self.test_leads, temp_filename)
            
            # Verify file was created
            self.assertTrue(os.path.exists(temp_filename))
            
            # Verify CSV content
            with open(temp_filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                self.assertEqual(len(rows), 2)
                self.assertEqual(rows[0]['name'], 'Business 1')
                self.assertEqual(rows[1]['name'], 'Business 2')
                
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_json_export(self):
        """Test JSON export functionality"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        try:
            DataExporter.to_json(self.test_leads, temp_filename)
            
            # Verify file was created
            self.assertTrue(os.path.exists(temp_filename))
            
            # Verify JSON content
            with open(temp_filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                self.assertEqual(len(data), 2)
                self.assertEqual(data[0]['name'], 'Business 1')
                self.assertEqual(data[1]['name'], 'Business 2')
                
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

class TestScraperIntegration(unittest.TestCase):
    """Integration tests for scraper functionality"""
    
    def test_empty_search_handling(self):
        """Test handling of empty search results"""
        # This would require mocking the web driver
        # For now, we'll test the data structures
        empty_leads = []
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_filename = f.name
        
        try:
            DataExporter.to_csv(empty_leads, temp_filename)
            
            # Verify empty CSV has header
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('name,address,phone', content)
                
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_duplicate_removal_logic(self):
        """Test duplicate removal logic"""
        leads_with_duplicates = [
            BusinessLead(name="Business A", address="Address 1", phone="Phone 1"),
            BusinessLead(name="Business B", address="Address 2", phone="Phone 2"),
            BusinessLead(name="Business A", address="Address 1", phone="Phone 1"),  # Duplicate
            BusinessLead(name="Business C", address="Address 3", phone="Phone 3"),
        ]
        
        # Simulate duplicate removal logic
        seen = set()
        unique_leads = []
        for lead in leads_with_duplicates:
            identifier = f"{lead.name}|{lead.address}"
            if identifier not in seen:
                seen.add(identifier)
                unique_leads.append(lead)
        
        self.assertEqual(len(unique_leads), 3)  # Should remove 1 duplicate
        names = [lead.name for lead in unique_leads]
        self.assertIn("Business A", names)
        self.assertIn("Business B", names)
        self.assertIn("Business C", names)

def run_basic_functionality_test():
    """Run a basic functionality test without web scraping"""
    print("Running basic functionality tests...")
    print("-" * 40)
    
    # Test BusinessLead creation
    print("✓ Testing BusinessLead creation...")
    lead = BusinessLead(
        name="Test Restaurant",
        address="123 Main St, Test City",
        phone="(555) 123-4567",
        website="https://testrestaurant.com"
    )
    assert lead.name == "Test Restaurant"
    print("  BusinessLead creation: PASSED")
    
    # Test RateLimiter
    print("✓ Testing RateLimiter...")
    limiter = RateLimiter(min_delay=0.1, max_delay=0.2)
    import time
    start_time = time.time()
    limiter.wait()
    end_time = time.time()
    assert 0.1 <= (end_time - start_time) <= 0.3  # Allow some tolerance
    print("  RateLimiter: PASSED")
    
    # Test data export
    print("✓ Testing data export...")
    test_leads = [
        BusinessLead(name="Restaurant 1", address="Address 1", phone="Phone 1"),
        BusinessLead(name="Restaurant 2", address="Address 2", phone="Phone 2")
    ]
    
    # Test CSV export
    csv_filename = "test_export.csv"
    DataExporter.to_csv(test_leads, csv_filename)
    assert os.path.exists(csv_filename)
    
    # Test JSON export
    json_filename = "test_export.json"
    DataExporter.to_json(test_leads, json_filename)
    assert os.path.exists(json_filename)
    
    # Cleanup
    os.remove(csv_filename)
    os.remove(json_filename)
    print("  Data export: PASSED")
    
    print("\n✓ All basic functionality tests passed!")

def run_configuration_test():
    """Test configuration loading"""
    print("\nTesting configuration...")
    print("-" * 25)
    
    try:
        from config import get_config, update_config
        
        # Test default config
        config = get_config()
        assert 'browser' in config
        assert 'rate_limit' in config
        assert 'scraping' in config
        print("✓ Configuration loading: PASSED")
        
        # Test config update
        updated_config = update_config(browser={'headless': False})
        assert updated_config['browser']['headless'] == False
        print("✓ Configuration update: PASSED")
        
    except ImportError:
        print("✗ Configuration module not found")

def main():
    """Run all tests"""
    print("Business Lead Scraper - Test Suite")
    print("=" * 40)
    
    try:
        # Run basic functionality tests
        run_basic_functionality_test()
        
        # Run configuration tests
        run_configuration_test()
        
        # Run unit tests
        print("\nRunning unit tests...")
        print("-" * 20)
        unittest.main(argv=[''], exit=False, verbosity=2)
        
        print("\n" + "=" * 40)
        print("All tests completed!")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
