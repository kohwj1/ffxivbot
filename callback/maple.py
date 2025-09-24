import json, os, requests
from dotenv import load_dotenv

load_dotenv()

openapi_maple_token = os.getenv('openapi_maple_token')
base_uri = 'https://open.api.nexon.com/maplestory/v1'

def get_character(character):
    res_ocid = requests.request("GET", f"{base_uri}/id?character_name={character}", headers={'x-nxopen-api-key': openapi_maple_token})
    
    if res_ocid.status_code != 200:
        return None
    
    ocid = json.loads(res_ocid.text)['ocid']

    res_character = requests.request("GET", f"{base_uri}/character/basic?ocid={ocid}", headers={'x-nxopen-api-key': openapi_maple_token})

    if res_character.status_code != 200:
        return None

    character_info = json.loads(res_character.text)
    return character_info

if __name__ == '__main__':
    print(get_character('무난한밀크티'))