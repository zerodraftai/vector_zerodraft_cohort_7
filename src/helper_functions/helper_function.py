def read_input_text_from_s3(s3_client,bucket_name, file_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    return response['Body'].read().decode('utf-8')


def write_input_text_file_to_s3(s3_client, bucket_name, file_key, content):
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=content)