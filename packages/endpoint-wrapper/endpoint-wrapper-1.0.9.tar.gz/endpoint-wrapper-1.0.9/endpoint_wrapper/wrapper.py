import json
import time
from confluent_kafka import Producer, Consumer
from endpoint_wrapper.util.basic import without_keys, run_cmd
from endpoint_wrapper.util.handle_error import handle_error
import signal

def kafka_wrapper( key, model, runner, group_id, subscribe_to, bootstrap_server_url='localhost:9092',
                   output_exclude_keys=None, log_level=0):
    consumer = None
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGINT, original_sigint_handler)
    try:
        output_exclude_keys = [] if output_exclude_keys is None else output_exclude_keys

        producer = Producer({'bootstrap.servers': bootstrap_server_url})
        consumer = Consumer({
            'group.id': group_id, #'detector_1',
            'bootstrap.servers': bootstrap_server_url
        })
        consumer.subscribe(subscribe_to)  #['frame']
   
        def handler():
            consumer.close()
        signal.signal(signal.SIGINT, handler)
        time.sleep(2)
        start_time = time.time()
        while True:
            msg = consumer.poll(1.0)
            current_time = time.time()
            if msg is None:
                if current_time - start_time > 2:
                    start_time = current_time
                    if log_level > 0:
                        print(bootstrap_server_url)
                        print('No message')
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            payload = json.loads(msg.value().decode("utf-8"))
            if log_level > 0:
                print(payload['frame_idx'])

            result = runner(model=model, input=payload)
            output_payload = without_keys(payload, *output_exclude_keys)
            produced_message = { **output_payload, 'result': result }
            print(produced_message)

            producer.produce('detection-result',
                             key=key,
                             value=json.dumps(produced_message).encode('utf-8')
                             )
            producer.poll(0)

            start_time = current_time
        consumer.close()
    except KeyboardInterrupt:
        print("CTRL+C")
    except Exception as ex:
        print(ex)
        consumer.close()
        handle_error(ex)
    finally:
        print('finally')

