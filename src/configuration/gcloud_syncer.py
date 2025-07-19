import os

class GCloudSyncer:

    def sync_folder_to_gcloud(self, gcp_bucket_url, filepath, filename):
        command = f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_url}/"
        exit_code = os.system(command)
        if exit_code != 0:
            print("Upload failed.")
        else:
            print("Upload successful.")

    def sync_folder_from_gcloud(self, gcp_bucket_url, filename, destination):
        command = f"gsutil cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        exit_code = os.system(command)
        if exit_code != 0:
            print("Download failed.")
        else:
            print("Download successful.")

    