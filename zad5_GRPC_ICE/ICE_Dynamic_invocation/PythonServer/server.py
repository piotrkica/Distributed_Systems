import Ice
import sys

import Demo

# When running add parameter: --Ice.Config=absolute/path/to/config.server

class CalcI(Demo.Calc):
    def sortBuckets(self, bucketMap, current=None):
        result = []
        for k in sorted(bucketMap.keys()):
            result.extend(sorted(bucketMap[k]))
        print(f"Sorted array of buckets: {result}")
        return result

    def sumOfRoots(self, sq,  current=None):
        result = sum([x**0.5 for x in sq])
        print(f"Sequence: {sq}, result={result}")
        return result

    def payment(self, transaction, current=None):
        print(f"Transaction completed (timestamp={transaction.timestamp}):\n"
              f"{transaction.buyer} transferred to {transaction.seller} {transaction.moneyAmount}zł")


with Ice.initialize(sys.argv) as communicator:
    adapter = communicator.createObjectAdapter("Adapter1")
    adapter.add(CalcI(), communicator.stringToIdentity("Adapter1"))
    adapter.activate()
    communicator.waitForShutdown()
