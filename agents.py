# agents.py

import csv 
import anthropic
from prompts import *
import logging
import os
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(filename='csv_generator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable to store the API key
ANTHROPIC_API_KEY = None

def set_api_key(api_key: str) -> None:
    global ANTHROPIC_API_KEY
    ANTHROPIC_API_KEY = api_key
    logging.info("API key set successfully")

def get_anthropic_client() -> anthropic.Anthropic:
    if not ANTHROPIC_API_KEY:
        logging.error("Anthropic API key not set")
        raise ValueError("Anthropic API key not set. Please set it using set_api_key() function.")
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def read_csv(file_path: str) -> List[List[str]]:
    try:
        with open(file_path, "r", newline="") as csvfile:
            csv_reader = csv.reader(csvfile)
            data = [row for row in csv_reader]
        logging.info(f"Successfully read CSV file: {file_path}")
        return data
    except FileNotFoundError:
        logging.error(f"CSV file not found: {file_path}")
        raise
    except csv.Error as e:
        logging.error(f"Error reading CSV file {file_path}: {str(e)}")
        raise

def save_to_csv(data: str, output_file: str, headers: List[str] = None) -> None:
    try:
        mode = 'w' if headers else 'a'
        with open(output_file, mode, newline="") as f:
            writer = csv.writer(f)
            if headers:
                writer.writerow(headers)
            for row in csv.reader(data.splitlines()):
                writer.writerow(row)
        logging.info(f"Successfully saved data to CSV file: {output_file}")
    except csv.Error as e:
        logging.error(f"Error writing to CSV file {output_file}: {str(e)}")
        raise
    except IOError as e:
        logging.error(f"IOError while writing to CSV file {output_file}: {str(e)}")
        raise

def analyzer_agent(sample_data: str) -> str:
    try:
        client = get_anthropic_client()
        sonnet = "claude-3-5-sonnet-20240620"
        message = client.messages.create(
            model=sonnet,
            max_tokens=400,
            temperature=0.1,
            system=ANALYZER_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
                }
            ]
        )
        logging.info("Successfully completed analysis")
        return message.content[0].text
    except anthropic.APIError as e:
        logging.error(f"Anthropic API error in analyzer_agent: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in analyzer_agent: {str(e)}")
        raise

def generator_agent(analysis_result: str, sample_data: str, num_rows: int = 30) -> str:
    try:
        client = get_anthropic_client()
        sonnet = "claude-3-5-sonnet-20240620"
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
        logging.info(f"Successfully generated {num_rows} rows of data")
        return message.content[0].text
    except anthropic.APIError as e:
        logging.error(f"Anthropic API error in generator_agent: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in generator_agent: {str(e)}")
        raise