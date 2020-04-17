import sys, getopt
import json,re,os

def main(argv):
    try:
      opts, args = getopt.getopt(argv,"hf:m:o:",["folder=","mainfile=", "outputfile"])
    except getopt.GetoptError:
      print ('MergeSchema.py -f <folder> -m <mainfile> -o <outputfile>')
      sys.exit(2)
    schemafolder = ""
    mainfile = ""
    outputfile = ""
    for opt, arg in opts:
        if opt == '-h':
            print ('MergeSchema.py -f <folder> -m <mainfile>')
            sys.exit()
        elif opt in ("-f", "--folder"):
            schemafolder = arg
        elif opt in ("-m", "--ofile"):
            mainfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg

    mainfilename = schemafolder + '\\' + mainfile
    mainjo = GetReplaceJsonObject(mainfilename)
    mainjo['definitions'] = {}

    for filename in os.listdir(schemafolder):
        if filename.endswith(".json") and filename != mainfile:
            defFile = schemafolder + '\\' + filename
            defObj = GetReplaceJsonObject(defFile)
            mainjo['definitions'][os.path.splitext(filename)[0]] = defObj['definition']

    with open(outputfile, 'w') as outputjson:
        json.dump(mainjo, outputjson, indent=4)

def GetReplaceJsonObject(filename):
    with open(filename) as jsonfile:
        jo = json.load(jsonfile)
        return GetReplaceJsonObjectIte(jo)

def GetReplaceJsonObjectIte(jsonobj):
    for key in jsonobj:
        if key == '$ref':
            ref = jsonobj['$ref']
            name = re.match(r'([a-zA-Z0-9]+).json',ref).group(1)
            jsonobj['$ref'] = '#definitions/' + os.path.splitext(name)[0]
        elif type(jsonobj[key]) is dict:
            jsonobj[key] = GetReplaceJsonObjectIte(jsonobj[key])
        elif type(jsonobj[key]) is list:
            for i in range(len(jsonobj[key])):
                if type(jsonobj[key][i]) is dict:
                    jsonobj[key][i] = GetReplaceJsonObjectIte(jsonobj[key][i])
    return jsonobj


if __name__ == "__main__":
    main(sys.argv[1:])