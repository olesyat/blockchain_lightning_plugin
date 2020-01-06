#!/usr/bin/env python3

from lightning import Plugin

plugin = Plugin()

@plugin.init()
def init(options, configuration, plugin):
	plugin.log("Client plugin initialized")


plugin.run()