from multiprocessing import Process
import markovify
from random import randint
import time
from kafka import KafkaProducer
import traceback

def produce(text_model):
    retry_wait = 1
    
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            msg = text_model.make_short_sentence(140)
            producer.send('jb-topic', str.encode(msg))
            print(msg)
            time.sleep(randint(0, 9))
            producer.close()
        except Exception as e:
            print(e, ' Waiting {}'.format(retry_wait))
            traceback.print_exc()
            time.sleep(retry_wait)
            retry_wait += retry_wait + retry_wait/1000
 
            
if __name__ == "__main__":

    with open("hhgttg.txt") as f:
        text = f.read()
    text_model = markovify.Text(text)

    producer = Process(name='producer', target=produce, args=[text_model])
    producer.deamon = True

    producer.start()
     
    producer.join()

