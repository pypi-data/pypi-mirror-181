from treelib import Tree


def create_tree(tree_list):
    """
    创建树结构
    :param tree_list: 树列表
    :return: 树结构
    """
    tree = Tree()
    for node in tree_list:
        tree.create_node(*node)
    return tree


def get_node_path_by_id(tree, node_id):
    """
    获取节点路径
    :param tree: 树结构
    :param node_id: 节点id
    :return: 节点路径
    """
    path = []
    node_tree = tree.rsearch(node_id)
    while True:
        try:
            path.append(next(node_tree))
        except StopIteration as e:
            break
    return path


def get_node_path_by_tag(tree, node_id):
    """
    获取节点路径
    :param tree: 树结构
    :param node_id: 节点id
    :return: 节点路径
    """
    path = []
    node_tree = tree.rsearch(node_id)
    while True:
        try:
            nodes_id = next(node_tree)
            tag_name = translate_node_id_to_tag(tree, nodes_id)
            path.append(tag_name)
        except StopIteration as e:
            break
    return path


def translate_node_id_to_tag(tree, node_id):
    """
    节点id转换为tag
    :param tree: 树结构
    :param node_id: 节点id
    :return: 节点tag
    """
    node = tree.get_node(node_id)
    tag = node.tag
    return tag
