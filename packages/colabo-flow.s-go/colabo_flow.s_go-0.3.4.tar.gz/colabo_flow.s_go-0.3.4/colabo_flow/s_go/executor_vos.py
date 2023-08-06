# describes types used in the ColaboFlow.GO puzzle

from dataclasses import dataclass, field
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
from enum import Enum

from pika.channel import Channel
from typing import Optional, NamedTuple

""" Environment under which the executor can execute """
# PY > 3.4
class EExecutingEnvironment(str, Enum):
	""" Executor can execute on any environment, no environment related code """
	ISOMORPHIC = "ISOMORPHIC",
	""" Executor has frontend dependencies """
	FRONTEND = "FRONTEND",
	""" Executor has backend dependencies """
	BACKEND = "BACKEND",

"""
references to the executor implementation
"""
@dataclass
class IExecutorImplementationReference():
	method: Optional[Callable] = None; # TExecutorReferenceMethod
	async_method: Optional[Callable] = None; # TExecutorReferenceMethod

"""
Describes a task executor, its location, initiation, environment, etc
"""
@dataclass
class ITaskExecutor():
	"""
	id of executor. It should be unique
	at least at the level of each environment
	(maybe we should keep it unique overall, as, for example, isomorphic executors can migrate environments)
	"""
	id: str

	""" describes executor """
	description: str

	"""where the executor can be executed"""
	environment: EExecutingEnvironment

	"""reference to the executor implementation"""
	reference: IExecutorImplementationReference

"""
Tells the type of an event
https://www.lucidchart.com/pages/bpmn-activity-types
"""
class EFlowTaskType(str, Enum):
	REGULAR = "TASK.REGULAR",
	LOOP = "TASK.LOOP",
	MULTIPLE_PARALLEL = "TASK.MULTIPLE_PARALLEL",
	MULTIPLE_SEQUENTIAL = "TASK.MULTIPLE_SEQUENTIAL",
	COMPENSATION = "TASK.COMPENSATION",
	COMPENSATION_LOOP = "TASK.COMPENSATION_LOOP",

	SUBPROCESS = "TASK.SUBPROCESS",
	SUBPROCESS_LOOP = "TASK.SUBPROCESS_LOOP",
	SUBPROCESS_MULTIPLE_PARALLEL = "TASK.SUBPROCESS_MULTIPLE_PARALLEL",
	SUBPROCESS_MULTIPLE_SEQUENTIAL = "TASK.SUBPROCESS_MULTIPLE_SEQUENTIAL",
	SUBPROCESS_COMPENSATION = "TASK.SUBPROCESS_COMPENSATION",
	SUBPROCESS_ADHOC = "TASK.SUBPROCESS_ADHOC",

	SUBPROCESS_EVENT = "TASK.SUBPROCESS_EVENT",

	TRANSACTION = "TASK.TRANSACTION",

	CALL_ACTIVITY = "TASK.CALL_ACTIVITY",

	# EXECUTABLE
	BUSINESS_RULE = "TASK.BUSINESS_RULE",
	MANUAL = "TASK.MANUAL",
	RECEIVE = "TASK.RECEIVE",
	SCRIPT = "TASK.SCRIPT",
	SEND = "TASK.SEND",
	SERVICE = "TASK.SERVICE",
	USER = "TASK.USER",

"""
 References the executor that should execute the task.
 It also tells the environment in which it should be executed
"""
@dataclass
class IExecutorReference:
	"""
	 id of executor. It should be unique
	 at least at the level of each environment
	 (maybe we should keep it unique overall, as, for example, isomorphic executors can migrate environments)
	 """
	id: str

	"""where the executor should be executed"""
	environment: EExecutingEnvironment

	"""
	 id inside of the executor.

	 It is usually a name or an (lookup) id of a *methodor *exportthat should be executed in the module representing the executor

	 Taken from colabo/src/isomorphic/dev_puzzles/flow/core/lib/flow-types/flow-types-vos.ts
	"""
	subId: Optional[str] = None

class EFlowPlacePortType (str, Enum):
	IN = "IN",
	OUT = "OUT",
	INOUT = "INOUT",

class EFlowPlaceType (str, Enum):
	TASK = "TASK",
	EVENT = "EVENT",
	GATEWAY = "GATEWAY",

IExtension = NamedTuple("IExtension", [
])

"""
Describes ports that a place is connected to other places
"""
@dataclass
class IFlowPlacePort:
	name: str
	type: EFlowPlacePortType

@dataclass
class IFlowPlace:
	"""
	the exact type of the place (to support simpler searching and management)
	TODO: understand if we need it, as places are already distributed across different arrays.
	The distribution can change, often places are aggregated in a single array, and it is really just about extended entity size.
	So probably yes, we will keep it
	"""
	# I had to add the default value to avoid the error `TypeError: non-default argument 'placeType' follows default argument` coming from
	# `class IFlowTask(IFlowPlace, IFlowElement):`
	placeType: EFlowPlaceType = EFlowPlaceType.TASK

	""" additional space for extension of the place without explicit mechanism, like classes implementations or interfaces extensions """
	extension: Optional[IExtension] = None

"""
Describes any flow element either place or sequence, etc
Each of them can have id, name, description
"""
@dataclass
class IFlowElement():
	""" place id, uniquely identifying the place across the flow that contains the place"""
	id: str

	""" name of the place, can overlap with the names of other places inside the flow, but it is not recommended as making confusion"""
	name: Optional[str] = None

	""" description of the place (activity, task, event, ...)"""
	description: Optional[str] = None

	inputs: Optional[list[IFlowPlacePort]] = field(default_factory=list)
	outputs: Optional[list[IFlowPlacePort]] = field(default_factory=list)
	inoutputs: Optional[list[IFlowPlacePort]] = field(default_factory=list)

	# """ transformations required on task inputs and outputs"""
	# transformations: IFlowElementTransformations = None

"""
Describes flow task

Flow Task is conceptually (from the perspective of flow) atomic element of flow execution
With various types of sequences it is connected with other flow entities
"""
@dataclass
class IFlowTask(IFlowPlace, IFlowElement):
	"""
	The type of the task

	if present, it helps to distinguish different types of tasks
	and help with interpreting additional extensions of the task
	"""
	type: Optional[EFlowTaskType] = None

	"""reference to the entity (worker, service, actor) that is designed to execute the task"""
	executorRef: Optional[IExecutorReference] = None

	"""
	Hash array of params that can be provided to the activity in order to tune its behavior to needed one.

	The difference between **params*and **input data*is in that that input data can change on any activity (task instance, a particular execution of task) while `params` are intended to be fixed for all executions of a particular task in the workflow
	"""
	params: dict[str, Any] = field(default_factory=dict)

	# # extends: ITagsArray
	# tags: Optional[list[str]] = field(default_factory=list)

	def __post_init__(self):
		self.placeType = EFlowPlaceType.TASK


@dataclass
class ITagsArray():
	tags: Optional[list[str]] = None

"""
Describes any flow element either place or sequence, etc
Each of them can be tagged, have origin element and initiating token info
"""
@dataclass
class IFlowElementInstance(ITagsArray):

	# I had to add the default value to avoid the error `TypeError: non-default argument 'id' follows default argument` coming from
	"""
	element instance id, uniquely identifying the element across the flow execution engine
	there cannot be any other element execution with the same id in the scope of our (resolution) interest
	"""
	id: str = "<UNDEFINED>"

	# I had to add the default value to avoid the error `TypeError: non-default argument 'originId' follows default argument` coming from
	"""
	the id of the element this is the instance (execution) of
	"""
	originId: str = "<UNDEFINED>"

# 	/** The ids of the tokens that initiated the element instantiation
# 	 * The key to the hash is place's port id at which the token arrived to
# 	 *
# 	 * the record's **key** is port i and
# 	 *
# 	 * record's **value** is token id placed on that port
# 	 *
# 	 * TODO: The motivation to have it here and not at `IFlowPlaceInstance` is that we want to know about non-places (like sequences) what initiated them as well. On the other hand, non places should not bother on the tokens' PRESENCE (as one of the key distinction between flow's place and element). Therefore it could make sense that this should be part of the flow audit, rather than flow instance execution.
# 	 *
# 	 * At the moment we will keep it here, and provide `EFlowSpecialPortIds.DEFAULT` for non-places (specifically sequences)
# 	 */
# 	initiatedTokenIdsPerPorts: Record<str, str>;

# 	/** The list of currently  */
# 	currentTokenIds: str[];

# 	/** The status of the token that initiated the instance of the element
# 	 *
# 	 * TODO: This probably should be renamed and refactored to detach the focus from token to the instance itself, especially when there are more than one token in the instance
# 	 */
# 	tokenStatus: ETokenStatusInFlowPlaceInstance;

"""
Describes place instance of any type of the place in a flow
It tells which type of a place the place is (task, event, gateway, ...)
"""
@dataclass
class IFlowPlaceInstance(IFlowElementInstance):
	# I had to add the default value to avoid the error `TypeError: non-default argument 'placeType' follows default argument` coming from
	"""
	the exact type of the place (to support simpler searching and management)
	TODO: understand if we need it, as place instances are already distributed across different arrays.
	The distribution can change, often places instances are aggregated in a single array, so to get the info we need to drill to places which might be either expensive or not easily possible (when business logic is not close enough to places) and it is really just about extended entity size.
	So probably yes, we will keep it
	"""
	placeType: EFlowPlaceType = EFlowPlaceType.TASK

	# /** References to the place's instance inputs (stored in DataTalksCache)
	#  *
	#  * the key to the record is portId and value is cache entry reference (`IDataTalksCacheEntryReference`)
	#  *
	#  * It references to the data as they arrived to the input port and not the data that got transformed on the way between data arrival to the port and their execution by the task executor
	#  */
	# executionInputReferences: Record<str, IDataTalksCacheEntryReference>;

	# /** References to the place's instance outputs (stored in DataTalksCache)
	#  *
	#  * the key to the record is portId and value is cache entry reference (`IDataTalksCacheEntryReference`)
	#  */
	# executionOutputReferences: Record<str, IDataTalksCacheEntryReference>;

"""
Describes flow task instance

Flow Task instance is conceptually (from the perspective of flow) an instance of atomic element of flow execution
"""
@dataclass
class IFlowTaskInstance(IFlowPlaceInstance):
	"""
	reference to the entity (worker, service, actor) that is designed to execute the task
	"""
	executorInstanceId: Optional[str] = None

	# /** status of the running instance of the task */
	# status: EFlowTaskExecutionStatus;
	# /** The exit value of the task execution
	#  *
	#  * **TODO**:
	#  * + currently not used
	#  * + the idea is to optimise branching out from the task to its successors in a way
	#  * 	+ condensing: avoiding gateways
	#  * 	+ states/variables: avoiding having complex variables for conditioning if condition can be resolved based on the last task exit value only
	#  * + It could still be used as a value transmitted down the control flow and used in the immediately following gateway
	#  * + gateway should use conditional values of its outgoing sequences to understand which sequence to follow
	#  */
	# exitValue?: str
	# /** additional space for extension of the flow without explicit mechanism, like classes implementations or interfaces extensions */
	# extension?: IFlowTaskInstanceExtension;
