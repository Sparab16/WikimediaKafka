import json

from kafka import KafkaConsumer

from creds_config.kafka_connect_creds import *
from creds_config.kafka_config import *
from project.wikimedia.Opensearch.opensearch import OpensearchClass


class WikimediaConsumerClass:

    @staticmethod
    def get_config() -> dict:
        config = dict()

        # Kafka server connection configs
        config['bootstrap_servers'] = bootstrap_servers
        config["security_protocol"] = "SASL_SSL"
        config["sasl_mechanism"] = "PLAIN"
        config["sasl_plain_username"] = sasl_plain_username
        config["sasl_plain_password"] = sasl_plain_password

        # Data serialization configs
        config["key_deserializer"] = bytes.decode
        config["value_deserializer"] = bytes.decode

        # Consumer Group
        config["group_id"] = "wikimedia_opensearch"
        config["auto_offset_reset"] = "latest"

        return config

    @staticmethod
    def start_consumer():
        topic = topic_name
        config = WikimediaConsumerClass.get_config()

        # Create a Consumer client
        consumer = KafkaConsumer(topic, **config)

        # Create an Opensearch client
        os_client = OpensearchClass()

        # Create Opensearch index if not exist
        os_client.create_index_if_not_exist()

        try:
            while True:
                try:

                    records_dict = consumer.poll(timeout_ms=5000, max_records=10000)

                    # Get value part from records_dict -> {TopicPartition(.... : [ConsumerRecord(
                    # topic='wikimedia.recentchange', partition=1, offset=14, timestamp=1683701854482,
                    # timestamp_type=0, key=None, value="b'demo-0'", headers=[], checksum=None,
                    # serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(
                    # topic='wikimedia.recentchange',....)]}

                    records_list = list(
                        records_dict.values())

                    if len(records_list) > 0:
                        records_list = records_list[0]  # Get the list of records

                        for record in records_list:
                            cleaned_value = record.value.replace("\x00",
                                                                 '{}')  # In some cases we were seeing value='\x00'
                            # which is causing problems
                            json_doc = json.loads(cleaned_value)

                            if len(json_doc.items()) > 0:
                                print(record.partition, record.offset, json_doc)
                                os_client.index_document(json_doc, json_doc['meta']['id'])

                                print(f"Record with id = {json_doc['meta']['id']} inserted in Opensearch")
                    else:
                        print("No records exist at time. Will check for new records in 3 seconds..")
                except Exception as e:
                    print(e)
        except KeyboardInterrupt:
            print("Key is pressed to stop the Consumer...")
        finally:
            print("Consumer is closing now...")
            consumer.close()
            print("Consumer is closed")
