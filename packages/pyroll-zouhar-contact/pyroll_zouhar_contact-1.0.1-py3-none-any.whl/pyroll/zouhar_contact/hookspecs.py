from pyroll.core import RollPass


@RollPass.hookspec
def zouhar_contact_c1(roll_pass):
    """Get the value of the Zouhar C1 constant for the given roll pass.
    Return None if the implementation cannot serve this.
    The first not None result is taken."""


@RollPass.hookspec
def zouhar_contact_c2(roll_pass):
    """Get the value of the Zouhar C2 constant for the given roll pass.
    Return None if the implementation cannot serve this.
    The first not None result is taken."""


@RollPass.hookspec
def zouhar_contact_c3(roll_pass):
    """Get the value of the Zouhar C3 constant for the given roll pass.
    Return None if the implementation cannot serve this.
    The first not None result is taken."""


@RollPass.hookspec
def zouhar_contact_in_width(roll_pass):
    """Get the value of the incoming profile width for the given roll pass.
    Return None if the implementation cannot serve this.
    The first not None result is taken."""
