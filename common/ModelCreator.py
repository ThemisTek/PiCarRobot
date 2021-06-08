from enum import Enum

class NetworkEnum(Enum):
    MobileNetSimple = 0
    MobilenetOptimized = 1

class NetworkModel:
    def __init__(self,networkType : NetworkEnum):
        self.networkType = networkType