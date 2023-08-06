"""This module contains the functions to manage path and create trees of tasks"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Union, List, Callable


class Path:
    """represents a path of a task or parameter in a task hierarchy.

    The string notation for paths is that each step is separated by a colon.
    """

    def __init__(self, steps: Union[List[str], str]):
        """Constructor method.

        Args:
            steps: a list of strings containing single steps of the path or a string containing the
                whole path using colons as delimiters between the steps, e.g. "root.taskA.taskB"
        """
        if steps is None:
            self.steps = []
        else:
            if isinstance(steps, str):
                self.steps = steps.split(".")
            else:
                self.steps = steps

    @property
    def target(self):
        """the final step of the path"""
        return self.steps[-1]

    @property
    def length(self):
        """length of the path"""
        return len(self.steps)

    @property
    def root(self):
        """the root of the path"""
        return self.steps[0]

    def parent(self) -> Path:
        """a new path object containing all but the target of this path."""
        return Path(self.steps[:-1])

    def remove(self, path: Path) -> Path:
        """a new path object containing all but the passed path"""
        steps = self.steps.copy()
        remove_steps = path.steps.copy()
        while remove_steps:
            remove_step = remove_steps.pop(0)
            if not steps:
                return Path([])
            if steps[0] == remove_step:
                steps.remove(remove_step)

        return Path(steps)

    def __str__(self):
        return '.'.join(self.steps)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self.steps))

    def __eq__(self, other):
        if not isinstance(other, Path):
            return False
        return self.steps == other.steps

    def __ne__(self, other):
        return not self == other


def concat(path: Path, target: str) -> Path:
    """a new path object with the target added to the path."""
    return Path([*path.steps, target])


def prepend(root: str, other: Path) -> Path:
    """a new path object with the root prepended to the path."""
    return Path([root, *other.steps])


@dataclass
class Node:
    """representing a Node in the task tree"""
    value: object
    children: List[Node]


def is_path_string(string: object) -> bool:
    """check if the string ia a path string"""
    return isinstance(string, str) and string.find('.') != -1


def traverse(tree: Union[List[Node], Node], on_each: Callable):
    """used to traverse to a tree, on_each is called with every node of the tree."""
    stack = []

    if isinstance(tree, list):
        stack.extend(tree)
    elif isinstance(tree, Node):
        stack.append(tree)
    else:
        raise TypeError("tree is neither List[Node] nor Node")

    while stack:
        current_node = stack.pop()

        stack.extend(current_node.children)

        on_each(current_node)
