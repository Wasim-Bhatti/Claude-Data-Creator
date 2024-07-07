import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import json
import logging
from agents import read_csv, save_to_csv, analyzer_agent, generator_agent, set_api_key

class CSVGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("CSV Generator")
        master.geometry("600x400")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.main_frame = ttk.Frame(master, padding="20 20 20 20")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        # API Key input
        self.api_key_label = ttk.Label(self.main_frame, text="Anthropic API Key:")
        self.api_key_label.grid(row=0, column=0, sticky=tk.W, pady=10)
        self.api_key_entry = ttk.Entry(self.main_frame, width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, columnspan=2, pady=10)
        
        # Save API Key button
        self.save_api_key_button = ttk.Button(self.main_frame, text="Save API Key", command=self.save_api_key)
        self.save_api_key_button.grid(row=1, column=1, pady=5)

        # File path input
        self.file_path_label = ttk.Label(self.main_frame, text="CSV File Path:")
        self.file_path_label.grid(row=2, column=0, sticky=tk.W, pady=10)
        self.file_path_entry = ttk.Entry(self.main_frame, width=40)
        self.file_path_entry.grid(row=2, column=1, pady=10)
        self.browse_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=2, column=2, pady=10, padx=(5, 0))

        # Number of rows input
        self.rows_label = ttk.Label(self.main_frame, text="Number of Rows:")
        self.rows_label.grid(row=3, column=0, sticky=tk.W, pady=10)
        self.rows_entry = ttk.Entry(self.main_frame, width=10)
        self.rows_entry.grid(row=3, column=1, sticky=tk.W, pady=10)

        # Generate button
        self.generate_button = ttk.Button(self.main_frame, text="Generate CSV", command=self.generate_csv)
        self.generate_button.grid(row=4, column=1, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)

        # Status label
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.api_key_entry.insert(0, config.get('api_key', ''))
                self.file_path_entry.insert(0, config.get('last_file_path', ''))
                self.rows_entry.insert(0, config.get('last_row_count', ''))
        except FileNotFoundError:
            logging.info("No config file found. Starting with empty fields.")
        except json.JSONDecodeError:
            logging.error("Error decoding config file. Starting with empty fields.")

    def save_config(self):
        config = {
            'api_key': self.api_key_entry.get(),
            'last_file_path': self.file_path_entry.get(),
            'last_row_count': self.rows_entry.get()
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)

    def save_api_key(self):
        api_key = self.api_key_entry.get()
        if api_key:
            set_api_key(api_key)
            self.status_label.config(text="API Key saved successfully!")
            self.save_config()
        else:
            messagebox.showerror("Error", "Please enter an API Key")

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, filename)
        self.save_config()

    def generate_csv(self):
        file_path = self.file_path_entry.get()
        desired_rows = self.rows_entry.get()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid CSV file")
            return

        if not desired_rows.isdigit() or int(desired_rows) <= 0:
            messagebox.showerror("Error", "Please enter a valid number of rows (positive integer)")
            return

        desired_rows = int(desired_rows)

        self.progress['value'] = 0
        self.generate_button.state(['disabled'])
        self.status_label.config(text="Starting generation process...")

        threading.Thread(target=self.generate_csv_thread, args=(file_path, desired_rows)).start()

    def generate_csv_thread(self, file_path, desired_rows):
        try:
            sample_data = read_csv(file_path)
            sample_data_str = "\n".join([",".join(row) for row in sample_data])

            self.update_progress("Analyzing data...", 10)
            analysis_result = analyzer_agent(sample_data_str)

            output_file = os.path.join(os.path.dirname(file_path), "new_dataset.csv")
            headers = sample_data[0]
            save_to_csv("", output_file, headers)

            batch_size = 30
            generated_rows = 0

            while generated_rows < desired_rows:
                rows_to_generate = min(batch_size, desired_rows - generated_rows)
                self.update_progress(f"Generating rows {generated_rows + 1} to {generated_rows + rows_to_generate}...", 
                                     10 + int(90 * generated_rows / desired_rows))
                generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate)
                save_to_csv(generated_data, output_file)
                generated_rows += rows_to_generate

            self.master.after(0, self.generation_complete, output_file)
        except Exception as e:
            logging.error(f"Error in generate_csv_thread: {str(e)}")
            self.master.after(0, self.generation_error, str(e))

    def update_progress(self, message, value):
        self.master.after(0, self._update_progress, message, value)

    def _update_progress(self, message, value):
        self.status_label.config(text=message)
        self.progress['value'] = value

    def generation_complete(self, output_file):
        self.progress['value'] = 100
        self.generate_button.state(['!disabled'])
        self.status_label.config(text="Generation complete!")
        messagebox.showinfo("Success", f"Generated data has been saved to {output_file}")

    def generation_error(self, error_message):
        self.progress['value'] = 0
        self.generate_button.state(['!disabled'])
        self.status_label.config(text="An error occurred.")
        messagebox.showerror("Error", f"An error occurred: {error_message}")
        logging.error(f"Error during CSV generation: {error_message}")

if __name__ == "__main__":
    logging.basicConfig(filename='gui.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    root = tk.Tk()
    gui = CSVGeneratorGUI(root)
    root.mainloop()