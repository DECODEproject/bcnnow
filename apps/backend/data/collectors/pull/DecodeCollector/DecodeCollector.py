import sys
sys.path.append('/home/code/projects/decode-bcnnow/')

from apps.backend.data.collectors.polling.DecodeCollector.Config import Config as collectorConfig
collectorCfg = collectorConfig().get()
from config.Config import Config as globalConfig
globalCfg = globalConfig().get()

class DecodeCollector:

    def __init__(self, ):
        return

    # Start reader process
    def start(self, base, resourceIDs=[]):
        return

    # Send request to get data
    def sendRequest(self, url):
        return

    # Build a record in the standard format
    def buildRecord(self, item):
        return

    # Save data to permanent storage
    def saveData(self, data):
        return

if __name__ == "__main__":
    DecodeCollector().start('', [])