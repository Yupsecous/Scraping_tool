"""
Discord Invite Link Scraper - GUI Version
User-friendly graphical interface for scraping Discord invite links
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import queue
import sys
import os

# Import the scraper class
from discord_scraper import DiscordLinkScraper

class DiscordScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Invite Link Scraper")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.scraper = None
        self.is_running = False
        self.output_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        
        # Start checking output queue
        self.check_queue()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Discord Invite Link Scraper", 
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Output file
        ttk.Label(settings_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_file_var = tk.StringVar(value="invite_link.txt")
        output_entry = ttk.Entry(settings_frame, textvariable=self.output_file_var, width=40)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(settings_frame, text="Browse", command=self.browse_output_file).grid(row=0, column=2)
        
        # Max searches
        ttk.Label(settings_frame, text="Max Searches:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.max_searches_var = tk.StringVar(value="50")
        max_searches_spinbox = ttk.Spinbox(settings_frame, from_=1, to=1000, textvariable=self.max_searches_var, width=10)
        max_searches_spinbox.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        # Use Google API checkbox
        self.use_api_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Use Google Custom Search API (100 free/day)", 
                       variable=self.use_api_var).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Control Buttons Frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Start Scraping", command=self.start_scraping, width=20)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_scraping, 
                                      state=tk.DISABLED, width=20)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="Open Output File", command=self.open_output_file, width=20).pack(side=tk.LEFT)
        
        # Progress Frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.progress_var).grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 10))
        
        # Stats
        stats_frame = ttk.Frame(progress_frame)
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        
        self.total_links_var = tk.StringVar(value="Total Links: 0")
        ttk.Label(stats_frame, textvariable=self.total_links_var).grid(row=0, column=0, sticky=tk.W)
        
        self.new_links_var = tk.StringVar(value="New Links: 0")
        ttk.Label(stats_frame, textvariable=self.new_links_var).grid(row=0, column=1, sticky=tk.W)
        
        # Output log
        ttk.Label(progress_frame, text="Log:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=15, width=80)
        self.log_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        progress_frame.rowconfigure(4, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Load initial stats
        self.update_stats()
    
    def browse_output_file(self):
        """Browse for output file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=self.output_file_var.get()
        )
        if filename:
            self.output_file_var.set(filename)
            self.update_stats()
    
    def open_output_file(self):
        """Open the output file in default text editor."""
        filename = self.output_file_var.get()
        if os.path.exists(filename):
            if sys.platform == "win32":
                os.startfile(filename)
            elif sys.platform == "darwin":
                os.system(f"open {filename}")
            else:
                os.system(f"xdg-open {filename}")
        else:
            messagebox.showwarning("File Not Found", f"File {filename} does not exist yet.")
    
    def update_stats(self):
        """Update statistics display."""
        filename = self.output_file_var.get()
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    links = [line.strip() for line in f if line.strip() and line.strip().startswith('http')]
                self.total_links_var.set(f"Total Links: {len(links)}")
            except:
                self.total_links_var.set("Total Links: 0")
        else:
            self.total_links_var.set("Total Links: 0")
    
    def log(self, message):
        """Add message to log."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.output_queue.put(("log", message))
    
    def update_progress(self, message):
        """Update progress message."""
        self.progress_var.set(message)
        self.status_var.set(message)
    
    def start_scraping(self):
        """Start the scraping process."""
        if self.is_running:
            return
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Get settings
        output_file = self.output_file_var.get()
        try:
            max_searches = int(self.max_searches_var.get())
        except:
            max_searches = 50
            messagebox.showerror("Invalid Input", "Max searches must be a number. Using default: 50")
        
        use_api = self.use_api_var.get()
        
        # Load API config if needed
        api_key = None
        search_engine_id = None
        if use_api:
            try:
                import json
                with open('google_api_config.json', 'r') as f:
                    config = json.load(f)
                    api_key = config.get('api_key')
                    search_engine_id = config.get('search_engine_id')
            except:
                messagebox.showwarning("API Not Configured", 
                    "Google API not configured. Using free scraping method instead.")
                use_api = False
        
        # Start scraping in separate thread
        thread = threading.Thread(target=self.run_scraper, 
                                 args=(output_file, max_searches, use_api, api_key, search_engine_id),
                                 daemon=True)
        thread.start()
        
        self.log("Starting scraper...")
        self.update_progress("Scraping in progress...")
    
    def run_scraper(self, output_file, max_searches, use_api, api_key, search_engine_id):
        """Run the scraper in a separate thread."""
        try:
            # Create scraper instance
            scraper = DiscordLinkScraper(
                output_file=output_file,
                use_google_api=use_api,
                api_key=api_key,
                search_engine_id=search_engine_id
            )
            
            initial_count = len(scraper.discord_links)
            self.output_queue.put(("log", f"Loaded {initial_count} existing links"))
            
            # Override print to capture output
            original_print = print
            def log_print(*args, **kwargs):
                message = ' '.join(str(arg) for arg in args)
                self.output_queue.put(("log", message))
            
            # Temporarily replace print
            import builtins
            builtins.print = log_print
            
            # Run scraper
            queries = scraper.generate_search_queries()
            total_searches = min(len(queries), max_searches)
            
            self.output_queue.put(("log", f"Will perform {total_searches} searches"))
            self.output_queue.put(("log", "=" * 60))
            
            new_links_count = 0
            for i, (source_type, query) in enumerate(queries[:total_searches], 1):
                if not self.is_running:
                    self.output_queue.put(("log", "Scraping stopped by user"))
                    break
                
                self.output_queue.put(("progress", f"[{i}/{total_searches}] Searching {source_type}: {query}"))
                
                try:
                    if source_type == 'x.com':
                        links = scraper.search_x_com_via_google(query)
                    else:
                        links = scraper.search_articles(query)
                    
                    new_links = links - scraper.discord_links
                    scraper.discord_links.update(links)
                    
                    if new_links:
                        new_links_count += len(new_links)
                        self.output_queue.put(("log", f"Found {len(new_links)} new links!"))
                        for link in new_links:
                            self.output_queue.put(("log", f"  - {link}"))
                    
                    # Save periodically
                    if i % 10 == 0:
                        scraper.save_links()
                        self.output_queue.put(("log", f"Progress saved: {len(scraper.discord_links)} total links"))
                        self.output_queue.put(("stats", len(scraper.discord_links)))
                    
                except Exception as e:
                    self.output_queue.put(("log", f"Error: {str(e)}"))
            
            # Final save
            scraper.save_links()
            
            # Restore original print
            builtins.print = original_print
            
            # Update final stats
            final_count = len(scraper.discord_links)
            self.output_queue.put(("log", "=" * 60))
            self.output_queue.put(("log", f"Scraping completed!"))
            self.output_queue.put(("log", f"Total unique Discord invite links: {final_count}"))
            self.output_queue.put(("log", f"New links found: {new_links_count}"))
            self.output_queue.put(("log", f"Links saved to: {output_file}"))
            self.output_queue.put(("done", final_count))
            
        except Exception as e:
            self.output_queue.put(("error", str(e)))
    
    def stop_scraping(self):
        """Stop the scraping process."""
        self.is_running = False
        self.log("Stopping scraper...")
    
    def check_queue(self):
        """Check output queue for messages."""
        try:
            while True:
                msg_type, data = self.output_queue.get_nowait()
                
                if msg_type == "log":
                    self.log_text.insert(tk.END, data + "\n")
                    self.log_text.see(tk.END)
                elif msg_type == "progress":
                    self.update_progress(data)
                elif msg_type == "stats":
                    current_total = int(self.total_links_var.get().split(':')[1].strip()) if ':' in self.total_links_var.get() else 0
                    self.total_links_var.set(f"Total Links: {data}")
                    new_count = max(0, data - current_total)
                    self.new_links_var.set(f"New Links: {new_count}")
                elif msg_type == "done":
                    self.is_running = False
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.progress_bar.stop()
                    self.update_progress("Completed!")
                    self.update_stats()
                    messagebox.showinfo("Completed", f"Scraping completed!\nTotal links: {data}")
                elif msg_type == "error":
                    self.is_running = False
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.progress_bar.stop()
                    self.update_progress("Error occurred")
                    messagebox.showerror("Error", f"An error occurred:\n{data}")
        
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queue)

def main():
    """Main function."""
    root = tk.Tk()
    app = DiscordScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

