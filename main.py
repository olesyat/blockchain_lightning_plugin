#!/usr/bin/env python3

import bitcoin.rpc
import random
from os.path import abspath
from lightning import LightningRpc

bitcoin.SelectParams("regtest")

def main():
	# Create RPC connection to bitcoin daemon
	bt_cli = bitcoin.rpc.Proxy()
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
	
	# Fund channel with Merchant, 0.1BTC = 10.000.000 satoshi
	client_channel_reply = client_node.createchannel(merchant_info["node_id"], "0.1btc")
	print("Channel was funded")
	
	print("Current blockchain height is ", bt_cli.getblockcount())
	
	# Include funding transaction in blockchain
	address = bt_cli.getnewaddress()
	bt_cli.generatetoaddress(6, address)
	print("Current blockchain height is ", bt_cli.getblockcount())
	
	# Waiting for lightningd synchronize with bitcoind
	route = False
	while not route:
		try:
			route = client_node.getroute(merchant_info["node_id"], 100, 1)
		except Exception as e:
			continue
	print("Route was found")
	
	# Create invoice 
	invoice_label = "invoice#1"
	merchant_invoice = merchant_node.createinvoice(100, invoice_label, "test payment to merchant")
	
	# Pay by invoice
	client_pay_reply = client_node.payinvoice(merchant_invoice["bolt11"])
	
	# Wait for payment status to become complete
	client_node.waitsendpay(merchant_invoice["payment_hash"])
	print("Client's payment complete")
	
	# Wait for invoice status to become paid
	merchant_node.waitinvoice(invoice_label)
	print("Merchant's invoice is paid")
	
	# Close payment channel
	client_node.close(client_channel_reply["channel_id"])

	# Include final transaction in blockchain
	bt_cli.generatetoaddress(6, address)


if __name__ == "__main__":
	main()
