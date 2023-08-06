from __future__ import (
    annotations,
)

from ._full_path import (
    FullPathModule,
)
from dataclasses import (
    dataclass,
)
import grimp
from grimp.application.ports.graph import (
    AbstractImportGraph,
)
from typing import (
    cast,
    FrozenSet,
    NoReturn,
    Union,
)


@dataclass(frozen=True)  # type: ignore[misc]
class _ImportGraph:  # type: ignore[no-any-unimported]
    graph: AbstractImportGraph  # type: ignore[no-any-unimported]


@dataclass(frozen=True)
class ImportGraph:
    _inner: _ImportGraph
    roots: FrozenSet[FullPathModule]

    @staticmethod
    def from_modules(
        root_modules: Union[FullPathModule, FrozenSet[FullPathModule]],
        external_packages: bool,
    ) -> ImportGraph:
        _root_modules = (
            root_modules
            if isinstance(root_modules, frozenset)
            else frozenset([root_modules])
        )
        raw_modules = frozenset(r.module for r in _root_modules)
        graph = grimp.build_graph(*raw_modules, include_external_packages=external_packages)  # type: ignore[misc]
        return ImportGraph(_ImportGraph(graph), _root_modules)  # type: ignore[misc]

    @classmethod
    def build_graph(
        cls, raw_roots: Union[str, FrozenSet[str]], external_packages: bool
    ) -> Union[ImportGraph, NoReturn]:
        roots = (
            raw_roots
            if isinstance(raw_roots, frozenset)
            else frozenset([raw_roots])
        )
        modules = frozenset(FullPathModule.assert_module(r) for r in roots)
        return cls.from_modules(modules, external_packages)

    def chain_exists(
        self,
        importer: FullPathModule,
        imported: FullPathModule,
        as_packages: bool,
    ) -> bool:
        return cast(
            bool,
            self._inner.graph.chain_exists(importer.module, imported.module, as_packages),  # type: ignore[misc]
        )

    def find_children(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_children(module.module))  # type: ignore[misc]
        return frozenset(FullPathModule.assert_module(i) for i in items)

    def find_modules_that_directly_import(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_modules_that_directly_import(module.module))  # type: ignore[misc]
        return frozenset(FullPathModule.assert_module(i) for i in items)

    def find_modules_directly_imported_by(
        self, module: FullPathModule
    ) -> FrozenSet[FullPathModule]:
        items: FrozenSet[str] = frozenset(self._inner.graph.find_modules_directly_imported_by(module.module))  # type: ignore[misc]
        return frozenset(FullPathModule.assert_module(i) for i in items)


__all__ = [
    "FullPathModule",
]
