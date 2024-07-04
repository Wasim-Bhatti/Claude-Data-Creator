# prompts.py 

ANALYZER_SYSTEM_PROMPT = """You are an AI agent that analyzes the CSV provided by the user. 
The focus of your analysis should be on what the data is, how it is formatted, what each column stands for, and how new data should be generated """

GENERATOR_SYSTEM_PROMPT = """ YOu are an AI agent that generates new CSV rows based on analysis results and sample data.
Follow the exact formatting and do not output any extra text. You only output formatted data, never any other text."""

ANALYZER_USER_PROMPT = """Analyze the structure and patterns of this sample dataset

{sample_data}

Provide a concise summary of the following: 
1. Formatting of the dataset, be completely clear when describing the structure of the CSV.
2. What the dataset represents, what each column stands for. 
3. How new data should look like, based on the patterns shown in the data / and the ones you have analyzed.

"""

GENERATOR_USER_PROMPT = """Generate {num_rows} new CSV rows based on this analysis and sample data

Analysis:
{analysis_result}

Sample Data:
{sample_data}

Use the exactly the same formatting as the original data. Output only the generated rows, no extra text.

DO NOT INCLUDE ANY TXT BEFORE OR AFTER THE DATA. JUST START BY OUTPUTTING THE NEW ROWS. NO EXTRA TEXT!!!

"""


