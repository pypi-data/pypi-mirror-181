from pyroll.core import RollPass
from logging import getLogger

_log = getLogger(__name__)


@RollPass.hookimpl
def zouhar_contact_c1(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def zouhar_contact_c2(roll_pass: RollPass):
    return 0


@RollPass.hookimpl
def zouhar_contact_c3(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def zouhar_contact_in_width(roll_pass: RollPass):
    return roll_pass.in_profile.width


@RollPass.Roll.hookimpl
def contact_area(roll_pass: RollPass):
    if (
            roll_pass.zouhar_contact_c1 is not None
            and
            roll_pass.zouhar_contact_c2 is not None
            and
            roll_pass.zouhar_contact_c3 is not None
            and
            roll_pass.zouhar_contact_in_width is not None
    ):
        _log.debug(f"Used Zouhar contact model for roll pass {roll_pass.label}.")
        return (
                       roll_pass.out_profile.width * roll_pass.zouhar_contact_c2
                       + 0.5 * (
                               roll_pass.out_profile.width
                               + roll_pass.zouhar_contact_in_width * roll_pass.zouhar_contact_c1
                       )
                       * (1 - roll_pass.zouhar_contact_c2)
               ) * roll_pass.zouhar_contact_c3 * roll_pass.roll.contact_length
