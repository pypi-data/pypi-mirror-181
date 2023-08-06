import click
from typing import Dict
from pathlib import Path
from git import Repo, Commit

from junction import __version__
from junction.confluence import Confluence
from junction.git import (
    find_repository_root,
    find_commits_on_branch_after,
    filter_modifications_to_folder,
    get_modifications,
)
from junction.delta import Delta, MovePage, UpdatePage, CreatePage, DeletePage
from junction.image_attachment import create_image_attachments

@click.command()
@click.option('--content_path',default='docs/',type=click.STRING)
@click.option('--images_path',default='images/',type=click.STRING)
@click.option("--branch", default="main")
@click.option("--since", default="HEAD~1",type=click.STRING)
@click.option('--key', envvar='CONFLUENCE_API_KEY', type=click.STRING)
@click.argument('confluence_api', envvar='CONFLUENCE_API_URL', type=click.STRING)
@click.argument('username', envvar='CONFLUENCE_USERNAME', type=click.STRING)
@click.argument('space', envvar='CONFLUENCE_SPACE_KEY', type=click.STRING)
@click.argument('since',default='HEAD~1')
def main(
    content_path: str,
    images_path: str,
    since: str,
    branch: str,
    confluence_api: str,
    username: str,
    space: str,
    key: str,
) -> None:

    """Tools for managing and publishing to a Confleunce Cloud wiki using Markdown files."""
    confluence = Confluence(
        api_url=confluence_api, 
        username=username, 
        password=key, 
        space_key=space
    )

    repo = _validate_git_dir('.')
    _validate_commitish(repo,since)
    _validate_branch(repo,branch)

    filter_path = Path(content_path)
    commits = find_commits_on_branch_after(branch, since, repo)
    deltas = {
        c: Delta.from_modifications(
            filter_modifications_to_folder(get_modifications(c), filter_path)
        )
        for c in commits
    }

    dry_run = False
    if dry_run:
        __pretty_print_deltas(deltas)
    else:
        if confluence:
            print('Exporting Changed Markdown Files')
            for delta in deltas.values():
                delta.execute(confluence)
            # export images from image directory as attachments
            print("Exporting Images")
            create_image_attachments(content_api=confluence.content,dir=images_path)
            print("Exporting Mermaid Diagrams")
            create_image_attachments(content_api=confluence.content,dir='mermaid')
        else:
            raise RuntimeError(
                "Confluence API client was not setup, but this should never happen; file a bug."
            )


def _validate_git_dir(value: str) -> Repo:
    path = Path(value)
    git_root = find_repository_root(path)
    if git_root is None:
        raise click.BadParameter(
            "junction must be run from within a git repository, or git-dir must point to a git repository"
        )
    else:
        return Repo(value)


def _validate_commitish(repo:Repo, value: str) -> str:
    try:
        if repo.commit(value):
            return value
        else:
            raise click.BadParameter("no commit found by dereferencing that commitish")
    except Exception:
        raise click.BadParameter(
            "this is an invalid commit-ish; valid examples include HEAD~3 or a commit SHA"
        )


def _validate_branch(repo:Repo, value: str) -> str:
    if value in repo.heads:
        return value
    else:
        raise click.BadParameter("you must provide a valid branch name e.g. master")


def __pretty_print_deltas(deltas: Dict[Commit, Delta]) -> None:
    for commit, delta in deltas.items():

        all_operations = (
            delta.adds
            + delta.updates
            + delta.deletes
            + delta.start_renames
            + delta.finish_renames
        )
        click.echo(
            f"{commit.hexsha} ({click.style(str(len(all_operations)), fg='cyan')} changes)"
        )
        for op in all_operations:
            if isinstance(op, CreatePage):
                click.echo(
                    f"\t{click.style('CREATE', fg='green')} {' / '.join(op.ancestor_titles + [op.title])}"
                )
            elif isinstance(op, UpdatePage):
                click.echo(
                    f"\t{click.style('UPDATE', fg='yellow')} {' / '.join(op.ancestor_titles + [op.title])}"
                )
            elif isinstance(op, DeletePage):
                click.echo(f"\t{click.style('DELETE', fg='red')} ?? / {op.title}")
            elif isinstance(op, MovePage):
                click.echo(
                    f"\t{click.style('RENAME', fg='blue')} ?? / {op.title} -> {' / '.join(op.ancestor_titles + [op.new_title])}"
                )
            else:
                click.echo(
                    f"\t{click.style(type(op).__name__, fg='magenta')} {op.title}"
                )
