#!/usr/bin/env python
import pika
import json
import time
import functools
from yachalk import chalk
# from dataclasses import replace
# https://docs.python.org/3/library/uuid.html
import uuid
from typing import Any
import asyncio
from asyncio import Future
import threading
import dataclasses

# https://pypi.org/project/setproctitle/
# https://github.com/dvarrazzo/py-setproctitle
# https://stackoverflow.com/a/1866700/257561
from setproctitle import setproctitle

# https://stackoverflow.com/a/53713336/257561
# https://github.com/konradhalas/dacite
from dacite import from_dict, Config

from colabo_flow.s_go.vos import (
	IColaboFlowGoMsg,
	EColaboFlowGoMsgType,
	IColaboFlowHostData,
	EProgrammingLanguageSupported,
	IColaboFlowGoMsgExtension_TaskExecute_Request,
	IColaboFlowGoTaskInstanceInfo,
	ETaskExecute_Progress_Status,
	IColaboFlowGoMsgExtension_TaskExecute_Progress,
	IColaboFlowGoMsgExtension_TaskExecute_Response
)
from colabo_flow.s_go.operators import createGoMsg
from colabo_flow.s_go.executor_vos import ITaskExecutor, IFlowTask
from colabo_flow.s_go.executor_operators import createTaskInstanceForTaskWithoutFlow

from colabo_flow.s_go.concurrency import run_async_func_under_thread, async_connection_callback_threadsafe
LANGUAGE = EProgrammingLanguageSupported.PYTHON

def host_registerTaskExecutor(host: IColaboFlowHostData, executor: ITaskExecutor):
	host.taskExecutorsAvailable[executor.id] = executor

def host_registerTask(host: IColaboFlowHostData, task: IFlowTask):
	host.tasksAvailable[task.id] = task

def getTaskExecutor(host: IColaboFlowHostData, executorId: str) -> ITaskExecutor:
	return host.taskExecutorsAvailable[executorId]

async def host_run(host: IColaboFlowHostData):
	proc_title = f"ColaboFlow.Go.Host-{host.hostName}"
	setproctitle(proc_title)

	connect(host)
	start_consuming(host)

	if host.sendHeartbeat:
		print(f"{host.appNameTextWithContext('host_run')} Sending heartbeats")
		sendHeartbeatsToHost(host)
	else:
		print(f"{host.appNameTextWithContext('host_run')} Not sending heartbeats (due to the host configuration)")

	if host.listenForOrchestratorRequests:
		print(f"{host.appNameTextWithContext('host_run')} Listening for the orchestrator requests")
		listenOnHostQueue(host)
	else:
		print(f"{host.appNameTextWithContext('host_run')} Not listening for the orchestrator requests (due to the host configuration)")

	print(f"{host.appNameTextWithContext('host_run')} Connection established, returning")

def connect(host: IColaboFlowHostData):
	"""
	connects to the ColaboFlow service through RabbitMQ broker
	"""
	print(f"{host.appNameTextWithContext('connect')} Connecting to the server...")
	parameters = (
		pika.ConnectionParameters(
			host=host.amqpUrl,
			port=5672,
			connection_attempts=5,
			retry_delay=1
		)
	)

	# https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html
	host.connection = pika.BlockingConnection(parameters)
	print(f"{host.appNameTextWithContext('connect')} Creating a channel...")
	host.chHostHeartbeat = host.connection.channel()
	# https://github.com/MassTransit/MassTransit/issues/370

	print(f"{host.appNameTextWithContext('connect')} Declaring the host queue ...")
	# TODO: `exclusive=True` is only if the queue is host (worker) specific and the ColaboFlow handles load-balancing (which is the most long-term reasonable scenario as there is more control on which task goes where and when, etc)
	host.chHostHeartbeat.queue_declare(queue=host.queueHost, durable=True, exclusive=False, auto_delete=False)
	# host.chHostHeartbeat.queue_bind(queue=host.queueHost, exchange="test_exchange", routing_key="standard_key")

	host.running = True

def _start_consuming(host: IColaboFlowHostData):
	"""
	Starts consuming messages from the ColaboFlow service through RabbitMQ broker

	NOTE: It runs in the context of a new connection-thread (`host.consumingThread`)
	it is necessary as the `host.chHostHeartbeat.start_consuming()` function is **blocking**
	"""

	while host.running:
		print(f"{host.appNameTextWithContext('_start_consuming')} started")
		# https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html#pika.adapters.blocking_connection.BlockingChannel.start_consuming
		host.chHostHeartbeat.start_consuming()
		print(f'{host.appNameTextWithContext("_start_consuming")} finished')
		# time.sleep(0.001)
		# NOTE: this will delay stopping when the stop_consuming() is triggered. We can avoid it with more clever algorithm
		time.sleep(0.1)
		# time.sleep(1)
		# time.sleep(2)

def start_consuming(host: IColaboFlowHostData):
	print(f"{host.appNameTextWithContext('start_consuming')} starting '_start_consuming' as a separate thread to avoid blocking the current ({chalk.blue('the message handling')}) thread")
	host.consumingThread = threading.Thread(target=_start_consuming, args=(host, ))
	host.consumingThread.name = f'{host.consumingThread.name}_start_consuming'
	host.consumingThread.start()
	native_id = host.consumingThread.native_id
	print(f"{host.appNameTextWithContext('start_consuming')} OK, the '_start_consuming' thread (with the native native_id: {chalk.blue.bold(native_id)} ) is spawned")

def _stop_consuming(host: IColaboFlowHostData):
	print(f"{host.appNameTextWithContext('_stop_consuming')} stopping consuming")
	host.chHostHeartbeat.stop_consuming()
	host.running = False
	print(f"{host.appNameTextWithContext('_stop_consuming')} stopped consuming")

def host_stop_consuming(host: IColaboFlowHostData):
	print(f"{host.appNameTextWithContext('host_stop_consuming')} launching _stop_consuming in the connection-thread")
	host.connection.add_callback_threadsafe(lambda: _stop_consuming(host))

def _basic_publish(host: IColaboFlowHostData, sendToQueue: str, msg: IColaboFlowGoMsg):
	print(f'{host.appNameTextWithContext("_basic_publish")} sending to the "{sendToQueue}" queue, the message: {msg}')
	msgStr = json.dumps(msg)
	host.chHostHeartbeat.basic_publish(exchange='', routing_key=sendToQueue, body=msgStr)

async def async_threaded_processColaboFlowMsg_TaskExecute(host: IColaboFlowHostData, msgServiceReqObj: IColaboFlowGoMsg):

	msgServiceTaskExecuteReqObjExtension: IColaboFlowGoMsgExtension_TaskExecute_Request = from_dict(data_class=IColaboFlowGoMsgExtension_TaskExecute_Request, data=msgServiceReqObj.extension)

	taskId: str = msgServiceTaskExecuteReqObjExtension.taskId
	taskInput: Any = msgServiceTaskExecuteReqObjExtension.taskInput
	queueReplyTo: str = msgServiceReqObj.replyTo
	if not queueReplyTo:
		queueReplyTo = host.queueHostHeartbeat

	# *************************
	# RETRIEVING THE TASK and TASK EXECUTOR
	# *************************/

	task: IFlowTask = host.tasksAvailable[taskId]

	print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} TASK EXECUTION REQUEST: taskId: {chalk.blue_bright(taskId)}, queueReplyTo: "{queueReplyTo}"')

	if not task:
		print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} task is missing for the id: {taskId}')

	print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} Executing id: {chalk.blue_bright(taskId)}, task.description: {task.description}')

	# create task instance
	taskInstanceId: str = f'taskId:lang-{LANGUAGE}:host-{host.hostName}:{uuid.uuid1()}'
	taskInstance: IFlowTaskInstance = createTaskInstanceForTaskWithoutFlow(task)
	taskInstance.id = taskInstanceId
	host.taskInstances[taskId] = taskInstance
	host.runningTaskInstancesInfos[taskId] = IColaboFlowGoTaskInstanceInfo(
		id = taskInstanceId,
		taskInstance = taskInstance,
	)

	# get the task executor
	if not task.executorRef or not task.executorRef.id:
		print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} Executor ID is not provided for the task: {taskId}')
		return

	taskExecutor: ITaskExecutor = getTaskExecutor(host, task.executorRef.id)
	print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} taskExecutor: {taskExecutor}')

	# *************************
	# REPLYING THE TASK PROGRESS (task instance id)
	# *************************/
	msgTaskExecutionProgress: IColaboFlowGoMsg = createGoMsg(host.hostName, EColaboFlowGoMsgType.TASK_EXECUTE_PROGRESS)
	msgTaskExecutionProgress.extension = IColaboFlowGoMsgExtension_TaskExecute_Progress(
		taskInstanceId = taskInstanceId,
		status = ETaskExecute_Progress_Status.INITIALIZED,
		progress = 0,
	)
	msgTaskExecutionProgress.msg = f"Task execution result for the taskId: '{taskId}' will be returned over the queue: '{queueReplyTo}'"

	msgTaskExecutionProgressDict: Any = dataclasses.asdict(msgTaskExecutionProgress)

	if host.reportsConfig.showExecutionMsgs:
		print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} Sending PROGRESS to the task execution requester (service) [queue: "{chalk.blue_bright(queueReplyTo)}"]: {json.dumps(msgTaskExecutionProgressDict)}')

	await async_connection_callback_threadsafe(host.connection, host.appNameTextWithContext, lambda: _basic_publish(host, queueReplyTo, msgTaskExecutionProgressDict), f"_basic_publish:msgTaskExecutionProgressDict")

	# *************************
	# EXECUTING THE TASK (task instance id)
	# *************************/
	print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} Executing task with taskId "{chalk.blue.bold(taskId)}"')

	if taskExecutor.reference.async_method:
		print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} executing async executor (taskExecutor.reference.async_method)')
		taskOutput = await taskExecutor.reference.async_method(taskInput)
	elif taskExecutor.reference.method:
		print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} executing sync executor (taskExecutor.reference.method)')
		taskOutput = taskExecutor.reference.method(taskInput)
	else:
		errorMsg = f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} Error, neither async nor non-async executor reference available for taskId: {taskId} and executorId: "{taskExecutor.id}"'
		print(errorMsg)
		raise Exception(errorMsg)

	print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} Task with taskId "{chalk.blue.bold(taskId)}" executed. Result is: {chalk.blue_bright(taskOutput)}')

	# *************************
	# SENDING EXECUTION RESPONSE
	# *************************/
	msgTaskExecutionReply: IColaboFlowGoMsg = createGoMsg(host.hostName, EColaboFlowGoMsgType.TASK_EXECUTE_RESPONSE)
	msgTaskExecutionReply.requestId = msgServiceReqObj.requestId
	msgTaskExecutionReply.msgReplyChainIds = [msgServiceReqObj.id]
	msgTaskExecutionReply.extension = IColaboFlowGoMsgExtension_TaskExecute_Response(
		taskOutput = taskOutput,
	)
	msgTaskExecutionReply.msg = f"Returning task execution for the taskId: '{taskId}' over queue: '{queueReplyTo}'"

	msgTaskExecutionProgressDict: Any = dataclasses.asdict(msgTaskExecutionProgress)

	if host.reportsConfig.showExecutionMsgs:
		print(f'{host.appNameTextWithContext("async_threaded_processColaboFlowMsg_TaskExecute")} Sending RESPONSE to the task execution requester (service) [queue: "{chalk.blue_bright(queueReplyTo)}"]: {msgTaskExecutionReply}')

	msgTaskExecutionReplyDict: Any = dataclasses.asdict(msgTaskExecutionReply)
	await async_connection_callback_threadsafe(host.connection, host.appNameTextWithContext, lambda: _basic_publish(host, queueReplyTo, msgTaskExecutionReplyDict), f"_basic_publish:msgTaskExecutionReplyDict")

def async_processColaboFlowMsg_TaskInstancesReport(host: IColaboFlowHostData, msg: IColaboFlowGoMsg):
	pass

def listenOnHostQueue(host: IColaboFlowHostData):
	# Listener (consumer)
	print(f'{host.appNameTextWithContext("listenOnHostQueue")} Listening on the queue: "{chalk.blue_bright(host.queueHost)}"')
	print(f'{host.appNameTextWithContext("listenOnHostQueue")} [*] Waiting for messages in %s. To exit press "{chalk.blue_bright("CTRL+C")}"')

	async def async_threaded_callback_host_msg_request(ch, method, properties, body):
		# print(f"{host.appNameTextWithContext('async_threaded_callback_host_msg_request')} Received {body}")
		msgObj: Any = json.loads(body)
		print(f"{host.appNameTextWithContext('async_threaded_callback_host_msg_request')} Received {msgObj}")
		# https://github.com/konradhalas/dacite#casting
		msg: IColaboFlowGoMsg = from_dict(data_class=IColaboFlowGoMsg, data=msgObj,
			config=Config(cast=[EColaboFlowGoMsgType])
		)
		print(f'{host.appNameTextWithContext("async_threaded_callback_host_msg_request")} msg.sender: "{chalk.blue_bright(msg.sender)}", msg.type: "{chalk.blue_bright(msg.type)}, msg.msg: "{chalk.blue_bright(msg.msg)}"')

		# print(f'{host.appNameTextWithContext("async_threaded_callback_host_msg_request")} futTaskExecute: "{futTaskExecute}"')
		# # set the `futTaskExecute` result in the context of the main-thread
		# loop.call_soon_threadsafe(async_threaded_callback_host_msg_request_set_result, futTaskExecute, msg["extension"]["taskOutput"])

		if msg.type == EColaboFlowGoMsgType.TASK_EXECUTE_REQUEST:
			if host.processOrchestratorTaskExecuteRequests:
				await async_threaded_processColaboFlowMsg_TaskExecute(host, msg)

		elif msg.type == EColaboFlowGoMsgType.TASK_INSTANCES_REPORT__REQUEST:
			await async_processColaboFlowMsg_TaskInstancesReport(host, msg)

		# acknowledging the received message
		# https://www.rabbitmq.com/tutorials/tutorial-six-python.html
		# https://github.com/rabbitmq/rabbitmq-tutorials/blob/main/python/rpc_server.py
		print(f'{host.appNameTextWithContext("async_threaded_callback_host_msg_request")} msg.sender: "{chalk.blue_bright(msg.sender)}", Acknowledging back (msg.type: "{chalk.blue_bright(msg.type)}, method.delivery_tag: {chalk.blue_bright(method.delivery_tag)})')
		await async_connection_callback_threadsafe(host.connection, host.appNameTextWithContext, lambda: ch.basic_ack(delivery_tag=method.delivery_tag), f"async_threaded_async_threaded_callback_host_msg_request:basic_ack")
		print(f'{host.appNameTextWithContext("async_threaded_callback_host_msg_request")} msg is acknowledged back')

	def callback_host_msg_request(ch, method, properties, body):
		"""
		A callback invited when a message with host request from the ColaboFlow service is received

		NOTE: It runs in the context of a new connection-thread (`host.consumingThread`)

		As we cannot conveniently run asyncio from it, and we constantly under a risk of blocking the connection-thread we are spawning the real business logic through an async function `async_threaded_callback_host_msg_request` under a separate thread
		"""

		print(f'{host.appNameTextWithContext("callback_host_msg_request")} Received a new message, launching `async_threaded_callback_host_msg_request` in a separate thread')

		run_async_func_under_thread(host.appNameTextWithContext, lambda: async_threaded_callback_host_msg_request(ch, method, properties, body), "async_threaded_callback_host_msg_request")

	# Note: prefetch is set to 1 here as an example only and to keep the number of threads created
	# to a reasonable amount. In production you will want to test with different prefetch values
	# to find which one provides the best performance and usability for your solution
	# host.chHostHeartbeat.basic_qos(prefetch_count=1)
	host.chHostHeartbeat.basic_qos(prefetch_count=host.concurrency_TasksNo)

	# https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.basic_consume
	# https://stackoverflow.com/questions/50404273/python-tutorial-code-from-rabbitmq-failing-to-run
	# on_message_callback = functools.partial(on_message, args=(host, ))
	# host.chHostHeartbeat.basic_consume(on_message_callback=on_message_callback, queue='standard')
	host.hostMsgRequestConsumerTag = host.chHostHeartbeat.basic_consume(on_message_callback=callback_host_msg_request, queue=host.queueHost, auto_ack=False)

"""
 * sends heartbeat messages back to the ColaboFlow service
 * to
 * 1. know the host exists
 * 2. know or update (not implemented yet) the available task executors
"""
def sendHeartbeatsToHost(host: IColaboFlowHostData):
	# https://stackoverflow.com/a/37512537/257561
	async def runHeartbeat():
		print(f"{host.appNameTextWithContext('sendHeartbeatsToHost')} started emitting, host.running: {host.running}")
		while host.running:
			# print(f"{host.appNameTextWithContext('sendHeartbeatsToHost')} running for host.heartbeatId: {host.heartbeatId}")
			sendHeartbeatToHost(host)
			# print(f"{host.appNameTextWithContext('sendHeartbeatsToHost')} sent for host.heartbeatId: {host.heartbeatId}")
			await asyncio.sleep(3)
			# print(f"{host.appNameTextWithContext('sendHeartbeatsToHost')} woke up for host.heartbeatId: {host.heartbeatId}")
		print(f"{appNameTextWithContext('sendHeartbeatsToHost')} stopped emitting, host.running: {host.running}")

	# def stop():
	# 	task.cancel()

	# asyncio.run(runHeartbeat())
	loop = asyncio.get_event_loop()
	# loop.call_later(5, stop)
	runHeartbeatTask = loop.create_task(runHeartbeat())

	# try:
	# 	loop.run_until_complete(runHeartbeatTask)
	# except asyncio.CancelledError:
	# 	pass

"""
sends a single heartbeat message back to the ColaboFlow service
It is invited by the `sendHeartbeatsToHost` function
"""
def sendHeartbeatToHost(host: IColaboFlowHostData):
	# TODO: support listening for the heartbeat reply and set the timeout after we should send a warning/error on no response
	heartbeat: IColaboFlowGoMsg = createGoMsg(host.hostName, EColaboFlowGoMsgType.HEARTBEAT)
	heartbeat.extension = {
		"id": host.heartbeatId,
		"queueHost": host.queueHost,
		"language": EProgrammingLanguageSupported.PYTHON,
		"taskIds": list(host.taskExecutorsAvailable.keys()),
	}
	heartbeat.msg = f"node host with tasks: {json.dumps(list(host.taskExecutorsAvailable.keys()))}",
	host.heartbeatId = host.heartbeatId + 1

	if host.reportsConfig.showHeartbeatMsgs:
		print(f'{host.appNameTextWithContext("sendHeartbeatToHost")} Sending heartbeat [from: "{host.hostName}", queue: "{chalk.blue_bright(host.queueHostHeartbeat)}"]')
		# print(f"{host.appNameTextWithContext('sendHeartbeatToHost')} Sending heartbeat [queue: '{chalk.blue_bright(host.queueHostHeartbeat)}']: {json.dumps(heartbeat.to_json())}")

	# host.chHostHeartbeat.basic_publish(exchange='', routing_key=host.queueHostHeartbeat, body=heartbeat.to_json())
	# host.connection.add_callback_threadsafe(
		# functools.partial(host.chHostHeartbeat.basic_publish, exchange='', routing_key=host.queueHostHeartbeat, body=heartbeat.to_json()))
	host.connection.add_callback_threadsafe(lambda: _sendHeartbeatToHost(host, heartbeat))

def _sendHeartbeatToHost(host: IColaboFlowHostData, heartbeat: IColaboFlowGoMsg):
	if host.reportsConfig.showHeartbeatMsgs:
		print(f'{host.appNameTextWithContext("_sendHeartbeatToHost")} Sending heartbeat [queue: "{chalk.blue_bright(host.queueHostHeartbeat)}"]: {heartbeat.extension["id"]}')
		# print(f"{host.appNameTextWithContext('_sendHeartbeatToHost')} Sending heartbeat [queue: '{chalk.blue_bright(host.queueHostHeartbeat)}']: {json.dumps(heartbeat.to_json())}")
	host.chHostHeartbeat.basic_publish(exchange='', routing_key=host.queueHostHeartbeat, body=heartbeat.to_json())

def host_close(host: IColaboFlowHostData):
	host.running = False
	if(host.hostMsgRequestConsumerTag):
		# host.chHostHeartbeat.basic_cancel(host.hostMsgRequestConsumerTag)
		host.connection.add_callback_threadsafe(lambda: host.chHostHeartbeat.basic_cancel(host.hostMsgRequestConsumerTag))
	host.consumingThread.join()
	# print(f"{host.appNameTextWithContext('host_close')} Closing the {chalk.bold.italic('channel')} to the ColaboFlow service...")
	# host.chHostHeartbeat.close()
	# print(f"{host.appNameTextWithContext('host_close')} Closing the {chalk.bold.italic('connection')} to the ColaboFlow service...")
	# host.connection.close()
