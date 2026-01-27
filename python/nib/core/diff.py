"""Tree diffing algorithm for efficient UI updates.

This module implements a diffing algorithm to compute the minimal set of
patches needed to transform one view tree into another. This enables
efficient incremental UI updates instead of full re-renders.

The algorithm compares nodes by their position-based IDs and generates
patch operations that the Swift runtime can apply to update the view tree.

Patch Operations:
    - ``replace``: Replace an entire subtree with a new node
    - ``props``: Update a node's properties
    - ``modifiers``: Update a node's modifiers
    - ``insert``: Insert a new child node
    - ``remove``: Remove a node from the tree

Note:
    Currently, incremental patching is disabled in :class:`~nib.App` due to
    Swift-side handling issues. Full renders are used instead.

Example:
    Internal usage::

        old_tree = {"id": "0", "type": "Text", "props": {"content": "Hello"}}
        new_tree = {"id": "0", "type": "Text", "props": {"content": "World"}}
        patches = diff_trees(old_tree, new_tree)
        # patches = [{"op": "props", "id": "0", "props": {"content": "World"}}]
"""

from typing import Any, Dict, List, Optional


def diff_trees(old_tree: Optional[Dict], new_tree: Optional[Dict]) -> List[Dict]:
    """Compute the difference between two view trees.

    Performs a recursive comparison of two serialized view trees and
    generates a list of patch operations that transform old_tree into
    new_tree.

    Args:
        old_tree: The previous view tree dictionary, or None for initial render.
        new_tree: The new view tree dictionary, or None if tree was removed.

    Returns:
        A list of patch operation dictionaries. Each patch has an "op" key
        indicating the operation type and an "id" key for the target node.

    Example:
        >>> old = {"id": "0", "type": "Text", "props": {"content": "A"}}
        >>> new = {"id": "0", "type": "Text", "props": {"content": "B"}}
        >>> patches = diff_trees(old, new)
        >>> patches[0]["op"]
        'props'
    """
    patches = []

    if old_tree is None:
        # First render - send full tree
        if new_tree is not None:
            patches.append({"op": "replace", "id": "0", "node": new_tree})
        return patches

    if new_tree is None:
        # Tree removed
        patches.append({"op": "remove", "id": old_tree.get("id", "0")})
        return patches

    # Diff the trees recursively
    _diff_nodes(old_tree, new_tree, patches)

    return patches


def _diff_nodes(old_node: Dict, new_node: Dict, patches: List[Dict]) -> None:
    """Recursively diff two nodes and collect patches.

    Compares node IDs, types, properties, modifiers, and children.
    Generates appropriate patch operations for any differences found.

    Args:
        old_node: The previous node dictionary.
        new_node: The new node dictionary.
        patches: List to append patch operations to.
    """
    old_id = old_node.get("id")
    new_id = new_node.get("id")

    # If IDs don't match, it's a different node - replace entire subtree
    if old_id != new_id:
        patches.append({"op": "replace", "id": new_id, "node": new_node})
        return

    # Same ID - check for changes
    node_id = new_id

    # Check if type changed (shouldn't happen with same ID, but just in case)
    if old_node.get("type") != new_node.get("type"):
        patches.append({"op": "replace", "id": node_id, "node": new_node})
        return

    # Check props changes
    old_props = old_node.get("props") or {}
    new_props = new_node.get("props") or {}

    if old_props != new_props:
        patches.append({"op": "props", "id": node_id, "props": new_props})

    # Check modifiers changes
    old_modifiers = old_node.get("modifiers")
    new_modifiers = new_node.get("modifiers")

    if old_modifiers != new_modifiers:
        patches.append({"op": "modifiers", "id": node_id, "modifiers": new_modifiers})

    # Diff children
    old_children = old_node.get("children") or []
    new_children = new_node.get("children") or []

    _diff_children(old_children, new_children, patches)


def _diff_children(old_children: List[Dict], new_children: List[Dict], patches: List[Dict]) -> None:
    """Diff two lists of child nodes.

    Compares children by their IDs to detect additions, removals, and
    modifications. Uses set operations for efficient lookup.

    Args:
        old_children: List of previous child node dictionaries.
        new_children: List of new child node dictionaries.
        patches: List to append patch operations to.
    """
    # Build maps by ID for efficient lookup
    old_by_id = {child.get("id"): child for child in old_children}
    new_by_id = {child.get("id"): child for child in new_children}

    old_ids = set(old_by_id.keys())
    new_ids = set(new_by_id.keys())

    # Removed nodes
    for removed_id in old_ids - new_ids:
        patches.append({"op": "remove", "id": removed_id})

    # Added nodes
    for added_id in new_ids - old_ids:
        patches.append({"op": "insert", "id": added_id, "node": new_by_id[added_id]})

    # Potentially modified nodes (exist in both)
    for common_id in old_ids & new_ids:
        _diff_nodes(old_by_id[common_id], new_by_id[common_id], patches)


def flatten_tree(tree: Optional[Dict]) -> Dict[str, Dict]:
    """Flatten a tree into a dict of id -> node for quick lookup.

    Creates a flat dictionary mapping node IDs to their properties,
    useful for O(1) lookups when comparing trees.

    Args:
        tree: The root of the view tree to flatten.

    Returns:
        Dictionary mapping node IDs to node dictionaries containing
        only type, props, and modifiers (no children).

    Example:
        >>> tree = {"id": "0", "type": "VStack", "children": [
        ...     {"id": "0.0", "type": "Text", "props": {"content": "Hi"}}
        ... ]}
        >>> flat = flatten_tree(tree)
        >>> flat["0.0"]["type"]
        'Text'
    """
    result = {}
    if tree is None:
        return result

    def _flatten(node: Dict):
        node_id = node.get("id")
        if node_id:
            # Store a shallow copy without children for comparison
            result[node_id] = {
                "type": node.get("type"),
                "props": node.get("props"),
                "modifiers": node.get("modifiers"),
            }
        children = node.get("children") or []
        for child in children:
            _flatten(child)

    _flatten(tree)
    return result
