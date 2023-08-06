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
    root: FullPathModule

    @staticmethod
    def build_graph(
        root_module: str, external_packages: bool
    ) -> Union[ImportGraph, NoReturn]:
        graph = grimp.build_graph(root_module, include_external_packages=external_packages)  # type: ignore[misc]
        root = FullPathModule.assert_module(root_module)
        return ImportGraph(_ImportGraph(graph), root)  # type: ignore[misc]

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
