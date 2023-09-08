from os import getenv

from pytape import api


user_key = getenv('TAPE_USER_KEY')

client = api.BearerClient(user_key)

# Retrieve a record
record = client.Record.find(9590591)

app_id = 21156

# Create a record
payload = {
	"fields": {
		"title": "Fulano Sicrano da Silva"
    }
}
created_rec = client.Record.create(app_id, payload)

# Update a record
payload = {
    'fields': {
        'title': 'Fulano Beltrano Soares'
    }
}
updated_rec = client.Record.update(created_rec['id'], payload)

# Delete a record. It doesn't return anything
client.Record.delete(created_rec['id'])

# Restore a record
restored_rec = client.Record.restore(created_rec['id'])

# Retrieve records for an app
options = {"limit": 2, "sort_by": "title", "sort_desc": True}
records = client.App.get_records(app_id, **options)['records']

filter_payload = {
    "filters": [
        {
            "field_id": "192075",
            "field_type": "single_text",
            "match_type": "contains",
            "values": [
                {
                    "value": "Soares"
                }
            ],
            "type": "text"
        }
    ]
}

filtered_recs = client.Record.filter(app_id, filter_payload)

print(created_rec)
