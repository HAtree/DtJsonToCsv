import json, os, sys, argparse

def csvLineBuilder(timeStampData, entitiesDict):
    csvLines = []
    
    headerLine = "Timestamp,"
    for entity in sorted(entitiesDict):
        headerLine += (str(entitiesDict[entity]) + ",")
    csvLines.append(headerLine + "\n")
    for timestamp in sorted(timeStampData):
        line = str(timestamp)
        for service in sorted(timeStampData[timestamp]):
            line = line + ", " + str(timeStampData[timestamp][service])
            # print (timestamp, " ", service, " ", timeStampData[timestamp][service])
        line = line + "\n"
        csvLines.append(line)
    return csvLines

def sortDataByTimestamp(data):
    """Returns a dictionary of the results, indexed by timestamp rather than by entity and a dictionary of the entities"""
    flatDataList = []
    timeStampData = {}
    #Grab just the datapoints out of the JSON as a dictionary to make it easier to work with
    dataPoints = data['dataResult']['dataPoints']
    entities = data['dataResult']['entities']
    # Denormalize our data! Write data into a "flatDataList" in the format
    #   (timestamp, service, value)
    for service in dataPoints:
        for dataPoint in dataPoints[service]:
            flatDataList.append( (dataPoint[0], service, dataPoint[1]) )
    # Now write this into a dictionary indexed by timestamp in the format
    #  "timestamp": {service: value, service: value}
    for dataTriple in flatDataList:
        try:
            timeStampData[dataTriple[0]][dataTriple[1]] = dataTriple[2]
        except KeyError:
            # No timestamp for this yet in the list
            timeStampData[dataTriple[0]] = {dataTriple[1]: dataTriple[2]}
    return timeStampData, entities

def writeToCsv(stringLineList, csvFileName):
    """takes a list of strings and writes them to a file line by line"""
    with open(csvFileName, "w") as out_file:
        out_file.writelines(stringLineList)
        out_file.close()

def convertTimestampsToExcel(timeStampDictionary):
    """takes a dictionary where the keys are UNIX Epoch timestamps and replaces the keys in-place with excel timestamp (days since 1/1/1900)
       also it would have been a much better idea to convert these in-place in sortDataByTimestamp() but its late..."""
    for ts in sorted(timeStampDictionary):
        #Convert to excel and replace the old key
        timeStampDictionary[(ts/86400000)+25569] = timeStampDictionary.pop(ts)

def main():
    usageText = "Converts a JSON File from a Dynatrace Timeseries API to a CSV file."
    argumentParser = argparse.ArgumentParser(description=usageText)
    argumentParser.add_argument("inputJSONFile", help="Path to JSON file to be convered to CSV")
    argumentParser.add_argument("-o", "--output_file", help="where to write the output CSV. If not specified output defaults to 'output.csv' in current directory")
    argumentParser.add_argument("-e", "--excel_timestamps", help="if set, converts timestamps into excel format. In excel set cell format to 'DATE' 'TIME' or 'SPECIAL dd:mm:yy hh:MM'", action="store_true")
    args = argumentParser.parse_args()

    INPUTFILE = args.inputJSONFile
    OUTPUTFILE = args.output_file if args.output_file else "output.csv"

    # Read in the downloaded JSON from disk
    print("Current Working Directory: "+ os.getcwd())
    with open(INPUTFILE, "r") as read_file:
        data = json.load(read_file)

    timeStampData, entities = sortDataByTimestamp(data)
    # DEBUG! Pretty Prent that...
    # for timeStamp in sorted(timeStampData):
    #     print("%d: ", timeStamp)
    #     for service in sorted(timeStampData[timeStamp]):
    #         print("\t" + service + ": " + str(timeStampData[timeStamp][service]))

    if (args.excel_timestamps):
        convertTimestampsToExcel(timeStampData)

    outputLines = csvLineBuilder(timeStampData, entities)
    # # DEBUG! Check we CSVified it correctly
    # for line in outputLines:
    #     print(line)
    writeToCsv(outputLines, OUTPUTFILE)

if __name__ == "__main__":
    main()