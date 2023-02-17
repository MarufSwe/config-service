import json
from jsonschema import validate, exceptions
from django.test import Client


def test_json_schema_validation():
    client = Client()

    # Valid JSON
    valid_data = {
        "firstName": "Hero",
        "secondName": "Alom",
        "ageInYears": 30,
        "address": "Bagura, Bangladesh",
        "creditScore": 834
    }
    response = client.post('/config', json.dumps(valid_data), content_type='application/json')
    assert response.status_code == 200

    # Invalid JSON
    invalid_data = {
        "firstName": "Hero",
        "secondName": "Alom",
        "ageInYears": "30",
        "address": "Bagura, Bangladesh",
        "creditScore": 834
    }
    response = client.post('/config', json.dumps(invalid_data), content_type='application/json')
    assert response.status_code == 400
    assert 'Invalid' in response.content.decode('utf-8')

    # Invalid schema
    with open('config_api/config_schema.json') as schema_file:
        schema = json.load(schema_file)
    del schema['properties']['firstName']
    del schema['required'][0]
    invalid_data = {
        "secondName": "Alom",
        "ageInYears": 30,
        "address": "Bagura, Bangladesh",
        "creditScore": 834
    }
    try:
        validate(instance=invalid_data, schema=schema)
    except exceptions.ValidationError:
        pass
    else:
        assert False, 'Validation should have failed but did not'

# for run the script use "python manage.py test_config_api.py"
