#!/usr/bin/env python3
"""
GUI version of Business Lead Scraper using tkinter
Simple graphical interface for the scraper
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import queue
from datetime import datetime
from business_lead_scraper import GoogleMapsScraper, YelpScraper, DataExporter, BusinessLead

class ScraperGUI:
    """GUI application for the Business Lead Scraper"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Business Lead Scraper")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.scraping = False
        self.results = []
        self.progress_queue = queue.Queue()
        
        # Setup GUI
        self.setup_gui()
        
        # Start progress checker
        self.check_progress()
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Business Lead Scraper", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input fields
        ttk.Label(main_frame, text="Keyword:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.keyword_var = tk.StringVar(value="restaurant")
        keyword_entry = ttk.Entry(main_frame, textvariable=self.keyword_var, width=30)
        keyword_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Location:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.location_var = tk.StringVar(value="New York")
        location_entry = ttk.Entry(main_frame, textvariable=self.location_var, width=30)
        location_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Source selection
        ttk.Label(options_frame, text="Source:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.source_var = tk.StringVar(value="both")
        source_combo = ttk.Combobox(options_frame, textvariable=self.source_var, 
                                   values=["google", "yelp", "both"], state="readonly")
        source_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # Max results
        ttk.Label(options_frame, text="Max Results:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(20, 0))
        self.max_results_var = tk.StringVar(value="20")
        max_results_spin = ttk.Spinbox(options_frame, from_=1, to=100, 
                                      textvariable=self.max_results_var, width=10)
        max_results_spin.grid(row=0, column=3, pady=2, padx=(10, 0))
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=True)
        headless_check = ttk.Checkbutton(options_frame, text="Headless mode", 
                                        variable=self.headless_var)
        headless_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Start/Stop button
        self.start_button = ttk.Button(control_frame, text="Start Scraping", 
                                      command=self.toggle_scraping)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export button
        self.export_button = ttk.Button(control_frame, text="Export to CSV", 
                                       command=self.export_results, state=tk.DISABLED)
        self.export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        self.clear_button = ttk.Button(control_frame, text="Clear Results", 
                                      command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        progress_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Results table
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview for results
        columns = ('Name', 'Address', 'Phone', 'Website', 'Rating', 'Source')
        self.tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to scrape")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def toggle_scraping(self):
        """Start or stop scraping"""
        if not self.scraping:
            self.start_scraping()
        else:
            self.stop_scraping()
    
    def start_scraping(self):
        """Start the scraping process"""
        # Validate inputs
        keyword = self.keyword_var.get().strip()
        location = self.location_var.get().strip()
        
        if not keyword or not location:
            messagebox.showerror("Error", "Please enter both keyword and location")
            return
        
        # Update UI
        self.scraping = True
        self.start_button.config(text="Stop Scraping")
        self.export_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.progress_var.set("Starting scraper...")
        self.status_var.set("Scraping in progress...")
        
        # Start scraping thread
        thread = threading.Thread(target=self.scrape_worker, daemon=True)
        thread.start()
    
    def stop_scraping(self):
        """Stop the scraping process"""
        self.scraping = False
        self.start_button.config(text="Start Scraping")
        self.progress_bar.stop()
        self.progress_var.set("Stopping...")
        self.status_var.set("Scraping stopped by user")
    
    def scrape_worker(self):
        """Worker thread for scraping"""
        try:
            keyword = self.keyword_var.get().strip()
            location = self.location_var.get().strip()
            source = self.source_var.get()
            max_results = int(self.max_results_var.get())
            headless = self.headless_var.get()
            
            all_leads = []
            
            # Scrape from Google Maps
            if source in ['google', 'both'] and self.scraping:
                self.progress_queue.put(("status", "Scraping Google Maps..."))
                
                scraper = GoogleMapsScraper(headless=headless)
                try:
                    leads = scraper.search_businesses(keyword, location, max_results)
                    all_leads.extend(leads)
                    
                    # Add results to GUI
                    for lead in leads:
                        if self.scraping:
                            self.progress_queue.put(("result", lead))
                        else:
                            break
                            
                finally:
                    scraper.close()
            
            # Scrape from Yelp
            if source in ['yelp', 'both'] and self.scraping:
                self.progress_queue.put(("status", "Scraping Yelp..."))
                
                scraper = YelpScraper(headless=headless)
                try:
                    leads = scraper.search_businesses(keyword, location, max_results)
                    all_leads.extend(leads)
                    
                    # Add results to GUI
                    for lead in leads:
                        if self.scraping:
                            self.progress_queue.put(("result", lead))
                        else:
                            break
                            
                finally:
                    scraper.close()
            
            # Remove duplicates
            if self.scraping:
                self.progress_queue.put(("status", "Removing duplicates..."))
                seen = set()
                unique_leads = []
                for lead in all_leads:
                    identifier = f"{lead.name}|{lead.address}"
                    if identifier not in seen:
                        seen.add(identifier)
                        unique_leads.append(lead)
                
                self.results = unique_leads
                
                if self.scraping:
                    self.progress_queue.put(("complete", f"Found {len(unique_leads)} unique leads"))
                
        except Exception as e:
            self.progress_queue.put(("error", str(e)))
        
        finally:
            if self.scraping:
                self.scraping = False
                self.progress_queue.put(("finished", None))
    
    def check_progress(self):
        """Check progress queue and update GUI"""
        try:
            while True:
                msg_type, data = self.progress_queue.get_nowait()
                
                if msg_type == "status":
                    self.progress_var.set(data)
                    self.status_var.set(data)
                
                elif msg_type == "result":
                    self.add_result_to_tree(data)
                
                elif msg_type == "complete":
                    self.progress_var.set(data)
                    self.status_var.set(data)
                
                elif msg_type == "error":
                    messagebox.showerror("Scraping Error", f"An error occurred: {data}")
                    self.stop_scraping()
                
                elif msg_type == "finished":
                    self.scraping = False
                    self.start_button.config(text="Start Scraping")
                    self.progress_bar.stop()
                    if self.results:
                        self.export_button.config(state=tk.NORMAL)
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_progress)
    
    def add_result_to_tree(self, lead):
        """Add a result to the treeview"""
        values = (
            lead.name,
            lead.address[:50] + "..." if len(lead.address) > 50 else lead.address,
            lead.phone,
            lead.website[:30] + "..." if len(lead.website) > 30 else lead.website,
            lead.rating,
            lead.source
        )
        self.tree.insert('', tk.END, values=values)
        
        # Scroll to bottom
        children = self.tree.get_children()
        if children:
            self.tree.see(children[-1])
    
    def export_results(self):
        """Export results to CSV"""
        if not self.results:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        # Ask for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"leads_{self.keyword_var.get()}_{timestamp}.csv"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialvalue=default_filename
        )
        
        if filename:
            try:
                DataExporter.to_csv(self.results, filename)
                messagebox.showinfo("Export Successful", 
                                  f"Results exported to {os.path.basename(filename)}")
                self.status_var.set(f"Exported {len(self.results)} leads to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def clear_results(self):
        """Clear all results"""
        if messagebox.askyesno("Clear Results", "Are you sure you want to clear all results?"):
            # Clear treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Clear results list
            self.results = []
            
            # Update UI
            self.export_button.config(state=tk.DISABLED)
            self.status_var.set("Results cleared")
            self.progress_var.set("Ready")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = ScraperGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application closed by user")

if __name__ == "__main__":
    main()
