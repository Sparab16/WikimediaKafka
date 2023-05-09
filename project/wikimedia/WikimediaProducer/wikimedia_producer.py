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
        config["value_serializer"] = str.encode

        return config

    @staticmethod
    def main():
        topic = WikimediaProducer.get_topic()
        url = WikimediaProducer.get_url()
        config = WikimediaProducer.get_config()

        producer = KafkaProducer(**config)

        producer.send(topic, "test-kafka")


WikimediaProducer.main()