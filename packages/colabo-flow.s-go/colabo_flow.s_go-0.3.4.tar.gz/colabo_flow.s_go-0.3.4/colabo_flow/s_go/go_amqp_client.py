#!/usr/bin/env python
# https://pypi.org/project/pika/
import pika
from pika.connection import Connection
import json
import time
from yachalk import chalk
from dataclasses import replace
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

from colabo_flow.s_go.config import connectConfig
from colabo_flow.s_go.vos import (
	IColaboFlowGoMsg,
	EColaboFlowGoMsgType,
	IColaboFlowClientData,
	IColaboFlowGoMsgExtension_TaskExecute_Request
)
from colabo_flow.s_go.operators import createGoMsg
from colabo_flow.s_go.concurrency import async_connection_callback_threadsafe

EXCHANGE = ""
DEBUG_TICKS = False

async def client_run(client: IColaboFlowClientData):

	# TODO: make more advanced mechanism, like thread-safe singleton
	# https://medium.com/analytics-vidhya/how-to-create-a-thread-safe-singleton-class-in-python-822e1170a7f6
	if(client.running):
		print(f"{client.appNameTextWithContext('client_run')} Client already running, returning")
		return

	proc_title = f"ColaboFlow.Go.Client-{client.clientName}"
	setproctitle(proc_title)

	connect(client)
	# start_consuming(client)
	process_data_events(client)

	print(f"{client.appNameTextWithContext('client_run')} Connection established, returning")

def connect(client: IColaboFlowClientData):
	"""
	connects to the ColaboFlow service through the RabbitMQ broker
	"""
	port = 5672
	print(f"{client.appNameTextWithContext('connect')} Connecting to the server... (host: {client.amqpUrl}, port: {port})")
	parameters = (
		pika.ConnectionParameters(
			host=client.amqpUrl,
			port=port,
			connection_attempts=5,
			retry_delay=1
		)
	)

	# https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html
	client.connection = pika.BlockingConnection(parameters)
	print(f"{client.appNameTextWithContext('connect')} Creating a channel...")
	client.channel = client.connection.channel()
	# https://github.com/MassTransit/MassTransit/issues/370
	print(f"{client.appNameTextWithContext('connect')} Declaring the orchestrator queue ...")
	client.channel.queue_declare(queue=client.queueServiceOrchestrator, durable=True, exclusive=False, auto_delete=False)

	client.connection.add_callback_threadsafe(lambda: _noop(client))

	client.running = True

def _noop(client: IColaboFlowClientData):
	print(f"{client.appNameTextWithContext('_noop')} launched with: `client.connection.add_callback_threadsafe(lambda: _noop(client))`")

def _start_consuming(client: IColaboFlowClientData):
	"""
	Starts consuming messages from the ColaboFlow service through RabbitMQ broker

	NOTE: It runs in the context of a new connection-thread (`client.connectionThread`)
	it is necessary as the `client.channel.start_consuming()` function is **blocking**
	"""

	while client.running:
		print(f"{client.appNameTextWithContext('_start_consuming')} started")
		# https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html#pika.adapters.blocking_connection.BlockingChannel.start_consuming
		client.channel.start_consuming()
		print(f'{client.appNameTextWithContext("_start_consuming")} finished')
		# time.sleep(0.001)
		# NOTE: this will delay stopping when the stop_consuming() is triggered. We can avoid it with more clever algorithm
		time.sleep(0.1)
		# time.sleep(1)
		# time.sleep(2)

def start_consuming(client: IColaboFlowClientData):
	print(f"{client.appNameTextWithContext('start_consuming')} starting '_start_consuming' as a separate thread to avoid blocking the current ({chalk.blue('the message handling')}) thread")
	client.consumingThread = threading.Thread(target=_start_consuming, args=(client, ))
	client.consumingThread.name = f'{client.consumingThread.name}_start_consuming'
	client.consumingThread.start()
	native_id = client.consumingThread.native_id
	print(f"{client.appNameTextWithContext('start_consuming')} OK, the '_start_consuming' thread (with the native native_id: {chalk.blue.bold(native_id)} ) is spawned")

def _process_data_events(client: IColaboFlowClientData):
	"""
	Starts consuming messages from the ColaboFlow service through RabbitMQ broker

	NOTE: It runs in the context of a new connection-thread (`client.connectionThread`)
	it is necessary as the `client.channel.process_data_events()` function is **blocking**
	"""

	while client.running:
		if DEBUG_TICKS:
			print(f"{client.appNameTextWithContext('_process_data_events')} started")
		# https://pika.readthedocs.io/en/stable/modules/adapters/blocking.html#pika.adapters.blocking_connection.BlockingChannel.process_data_events
		client.connection.process_data_events(1)
		if DEBUG_TICKS:
			print(f'{client.appNameTextWithContext("_process_data_events")} finished')
		# time.sleep(0.001)
		# NOTE: this will delay stopping when the stop_consuming() is triggered. We can avoid it with more clever algorithm
		time.sleep(0.1)
		# time.sleep(1)
		# time.sleep(2)

def process_data_events(client: IColaboFlowClientData):
	print(f"{client.appNameTextWithContext('process_data_events')} starting '_process_data_events' as a separate thread to avoid blocking the current ({chalk.blue('the message handling')}) thread")
	client.eventsThread = threading.Thread(target=_process_data_events, args=(client, ))
	client.eventsThread.name = f'{client.eventsThread.name}_process_data_events'
	client.eventsThread.start()
	native_id = client.eventsThread.native_id
	print(f"{client.appNameTextWithContext('process_data_events')} OK, the '_process_data_events' thread (with the native native_id: {chalk.blue.bold(native_id)} ) is spawned")

def _stop_consuming(client: IColaboFlowClientData):
	print(f"{client.appNameTextWithContext('_stop_consuming')} stopping consuming")
	client.channel.stop_consuming()
	client.running = False
	print(f"{client.appNameTextWithContext('_stop_consuming')} stopped consuming")

def stop_consuming(client: IColaboFlowClientData):
	print(f"{client.appNameTextWithContext('stop_consuming')} launching _stop_consuming in the connection-thread")
	client.connection.add_callback_threadsafe(lambda: _stop_consuming(client))

async def client_executeTask(client: IColaboFlowClientData, taskId: str, taskInput: Any):
	"""
	Asks a ColaboFlow infrastructure to execute a specific task

	:param IColaboFlowClientData client: client we want to use to execute task through
	:param str taskId: the id of the task we want to execute
	:param Any taskInput: the input we want to provide to the task while executing
	"""

	print(f'{client.appNameTextWithContext("client_executeTask")} taskId: "{chalk.blue_bright(taskId)}"')
	# Get the current event loop.
	loop = asyncio.get_running_loop()

	# Create a new Future object.
	futTaskExecute = loop.create_future()

	taskExecuteResponseQueue = f"client-task_execute_response-{uuid.uuid1()}";
	print(f'{client.appNameTextWithContext("client_executeTask")} futTaskExecute: "{futTaskExecute}"')
	print(f'{client.appNameTextWithContext("client_executeTask")} taskExecuteResponseQueue: "{taskExecuteResponseQueue}"')

	await async_connection_callback_threadsafe(client.connection, client.appNameTextWithContext, lambda: client.channel.queue_declare(queue=taskExecuteResponseQueue, exclusive=True), f"queue_declare:{taskExecuteResponseQueue}")

	print(f'{client.appNameTextWithContext("client_executeTask")} queue "{taskExecuteResponseQueue}" declared')

	msgTaskExecuteReq = createGoMsg(client.clientName, EColaboFlowGoMsgType.TASK_EXECUTE_REQUEST)

	# https://stackoverflow.com/a/50319825/257561
	# msg.replyTo = "test-client",
	msgTaskExecuteReq.replyTo = taskExecuteResponseQueue
	msgTaskExecuteReq.msg = f"executing task request from python, taskId: {taskId}"
	msgTaskExecuteReq.extension = IColaboFlowGoMsgExtension_TaskExecute_Request(
		taskId = taskId,
		taskInput = taskInput
	)

	msgTaskExecuteReqDict: Any = dataclasses.asdict(msgTaskExecuteReq)
	msgTaskExecuteReqStr = json.dumps(msgTaskExecuteReqDict)

	print(f'{client.appNameTextWithContext("client_executeTask")} Sending [queue: "{chalk.blue_bright(client.queueServiceOrchestrator)}"]: {msgTaskExecuteReqDict}')
	# https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.basic_publish
	await async_connection_callback_threadsafe(client.connection, client.appNameTextWithContext, lambda: client.channel.basic_publish(exchange='', routing_key=client.queueServiceOrchestrator, body=msgTaskExecuteReqStr), f"basic_publish:msgTaskExecuteReqStr")

	print(f"{client.appNameTextWithContext('client_executeTask')} [x] Sent {msgTaskExecuteReq}")

	def callback_task_execution_response_set_result(futTaskExecute, result):
		"""
		Sets result IMMEDIATELY, instead of calling it with `loop.call_soon_threadsafe()` from the `callback_task_execution_response` function, which is useful so we can printout the correct, new, future status.

		NOTE: It runs in the context of the main thread
		"""
		futTaskExecute.set_result(result)
		print(f'{client.appNameTextWithContext("callback_task_execution_response_set_result")} taskId: "{chalk.blue_bright(taskId)}", futTaskExecute: "{futTaskExecute}"')

	def callback_task_execution_response(ch, method, properties, body):
		"""
		A callback invited when a message with task execution response is received

		NOTE: It runs in the context of a new connection-thread (`client.consumingThread`)
		"""
		print(f'{client.appNameTextWithContext("callback_task_execution_response")} taskId: "{chalk.blue_bright(taskId)}" Received {body}')
		msg = json.loads(body)
		print(f'{client.appNameTextWithContext("callback_task_execution_response")} taskOutput: {msg["extension"]["taskOutput"]}')
		print(f'{client.appNameTextWithContext("callback_task_execution_response")} futTaskExecute: "{futTaskExecute}"')
		# set the `futTaskExecute` result in the context of the main-thread
		loop.call_soon_threadsafe(callback_task_execution_response_set_result, futTaskExecute, msg["extension"]["taskOutput"])

	# https://pika.readthedocs.io/en/stable/modules/channel.html#pika.channel.Channel.basic_consume
	# https://stackoverflow.com/questions/50404273/python-tutorial-code-from-rabbitmq-failing-to-run
	# TODO: client.consumerTag is a PoC, it has to be archived for each separate task that is executed
	client.consumerTag = client.channel.basic_consume(on_message_callback=callback_task_execution_response, queue=taskExecuteResponseQueue, auto_ack=True)

	print(f"{client.appNameTextWithContext('client_executeTask')} [*] Waiting for task execution response message. To exit press CTRL+C")

	# client.channel.start_consuming()
	# await start_consuming(client)
	# loop.create_task(
	# 	start_consuming(client)
	# )

	print(f'{client.appNameTextWithContext("client_executeTask")} Awaiting the taskId: "{chalk.blue_bright(taskId)}", futTaskExecute: {futTaskExecute}')
	result = await futTaskExecute
	print(f'{client.appNameTextWithContext("client_executeTask")} Leaving the taskId: "{chalk.blue_bright(taskId)}", futTaskExecute: {futTaskExecute}')
	return result

async def client_close(client: IColaboFlowClientData):
	print(f'{client.appNameTextWithContext("client_close")} Closing the connection')
	client.running = False
	print(f'{client.appNameTextWithContext("client_close")} Waiting on all the connection-related threads to client_close')
	if(client.consumerTag):
		client.connection.add_callback_threadsafe(lambda: client.channel.basic_cancel(client.consumerTag))
	if client.consumingThread:
		client.consumingThread.join()
	if client.eventsThread:
		client.eventsThread.join()
	# print(f"{client.appNameTextWithContext('client_close')} Closing the {chalk.bold.italic('channel')} to the ColaboFlow service...")
	# client.channel.close()
	# print(f"{client.appNameTextWithContext('client_close')} Closing the {chalk.bold.italic('connection')} to the ColaboFlow service...")
	# client.connection.close()
	print(f'{client.appNameTextWithContext("client_close")} Connection closed')
