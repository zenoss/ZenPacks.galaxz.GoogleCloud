import logging
LOG = logging.getLogger("zen.GoogleCloud")

# Zenoss Imports
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

# Twisted Imports
from twisted.internet.defer import inlineCallbacks, returnValue

# ZenPack Imports
from ZenPacks.galaxz.GoogleCloud import txgcp


class Project(PythonPlugin):
    required_properties = (
        'zGoogleCloudProjectId',
        'zGoogleCloudClientEmail',
        'zGoogleCloudPrivateKey',
        )

    deviceProperties = (
        PythonPlugin.deviceProperties +
        required_properties)

    @inlineCallbacks
    def collect(self, device, unused):
        LOG.info("%s: collecting data", device.id)

        client = txgcp.Client(
            device.zGoogleCloudProjectId,
            device.zGoogleCloudClientEmail,
            "\n".join(device.zGoogleCloudPrivateKey))

        instances = []

        zones = yield client.zones()
        import pdb; pdb.set_trace()
        for zone in zones:
            r = yield client.instances(zone=zone["id"])
            instances.extend(r)

        returnValue(instances)

    def process(self, device, results, unused):
        LOG.info("%s: processing data", device.id)

        import pdb; pdb.set_trace()

        return None
