import os

os.environ['__fdsdkpy_unittest__'] = 'True'

from tests.dhd import TestExpertSDK, TestOSIndependentSDK, TestStandardSDK
from tests.drd import TestRoboticSDK
from tests.test_constants import TestConstants
from tests.test_containers import TestContainers
from tests.test_numpy_containers import TestNumpyContainers
from tests.test_runtime import TestRuntime
from tests.test_adaptors import TestAdaptors
