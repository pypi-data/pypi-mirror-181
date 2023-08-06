
import chatgptprtk.req_call as rc
import chatgptprtk.server_call as sc

bot_eng=rc.chatgptCall()


def setApiKey(api_key=None):
    bot_eng.setApiKey(api_key)

def sendMessage(msg):
    resp=bot_eng.sendMessage(msg)
    return resp

def startServer(host=None,port=None):
    sc.startServer(host,port)