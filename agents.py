# agents.py

# Importing required libraries
import os 
import csv 
import anthropic
from prompts import *


# Setting up anthropic key
# Also ask the user to enter the key if not already entered

if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your Anthropic API key: ")


# Creating anthropic client

client = anthropic.Anthropic()
sonnet = "claude-3-5-sonnet-20240620"



# Function to read the CSV file from the user

def read_csv(file_path):
    data = []
    with open(file_path, "r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data


# Function to save to our CSV file from the user

def save_to_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a'
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in csv.reader(data.splitlines()):
            writer.writerow(row)


# Create the analyzer agent

def analyzer_agent(sample_data):
    message = client.messages.create(
        model=sonnet,
        max_tokens=400,
        temperature=0.1,
        system=ANALYZER_SYSTEM_PROMPT,
        messages =[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            }
        ]
    )
    return message.content[0].text


# Create the Generator Agent

def generator_agent(analysis_result, sample_data, num_rows=30):
    message = client.messages.create(
        model=sonnet,
        max_tokens=1500,
        temperature=1,
        system=GENERATOR_SYSTEM_PROMPT,
        messages=[
            {
                "role":"user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data
                )
            }
        ]
    )
    return message.content[0].text

# Get input from the user

file_path = input("\n Enter the name of your CSV file: ")
file_path = os.path.join('/app/data', file_path)
desired_rows = int(input("Enter the number of rows you want in the new dataset: "))

# Read the sample data from the input CSV file

sample_data = read_csv(file_path)
sample_data_str = "\n".join([",".join(row) for row in sample_data]) # Converts into a single string

print("\nLaunching team of Agents...")
analysis_result = analyzer_agent(sample_data_str) #Analyze the sample data using the Analyzer agent
print("\n##### Analyzer Agent output: ####\n")
print(analysis_result)
print("\n-----------------------------------------\n\nGenerating new data...")


# Setup the output of the file
output_file = "/app/data/new_dataset.csv"
headers = sample_data[0]
save_to_csv("", output_file, headers) #Create the output file with the headers

batch_size = 30 #Number of rows to generate in each batch
generated_rows = 0


#Generate data in batches until we reach the desired number of rows

while generated_rows < desired_rows:
    rows_to_generate = min(batch_size, desired_rows - generated_rows) # Calculate how many rows to generate in this batch
    generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate) #Generate a batch of data using the generator Agent
    save_to_csv(generated_data, output_file) #Append the generated data to the output file
    generated_rows += rows_to_generate #Update the count of generated rows
    print(f"Generated {generated_rows} rows out of {desired_rows}")


print(f"\nGenerated data has been saved to {output_file}") #Let the user know that the process is done