from opensearchpy import OpenSearch
from creds_config.opensearch_connect_creds import *

class OpensearchClass:

    def __init__(self, index_name):
        self.client = OpenSearch(
                hosts=[{"host": host, "port": port}],
                http_auth = auth,
                use_ssl = True
            )

        self.index_name = index_name

    def create_index_if_not_exist(self):
        is_index_exist = self.client.indices.exists(self.index_name)

        if not is_index_exist:

            index_body = {
                'settings': {
                    'index': {
                        'number_of_shards': 4
                    }
                }
            }

            self.client.indices.create(self.index_name, body=index_body)

            print(f"Index '{self.index_name}' is created successfully")
        else:
            print(f"Index '{self.index_name}' is already exist")

    def index_document(self, json_doc, id):

        self.client.index(
            index=self.index_name,
            body=json_doc,
            id=id
        )
