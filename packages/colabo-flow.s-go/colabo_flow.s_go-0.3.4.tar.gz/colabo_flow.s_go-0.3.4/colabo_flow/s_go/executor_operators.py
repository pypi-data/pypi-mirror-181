import uuid

from colabo_flow.s_go.executor_vos import EFlowPlaceType, IFlowTask, IFlowTaskInstance
"""
Creates a task-instance of the provided task. The task instance will relate to its originating task through the `originId` prop

@param task the task we want to create the instance of
@returns the created task instance of the provided task
"""
def createTaskInstanceForTaskWithoutFlow(task: IFlowTask)->IFlowTaskInstance:
	taskInstance: IFlowTaskInstance = IFlowTaskInstance(
		id = f'{task.id}:{uuid.uuid1()}',
		originId = task.id,
		placeType = EFlowPlaceType.TASK,
		# TBD
		# status = EFlowTaskExecutionStatus.WAITING,
		# tokenStatus = ETokenStatusInFlowPlaceInstance.JUST_ENTERED,
		# initiatedTokenIdsPerPorts = {},
		# executionInputReferences = {},
		# executionOutputReferences = {},
		# currentTokenIds = [],
	)
	return taskInstance
