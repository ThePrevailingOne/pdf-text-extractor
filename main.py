import os
from cloud_manager import Cloud_Manager

def main():
    file_path = input("Enter path to PDF for extraction: ")
    file_name = Cloud_Manager.get_file_name(file_path)

    print("")

    Cloud_Manager.upload_PDF(file_path)
    Cloud_Manager.process_PDF(file_name)
    Cloud_Manager.download_text(file_name)

    print("")
    print(f"extracted file has been stored successfully in results/{file_name}.")

if __name__ == "__main__":
    main()