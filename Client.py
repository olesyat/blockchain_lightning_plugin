#! /usr/bin/python3

from lightning import Plugin

plugin = Plugin()


class Client:
	def __init__(self, address):
    	pass


@plugin.init()
def init(options, configuration, plugin):
	plugin.log("Client plugin initialized")


plugin.run()