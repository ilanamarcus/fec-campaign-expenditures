# FEC expenditure analysis 
## Retrieves visualizes all of the schedule B filings for six different Democratic presidential candidates.

### Set up:
1. Create an anaconda environment using python 3.7
2. pip install requirements.txt
3. create a .env file with the following two properties:
   * KEY=FEC API developer key
   * FEC_URL="https://api.open.fec.gov/v1"

### Run: 
1. aggregate.py uses client.py to request data for specific candidates to create local csvs
2. plot.py reads from csvs created in aggregate and sends plots to plotly 