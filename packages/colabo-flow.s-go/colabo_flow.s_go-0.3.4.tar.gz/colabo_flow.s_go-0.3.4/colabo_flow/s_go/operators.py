# https://docs.python.org/3/library/uuid.html
import uuid
from colabo_flow.s_go.vos import ( EColaboFlowGoMsgType, IColaboFlowGoMsg )

def createGoMsg(sender: str, type: EColaboFlowGoMsgType) -> IColaboFlowGoMsg:
	msg =  IColaboFlowGoMsg(
		id = f"ColaboFlow-msg:{uuid.uuid1()}",
		requestId = f"ColaboFlow-request:{uuid.uuid1()}",
		sender = sender,
		# replyTo = "test",
		proxies = [],
		msgReplyChainIds = [],
		type = type,
	)

	return msg
