from redis import Redis
from multiprocessing import Process
import time
from kafka import KafkaConsumer

redis = Redis(host='redis', port=6379)

def store_handler():
    retry_wait = 1
    
    while True:
        try:
            consumer = KafkaConsumer(bootstrap_servers='kafka:9092',
                                     auto_offset_reset='earliest',
                                     consumer_timeout_ms=1000)
            consumer.subscribe(['jb-topic'])
            while True:
                for msg in consumer:
                    redis.hmset(msg.timestamp, {'msg': msg.value.decode()})
                    print('store-handler', 'saved msg')
                    
        except Exception as e:
            print(e, ' Waiting {:.0f}'.format(retry_wait))
            time.sleep(retry_wait)
            retry_wait += retry_wait + retry_wait/1000

def logs_handler():
    retry_wait = 1
    
    while True:
        try:
            consumer = KafkaConsumer(bootstrap_servers='kafka:9092',
                                     auto_offset_reset='earliest',
                                     consumer_timeout_ms=1000)
            consumer.subscribe(['jb-topic'])
            while True:
                for msg in consumer:
                    print("log-handler", msg.value.decode())
        except Exception as e:
            print(e, ' Waiting {:.0f}'.format(retry_wait))
            time.sleep(retry_wait)
            retry_wait += retry_wait + retry_wait/1000


if __name__ == "__main__":

    to_redis = Process(name='store-handler', target=store_handler)
    to_redis.deamon = True

    to_logs = Process(name='logs-handler', target=logs_handler)
    to_logs.deamon = True

    to_redis.start()
    to_logs.start()
     
    to_redis.join()
    to_logs.join()

