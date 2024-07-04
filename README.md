# Claude-Data-Creator
An A.I Agent (Based on Sonnet 3.5) to generate new synthetic data for LLM tuning purposes.

How to use: 

To start, you need to have Docker installed in your computer. As a recommendation, you should try out the Docker Desktop application, as it makes following your Docker image much easier.

To begin, pull the latest version of the project using your terminal.

`docker pull wasimirl/claude-data-creator-agent:latest`

Next, create a directory from which you want Docker to operate out of. This directory will have a sample of the CSV, for which is an example of synthetic data you are trying to create.
For example, you could just make a "Docker" folder on your desktop, which could look like this:

`docker run -it -v C:\Users\wasim\OneDrive\Desktop\Docker:/app/data wasimirl/claude-data-creator-agent`

How to use the application itself:

1. First, get your your Anthropic API key from your Anthropic account. A quick google search will take you there.
2. When asked for the name of CSV file, enter the name of the CSV file which contains a sample of the CSV data you are trying to create more of.
3. Next, enter the amount of new rows of data you are looking to generate.

And there you go! Once the application is done running, open the directory you gave the A.I Agent, and find your new set of generated data!

