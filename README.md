## Docker Compose POC
### producer -> kafka -> consumer -> redis

Producer
--------
Read the text file hhgttg.txt and produces new sentences using markov chains.  
The new sentences are publised to a kafka topic.

Consumer
--------
There are two message handlers in the consumer.  
The first one, writes the messages to stdout with a `print` statement.  
The second handler stores the messages as a dictionary in a redis instance.  

Requirements
------------
python 3
docker 1.17.0+
docker compose 1.17.0+


Run
---
`docker-compose up`

