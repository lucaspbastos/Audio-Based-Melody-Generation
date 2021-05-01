import sys, os

input = sys.argv[1]
output = sys.argv[2]

if os.path.exists(input):
    filename = os.listdir(input)[0]
    os.replace(input+"/"+filename, output+"/"+filename)
    
print(output+"/"+filename)
sys.stdout.flush()