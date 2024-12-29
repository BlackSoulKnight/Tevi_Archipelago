import json,pkgutil,os

def get_world_directory():
    return os.path.dirname(os.path.abspath(__file__))

TeviToApNames = json.loads(pkgutil.get_data(__name__, os.path.join('resources', 'ItemToReal.json')).decode())
ApNamesToTevi = {data: name for name, data in TeviToApNames.items()}