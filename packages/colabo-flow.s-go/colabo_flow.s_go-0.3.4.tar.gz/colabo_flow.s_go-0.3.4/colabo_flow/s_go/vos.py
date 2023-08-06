# describes types used in the ColaboFlow.GO puzzle

from dataclasses import dataclass
from enum import Enum
import json

# Patching JSON serialization in order to support serialization of @dataclass objects
# the code is idempotent
# --start--
# --start--
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
if not hasattr(JSONEncoder, "isPatchedFor_to_json"):
	JSONEncoder.default = _default
	JSONEncoder.isPatchedFor_to_json = True
# --end--

from typing import Any, Optional, Callable
from typing import NamedTuple
import threading

from pika.channel import Channel
from pika.connection import Connection
from colabo_flow.s_go.executor_vos import ITaskExecutor, IFlowTask, IFlowTaskInstance

@dataclass
class ReportsConfig:
	"""Reports Configuration Data Class."""
	showHeartbeatMsgs: bool
	showReportsMsgs: bool
	showExecutionMsgs: bool

@dataclass
class ConnectConfig:
	"""Connect Configuration Data Class."""

	APP_NAME: str
	AMQP_URL: str
	ORCHESTRATOR_QUEUE: str
	HOST_HEARTBEAT_QUEUE: str
	HOST_QUEUE: str

	concurrency_TasksNo: int


# PY > 3.4
class EColaboFlowGoMsgType(str, Enum):
	TASK_EXECUTE_REQUEST = "TASK_EXECUTE_REQUEST",
	TASK_EXECUTE_PROGRESS = "TASK_EXECUTE_PROGRESS",
	TASK_EXECUTE_RESPONSE = "TASK_EXECUTE_RESPONSE",
	TASK_INSTANCES_REPORT__REQUEST = "TASK_INSTANCES_REPORT__REQUEST",
	TASK_INSTANCES_REPORT__RESPONSE = "TASK_INSTANCES_REPORT__RESPONSE",
	HEARTBEAT = "HEARTBEAT",

"""
enumeration of all the languages that are supported by ColaboFlow
"""
class EProgrammingLanguageSupported(str, Enum):
	"""Javascript or its extensions that will be compiled to JavaScript eventually (TypeScript, Coffeescript)"""
	JAVASCRIPT = "JAVASCRIPT",
	PYTHON = "PYTHON",
	NATIVE = "NATIVE",

@dataclass
class IColaboFlowGoMsg:
	"""An interface describing messages exchanged between ColaboFlow.GO peers"""
	""" unique message id """
	id: str
	type: EColaboFlowGoMsgType;
	""" unique request id, should be kept the same along the course of a same single message exchange """
	requestId: str
	""" the id of the message sender """
	sender: str
	""" the name of the queue to reply to (if there is a reply to the message) """
	replyTo: str = None
	""" the list of proxies that forwarded the message """
	# PY > 3.9
	proxies: Optional[list[str]] = None
	""" list of msg ids with the history of the replying messages """
	msgReplyChainIds: Optional[list[str]] = None
	""" str message that can be used for human purpose mainly """
	msg: Optional[str] = None

	""" extension for various types of messages """
	extension: Optional[Any] = None

	def to_json(self):
		return json.dumps(self.__dict__)

@dataclass
class IColaboFlowGoMsgExtension_TaskExecute_Request():
	taskId: str
	taskInput: Optional[Any] = None

	def to_json(self):
		return json.dumps(self.__dict__)

class ETaskExecute_Progress_Status(str, Enum):
	INITIALIZED = "INITIALIZED",

"""Message extension for the task execution request"""
@dataclass
class IColaboFlowGoMsgExtension_TaskExecute_Request:
	""" the id if the task executing instance """
	taskId: str;

	"""input to the task we want to execute"""
	taskInput: Any;

	def to_json(self):
		return json.dumps(self.__dict__)

"""Message extension for the task execution progress"""
@dataclass
class IColaboFlowGoMsgExtension_TaskExecute_Progress:
	""" the id if the task executing instance """
	taskInstanceId: str
	""" the current status of the task execution """
	status: ETaskExecute_Progress_Status
	""" the percentage of the task executed """
	progress: float

	def to_json(self):
		return json.dumps(self.__dict__)

"""Message extension for the task execution response"""
@dataclass
class IColaboFlowGoMsgExtension_TaskExecute_Response:
	""" output of the executed task """
	taskOutput: Any

	def to_json(self):
		return json.dumps(self.__dict__)

""" Provides all required info about the task execution request and its progress, etc """
@dataclass
class IColaboFlowGoTaskInstanceInfo():
	""" taskInstance id """
	id: str
	""" task instance """
	taskInstance: IFlowTaskInstance

""" contains all the data that are necessary for a ColaboFlow.Go host to operate """
class IColaboFlowHostData():
	reportsConfig: ReportsConfig
	hostName: str
	amqpUrl: str
	queueHost: str
	queueHostHeartbeat: str
	connection: Optional[Connection] = None
	consumingThread: threading.Thread = None
	chHostHeartbeat: Optional[Channel] = None
	hostMsgRequestConsumerTag: Optional[str] = None
	"""
	the service heartbeat counter
	"""
	heartbeatId: int = 0
	sendHeartbeat: bool = True
	listenForOrchestratorRequests: bool = True
	processOrchestratorTaskExecuteRequests: bool = True

	""" 
	The max number of concurrent tasks that should run on the worker. 

	Default: 1, which means that there is no concurrency, it is just that tasks will be queued and processed from the queue when the worker gets available
	"""
	concurrency_TasksNo: int = 1

	taskExecutorsAvailable: dict[str, ITaskExecutor] = {}
	tasksAvailable: dict[str, IFlowTask] = {}
	taskInstances: dict[str, IFlowTaskInstance] = {}
	threads: list[int] = []

	running: bool = False

	"""
	Provides all required info about the task execution requests (except the executed ones) coming for this particular host and its progress, etc
	Provides all required info about the task execution request and its progress, etc
	***record key*** is the `id` of the `taskInstance`
	"""
	runningTaskInstancesInfos: dict[str, IColaboFlowGoTaskInstanceInfo] = {}

	"""
	Provides all required info about the finalized (finished, stopped, failed, ...) task execution requests coming for this particular host and its progress, etc
	Provides all required info about the task execution request and its progress, etc
	***record key*** is the `id` of the `taskInstance`
	"""
	finalizedTaskInstancesInfos: dict[str, IColaboFlowGoTaskInstanceInfo]

	def __init__(self, reportsConfig, hostName, appNameText, appNameTextWithContext, amqpUrl, queueHost, queueHostHeartbeat, queueServiceOrchestrator, listenForOrchestratorRequests = True, processOrchestratorTaskExecuteRequests = True):
		self.reportsConfig = reportsConfig
		self.hostName = hostName
		self.appNameText = appNameText
		self.appNameTextWithContext = appNameTextWithContext
		self.amqpUrl = amqpUrl
		self.queueHost = queueHost
		self.queueHostHeartbeat = queueHostHeartbeat
		self.queueServiceOrchestrator = queueServiceOrchestrator
		self.listenForOrchestratorRequests = listenForOrchestratorRequests
		self.processOrchestratorTaskExecuteRequests = processOrchestratorTaskExecuteRequests

"""
Contains all the data that are necessary for a ColaboFlow.Go client to operate
"""
class IColaboFlowClientData():
	clientName: str

	appNameText: Optional[str]

	appNameTextWithContext: Optional[Callable]

	amqpUrl: str

	queueServiceOrchestrator: str

	taskInstances: dict[str, IFlowTaskInstance]

	connection: Optional[Connection] = None

	channel: Optional[Channel] = None

	running: bool = False

	consumingThread: threading.Thread = None
	eventsThread: threading.Thread = None

	consumerTag = None

	def __init__(self, clientName, appNameText, appNameTextWithContext, amqpUrl, queueServiceOrchestrator, taskInstances={}, connection=None, channel=None):
		self.clientName = clientName
		self.appNameText = appNameText
		self.appNameTextWithContext = appNameTextWithContext
		self.amqpUrl = amqpUrl
		self.queueServiceOrchestrator = queueServiceOrchestrator
		self.taskInstances = taskInstances
		self.connection = connection
		self.channel = channel

