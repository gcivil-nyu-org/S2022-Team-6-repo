# import environ
import os
import boto3
import pandas as pd


class s3Config:
    def get_s3_client(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )

    def read_data(self, key):
        response = self.s3_client.get_object(
            Bucket=os.environ["AWS_S3_BUCKET"], Key=key
        )
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            dataframe = pd.read_csv(response.get("Body"))
        else:
            raise Exception("No bucket")  # pragma: no cover

        return dataframe

    def get_historical(self):
        return self.read_data("us/us-counties.csv")

    def get_live(self):
        return self.read_data("us/us-counties-live.csv")

    def get_avg(self, year=2022):
        return self.read_data(
            "us-rolling-avg/us-" + str(year) + ".csv"
        )  # pragma: no cover


# class s3ImageConfig:
#     def get_s3_client(self):
#         self.s3_client = boto3.client(
#             "s3",
#             aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
#             aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
#         )

#     def delete_user_image(self, username, key):
#         s3.Object('your-bucket', 'your-key').delete()
