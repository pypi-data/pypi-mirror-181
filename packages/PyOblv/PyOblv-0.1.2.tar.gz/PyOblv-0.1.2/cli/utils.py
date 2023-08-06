import os

from rich.console import Console

from oblv import OblvClient

cred_file_path = os.path.join(os.path.expanduser('~'),'.oblv','credentials')

console = Console()

def read_credentials():
    with open(cred_file_path,'r') as f:
        contents = f.read()
        contents = contents.split("\n")
        for c in range(2):
            contents[c]=contents[c].split(" = ")
        client = OblvClient(oblivious_user_id=contents[0][1],token=contents[1][1])
    return client


def render_output(object):
    if type(object)==list:
        console.print_json(data=[x.to_dict() for x in object])
    else:
        print(object)
