import json

from kafka import KafkaProducer, KafkaConsumer, TopicPartition
def kafka_producer(urls, work):
    producer = KafkaProducer(acks=0, compression_type='gzip', bootstrap_servers=['localhost:9092'],
                             api_version=(0, 10, 1),
                             value_serializer=lambda x: x.encode('utf-8'))

    channel = work["channel"]
    work_group_no = work["work_group_no"]
    date = work["start_date"]
    keyword = work["keyword"]
    timestamp = work["timestamp"]
    topic_name = "urls-" + timestamp

    producer.send(topic_name, value=str(json.dumps({
        'channel': channel, 'urls': urls, "work_group_no": work_group_no, "keyword": keyword, "date": date
    }, ensure_ascii=False)))
        # count = count + 1

    producer.flush()
    # return count


def kafka_consumer(topic_name):
    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        api_version=(0, 10, 1),
        session_timeout_ms=10000,
        enable_auto_commit=False,
        group_id=topic_name)

    topicPartition = TopicPartition(topic_name, 0)
    consumer.assign([topicPartition])
    consumer.seek_to_beginning(topicPartition)
    return consumer