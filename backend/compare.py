# compare.py

import ast
from zss import Node, simple_distance

# This class will convert AST nodes into a tree structure usable by zss
class ASTNodeWrapper(ast.NodeVisitor):
    def generic_visit(self, node):
        label = type(node).__name__  # Get the node type name (e.g., FunctionDef, Return)
        zss_node = Node(label)  # Create a ZSS tree node with that label

        # Visit child nodes and add them as children
        for field_name, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        zss_node.addkid(self.generic_visit(item))
            elif isinstance(value, ast.AST):
                zss_node.addkid(self.generic_visit(value))

        return zss_node

# This function converts code (as string) into a ZSS-compatible AST tree
def convert_ast_to_tree(code):
    try:
        parsed = ast.parse(code)
        wrapper = ASTNodeWrapper()
        return wrapper.generic_visit(parsed)
    except Exception as e:
        print("AST parsing failed:", e)
        return None

# Helper function to calculate size of a tree
def get_tree_size(node):
    size = 1  # Count current node
    for child in node.children:
        size += get_tree_size(child)
    return size

# Main similarity calculator
def calculate_similarity(code1, code2):
    tree1 = convert_ast_to_tree(code1)
    tree2 = convert_ast_to_tree(code2)

    if tree1 is None or tree2 is None:
        return 0.0  # If parsing fails, return 0% similarity

    distance = simple_distance(tree1, tree2)  # Lower = more similar

    size1 = get_tree_size(tree1)
    size2 = get_tree_size(tree2)
    max_size = max(size1, size2)

    similarity = 1 - (distance / max_size)
    return round(similarity * 100, 2)  # Return percentage
