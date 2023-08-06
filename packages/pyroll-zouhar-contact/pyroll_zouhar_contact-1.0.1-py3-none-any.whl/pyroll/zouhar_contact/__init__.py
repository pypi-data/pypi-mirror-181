from pyroll.core import RollPass

from . import hookspecs

RollPass.plugin_manager.add_hookspecs(hookspecs)

from . import zouhar_contact

RollPass.plugin_manager.register(zouhar_contact)
RollPass.Roll.plugin_manager.register(zouhar_contact)

from . import diamond_square

RollPass.plugin_manager.register(diamond_square)

from . import diamond_diamond

RollPass.plugin_manager.register(diamond_diamond)

from . import oval_square

RollPass.plugin_manager.register(oval_square)

from . import round_oval

RollPass.plugin_manager.register(round_oval)

from . import square_oval

RollPass.plugin_manager.register(square_oval)
