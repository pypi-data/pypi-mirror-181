from pathlib import Path
from typing import List

import typer

from gtdblib.tree.bootstrap_merge import bootstrap_merge_replicates
from gtdblib.tree.polytomy import collapse_polytomy

app = typer.Typer()


@app.command()
def bootstrap_merge(
        tree: Path = typer.Argument(
            ...,
            help='Path to the Newick tree that bootstrap values will be added to.'
        ),
        output: Path = typer.Argument(
            ...,
            help='Path to the output tree.'
        ),
        replicates: List[Path] = typer.Argument(
            ...,
            help='Path(s) to the replicate tree(s).'
        ),
):
    """
    Calculate non-parametric bootstrap values using multiple trees.
    """
    bootstrap_merge_replicates(tree, output, replicates)


@app.command()
def polytomy(
        tree: Path = typer.Argument(
            ...,
            help='Path to the Newick tree.'
        ),
        output: Path = typer.Argument(
            ...,
            help='Path to the output tree.'
        ),
        support: float = typer.Argument(
            ...,
            min=0.0,
            max=100.0,
            help='Collapse nodes that have a support [red]less than[/red] this value.'
        ),
):
    """
    Collapse nodes with low bootstrap support.
    """
    collapse_polytomy(tree, output, support)
