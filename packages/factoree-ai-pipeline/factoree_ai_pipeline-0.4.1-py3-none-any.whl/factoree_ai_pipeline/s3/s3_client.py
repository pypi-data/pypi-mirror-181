import boto3


class S3Client:
    def __init__(
            self,
            s3_access_key: str,
            s3_secret_key: str
    ):
        session = boto3.Session(
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key
        )
        self.s3 = session.resource('s3')
        self.s3_client = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)

    def put(self, bucket_name: str, filename: str, document: str) -> bool:
        return self.__verify_request(self.s3.Object(bucket_name, filename).put(Body=document))

    def delete(self, bucket_name: str, filename: str) -> bool:
        return self.__verify_request(self.s3.Object(bucket_name, filename).delete())

    def copy(self, copy_source: dict[str, str], dst_bucket: str, dst_filename: str) -> bool:
        self.s3.meta.client.copy(copy_source, dst_bucket, dst_filename)
        return self.key_exists(dst_bucket, dst_filename)

    def key_exists(self, bucket_name: str, filename: str) -> bool:
        res = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=filename)
        return True if 'Contents' in res else False

    @staticmethod
    def __verify_request(res_metadata: dict) -> bool:
        res = res_metadata.get('ResponseMetadata')
        return True if 200 <= res.get('HTTPStatusCode') < 300 else False
