from pyroll.core import RollPass
from pyroll.utils import for_in_profile_types, for_out_profile_types


@RollPass.hookimpl
@for_in_profile_types("diamond")
@for_out_profile_types("diamond")
def zouhar_contact_c2(roll_pass: RollPass):
    return 0.3


