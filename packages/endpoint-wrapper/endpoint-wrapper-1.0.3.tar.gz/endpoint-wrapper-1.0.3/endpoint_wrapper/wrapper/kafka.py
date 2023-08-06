import json
import time
from confluent_kafka import Producer, Consumer
from .util import without_keys

def kafka_wrapper( key, model, input_handler, runner, group_id, subscribe_to, bootstrap_server_url='localhost:9092',
                    output_exclude_keys=None):

    output_exclude_keys = [] if output_exclude_keys is None else output_exclude_keys

    producer = Producer({'bootstrap.servers': bootstrap_server_url})
    frame_consumer = Consumer({
        'group.id': group_id, #'detector_1',
        'bootstrap.servers': bootstrap_server_url
    })
    frame_consumer.subscribe(subscribe_to)  #['frame']
    time.sleep(2)

    while True:
        msg = frame_consumer.poll()
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        payload = json.loads(msg.value().decode("utf-8"))

        result = runner(model=model, input=input_handler(payload))
        output_payload = without_keys(payload, *output_exclude_keys)
        produced_message = { **output_payload, 'result': result }

        try:
            producer.produce('detection-result',
                             key=key,
                             value=json.dumps(produced_message).encode('utf-8')
                             )
            producer.poll(0)
        except Exception as e:
            print(f"Producer error: {str(e)}")

    frame_consumer.close()