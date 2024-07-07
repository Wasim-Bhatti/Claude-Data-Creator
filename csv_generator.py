import os
import json
import logging
import argparse
import threading
from agents import read_csv, save_to_csv, analyzer_agent, generator_agent, set_api_key

# Set up logging
logging.basicConfig(filename='csv_generator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class CSVGenerator:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f)

    def clear_config(self):
        self.config = {}
        self.save_config()

    def set_api_key(self, api_key):
        self.config['api_key'] = api_key
        set_api_key(api_key)
        self.save_config()
        logging.info("API Key saved successfully!")

    def generate_csv(self, file_path, desired_rows, progress_callback=None):
        try:
            sample_data = read_csv(file_path)
            sample_data_str = "\n".join([",".join(row) for row in sample_data])

            if progress_callback:
                progress_callback("Analyzing data...", 10)
            else:
                print("Analyzing data...")
            analysis_result = analyzer_agent(sample_data_str)

            output_file = os.path.join(os.path.dirname(file_path), "new_dataset.csv")
            headers = sample_data[0]
            save_to_csv("", output_file, headers)

            batch_size = 30
            generated_rows = 0

            while generated_rows < desired_rows:
                rows_to_generate = min(batch_size, desired_rows - generated_rows)
                if progress_callback:
                    progress_callback(f"Generating rows {generated_rows + 1} to {generated_rows + rows_to_generate}...", 
                                      10 + int(90 * generated_rows / desired_rows))
                else:
                    print(f"Generating rows {generated_rows + 1} to {generated_rows + rows_to_generate}...")
                generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate)
                save_to_csv(generated_data, output_file)
                generated_rows += rows_to_generate

            if progress_callback:
                progress_callback("Generation complete!", 100)
            else:
                print(f"Generated data has been saved to {output_file}")
            return output_file
        except Exception as e:
            logging.error(f"Error in generate_csv: {str(e)}")
            raise

def run_cli_interactive():
    generator = CSVGenerator()

    if 'api_key' not in generator.config:
        api_key = input("Please enter your Anthropic API key: ")
        generator.set_api_key(api_key)

    while True:
        file_path = input("Enter the path to the input CSV file: ")
        file_path = os.path.abspath(file_path)
        if os.path.exists(file_path):
            break
        print("File not found. Please enter a valid file path.")

    num_rows = input("Enter the number of rows to generate: ")
    while not num_rows.isdigit() or int(num_rows) <= 0:
        print("Please enter a valid positive integer.")
        num_rows = input("Enter the number of rows to generate: ")

    num_rows = int(num_rows)

    try:
        output_file = generator.generate_csv(file_path, num_rows)
        print(f"Generated data has been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def run_cli(args):
    generator = CSVGenerator()

    if args.api_key:
        generator.set_api_key(args.api_key)
    elif 'api_key' not in generator.config:
        api_key = input("Please enter your Anthropic API key: ")
        generator.set_api_key(api_key)

    try:
        output_file = generator.generate_csv(args.file_path, args.num_rows)
        print(f"Generated data has been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def run_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    class CSVGeneratorGUI(tk.Tk):
        def __init__(self):
            super().__init__()
            self.generator = CSVGenerator()
            self.title("CSV Generator")
            self.geometry("600x500")  # Increased height for clear data button

            self.style = ttk.Style()
            self.style.theme_use('clam')

            self.main_frame = ttk.Frame(self, padding="20 20 20 20")
            self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            self.create_widgets()

        def create_widgets(self):
            # API Key input
            self.api_key_label = ttk.Label(self.main_frame, text="Anthropic API Key:")
            self.api_key_label.grid(row=0, column=0, sticky=tk.W, pady=10)
            self.api_key_entry = ttk.Entry(self.main_frame, width=50, show="*")
            self.api_key_entry.grid(row=0, column=1, columnspan=2, pady=10)
            self.api_key_entry.insert(0, self.generator.config.get('api_key', ''))
            
            # Save API Key button
            self.save_api_key_button = ttk.Button(self.main_frame, text="Save API Key", command=self.save_api_key)
            self.save_api_key_button.grid(row=1, column=1, pady=5)

            # File path input
            self.file_path_label = ttk.Label(self.main_frame, text="CSV File Path:")
            self.file_path_label.grid(row=2, column=0, sticky=tk.W, pady=10)
            self.file_path_entry = ttk.Entry(self.main_frame, width=40)
            self.file_path_entry.grid(row=2, column=1, pady=10)
            self.file_path_entry.insert(0, self.generator.config.get('last_file_path', ''))
            self.browse_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_file)
            self.browse_button.grid(row=2, column=2, pady=10, padx=(5, 0))

            # Number of rows input
            self.rows_label = ttk.Label(self.main_frame, text="Number of Rows:")
            self.rows_label.grid(row=3, column=0, sticky=tk.W, pady=10)
            self.rows_entry = ttk.Entry(self.main_frame, width=10)
            self.rows_entry.grid(row=3, column=1, sticky=tk.W, pady=10)
            self.rows_entry.insert(0, self.generator.config.get('last_row_count', ''))

            # Generate button
            self.generate_button = ttk.Button(self.main_frame, text="Generate CSV", command=self.generate_csv_gui)
            self.generate_button.grid(row=4, column=1, pady=20)

            # Progress bar
            self.progress = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
            self.progress.grid(row=5, column=0, columnspan=3, pady=10)

            # Status label
            self.status_label = ttk.Label(self.main_frame, text="")
            self.status_label.grid(row=6, column=0, columnspan=3, pady=5)

            # Clear Data button
            self.clear_data_button = ttk.Button(self.main_frame, text="Clear Saved Data", command=self.clear_saved_data)
            self.clear_data_button.grid(row=7, column=1, pady=20)

        def save_api_key(self):
            api_key = self.api_key_entry.get()
            if api_key:
                self.generator.set_api_key(api_key)
                self.status_label.config(text="API Key saved successfully!")
            else:
                messagebox.showerror("Error", "Please enter an API Key")

        def browse_file(self):
            filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, filename)
            self.generator.config['last_file_path'] = filename
            self.generator.save_config()

        def update_progress(self, message, value):
            self.progress['value'] = value
            self.status_label.config(text=message)
            self.update_idletasks()

        def generate_csv_gui(self):
            file_path = self.file_path_entry.get()
            desired_rows = self.rows_entry.get()

            if not file_path or not os.path.exists(file_path):
                messagebox.showerror("Error", "Please select a valid CSV file")
                return

            if not desired_rows.isdigit() or int(desired_rows) <= 0:
                messagebox.showerror("Error", "Please enter a valid number of rows (positive integer)")
                return

            desired_rows = int(desired_rows)
            self.generator.config['last_row_count'] = desired_rows
            self.generator.save_config()

            self.generate_button.state(['disabled'])
            self.progress['value'] = 0

            def generation_thread():
                try:
                    output_file = self.generator.generate_csv(file_path, desired_rows, progress_callback=self.update_progress)
                    self.after(0, lambda: messagebox.showinfo("Success", f"Generated data has been saved to {output_file}"))
                except Exception as e:
                    error_message = str(e)
                    self.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {error_message}"))
                finally:
                    self.after(0, lambda: self.generate_button.state(['!disabled']))

            threading.Thread(target=generation_thread, daemon=True).start()

        def clear_saved_data(self):
            self.generator.clear_config()
            self.api_key_entry.delete(0, tk.END)
            self.file_path_entry.delete(0, tk.END)
            self.rows_entry.delete(0, tk.END)
            self.status_label.config(text="Saved data cleared")

    app = CSVGeneratorGUI()
    app.mainloop()


if __name__ == "__main__":
    if os.environ.get('DOCKER_ENV') == 'true':
        parser = argparse.ArgumentParser(description="Generate CSV data based on a sample CSV file.")
        parser.add_argument("file_path", nargs='?', help="Path to the input CSV file")
        parser.add_argument("num_rows", nargs='?', type=int, help="Number of rows to generate")
        parser.add_argument("--api_key", help="Anthropic API key")
        args = parser.parse_args()

        if args.file_path and args.num_rows:
            run_cli(args)
        else:
            run_cli_interactive()
    else:
        run_gui()