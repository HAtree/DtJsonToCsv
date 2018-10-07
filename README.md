# DtJsonToCsv
Converts JSON output from the Dynatrace Timeseries API into a CSV file, which can then be opened by excel to create graphs, or manipulate the data further. 

_Requires Python 3_

To use, call the script from the command line and pass in a JSON file from the timeseries API:
`py DTJsonToCsv.py easyTravelResponseTimes.json`

optionally pass in an output file directory and the -e flag to convert the unix timestamps from the API into excel format
`py DTJsonToCsv.py -e easyTravelResponseTimes.json -o easyTravelResponseTimes.csv`

```bash
usage: JsonToCsv-v1.py [-h] [-o OUTPUT_FILE] [-e] inputJSONFile

Converts a JSON File from a Dynatrace Timeseries API to a CSV file.

positional arguments:
  inputJSONFile         Path to JSON file to be convered to CSV

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        where to write the output CSV. If not specified output
                        defaults to 'output.csv' in current directory
  -e, --excel_timestamps
                        if set, converts timestamps into excel format. In
                        excel set cell format to 'DATE' 'TIME' or 'SPECIAL
                        dd:mm:yy hh:MM'
```
