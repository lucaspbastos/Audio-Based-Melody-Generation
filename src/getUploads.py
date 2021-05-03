import sys, os, json

input = sys.argv[1]
files = {}
i=0

if os.path.exists(input):
    for file in os.listdir(input):
        files[i] = input+"/"+file
        i+=1
    
print(json.dumps(files))
sys.stdout.flush()