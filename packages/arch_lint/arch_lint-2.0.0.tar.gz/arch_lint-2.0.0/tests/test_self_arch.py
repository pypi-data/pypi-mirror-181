from .arch import (
    forbidden_allowlist,
    project_dag,
)
from arch_lint.dag.check import (
    check_dag_map,
    dag_map_completeness,
)
from arch_lint.forbidden import (
    check_forbidden,
)
from arch_lint.graph import (
    ImportGraph,
)
from arch_lint.private import (
    check_private,
)

root = "arch_lint"


def test_dag_creation() -> None:
    project_dag()


def test_dag_completeness() -> None:
    graph = ImportGraph.build_graph(root, True)
    dag_map_completeness(project_dag(), graph, graph.root)


def test_dag() -> None:
    graph = ImportGraph.build_graph(root, True)
    check_dag_map(project_dag(), graph)


def test_forbidden_creation() -> None:
    forbidden_allowlist()


def test_forbidden() -> None:
    root = "arch_lint"
    graph = ImportGraph.build_graph(root, True)
    allowlist_map = forbidden_allowlist()
    check_forbidden(allowlist_map, graph)


def test_private() -> None:
    root = "arch_lint"
    graph = ImportGraph.build_graph(root, False)
    check_private(graph, graph.root)
