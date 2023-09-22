import os

os.environ['__forcedim_unittest__'] = 'True'

from tests.dhd import TestExpertSDK, TestOSIndependentSDK, TestStandardSDK
from tests.drd import TestRoboticSDK
from tests.test_constants import TestConstants
