from graphviz import Digraph

def generate_ast(parsed_command, filename='ast'):
    """Generate AST visualization as PNG with consistent node sizes"""
    dot = Digraph(comment='AST', format='png')
    
    # Global node styling
    dot.attr('node', 
             shape='ellipse',
             style='filled',
             fillcolor='#f0f8ff',
             fixedsize='true',
             width='1.8',
             height='0.9',
             fontsize='10',
             fontname='Arial')
    
    if isinstance(parsed_command, tuple):
        _add_ast_nodes(dot, parsed_command)
    
    dot.render(filename, view=True, cleanup=True)
    return f"{filename}.png"

def _add_ast_nodes(dot, node, parent_id=None):
    """Recursively add nodes to the AST with proper formatting"""
    max_label_length = 18  # Characters before truncation
    max_value_lines = 2    # Max lines for long values

    # Handle tuple nodes (commands like BOOK, VIEW, etc.)
    if isinstance(node, tuple):
        node_id = str(id(node))
        label = node[0]

        # Truncate long labels
        if len(label) > max_label_length:
            label = f"{label[:max_label_length]}..."

        dot.node(node_id, label=label)
        
        if parent_id:
            dot.edge(parent_id, node_id)

        # Process children, skipping None values
        for child in node[1:]:
            if child is None:
                continue  # Skip None children
                
            if isinstance(child, (tuple, dict, list)):
                _add_ast_nodes(dot, child, node_id)
            else:
                child_label = str(child)
                # Truncate child labels
                if len(child_label) > max_label_length:
                    child_label = f"{child_label[:max_label_length]}..."
                
                child_id = f"{node_id}_{id(child)}"
                dot.node(child_id, label=child_label)
                dot.edge(node_id, child_id)

    # Handle dictionary nodes (command details)
    elif isinstance(node, dict):
        node_id = str(id(node))
        dot.node(node_id, label="Details")
        
        if parent_id:
            dot.edge(parent_id, node_id)

        for key, value in node.items():
            key_id = f"{node_id}_{key}"
            
            # Format value with line breaks
            value_str = str(value)
            if len(value_str) > 15:
                # Split into chunks of 15 characters
                chunks = [value_str[i:i+15] for i in range(0, len(value_str), 15)]
                # Keep max 2 lines and add ellipsis if truncated
                value_str = '\n'.join(chunks[:max_value_lines])
                if len(chunks) > max_value_lines:
                    value_str += '...'

            # Create formatted label with separator
            dot.node(key_id, label=f"{key}\n──\n{value_str}")
            dot.edge(node_id, key_id)

            # Recursively process complex values
            if isinstance(value, (tuple, dict, list)):
                _add_ast_nodes(dot, value, key_id)

    # Handle list nodes (uncommon but possible)
    elif isinstance(node, list):
        node_id = str(id(node))
        dot.node(node_id, label="List")
        
        if parent_id:
            dot.edge(parent_id, node_id)

        for index, item in enumerate(node):
            item_id = f"{node_id}_item{index}"
            if isinstance(item, (tuple, dict, list)):
                _add_ast_nodes(dot, item, node_id)
            else:
                item_label = str(item)
                if len(item_label) > max_label_length:
                    item_label = f"{item_label[:max_label_length]}..."
                dot.node(item_id, label=item_label)
                dot.edge(node_id, item_id)