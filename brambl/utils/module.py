from typing import TYPE_CHECKING, Union, Dict, Sequence, Any, Optional

from brambl.utils.exceptions import ValidationError

if TYPE_CHECKING:
    from brambl import Brambl  # noqa: F401
    from brambl.module import Module  # noqa: F401


def attach_modules(
    parent_module: Union["Brambl", "Module"],
    module_definitions: Dict[str, Sequence[Any]],
    brambl: Optional[Union["Brambl", "Module"]] = None
) -> None:
    for module_name, module_info in module_definitions.items():
        module_class = module_info[0]

        if hasattr(parent_module, module_name):
            raise AttributeError(
                f"Cannot set {parent_module} module named '{module_name}'.  The brambl object "
                "already has an attribute with that name"
            )

        if brambl is None:
            setattr(parent_module, module_name, module_class(parent_module))
            brambl = parent_module
        else:
            setattr(parent_module, module_name, module_class(brambl))

        if len(module_info) == 2:
            submodule_definitions = module_info[1]
            module = getattr(parent_module, module_name)
            attach_modules(module, submodule_definitions, brambl)
        elif len(module_info) != 1:
            raise ValidationError("Module definitions can only have 1 or 2 elements.")
