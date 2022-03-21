import environ
import os


class s3Config:
    def get_s3_client(self):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access=os.environ["AWS_SECRET_ACCESS_KEY"],
        )

        return s3_client

    def get_historical(self):
        return 'us/us-counties.csv'

    def get_live(self):
        return 'us/us-counties-live.csv'

    def get_avg(self, year=2022):
        return 'us-rolling-avg/us-' + str(year) + '.csv'
