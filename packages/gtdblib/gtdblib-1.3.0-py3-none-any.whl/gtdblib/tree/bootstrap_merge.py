from math import floor
from pathlib import Path
from typing import Collection

import dendropy
from rich.progress import track

from gtdblib import log


def bootstrap_merge_replicates(input_tree: Path, output_tree: Path, replicate_trees: Collection[Path]):
    """Calculates non-parametric bootstraps for monophyletic groups and
    transposes them to the input tree.

    :param input_tree: The tree to merge the bootstraps to.
    :param output_tree: The path to write the tree to.
    :param replicate_trees: The trees to calculate the bootstraps from.
    """

    # Validate arguments
    if not isinstance(input_tree, Path):
        raise ValueError(f'Input tree is not a Path object.')
    if not isinstance(output_tree, Path):
        raise ValueError(f'Output tree is not a Path object.')
    if not isinstance(replicate_trees, Collection):
        raise ValueError(f'Replicate trees is not a Collection object.')
    if not all(isinstance(x, Path) for x in replicate_trees):
        raise ValueError(f'Not all replicate trees are Path objects.')

    # Method taken from genometreetk/tree_support.py
    tree = dendropy.Tree.get_from_path(str(input_tree), schema='newick', rooting='force-unrooted',
                                       preserve_underscores=True)
    for node in tree.internal_nodes():
        node.label = 0
        node.nontrivial_splits = 0

    log.info(f'Loading {len(replicate_trees):,} replicate trees')
    for rep_tree_file in track(replicate_trees, description="Processing..."):
        print(rep_tree_file)
        rep_tree = dendropy.Tree.get_from_path(str(rep_tree_file), schema='newick', rooting='force-unrooted',
                                               preserve_underscores=True)

        rep_tree_list = dendropy.TreeList([rep_tree])

        rep_tree_taxa_set = set([x.taxon.label for x in rep_tree.leaf_nodes()])

        for i, node in enumerate(tree.internal_nodes()):
            taxa_labels = set([x.taxon.label for x in node.leaf_nodes()]).intersection(rep_tree_taxa_set)

            split = rep_tree.taxon_namespace.taxa_bitmask(labels=taxa_labels)
            normalized_split = dendropy.Bipartition.normalize_bitmask(
                bitmask=split,
                fill_bitmask=rep_tree.taxon_namespace.all_taxa_bitmask(),
                lowest_relevant_bit=1)

            if len(taxa_labels) > 1:
                # tabulate results for non-trivial splits
                node.label += int(rep_tree_list.frequency_of_bipartition(split_bitmask=normalized_split))
                node.nontrivial_splits += 1

    for node in tree.internal_nodes():
        if node.nontrivial_splits > 0:
            node.label = str(int(floor(node.label * 100.0 / node.nontrivial_splits)))
        else:
            node.label = 'NA'

    tree.write_to_path(str(output_tree), schema='newick', suppress_rooting=True, unquoted_underscores=True)
    log.info(f'Wrote tree to: {output_tree}')

    return
