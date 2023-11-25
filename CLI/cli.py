import sys, os, json

"""
Example usage:
python cli.py "song a, song b"
"""

site = "http://127.0.0.1:32194"

def usage():
    print("The correct usage of this app is python cli.py \"song a, song b, song c\"")
    exit()

argv = sys.argv

if(len(argv) != 2):
    usage()

songs = json.dumps({'songs': argv[1].split(", ")})

cmd = "wget --header='Content-Type: application/json' --post-data '" + str(songs) + "' " + site + "/api/recommend/ -q -O -"

os.system(cmd)
