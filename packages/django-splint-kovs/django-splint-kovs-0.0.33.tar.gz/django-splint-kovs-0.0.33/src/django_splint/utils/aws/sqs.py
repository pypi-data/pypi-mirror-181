import json
from django.conf import settings

import boto3

class AWSSQSHandler:
    """AWS ECS service handler."""

    service_name = 'sqs'
    client = boto3.client(
        service_name=service_name,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION,
    )

    def send_message(self, queue_url, data, **kwargs):
        return self.client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(data),
            **kwargs
        )