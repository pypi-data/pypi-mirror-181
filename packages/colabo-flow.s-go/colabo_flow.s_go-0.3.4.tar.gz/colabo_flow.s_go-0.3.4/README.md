# Run

## Hosts

```sh
python3 create_host.py

# send a test message with the RabbitMQ CLI
# https://www.rabbitmq.com/management-cli.html
rabbitmqadmin publish exchange=amq.default routing_key=test payload="Hello, world from RabbitMQ CLI"

# delete the queue `colabo.flow.host.node`
rabbitmqadmin delete queue name=colabo.flow.host.node

# delete all the messages in the `colabo.flow.host.node` queue
rabbitmqadmin purge queue name=colabo.flow.host.node
rabbitmqadmin purge queue name=colabo.flow.host.terra-python
rabbitmqadmin purge queue name=colabo.flow.host.heartbeat

cd /Users/mprinc/data/development/colabo-zontik/colabo/src/services/puzzles/flow/go

python3 create_host_terra.py
```

# Clients

```sh
cd /Users/mprinc/data/development/colabo-zontik/colabo/src/services/puzzles/flow/go

# sending a task request by python client
python3 create_client_terra.py
```

# Messages

```sh
# delete all the messages in the `colabo.flow.host.node` queue
rabbitmqadmin purge queue name=colabo.flow.host.node
```

## Heartbeat

```sh
# heartbeat for discovering python test host with a single task: `com.welcometerra.video.ffmpeg-multiple`
rabbitmqadmin publish exchange=amq.default routing_key=colabo.flow.host.heartbeat payload='{"id": "ColaboFlow-msg:371f4180-5c92-11ed-bc66-96ba02116486", "type": "HEARTBEAT", "requestId": "ColaboFlow-request:371f42f2-5c92-11ed-bc66-96ba02116486", "sender": "host-python-1", "replyTo": null, "proxies": [], "msgReplyChainIds": [], "msg": ["node host with tasks: ['com.welcometerra.video.ffmpeg-multiple']"], "extension": {"id": 2, "queueHost": "colabo.flow.host.python", "language": "PYTHON", "taskIds": ["com.welcometerra.video.ffmpeg-multiple"]}}'
```

Here is the full message:

```json
{
	"id": "ColaboFlow-msg:371f4180-5c92-11ed-bc66-96ba02116486",
	"type": "HEARTBEAT",
	"requestId": "ColaboFlow-request:371f42f2-5c92-11ed-bc66-96ba02116486",
	"sender": "host-python-1",
	"replyTo": null,
	"proxies": [],
	"msgReplyChainIds": [],
	"msg": ["node host with tasks: ['com.welcometerra.video.ffmpeg - multiple']"
	],
	"extension": {
		"id": 2,
		"queueHost": "colabo.flow.host.python",
		"language": "PYTHON",
		"taskIds": ["com.welcometerra.video.ffmpeg-multiple"]
	}
}
```

## process_video

```json
{
	"userId": 16,
	"videoId": 49,
	"videoFileLocalPath": "/var/folders/f5/s2lwsbwx34728zbv9vd91f4w0000gn/T/tmpzz4ykin9.mp4",
	"first_name": "Sasha",
	"email": "mprinc@gmail.com",
	"username": "mprinc",
	"task_context": {
		"processId": 1,
		"userId": 16,
		"userName": "mprinc",
		"videoId": 49,
		"videoName": "ALWAYS BE SILENT IN FIVE SITUATIONS _ APJ Abdul Kalam Quotes _ Life Quotes - Quotation & Motivation.mp4",
		"name": "process_video",
		"id": 1
	},
	"videoToAudio": false
}
```
