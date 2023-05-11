# Wikistream

Wikistream is a streaming data pipeline that uses Apache Kafka to collect and process data from Wikimedia. 
The project aims to provide real-time insights and analytics on Wikimedia data using Opensearch Dashboard 
to help users analyze and understand trends, patterns, and user behavior on Wikimedia platforms.
The project is built using Python, Kafka-Python, and Opensearch library, and consists of several 
components, including a Kafka Producer that collects and sends data to a Kafka topic, a Kafka Consumer 
that reads data from the Kafka topic and processes it, and an OpenSearch cluster that serves as the 
sink for the processed data.

## Appendix

The project includes instructions on how to set up and configure the pipeline, as well as sample code 
and configuration files that can be used as a starting point. It also includes a sample dashboard built 
on OpenSearch Dashboard that showcases the potential of the pipeline for data analysis and visualization.

Overall, the project provides a powerful tool for collecting and analyzing real-time data from Wikimedia 
platforms, and can be used by researchers, analysts, and developers alike to gain insights and 
create innovative applications and services.

## Prerequisites
Before running the project, make sure you have the following prerequisites installed on your system:
- Python 3.6 or later
- kafka-python library (install using pip install kafka-python)
- requests library (install using pip install requests)
- opensearch library (install using pip install opensearch-py)
- Apache Kafka cluster, either locally
(Using <a href="https://www.conduktor.io/kafka/starting-kafka/">Windows Subsystem Linux</a>) or
remotely accessible(<a href="https://www.conduktor.io/kafka/how-to-start-kafka-with-conduktor/">Conduktor</a> or 
<a href="https://www.confluent.io/confluent-cloud/?utm_medium=sem&utm_source=bing&utm_campaign=ch.sem_br.brand_tp.prs_tgt.confluent-brand_mt.mbm_rgn.india_lng.eng_dv.all_con.confluent-cloud&utm_term=%2Bconfluent%20%2Bcloud&creative=&device=c&placement=&msclkid=abc6040c586011993d406050f8ae5ae1">
Confluent</a>)
- Opensearch Cluster, either locally(Using <a href="https://opensearch.org/docs/latest/install-and-configure/install-dashboards/docker/">Docker</a>)
or remotely accessible(Using <a href="https://bonsai.io/">Bonsai.io</a>)

## Run Locally

- Clone the project

```bash
  git clone https://github.com/Sparab16/WikimediaKafka.git
```

- Go to the project directory

```bash
  cd WikimediaKafka
```

- Install dependencies

```bash
  pip install -r requirements.txt
```

-  Create a folder named `creds_config`

    - Inside the `creds_config` folder, create configuration files for the following:
        - Kafka Configurations
            ```
            topic_name = <topic_name>
            source_url = "https://stream.wikimedia.org/v2/stream/recentchange"
            ```
        - Kafka Connect Credentials
            ```
            sasl_plain_username = <username>
            sasl_plain_password= <password>
            bootstrap_servers = <server>
            ```
        - OpenSearch Connect Credentials
            ```
            host = <connection-host>
            port = <port>
            auth = (<username>, <password>)
            index_name= <index-name>
            ```
- Run the producer.py and consumer.py. This will start reading streaming data from the 
Wikimedia API and sending it to the specified Kafka topic.

_Note_ :- By default, the script will run indefinitely until you manually stop it by pressing ```Ctrl+C```



## OpenSearch API Reference

#### Bonsai Console

![bonsai_console.png](ref%2Fimages%2Fbonsai_console.png)

#### 1. Get Index

```http
  GET /<index-name>
```

| Parameter | Type     | Description                             |
|:----------|:---------|:----------------------------------------|
| `host`    | `string` | **Required :** Your Host                |
| `port`    | `string` | **Required :** Your Port                |
| `auth`    | `tuple`  | **Required :** Your Username & Password |


#### 2. Get Document

```http
  GET /<index-name>/_doc/<id>
```

| Parameter | Type     | Description                             |
|:----------|:---------|:----------------------------------------|
| `host`    | `string` | **Required :** Your Host                |
| `port`    | `string` | **Required :** Your Port                |
| `auth`    | `tuple`  | **Required :** Your Username & Password |

#### 3. Delete Index

```http
  DELETE /<index-name>
```

| Parameter | Type     | Description                             |
|:----------|:---------|:----------------------------------------|
| `host`    | `string` | **Required :** Your Host                |
| `port`    | `string` | **Required :** Your Port                |
| `auth`    | `tuple`  | **Required :** Your Username & Password |


For more information related to API's. <a href="https://opensearch.org/docs/latest/api-reference/index-apis/index/">
Click here</a>



## Conduktor Platform

Conduktor is a platform that provides an intuitive GUI for managing and monitoring Apache Kafka clusters. It is designed to simplify and streamline the management of Kafka clusters and make it easier for developers, DevOps teams, and data engineers to work with Kafka.


#### Topic UI
![conduktor_topic.png](ref%2Fimages%2Fconduktor_topic.png)

#### Consumer Group UI
![conduktor_consumer.png](ref%2Fimages%2Fconduktor_consumer.png)



## OpenSearch

OpenSearch is a distributed, open source search and analytics engine that is designed to handle large-scale data processing and analysis. It is a fork of Elasticsearch and is fully compatible with Elasticsearch APIs, making it a popular choice for organizations looking to build robust and scalable search and analytics solutions.

Integration of OpenSearch with Apache Kafka provides a powerful platform for real-time data processing and analysis. By using Kafka as a data pipeline, users can easily collect and send data from a wide range of sources to OpenSearch, where it can be analyzed, visualized, and stored

#### Console UI

![opensearch_console.png](ref%2Fimages%2Fopensearch_console.png)

#### Dashboard UI


![opensearch_dashboard.png](ref%2Fimages%2Fopensearch_dashboard.png)

## Authors

- [@Sparab16](https://github.com/Sparab16)

## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shrey16/)

## LICENSE

MIT License

Copyright (c) [2023] [Shreyas Parab]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

