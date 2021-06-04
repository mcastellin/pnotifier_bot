import logging
import boto3
import sys
import os

TABLE_NAME = "subscriptions"

DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:4566")
ddb = boto3.resource(
    "dynamodb",
    aws_access_key_id="00000",
    aws_secret_access_key="0000",
    endpoint_url=DYNAMODB_ENDPOINT_URL,
    region_name="eu-west-1",
)


def get_subscription(chat_id):
    subscriptions = ddb.Table(TABLE_NAME)
    response = subscriptions.get_item(
        Key={"chat_id": chat_id, "subscription_status": "true"}
    )
    if "Item" in response:
        return response["Item"]
    else:
        return None


def add_subscription(chat_id, first_name):
    subscriptions = ddb.Table(TABLE_NAME)
    subscriptions.put_item(
        Item={
            "chat_id": chat_id,
            "first_name": first_name,
            "subscription_status": "true",
        }
    )


def remove_subscription(chat_id):
    subscr = get_subscription(chat_id)
    if subscr is not None:
        subscriptions = ddb.Table(TABLE_NAME)
        subscriptions.delete_item(
            Key={"chat_id": chat_id, "subscription_status": "true"}
        )
        return True

    return False


def _create_table():
    subscriptions = ddb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "chat_id", "KeyType": "HASH"},
            {"AttributeName": "subscription_status", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "chat_id", "AttributeType": "N"},
            {"AttributeName": "subscription_status", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    subscriptions.meta.client.get_waiter("table_exists").wait(TableName=TABLE_NAME)


# Create new table if does not exists
if TABLE_NAME not in list(map(lambda t: t.name, ddb.tables.all())):
    logging.info(f"Creating table {TABLE_NAME} in DynamoDb")
    _create_table()

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "delete":
        print("Deleting subscriptions table!")
        subscriptions = ddb.Table(TABLE_NAME)
        subscriptions.delete()
