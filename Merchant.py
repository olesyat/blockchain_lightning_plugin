#!/usr/bin/env python3

from lightning import LightningRpc
from lightning import Plugin

plugin = Plugin()

created_invoices = dict()
connected_peers = dict()
opened_channels = dict()


@plugin.init()
def init(options, configuration, plugin, request):
    """"""
    plugin.log("Merchant plugin initialized")


@plugin.method("connectinfo")
def connect_info(plugin):
    """"""
    info = plugin.rpc.getinfo()
    return {
            "node_id": info["id"], 
            "address": info["binding"][0]["address"],
            "port": info["binding"][0]["port"]
            }


@plugin.subscribe("connect")
def on_connect(plugin, id, address):
    """"""
    plugin.log("Received connect event for peer {}".format(id))
    connected_peers[id] = address


@plugin.subscribe("disconnect")
def on_connect(plugin, id):
    """"""
    plugin.log("Received disconnect event for peer {}".format(id))
    connected_peers.pop(id)


@plugin.subscribe("channel_opened")
def on_opened_channel(plugin, id, funding_satoshis, funding_txid, funding_locked):
    plugin.log("Peer with id {} successfully funded channel with capacity {}".format(id, funding_satoshis))
    opened_channels[id] = {"capacity": funding_satoshis, "txid": funding_txid, "in_block":funding_locked}


@plugin.method("openedchannels")
def list_channels(plugin):
    return opened_channels

@plugin.method("createinvoice")
def create_invoice(plugin, amount, label, description, expiry="1m"):
    """"""
    invoice = plugin.rpc.invoice(amount, label, description, expiry)
    created_invoices[label] = {"amount": amount, "description": description, "expiry": expiry, "hash":invoice}
    return invoice


@plugin.method("invoicestatus")
def invoice_status(plugin, label=None):
    """Return the status of a specific invoice, if it exists, or the status of all invoices if given no label"""
    return plugin.rpc.listinvoices(label) if label != None else plugin.rpc.listinvoices()


@plugin.method("funds")
def list_funds(plugin):
    """Lists the total funds the lightning node owns off- and onchain in BTC."""
    unit = "BTC"
    div =  100*1000*1000
    funds = plugin.rpc.listfunds()
    onchain_value = sum([int(x["value"]) for x in funds["outputs"]])
    offchain_value = sum([int(x["channel_sat"]) for x in funds["channels"]])
    total_funds = onchain_value + offchain_value
    return {
        'total_'+unit: total_funds//div,
        'onchain_'+unit: onchain_value//div,
        'offchain_'+unit: offchain_value//div,
    }


@plugin.subscribe("invoice_payment")
def on_invoice_payment(plugin, label, preimage, msat):
    """"""
    created_invoices.pop(label)
    plugin.log("Invoice (label {}, msat {}) was paid".format(label, msat))


plugin.run()
