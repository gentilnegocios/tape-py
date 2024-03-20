from os import getenv

from pytape import api


user_key = getenv('TAPE_USER_KEY')

client = api.BearerClient(user_key)

# Retrieve a record
record = client.Record.find(9590591)

# Create a record
payload = {
	"fields": {
		"title": "Title"
    }
}
created_rec = client.Record.create(1234, payload)

# Update a record
payload = {
    'fields': {
        'title': 'Title 2'
    }
}
updated_rec = client.Record.update(created_rec['record_id'], payload)

# Delete a record. It doesn't return anything
client.Record.delete(created_rec['record_id'])

# Restore a record
restored_rec = client.Record.restore(created_rec['record_id'])

# Retrieve records for an app
options = {"limit": 2, "sort_by": "title", "sort_desc": True}
records = client.App.get_records(1234, **options)['records']

filter_payload = {
    "filters": [
        {
            "field_id": "192075",
            "field_type": "single_text",
            "match_type": "contains",
            "values": [
                {
                    "value": "Value"
                }
            ],
            "type": "text"
        }
    ]
}

filtered_recs = client.Record.filter(1234, filter_payload)

print(created_rec)
