class MockRTDEControlInterface:
    def __init__(self, ip_address):
        pass

    def getJointTorques(self):
        return [0.0] * 6

    def stopL(self, acceleration):
        pass

    def moveL(self, pose, asynchronous=False):
        pass


class MockRTDEReceiveInterface:
    def __init__(self, ip_address):
        pass

    def getActualTCPPose(self):
        return [0.0] * 6


