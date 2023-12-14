def calculate_overlapping_nodes(node_min,node_max, instance_min, instance_max):
    if (instance_min <= node_min <= instance_max) or (instance_min <= node_max <= instance_max):
        return True
    if (node_min <= instance_min <= node_max) or (node_min <= instance_max <= node_max):
        return True
    return False
    
print(calculate_overlapping_nodes(58, 60, 40, 70)) # True
print(calculate_overlapping_nodes(50, 60, 55, 70)) # True
print(calculate_overlapping_nodes(50, 60, 55, 58)) # True
print(calculate_overlapping_nodes(50, 60, 40, 45)) # False
print(calculate_overlapping_nodes(50, 60, 65, 85)) # False