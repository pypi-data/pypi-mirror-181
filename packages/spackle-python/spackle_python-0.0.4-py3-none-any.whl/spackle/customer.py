import json
import time

from spackle import dynamodb
from spackle.exceptions import SpackleException


class Customer:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def retrieve(customer_id):
        dynamodb_client = dynamodb.get_client()
        response = dynamodb_client.get_item(
            TableName=dynamodb.table_name,
            Key={
                "AccountId": {"S": dynamodb.identity_id},
                "CustomerId": {"S": customer_id},
            },
        )

        data = json.loads(response["Item"]["State"]["S"])
        return Customer(data)

    def enabled(self, key):
        for feature in self.data["features"]:
            if feature["name"] == key:
                return feature["value_enabled"]

        return False

    def limit(self, key):
        for feature in self.data["features"]:
            if feature["name"] == key:
                return feature["value_limit"]

        return 0
