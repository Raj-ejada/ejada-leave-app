import os
import boto3
from ..config import settings

def send_email(to, subject, html_body):
    if settings.ENV == "local":
        print(f"[EMAIL MOCK] To={to} Subject={subject}")
        return
    ses = boto3.client("ses", region_name=settings.AWS_REGION)
    ses.send_email(
        Source=settings.SES_SENDER,
        Destination={"ToAddresses": [to]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Html": {"Data": html_body}}
        }
    )
