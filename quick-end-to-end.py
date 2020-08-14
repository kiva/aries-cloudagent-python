import requests
import json
from random import randint
headers_invitation = {
    'accept': 'application/json',
}

response = requests.post('http://0.0.0.0:8022/connections/create-invitation', headers=headers_invitation)


res_json = json.loads(response.text)

# print(res_json["invitation"])


headers_accept_alice = {
    'accept': 'application/json',
    'Content-Type' : 'application/json',
}

alice_data = json.dumps(res_json["invitation"])

response_alice = requests.post('http://0.0.0.0:8032/connections/receive-invitation', headers=headers_accept_alice, data=alice_data)

alice_invitation_response = json.loads(response_alice.text)

alice_connection_id = alice_invitation_response["connection_id"]

url_alice = "http://0.0.0.0:8032/connections/" + alice_connection_id + "/accept-invitation"

accept_alice = requests.post(url_alice, headers_invitation)

get_faber_connections = requests.get("http://0.0.0.0:8022/connections", headers=headers_invitation)

faber_connections_json = json.loads(get_faber_connections.text)

faber_connection_id = faber_connections_json["results"][0]["connection_id"]

print(faber_connection_id + "\n\n")

url_faber= "http://0.0.0.0:8022/connections/"+faber_connection_id+"/accept-request"

accept_faber = requests.post(url_faber, headers_invitation)

schema_version_faber = "1.0." + str(randint(0,101))

faber_schema = {
     "schema_version" : schema_version_faber,
     "attributes": [ "name", "photo~attach"],
     "schema_name": "ID"
}

faber_schema_request = requests.post("http://0.0.0.0:8022/schemas", headers=headers_accept_alice, data=faber_schema)


schema_response = json.loads(faber_schema_request.text)

schema_id = schema_response["schema_id"]
schema_name = schema_response["schema"]["name"]
schema_version = schema_response["schema"]["version"]
broken_up_schema_id =  schema_id.split(':')
issuer_did = broken_up_schema_id[0]

cred_def = {
  "tag": "default",
  "schema_id": schema_response
}

cred_def_request = requests.post("http://0.0.0.0:8022/credential-definitions", headers=headers_accept_alice, data=cred_def)

cred_def_json = json.loads(cred_def_request.txt)

cred_def_id = cred_def_json["credential_definition_id"]


faber_credential = {
  "credential_proposal": {
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
    "attributes": [
      {
        "name": "name",
        "value": "martini"
      },
      {
        "name": "photo~attach",
        "value": "martini"
      },
    ]
  },
  "schema_version": schema_version,
  "schema_name": schema_name,
  "trace": false,
  "schema_id": schema_id,
  "cred_def_id": schema_version,
  "comment": "string",
  "auto_remove": true,
  "issuer_did": issuer_did,
  "schema_issuer_did": issuer_did
}


cred_def_request = requests.post("http://0.0.0.0:8022/issue-credential/create", headers=headers_accept_alice, data= faber_credential)


# print(accept_faber.text)