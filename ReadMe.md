- [Introduction](#introduction)
  - [Creating Single Active Consumer Per Queue](#creating-single-active-consumer-per-queue)
    - [Problem Statement](#problem-statement)
      - [Diagram](#diagram)
      - [Usage - Linux](#usage---linux)

# Introduction
This Module contains various implementations using RabbitMQ

## Creating Single Active Consumer Per Queue
### Problem Statement
Imagine you have multiple requests coming from multiple callers, but you want to process those requests separately but requests from same caller sequentially and in order.

That would require us to have some sort of queue(RabbitMQ in this case) which maintain the request order from the caller. To process the requests we would spawn new dedicated thread per caller (Could be a Daemon Process as well if work is resource intensive), once the work is down we can setup a timeout, to stop the processing thread.

#### Diagram


#### Usage - Linux
***Setup the environment***
``` bash
python -m .venv venv 
source .venv/bin/activate
pip install requirements.txt
docker compose up
```


***Run the Test file***
``` bash
python test.py 
```
