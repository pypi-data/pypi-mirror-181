from pyroll.core import RollPass
from pyroll.utils import for_in_profile_types, for_out_profile_types


@RollPass.hookimpl
@for_in_profile_types("oval")
@for_out_profile_types("square")
def zouhar_contact_c2(roll_pass: RollPass):
    return 0.1


@RollPass.hookimpl
@for_in_profile_types("oval")
@for_out_profile_types("square")
def zouhar_contact_in_width(roll_pass: RollPass):
    return roll_pass.in_profile.local_width(roll_pass.in_profile.height / 2)
