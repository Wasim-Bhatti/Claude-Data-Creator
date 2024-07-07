# prompts.py 

ANALYZER_SYSTEM_PROMPT = """You are an AI agent that analyzes the structure of the CSV provided by the user. 
The focus of your analysis should be on how the data is formatted, what the data exactly is, and what each column stands for, and how exactly the new data should be generated.
You also remind the generator agent about the common rules of how CSVs are formatted so there is no error is how data is generated.  """

GENERATOR_SYSTEM_PROMPT = """You are an AI agent that generates new CSV rows based on analysis results and sample data. You make sure to follow all rules required for CSVs so that the data is not generated incorrectly. """

ANALYZER_USER_PROMPT = """Analyze the structure and patterns of this sample dataset

{sample_data}

Provide a concise and accurate summary of the following: 
1. Formatting of the dataset, be completely clear when describing the structure of the CSV, such as how many columns, and other important information.
2. What the dataset represents, what each column stands for clearly. 
3. How new data should look like, based on the patterns shown in the data.

"""

GENERATOR_USER_PROMPT = """Generate {num_rows} new CSV rows based on this analysis and sample data, making sure to surround each entry in each column with quotations, so that elements with multiple commas in them still appear as one entity:

Analysis:
{analysis_result}

Sample Data:
{sample_data}

Use the exactly the same formatting as the original data. Output only the generated rows, keeping in mind all rules that CSV files follow (such as how to deal with commas in columns)

DO NOT INCLUDE ANY TXT BEFORE OR AFTER THE DATA. JUST START BY OUTPUTTING THE NEW ROWS. NO EXTRA TEXT, NO DATA OUTSIDE THEIR COLUMNS.

"""


