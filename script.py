import json
import re
from google.cloud import vision
from google.cloud import storage
from decouple import config

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=config("GOOGLE_APPLICATION_CREDENTIALS")

class Script:
    def async_detect_document(gcs_source_uri, gcs_destination_uri):
        mime_type = 'application/pdf'

        batch_size = 100

        client = vision.ImageAnnotatorClient()

        feature = vision.Feature(
            type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

        gcs_source = vision.GcsSource(uri=gcs_source_uri)
        input_config = vision.InputConfig(
            gcs_source=gcs_source, mime_type=mime_type)

        gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
        output_config = vision.OutputConfig(
            gcs_destination=gcs_destination, batch_size=batch_size)

        async_request = vision.AsyncAnnotateFileRequest(
            features=[feature], input_config=input_config,
            output_config=output_config)

        operation = client.async_batch_annotate_files(
            requests=[async_request])

        print('Waiting for the operation to finish.')
        operation.result(timeout=420)

    def write_to_text(gcs_destination_uri, local_file_name):
        storage_client = storage.Client()

        match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
        bucket_name = match.group(1)
        prefix = match.group(2)

        bucket = storage_client.get_bucket(bucket_name)

        blob_list = list(bucket.list_blobs(prefix=prefix))

        open(f"results/{local_file_name[:-4]}.txt", "w")

        for blob in blob_list:
            print("")
            print(blob.name)
            print("")

        for blob in blob_list:
            output = blob

            json_string = output.download_as_string()
            response = json.loads(json_string)

            page = 1
            print("so, we meet again")
            for page_response in response['responses']:

                first_page_response = page_response

                try:
                    annotation = first_page_response['fullTextAnnotation']
                except(KeyError):
                    print("No annotation found in this page.")

                print(f"Page {page}\n \n")
                print(annotation['text'])
                print("\n\n")

                with open(f"results/{local_file_name[:-4]}.txt", "a+", encoding="utf-8") as f:
                    f.write(f"Page {page}\n \n")
                    f.write(annotation['text'])
                    f.write("\n\n")
                    page += 1