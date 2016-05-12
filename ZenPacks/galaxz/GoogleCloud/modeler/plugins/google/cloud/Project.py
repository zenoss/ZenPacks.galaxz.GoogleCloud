import logging
LOG = logging.getLogger("zen.GoogleCloud")

# Zenoss Imports
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

# Twisted Imports
from twisted.internet.defer import inlineCallbacks, returnValue

# ZenPack Imports
from ZenPacks.galaxz.GoogleCloud import txgcp


class Project(PythonPlugin):

    relname = "instances"
    modname = "ZenPacks.galaxz.GoogleCloud.Instance"

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
        for zone in zones['items']:
            r = yield client.instances(zone=zone["name"])
            if "items" in r:
                instances.extend(r['items'])

        returnValue({"instances": instances})

    def process(self, device, results, unused):
        LOG.info("%s: processing data", device.id)

        rm = self.relMap()

        for instance in results["instances"]:
            rm.append(self.objectMap({
                "id": self.prepId("instance-{}".format(instance["id"])),
                "title": instance["name"],
                "description": instance.get("description"),
                "zone": instance.get("zone", "").split("/")[-1],
                "machineType": instance.get("machineType", "").split("/")[-1],
                "diskCount": len(instance.get("disks", [])),
                "nicCount": len(instance.get("networkInterfaces", [])),
                "status": instance.get("status"),
                }))

        return rm
