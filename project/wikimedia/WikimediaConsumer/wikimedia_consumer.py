from kafka import KafkaConsumer

from creds_config.kafka_connect_creds import *


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
        config["value_deserializer"] = bytes.decode

        # Consumer Group
        config["group_id"] = "wikimedia_group"
        config["auto_offset_reset"] = "latest"

        return config

    @staticmethod
    def main():
        topic = WikimediaConsumer.get_topic()
        config = WikimediaConsumer.get_config()

        consumer = KafkaConsumer(topic, **config)

        try:
            while True:
                records_dict = consumer.poll(10000)
                records_list = list(records_dict.values()) # Get value part from records_dict -> {TopicPartition(topic='wikimedia.recentchange', partition=1): [ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=14, timestamp=1683701854482, timestamp_type=0, key=None, value="b'demo-0'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=15, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-2'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=16, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-5'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=17, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-6'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=18, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-8'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=6, serialized_header_size=-1), ConsumerRecord(topic='wikimedia.recentchange', partition=1, offset=19, timestamp=1683701854483, timestamp_type=0, key=None, value="b'demo-10'", headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=7, serialized_header_size=-1)]}

                if len(records_list) > 0:
                    records_list = records_list[0] # Get the list of records

                    for record in records_list:
                        print(f"Topic = {record.topic} "
                              f"Partition = {record.partition} "
                              f"Offset = {record.offset} "
                              f"Value = {record.value}")
                else:
                    print("No records exist at time. Will check for new records in 10 seconds..")

        except KeyboardInterrupt:
            print("Key is pressed to stop the Consumer...")
        except Exception as e:
            print("Error occurred ", e)
        finally:
            print("Consumer is closing now...")
            consumer.close()
            print("Consumer is closed")


WikimediaConsumer.main()
