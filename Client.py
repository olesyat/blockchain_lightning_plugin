#!/usr/bin/env python3

from lightning import Plugin

plugin = Plugin()

@plugin.init()
def init(options, configuration, plugin):
	plugin.log("Client plugin initialized")


@plugin.method("link")
def link(plugin, id, host=None, port=None):
	peer = id
	if host is not None: peer += "@" + str(host)
	if port is not None: peer += ":" + str(port)
	response = plugin.rpc.connect(peer)
	plugin.log("client plugin link method's response for peer with id {} is {}".format(id, response))
	if "id" in response.keys():
		if response["id"] == id:
			return {"code": 0}
	else:
		return response 


# fund channel with merchant
@plugin.method("createchannel")
def create_channel(plugin, id, amount):
	pass


# pay invoice
@plugin.method("payinvoice")
def pay(plugin, bolt11):
	response = plugin.rpc.pay(bolt11)


# get payment status


# 

plugin.run()