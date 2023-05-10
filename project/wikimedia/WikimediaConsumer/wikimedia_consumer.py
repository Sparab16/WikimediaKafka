import json

from kafka import KafkaConsumer

from creds_config.kafka_connect_creds import *
from project.wikimedia.Opensearch.opensearch import OpensearchClass


class WikimediaConsumer:

    @staticmethod
    def get_topic() -> str:
        return "wikimedia.recentchange"

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
        config["group_id"] = "wikimedia_group"
        config["auto_offset_reset"] = "earliest"

        return config

    @staticmethod
    def main():
        topic = WikimediaConsumer.get_topic()
        config = WikimediaConsumer.get_config()

        # Create a Consumer client
        consumer = KafkaConsumer(topic, **config)

        # Create an Opensearch client
        os_client = OpensearchClass(index_name="wikimedia")

        # Create Opensearch index if not exist
        os_client.create_index_if_not_exist()

        while True:
            try:
                records_dict = consumer.poll(3000)
                records_list = list(records_dict.values()) # Get value part from records_dict -> {TopicPartition(topic='wikimedia.recentchange', partition=1): [ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=14, timestamp=1683701854482, timestamp_type=0, key=None, value="b'demo-0'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=15, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-2'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=16, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-5'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=17, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-6'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=18, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-8'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=19, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-10'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=7, serialized_header_size=-1)]}

                if len(records_list) > 0:
                    records_list = records_list[0] # Get the list of records

                    for record in records_list:
                        cleaned_value = record.value.replace("\x00", '{}') # In some cases we were seeing value='\x00' which is causing problems
                        json_doc = json.loads(cleaned_value)

                        if len(json_doc.items()) > 0:
                            print(json_doc)
                            os_client.index_document(json_doc, json_doc['meta']['id'])

                            print(f"Record with id = {json_doc['meta']['id']} inserted in Opensearch")
                else:
                    print("No records exist at time. Will check for new records in 3 seconds..")
            except KeyboardInterrupt:
                print("Key is pressed to stop the Consumer...")
            except Exception:
                pass
            finally:
                print("Consumer is closing now...")
                consumer.close()
                print("Consumer is closed")



WikimediaConsumer.main()
