import json
from jsonschema import validate
from django.http import HttpResponse, JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from config_service.settings import GOOGLE_CLOUD_STORAGE_BUCKET_NAME
from config_api.gcs_storage import GoogleCloudStorage


def config_view(request):
    if request.method == 'GET':
        try:
            config_file = default_storage.open('configuration-file.json', 'r')
            config_data = config_file.read()
            config_file.close()
            return JsonResponse(json.loads(config_data))
        except Exception as e:
            return HttpResponse(status=500, content='Error retrieving configuration file')

    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            with open('config_api/config_schema.json') as schema_file:
                schema = json.load(schema_file)
            validate(instance=request_data, schema=schema)

            file_content = json.dumps(request_data)
            file_name = 'configuration-file.json'
            file = ContentFile(file_content)
            storage = GoogleCloudStorage(bucket_name=GOOGLE_CLOUD_STORAGE_BUCKET_NAME)
            storage.save(file_name, file)
            return HttpResponse(status=200, content='File saved successfully')
        except Exception as e:
            return HttpResponse(status=400, content='Invalid' + str(e))
