# We provide it that a regular ColaboFlow consuming code can be lighter and without heavy boilerplate and knowledge of configuration parameters

import asyncio
import threading
from yachalk import chalk
from typing import Any

import sys
import os
from os.path import abspath, dirname, join

import threading
from collections.abc import Callable

from colabo_flow.s_go.concurrency import asyncio__provide_and_set_loop

colaboFlow_client_run: Callable = None
appNameTextWithContext: Callable = None
colaboFlow_client_ExecuteTask_Asynced: Callable = None

# Django - ColaboFlow
# --------------------------
# We need this as we cannot simply start asyncio loop runner (via `asyncio.run(...)`)
# as it would block the main django thread
#
# Therefore, we create a separate ColaboFlow's `asyncio_loop_thread` that will run the asyncio loop
# and receive all the ColaboFlow requests
# --------------------------

asyncio_loop_thread: threading.Thread = None
threaded_django_asyncio_loop: asyncio.AbstractEventLoop = None
running_asyncio_loop: asyncio.AbstractEventLoop = None

async def _threaded_colaboFlow_django_main():
	"""
	Lunches a local (django) ColaboFlow client under a separate django thread with a separate django asyncio loop and keeps it running/alive within a `while ... asyncio.sleep()` loop forever

	TODO: make a more friendly on-keyboard exit

	NOTE: runs in a separate `asyncio_loop_thread` thread with a separate `threaded_django_asyncio_loop` loop
	"""

	global threaded_django_asyncio_loop, running_asyncio_loop
	print(f"{appNameTextWithContext('_threaded_colaboFlow_django_main')} launching colaboFlow on the threaded_django_asyncio_loop: {threaded_django_asyncio_loop}")

	# we need to set it here as (currently) the calling function (`_threaded_colaboFlow_django_loop()`)
	# doesn't create an asyncio event loop but this method is started with `asyncio.run()` which creates loop internally
	# before launching this function
	threaded_django_asyncio_loop = asyncio__provide_and_set_loop(appNameTextWithContext)

	# lunch a local (django) colabo client under a separate django thread with a separate django asyncio loop
	await colaboFlow_client_run()

	# keeps alive the django asyncio event loop
	while True:
		print(f'{appNameTextWithContext("_threaded_colaboFlow_django_main")} threaded_django_asyncio_loop: {threaded_django_asyncio_loop}, beep ...')
		await asyncio.sleep(7)

def _threaded_colaboFlow_django_loop():
	"""
	NOTE: runs in a separate `asyncio_loop_thread` thread with a separate `threaded_django_asyncio_loop` loop
	"""

	# global threaded_django_asyncio_loop

	# threaded_django_asyncio_loop = asyncio__provide_and_set_loop(appNameTextWithContext)
	# print(f"{appNameTextWithContext('_threaded_colaboFlow_django_loop')} created/received the asyncio loop: {threaded_django_asyncio_loop}")

	# TODO: would be healthier if we can run with `threaded_django_asyncio_loop.run_forever()` and
	# 1) make loop running forever and
	# 2) avoid having wired `while True` in the `_threaded_colaboFlow_django_main`
	asyncio.run(_threaded_colaboFlow_django_main())
	# print(f"{appNameTextWithContext('_threaded_colaboFlow_django_loop')} starting: threaded_django_asyncio_loop.run_forever()")
	# threaded_django_asyncio_loop.run_forever()

def colaboFlow_django_start_loop(
	_colaboFlow_client_run: Callable,
	_appNameTextWithContext: Callable,
	_colaboFlow_client_ExecuteTask_Asynced: Callable,
):
	global asyncio_loop_thread, colaboFlow_client_run, appNameTextWithContext, colaboFlow_client_ExecuteTask_Asynced

	colaboFlow_client_run = _colaboFlow_client_run
	appNameTextWithContext = _appNameTextWithContext
	colaboFlow_client_ExecuteTask_Asynced = _colaboFlow_client_ExecuteTask_Asynced

	if asyncio_loop_thread:
		raise Exception(f"{appNameTextWithContext('colaboFlow_django_start_loop')} Error, asyncio_loop_thread is already started. asyncio_loop_thread: {asyncio_loop_thread}")

	asyncio_loop_thread = threading.Thread(target=_threaded_colaboFlow_django_loop)
	asyncio_loop_thread.name = f'{asyncio_loop_thread.name}___threaded_colaboFlow_django_loop'
	asyncio_loop_thread.start()
	native_id = asyncio_loop_thread.native_id
	print(f"{appNameTextWithContext('colaboFlow_django_start_loop')} OK, the 'asyncio_loop_thread' thread  (with the native native_id: {chalk.blue.bold(native_id)} ) is spawned with through function '_threaded_colaboFlow_django_loop'")

def colaboFlow_django_ExecuteTask_Asynced(taskId: str, taskInput: Any)->None:
	global threaded_django_asyncio_loop

	if not appNameTextWithContext:
		errMsg = f'[colaboFlow_django_ExecuteTask_Asynced] Error. Missing `appNameTextWithContext`. Did you forget to call `colaboFlow_django_start_loop()`'
		print(errMsg)
		raise Exception(errMsg)

	if not threaded_django_asyncio_loop:
		errMsg = f'{appNameTextWithContext("colaboFlow_django_ExecuteTask_Asynced")} Error. Missing `threaded_django_asyncio_loop`. Did you forget to call `colaboFlow_django_start_loop()`'
		print(errMsg)
		raise Exception(errMsg)
	print(f'{appNameTextWithContext("colaboFlow_django_ExecuteTask_Asynced")} executing taskId: {taskId} on the threaded_django_asyncio_loop: {threaded_django_asyncio_loop}')
	threaded_django_asyncio_loop.call_soon_threadsafe(colaboFlow_client_ExecuteTask_Asynced, taskId, taskInput)

