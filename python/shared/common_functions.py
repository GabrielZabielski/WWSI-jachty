import boto3
from shared.jacht import Jacht


def set_values_from_dynamo(jacht_obj: Jacht, dynamodb_item: dict):
    jacht_obj.jacht_id = dynamodb_item["jacht"].split("-")[0]
    jacht_obj.name = dynamodb_item["name"]
    jacht_obj.price = str(dynamodb_item["price"])
    jacht_obj.desc = dynamodb_item["desc"]
    jacht_obj.reservation = dynamodb_item["reservation"]


def get_jacht(jacht_id: str = ""):
    client = boto3.resource('dynamodb').Table("jachty")
    response = client.scan()
    # if not jacht_id:
    #     response = client.scan()
    # else:
    # TODO idk why doesn't work...
    # response = client.get_item(
    #     Key={
    #         "jacht": {
    #             "ComparisonOperator": "EQ",
    #             "AttributeValueList": [{"S": "1"}]
    #         }
    #     }
    # )
    # response = client.query(
    #     Select='ALL_ATTRIBUTES',
    #     FilterExpression="jacht = :j",
    #     ExpressionAttributeValues={
    #         "jacht": {"S": "1"}
    #     }
    # )
    # response = client.scan(
    #     ScanFilter={
    #         "jacht": {
    #             "AttributeValueList": [{"S": "1"}],
    #             "ComparisonOperator": "EQ"
    #         }
    #     }
    # )
    jachts = []
    # print(response)
    for item in response["Items"]:

        jacht = Jacht()
        set_values_from_dynamo(jacht, item)
        jachts.append(jacht)
    if jacht_id:
        return [j.get_item() for j in jachts if j.jacht_id == jacht_id]
    return [jacht.get_item() for jacht in jachts]


def get_email(token):
    client = boto3.client('cognito-idp')
    response = client.get_user(
        AccessToken=token
    )
    return [a["Value"] for a in response["UserAttributes"] if a["Name"] == "email"][0]


if __name__ == '__main__':
    print(len(get_jacht()))
    print(len(get_jacht("1")))
