import threading
import asyncio
from typing import Any
from yachalk import chalk

def asyncio__provide_and_set_loop(appNameTextWithContext)->asyncio.AbstractEventLoop:
	"""
	Tries to retrieve (and set if not set already) an asyncio loop in the current thread through three steps: (i) retrieving, (ii) triggering creation implicitly, (iii) creating explicitly

	Finally it returns the event loop
	"""

	asyncio_loop: asyncio.AbstractEventLoop = None
	# asyncio_loop = asyncio.new_event_loop()
	# asyncio.set_event_loop(asyncio_loop)

	try:
		current_running_loop = asyncio.get_running_loop()
		print(f"{appNameTextWithContext('asyncio__provide_and_set_loop')} current_running_loop: {current_running_loop}")
		asyncio_loop = current_running_loop
	except Exception as err:
		print(f"{appNameTextWithContext('asyncio__provide_and_set_loop')} Missing a running loop (asyncio.get_running_loop()): {err}")

	if(not asyncio_loop):
		print(f"{appNameTextWithContext('asyncio__provide_and_set_loop')} Trying to trigger the creation (implicitly) of an asyncio loop (asyncio.get_event_loop())")
		try:
			# should trigger creating a asyncio loop

			# from: https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_event_loop
			# Deprecated since version 3.10: Deprecation warning is emitted if there is no running event loop. In future Python releases, this function will be an alias of get_running_loop().
			event_loop = asyncio.get_event_loop()
			print(f"{appNameTextWithContext('asyncio__provide_and_set_loop')} event_loop: {event_loop}")
			asyncio_loop = event_loop
		except Exception as err:
			print(f"{appNameTextWithContext('asyncio__provide_and_set_loop')} Problem with triggering a creation of a new asyncio loop (asyncio.get_event_loop()): {err}")

	if(not asyncio_loop):
		print(f"{appNameTextWithContext('asyncio__provide_and_set_loop')} Explicitly creating a new loop (asyncio.new_event_loop())")
		asyncio_loop = asyncio.new_event_loop()
		asyncio.set_event_loop(asyncio_loop)

	print(f"{appNameTextWithContext('asyncio__provide_and_set_loop')} returning asyncio__provide_and_set_loop: {asyncio__provide_and_set_loop}")

	return asyncio_loop

# set of a background tasks that keeps strong references to tasks
# to protect getting them destroyed before they get execution finished
background_tasks = set()

def run_background_task(loop, _lambda):
	"""
	`run_background_task(the_loop, lambda: processColaboFlowMsg_TaskExecute(host, msg))`
	"""

	task = loop.create_task(_lambda())

	# # Add task to the set. This creates a strong reference.
	background_tasks.add(task)

	# To prevent keeping references to finished tasks forever,
	# make each task remove its own reference from the set after
	# completion:
	task.add_done_callback(background_tasks.discard)

async def async_connection_callback_threadsafe(connection, appNameTextWithContext, _lambda, lambdaName: str)->bool:
	"""
	Executes _lambda function in the context of the connection-thread and
	it provides an await mechanism for waiting for its completion
	"""

	# Get the current event loop.
	loop = asyncio.get_running_loop()

	# Create a new Future object
	futLambdaExecuted = loop.create_future()

	def _runLambdaInContext():
		print(f"{appNameTextWithContext('async_connection_callback_threadsafe:_runLambdaInContext')}:[{lambdaName}] start, futLambdaExecuted: {futLambdaExecuted}")
		_lambda()
		# futLambdaExecuted.set_result(True)
		loop.call_soon_threadsafe(futLambdaExecuted.set_result, True)
		print(f"{appNameTextWithContext('async_connection_callback_threadsafe:_runLambdaInContext')}:[{lambdaName}] end, futLambdaExecuted: {futLambdaExecuted}")

	print(f"{appNameTextWithContext('async_connection_callback_threadsafe')}:[{lambdaName}] before add_callback_threadsafe, futLambdaExecuted: {futLambdaExecuted}")
	connection.add_callback_threadsafe(lambda: _runLambdaInContext())
	print(f"{appNameTextWithContext('async_connection_callback_threadsafe')}:[{lambdaName}] awaiting futLambdaExecuted: {futLambdaExecuted}")
	await futLambdaExecuted
	print(f"{appNameTextWithContext('async_connection_callback_threadsafe')}:[{lambdaName}] after add_callback_threadsafe, futLambdaExecuted: {futLambdaExecuted}")

async def async_run_func_under_thread(appNameTextWithContext, _async_lambda, lambdaName: str)->Any:
	"""
	Executes _async_lambda function in the context of a new thread and
	it provides an await mechanism for waiting for its completion
	"""

	# Get the current event loop.
	external_loop = asyncio.get_running_loop()

	# Create a new Future object
	futLambdaExecuted = external_loop.create_future()

	def threaded_runLambdaUnderThread():
		print(f"{appNameTextWithContext('async_run_func_under_thread:threaded_runLambdaUnderThread')} start, futLambdaExecuted: {futLambdaExecuted}")

		threaded_asyncio_loop = asyncio.new_event_loop()
		asyncio.set_event_loop(threaded_asyncio_loop)
		print(f"{appNameTextWithContext('async_run_func_under_thread:threaded_runLambdaUnderThread')} created the asyncio loop: {threaded_asyncio_loop}")

		result: Any = asyncio.run(_async_lambda())
		print(f"{appNameTextWithContext('run_async_func_under_thread:threaded_runLambdaUnderThread')}:[{lambdaName}] _async_lambda is finished")

		# TODO: it seems it is not necessary, as will just keep the thread running for ever and still no need as the `asyncio.run()` is sufficient and it is blocking until the coroutine is finished
		# print(f"{appNameTextWithContext('async_run_func_under_thread:threaded_runLambdaUnderThread')} starting: threaded_asyncio_loop.run_forever()")
		# threaded_asyncio_loop.run_forever()

		# should not be used, it will not be captured in the calling thread ...
		# futLambdaExecuted.set_result(True)
		# ... but rather call it in the context of the loop of the external thread
		external_loop.call_soon_threadsafe(futLambdaExecuted.set_result, True)
		print(f"{appNameTextWithContext('async_run_func_under_thread:threaded_runLambdaUnderThread')} end, futLambdaExecuted: {futLambdaExecuted}")

	print(f"{appNameTextWithContext('async_run_func_under_thread')} before add_callback_threadsafe, futLambdaExecuted: {futLambdaExecuted}")

	taskThread = threading.Thread(target=threaded_runLambdaUnderThread, args=())
	taskThread.name = f'{name}_{taskThread.name}'
	taskThread.start()
	native_id = taskThread.native_id
	print(f"{appNameTextWithContext('async_run_func_under_thread')} OK, the '{name}' thread (with the native native_id: {chalk.blue.bold(native_id)} ) is spawned")

	print(f"{appNameTextWithContext('async_run_func_under_thread')} awaiting futLambdaExecuted: {futLambdaExecuted}")
	await futLambdaExecuted
	print(f"{appNameTextWithContext('async_run_func_under_thread')} after add_callback_threadsafe, futLambdaExecuted: {futLambdaExecuted}")

def run_async_func_under_thread(appNameTextWithContext, _async_lambda, lambdaName: str)->Any:
	"""
	Executes _async_lambda function in the context of a new thread and
	it provides an await mechanism for waiting for its completion
	"""

	def threaded_runLambdaUnderThread():
		print(f"{appNameTextWithContext('run_async_func_under_thread:threaded_runLambdaUnderThread')}:[{lambdaName}] started")

		threaded_asyncio_loop = asyncio.new_event_loop()
		asyncio.set_event_loop(threaded_asyncio_loop)
		print(f"{appNameTextWithContext('run_async_func_under_thread:threaded_runLambdaUnderThread')}:[{lambdaName}] created the asyncio loop: {threaded_asyncio_loop}")

		print(f"{appNameTextWithContext('run_async_func_under_thread:threaded_runLambdaUnderThread')}:[{lambdaName}] launching _async_lambda")
		# https://docs.python.org/3/library/asyncio-runner.html#asyncio.run
		result: Any = asyncio.run(_async_lambda())
		print(f"{appNameTextWithContext('run_async_func_under_thread:threaded_runLambdaUnderThread')}:[{lambdaName}] _async_lambda is finished")
		# TODO: it seems it is not necessary, as will just keep the thread running for ever and still no need as the `asyncio.run()` is sufficient and it is blocking until the coroutine is finished
		# print(f"{appNameTextWithContext('run_async_func_under_thread:threaded_runLambdaUnderThread')}:[{lambdaName}] starting: threaded_asyncio_loop.run_forever()")
		# threaded_asyncio_loop.run_forever()

		print(f"{appNameTextWithContext('run_async_func_under_thread:threaded_runLambdaUnderThread')}:[{lambdaName}] task ended")

	print(f"{appNameTextWithContext('run_async_func_under_thread')}:[{lambdaName}] before add_callback_threadsafe")

	taskThread = threading.Thread(target=threaded_runLambdaUnderThread, args=())
	taskThread.name: str = f'{lambdaName}_{taskThread.name}'
	taskThread.start()
	native_id = taskThread.native_id
	print(f"{appNameTextWithContext('run_async_func_under_thread')}:[{lambdaName}] OK, the '{lambdaName}' thread (with the native native_id: {chalk.blue.bold(native_id)} ) is spawned")

	# print(f"{appNameTextWithContext('run_async_func_under_thread')}:[{lambdaName}] waiting for the thread to finish ...")
	# taskThread.join()
	# print(f"{appNameTextWithContext('run_async_func_under_thread')}:[{lambdaName}] thread finished")
