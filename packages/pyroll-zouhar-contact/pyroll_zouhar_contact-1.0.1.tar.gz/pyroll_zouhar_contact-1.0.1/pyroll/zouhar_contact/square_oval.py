from pyroll.core import RollPass
from pyroll.utils import for_in_profile_types, for_out_profile_types


@RollPass.hookimpl
@for_in_profile_types("square")
@for_out_profile_types("oval")
def zouhar_contact_c1(roll_pass: RollPass):
    return 0.82


@RollPass.hookimpl
@for_in_profile_types("square")
@for_out_profile_types("oval")
def zouhar_contact_c2(roll_pass: RollPass):
    return 0.2


@RollPass.hookimpl
@for_in_profile_types("square")
@for_out_profile_types("oval")
def zouhar_contact_c3(roll_pass: RollPass):
    return 1.02
