#! /usr/bin/python3

from lightning import Plugin

plugin = Plugin()

class Merchant:
    
    def __init__(self, address, channels=None):
    	wallet_addres =  address
    	# dict with info about channels
    	channels = channels

    def create_invoice(self, amount):
    	# merchant creates an invoice with the expected <amount> in millisatoshi
    	# label must be a unique string or number (which is treated as a string, so “01” is different from “1”);
    	# it is never revealed to other nodes on the lightning network, but it can be used to query the status of this invoice
    	# lightning-cli invoice <amount> <label> <description>
    	pass
    
    def get_channel_info(self):
    	# A notification for topic channel_opened is sent if a peer
    	# successfully funded a channel with us. It contains the peer id,
	    # the funding amount (in millisatoshis), the funding transaction id, and a boolean indicating if the funding transaction has been included into a block. 
    	pass


    def invoice_payment(self):
    	# on successful invoice payment
    	pass


@plugin.init()
def init(options, configuration, plugin):
	plugin.log("Merchant plugin initialized")


plugin.run()