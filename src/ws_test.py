import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json


ColumnNames = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style", "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight", "engine-type", "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm", "city-mpg", "highway-mpg", "price"]

def set_input():
    pass

def call_ws():
    # feature that are considered in the training module
    my_input1 = ["3", "", "audi", "diesel", "std", "two", "convertible", "rwd", "front", "88.6", "168.8", "64.1", "48.8", "2548", "dohc", "four", "130", "mpfi", "3.47", "2.68", "9", "511", "5000", "21", "27", "0"]
    my_input2 = ["3", "", "audi", "diesel", "std", "two", "convertible", "rwd", "front", "88.6", "168.8", "64.1", "48.8", "2548", "dohc", "four", "130", "mpfi", "3.47", "2.68", "9", "111", "5000", "21", "27", "0"]
    my_input_list = []
    my_input_list.append(my_input1)
    my_input_list.append(my_input2)
    my_data = {"Inputs":{
        "input1":{
            "ColumnNames": ColumnNames,
            "Values":my_input_list
        },
    }, "GlobalParameters": {}
    }

    body = str.encode(json.dumps(my_data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/00c2c1f669144e68b0f320e4dc1d5d23/services/3c2281e1b1ea4311bb324491218f4df2/execute?api-version=2.0&details=true'
    api_key = 'vmXLRKhaeo4fxYtekazgEZ16VAKqGxP9LPp+Dkm25nKY3EQMmGd9k0NWjS9mlhuKWnzz4f02YxOGznz3C7LcLw=='  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    req = urllib2.Request(url, body, headers)
    try:
        response = urllib2.urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers)
        # response = urllib.request.urlopen(req)

        result = response.read()
        resposnse_dic = json.loads(result)      # dictinary with key="Results"
        results_dic = resposnse_dic["Results"]  # dictinary with key="output1"
        output_dic = results_dic["output1"]     # keys are "type" (-> table), "value" (-> ColumnNames, ColumnTypes, Values)
        value_dic = output_dic["value"]         # keys are "ColumnNames", "ColumnTypes", "Values")

        column_names = value_dic["ColumnNames"] # Column name returned
        column_types = value_dic["ColumnTypes"] # Column type returned
        values = value_dic["Values"]            # List of the same length of my_input_list


        for v in values:
            print "Output found"
            for i in range(len(column_names)):
                if i == len(column_names)-1:
                    predicted_value = v[i].split(".")[0]
                    scored_label = v[i].split(".")[1]
                    print "\t* Predicted value:", predicted_value, "(with score 0."+str(scored_label)+") *"
                else:
                    print "\t",column_names[i]+"("+column_types[i]+"):", v[i]


    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        print(json.loads(error.read()))


call_ws()