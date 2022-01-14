import boto3
from shared.jacht import Jacht

client = boto3.resource('dynamodb').Table("jachty")


def dynamo_put_example_jachts():
    jachts = []
    for i in range(0,10):
        jacht = Jacht()
        jacht.set_example_values(f"{str(i)}-index", f"jacht numer {i}", f"{str(i * 1000)},00")
        jachts.append(jacht)

    for jacht in jachts:
        client.put_item(
            Item=jacht.get_item()
        )


if __name__ == '__main__':
    dynamo_put_example_jachts()
