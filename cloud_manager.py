import re
import os
from script import Script
from google.cloud import storage
from decouple import config

class Cloud_Manager:
    def get_file_name(file_path):
        return re.match(r'.*/(.+)', file_path).group(1)

    def upload_PDF(file_path):
        if file_path[-3:] != "pdf":
            print("File must be in PDF format")
            raise
            return

        if file_path[:2] == "./":
            file_path = "./" + file_path

        bucket_name = config("BUCKET_NAME")
        file_name = Cloud_Manager.get_file_name(file_path)

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        blob.upload_from_filename(file_path)

    def process_PDF(src_file_name):
        bucket_name = config("BUCKET_NAME")
        src_file_uri = f"gs://{bucket_name}/{src_file_name}"
        dst_file_uri = f"gs://{bucket_name}/{src_file_name}"[:-4] + "-result"

        Script.async_detect_document(src_file_uri, dst_file_uri)

    def download_text(file_name):
        bucket_name = config("BUCKET_NAME")
        dst_file_uri = f"gs://{bucket_name}/{file_name}"[:-4] + "-result"

        if not os.path.isdir("./results"):
            print("not there!")
            os.mkdir("/results")
            print("should be there", os.path.isdir("./results"))

        Script.write_to_text(dst_file_uri, file_name)