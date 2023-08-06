from colabo_flow.s_go.vos import ReportsConfig, ConnectConfig

AMQP_URL = "localhost";
ORCHESTRATOR_QUEUE = "colabo.flow.orchestrator";
HOST_NODE_QUEUE = "colabo.flow.host.node";
HOST_PYTHON_QUEUE = "colabo.flow.host.python";
HOST_HEARTBEAT_QUEUE = "colabo.flow.host.heartbeat";

reportsConfig = ReportsConfig(
	showHeartbeatMsgs = False,
	showReportsMsgs = True,
	showExecutionMsgs = True,
)

connectConfig = ConnectConfig(
	APP_NAME="client-python",
	AMQP_URL=AMQP_URL,
	ORCHESTRATOR_QUEUE=ORCHESTRATOR_QUEUE,
	HOST_HEARTBEAT_QUEUE=HOST_HEARTBEAT_QUEUE,
	HOST_QUEUE=HOST_PYTHON_QUEUE
)
