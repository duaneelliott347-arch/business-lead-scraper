#!/usr/bin/env python3
"""
Setup script for Business Lead Scraper
Installs dependencies and sets up ChromeDriver
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    success, stdout, stderr = run_command(f"{sys.executable} -m pip install -r requirements.txt")
    
    if success:
        print("✓ Dependencies installed successfully")
        return True
    else:
        print(f"✗ Failed to install dependencies: {stderr}")
        return False

def setup_chromedriver():
    """Set up ChromeDriver using webdriver-manager"""
    print("Setting up ChromeDriver...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # Download and setup ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver_path = ChromeDriverManager().install()
        print(f"✓ ChromeDriver installed at: {driver_path}")
        
        # Test ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        driver.quit()
        print("✓ ChromeDriver test successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to setup ChromeDriver: {e}")
        print("Please install Chrome browser and try again")
        return False

def create_output_directory():
    """Create output directory"""
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)
    print(f"✓ Output directory created: {output_dir.absolute()}")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    
    print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def main():
    """Main setup function"""
    print("Business Lead Scraper Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Setup ChromeDriver
    if not setup_chromedriver():
        print("\nWarning: ChromeDriver setup failed. You may need to install it manually.")
        print("Visit: https://chromedriver.chromium.org/")
    
    # Create output directory
    create_output_directory()
    
    print("\n" + "=" * 30)
    print("Setup completed successfully!")
    print("\nYou can now run the scraper with:")
    print('python business_lead_scraper.py --keyword "restaurant" --location "New York"')
    print("\nFor more options, run:")
    print("python business_lead_scraper.py --help")

if __name__ == "__main__":
    main()
