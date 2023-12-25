class ScrollException(Exception):
    def __init__(self, message):
        super().__init__(message)

class YouLiPlaceException(Exception):
    def __init__(self, message):
        super().__init__(message)

class YouLiLingShiException(Exception):
    def __init__(self, message):
        super().__init__(message)

class TargetRegionNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidOperation(Exception):
    def __init__(self, message):
        super().__init__(message)

class CiShuNotEnoughException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BaiYeOverException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BossNotDefeatedException(Exception):
    def __init__(self, message):
        super().__init__(message)

class FinishedTaskException(Exception):
    def __init__(self, message):
        super().__init__(message)

class TiaoZhanTimesNotEnoughException(Exception):
    def __init__(self, message):
        super().__init__(message)

class MianZhanException(Exception):
    def __init__(self, message):
        super().__init__(message)

class ShuangXiuException(Exception):
    def __init__(self, message):
        super().__init__(message)