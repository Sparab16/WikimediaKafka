import requests
import json

from kafka import KafkaProducer

from creds_config.kafka_connect_creds import *


class WikimediaProducer:
    @staticmethod
    def get_topic() -> str:
        return "wikimedia.recentchange"

    @staticmethod
    def get_url() -> str:
        return "https://stream.wikimedia.org/v2/stream/recentchange"

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
        config["key_serializer"] = str.encode
        config["value_serializer"] = str.encode

        return config

    @staticmethod
    def main():
        topic = WikimediaProducer.get_topic()
        url = WikimediaProducer.get_url()
        config = WikimediaProducer.get_config()

        # Create producer object
        producer = KafkaProducer(**config)

        try:
            with requests.get(url, stream=True) as response:
                for res in response.iter_lines(decode_unicode=True):

                    res_list = res.split(":", maxsplit=1) # Split to get data and value part

                    if "data" in res_list[0]: # lines written all the lines, we need lines starting from data
                        json_response = json.loads(res_list[1])

                        print(json_response)

                        # Send data to Producer
                        producer.send(topic, json.dumps(json_response), key=json_response['meta']['id'])

        except KeyboardInterrupt:
            print("Key is pressed to stop the Producer...")
        except Exception as e:
            print(f"Error occurred {str(e)}")
        finally:
            print("Producer is closing now...")
            producer.close()
            print("Producer is closed")


WikimediaProducer.main()
