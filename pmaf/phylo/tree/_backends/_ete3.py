import ete3


class TreeEte3Base:
    def __init__(self, tree, src="newick", copy=False):
        if src == "newick-fp":
            self._tree = ete3.PhyloTree(tree, quoted_node_names=True, format=1)
        elif src == "newick-str":
            self._tree = ete3.PhyloTree(tree, quoted_node_names=True, format=1)
        elif src == "object":
            if isinstance(tree, ete3.Tree):
                if copy:
                    self._tree = tree.copy()
                else:
                    self._tree = tree
            else:
                raise TypeError("`tree` has invalid type.")
        else:
            raise TypeError("`tree` has invalid type.")

    def write_newick(
        self,
        tree_fp,
        tree_format=1,
        root_node=False,
        output_format="newick",
        quoted_nodes=False,
        **kwargs
    ):
        if output_format == "newick":
            return self._tree.write(
                format=tree_format,
                outfile=tree_fp,
                format_root_node=root_node,
                quoted_node_names=quoted_nodes,
            )
        else:
            raise NotImplementedError

    def get_string(
        self,
        tree_format=1,
        root_node=False,
        output_format="newick",
        quoted_nodes=False,
        **kwargs
    ):
        if output_format == "newick":
            return self._tree.write(
                format=tree_format,
                format_root_node=root_node,
                quoted_node_names=quoted_nodes,
            )
        else:
            raise NotImplementedError

    def ladderize(self):
        self._tree.ladderize()

    def unroot(self):
        self._tree.unroot()

    def sort(self):
        self._tree.sort_descendants()

    def prune_for_ids(self, node_ids):
        ret = False
        if type(node_ids) == set:
            ret = self._tree.prune(list(node_ids), preserve_branch_length=True)
        return ret

    def copy(self):
        return TreeEte3Base(self._tree, src="object", copy=True)

    def get_ascii_art(self):
        ret = self._tree.get_ascii(show_internal=False)
        return ret

    def resolve_polytomy(self):
        return self._tree.resolve_polytomy()

    def make_tree_art(self, tree_art_file_path):
        tree_style = ete3.TreeStyle()
        tree_style.show_leaf_name = False
        tree_style.show_branch_length = True
        tree_style.show_branch_support = False

        def custom_layout(node):
            node_face = ete3.TextFace(node.name, tight_text=False)
            ete3.add_face_to_node(node_face, node, column=0, position="branch-right")

        tree_style.layout_fn = custom_layout
        ret = self._tree.render(tree_art_file_path, tree_style=tree_style)
        return ret

    def get_tips(self, names=False):
        return tuple(
            [
                node.name if names else node
                for node in self._tree.traverse()
                if node.is_leaf()
            ]
        )

    def get_nodes(self, names=False):
        return tuple([node.name if names else node for node in self._tree.traverse()])

    def get_internal_nodes(self, names=False):
        return tuple(
            [
                node.name if names else node
                for node in self._tree.traverse()
                if not node.is_leaf()
            ]
        )

    def find_node_by_name(self, node_name):
        return next(self._tree.iter_search_nodes(name=node_name))

    def get_mcra_node_for_nodes(self, nodes):
        return self._tree.get_common_ancestor(nodes)

    def detach_node(self, node):
        return node.detach()

    def add_str_node_names(self, map_dict, only_tips):
        for node in self._tree.traverse():
            if node.name in map_dict.keys():
                if only_tips:
                    if node.is_leaf():
                        node.name = "{} [{}]".format(
                            str(node.name), map_dict[node.name]
                        )
                else:
                    node.name = "{} [{}]".format(str(node.name), map_dict[node.name])
        return

    @staticmethod
    def get_node_copy(node):
        tmp_node = ete3.PhyloTree()
        for feature in node.features:
            tmp_node.add_feature(feature, getattr(node, feature))
        return tmp_node

    def replace_node_names(self, map_dict, only_tips):
        for node in self._tree.traverse():
            if node.name in map_dict.keys():
                if only_tips:
                    if node.is_leaf():
                        node.name = map_dict[node.name]
                else:
                    node.name = map_dict[node.name]
        return

    def count(self):
        return len(self._tree)

    @property
    def engine(self):
        return self._tree

    @property
    def name(self):
        return "ETE3"
