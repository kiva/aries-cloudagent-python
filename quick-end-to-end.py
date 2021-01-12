import requests
import json
from random import randint
import time 

headers_invitation = {
    'accept': 'application/json',
}

response = requests.post('http://0.0.0.0:8022/connections/create-invitation', headers=headers_invitation)

res_json = json.loads(response.text)

headers_accept_alice = {
    'accept': 'application/json',
    'Content-Type' : 'application/json',
}

alice_data = json.dumps(res_json["invitation"])

response_alice = requests.post('http://0.0.0.0:8032/connections/receive-invitation', headers=headers_accept_alice, data=alice_data)

schema_version_faber = "1.0." + str(randint(0,1000001))

faber_schema = {
     "schema_version" : schema_version_faber,
     "attributes": [ "name", "photo~attach"],
     "schema_name": "ID"
}


faber_schema_request = requests.post("http://0.0.0.0:8022/schemas", headers=headers_accept_alice, data=json.dumps(faber_schema))

schema_response = json.loads(faber_schema_request.text)

print("SCHEMA RESPONSE:\n\n" + str(schema_response) + "\n\n")

schema_id = schema_response["schema_id"]
schema_name = schema_response["schema"]["name"]
schema_version = schema_response["schema"]["version"]
broken_up_schema_id =  schema_id.split(':')
issuer_did = broken_up_schema_id[0]

cred_def = {
  "schema_id": schema_id,
  "tag": 'default',
  "revocation_registry_size": 0,
  "support_revocation": True
}



cred_def_request = requests.post("http://0.0.0.0:8022/credential-definitions", headers=headers_accept_alice, data=json.dumps(cred_def))

time.sleep(5)

print(cred_def_request.text)
cred_def_json = json.loads(cred_def_request.text)

print(str("hello:") +str(cred_def_json))

cred_def_id = cred_def_json["credential_definition_id"]

print("CRED DEF ID:\n\n" + cred_def_id + "\n\n") 


get_faber_connections = requests.get("http://0.0.0.0:8022/connections", headers=headers_invitation)

faber_connections_json = json.loads(get_faber_connections.text)

faber_connection_id = faber_connections_json["results"][0]["connection_id"]

credential_faber = {
  "schema_issuer_did": issuer_did,
  "schema_version": schema_version,
  "schema_id": schema_id,
  "comment": "string",
  "issuer_did": issuer_did,
  "connection_id": faber_connection_id,
  "credential_proposal": {
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
    "attributes": [
      {
        "name": "name",
        "value": "martini"
      },
      {
        "name": "photo~attach",
        "value": "martini" + str(randint(0,10001))
        },
    ]
  },
  "schema_name": schema_name,
  "cred_def_id": cred_def_id,
}


cred_send = requests.post("http://0.0.0.0:8022/issue-credential/send", headers=headers_accept_alice, data=json.dumps(credential_faber))


print(cred_send.text)

# # # # print(accept_faber.text)