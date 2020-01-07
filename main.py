#!/usr/bin/env python3

from os.path import abspath
from lightning import LightningRpc

def main():
	# Create two instances of the LightningRpc object using two different local c-lightning daemons
	client_node = LightningRpc("/tmp/l1-regtest/regtest/lightning-rpc")
	merchant_node = LightningRpc("/tmp/l2-regtest/regtest/lightning-rpc")
	# start Merchant plugin
	merchant_plugin_path = abspath("Merchant.py")
	response = merchant_node.plugin("start", merchant_plugin_path)
	for plugin in response["plugins"]:
		if plugin["name"] == merchant_plugin_path:
			if plugin["active"] == True:
				break
			else:
				print("Merchant plugin is not loaded")
	print("Merchant plugin initialized")
	# start Client plugin
	client_plugin_path = abspath("Client.py")
	response = client_node.plugin("start", client_plugin_path)
	for plugin in response["plugins"]:
		if plugin["name"] == client_plugin_path:
			if plugin["active"] == True:
				break
			else:
				print("Client plugin is not loaded")
	print("Client plugin initialized")
	# Connect client with merchant node
	# get merchant id, address and port using plugin's RPC method
	merchant_info = merchant_node.connectinfo()
	for i in merchant_info:
		print("Merchant's {} is {}".format(i, merchant_info[i]))
	client_connect_reply = client_node.link(merchant_info["node_id"],
											merchant_info["address"],
											merchant_info["port"])
	if client_connect_reply["code"] == 0:
		print("Client node is connected to Merchant")
	else:
		print("Client node couldn't connect to Merchant")
	# Fund channel with Merchant
	
if __name__ == "__main__":
	main()