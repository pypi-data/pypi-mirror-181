import importlib
import inspect
from pathlib import Path
from typing import List, Set, Type

from valid8 import validate

from optool.autocode import Attribute, autocomplete


@autocomplete
class Reflection:
    __slots__ = '_root'
    root: Path = Attribute(validators=[Path.exists, Path.is_dir])

    @classmethod
    def from_package(cls, package):
        validate("The module", package, custom=inspect.ismodule)
        file_path = Path(package.__file__)
        if str(file_path.stem) != "__init__":
            raise ValueError(f"The given package {package!r} is not a package, since its corresponding file is not "
                             f"a '__init__.py' file, but {str(file_path)}. Did you intend to start from a module?")
        # noinspection PyArgumentList
        return cls(file_path.parent)

    @classmethod
    def from_module(cls, module):
        validate("The module", module, custom=inspect.ismodule)
        file_path = Path(module.__file__)
        if str(file_path.stem) == "__init__":
            raise ValueError(f"The given module {module!r} is not a module, since its corresponding file is "
                             f"a '__init__.py' file. Did you intend to start from a package?")
        file_path = Path(module.__file__)
        # noinspection PyArgumentList
        return cls(file_path)

    def find_python_files(self, include_init: bool = True) -> List[Path]:
        paths_generator = self.root.glob("**/*.py")
        if include_init:
            return list(paths_generator)
        return [path for path in paths_generator if str(path.stem) != "__init__"]

    def find_subclasses(self, superclass: Type, include_superclass: bool = False) -> Set[Type]:
        validate("The superclass", superclass, custom=inspect.isclass)

        def predicate(obj):
            return inspect.isclass(obj) and issubclass(obj, superclass)

        classes: List[Type] = []
        for file in self.find_python_files():
            module_name = f"{self.root.stem}.{str(file.relative_to(self.root)).replace('/', '.').replace('.py', '')}"
            classes.extend(cls for name, cls in inspect.getmembers(importlib.import_module(module_name), predicate))

        distinct_classes = set(classes)
        if not include_superclass:
            distinct_classes.remove(superclass)
        return distinct_classes
