#!./venv/bin/python2
import datetime
from pprint import pprint
import time
import boto3
import dronekit
ADDRESS = "/dev/ttyUSB0"
BAUD_RATE = 57600
NEEDED_PROPERTIES = {
    "ATTITUDE": ("mavpackettype", "pitch", "roll", "yaw"),
    "OPTICAL_FLOW_RAD": (
        "distance",
        "integrated_x",
        "integrated_xgyro",
        "integrated_y",
        "integrated_ygyro",
        "integrated_zgyro",
        "mavpackettype")
}
# REFRESH_PERIOD = datetime.timedelta(milliseconds=250)
fresh_data = {}
REGION = "eu-west-1"
TABLE_NAME = "drone_table"

DYNAMODB = boto3.client("dynamodb", region_name=REGION)


def connect(address):
    """Connects to a vehicle and returns its wrapper object"""
    print("connecting to vehicle on: {}".format(address))
    return dronekit.connect(ADDRESS, baud=BAUD_RATE, wait_ready=False)


def filter_payload(payload):
    """Filters payload to contain only needed data"""
    return {key: payload[key]
            for key in payload if key in NEEDED_PROPERTIES[payload["mavpackettype"]]}


def handle(self, name, msg):
    """Handles a message from the vehicle"""
    # print(name)
    payload = msg.to_dict()
    # pprint(payload, indent=2)
    payload = filter_payload(payload)
    fresh_data[name] = payload
    # pprint(payload)
    # put_payload(payload)


def loop(f=None, seconds=60):
    """Keeps the script running"""
    while True:
        time.sleep(seconds)
        if f is not None:
            f()


def put_payload(payload):
    """Saves a payload to the database"""
    item = to_item(payload)
    pprint(item)
    DYNAMODB.put_item(
        Item=item,
        TableName=TABLE_NAME
    )


def send():
    for name in fresh_data:
        put_payload(fresh_data[name])


def to_item(payload):
    """Transforms a payload into the DynamoDB-expected form"""
    return {key: to_property(payload[key]) for key in payload}


def to_property(value):
    """Transforms a value into the DynamoDB-expected form"""
    if isinstance(value, (int, long, float)):
        return {"N": str(value)}
    elif isinstance(value, basestring):
        return {"S": str(value)}
    else:
        raise ValueError("Wrong property type!")


if __name__ == "__main__":
    vehicle = connect(address=ADDRESS)
    for needed_event in NEEDED_PROPERTIES:
        vehicle.add_message_listener(needed_event, handle)
    # vehicle.add_message_listener("OPTICAL_FLOW_RAD", handle_ofr)
    # dummy_data = {
    #     'distance': 2.183000087738037,
    #     'integrated_x': 0.0,
    #     'integrated_xgyro': 0.0,
    #     'integrated_y': -0.0,
    #     'integrated_ygyro': -0.0,
    #     'integrated_zgyro': 0.0,
    #     'integration_time_us': 0,
    #     'mavpackettype': 'OPTICAL_FLOW_RAD',
    #     'quality': 0,
    #     'sensor_id': 0,
    #     'temperature': 3400,
    #     'time_delta_distance_us': 16980,
    #     'time_usec': 2176498438
    # }
    # put_payload(dummy_data)
    loop(f=send, seconds=0.1)
    vehicle.close()
    print("Goodbye!")
