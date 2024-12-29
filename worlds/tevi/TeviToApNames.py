import json,pkgutil,os


TeviToApNames = json.loads(pkgutil.get_data(__name__, os.path.join('resources', 'ItemToReal.json')).decode())
ApNamesToTevi = {data: name for name, data in TeviToApNames.items()}