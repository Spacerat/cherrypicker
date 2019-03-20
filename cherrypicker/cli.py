#! /usr/bin/env python3

import sh
import click
import re


def real_git(*args, **kwargs):
    mock_git(*args, **kwargs)
    return sh.git(*args, **kwargs)


def mock_git(*args, **kwargs):
    click.echo(sh.git.bake(*args, **kwargs), err=True)
    return ""


def branch_exists(name):
    try:
        get_commit_hash(name)
        return True
    except:
        return False


def get_current_branch():
    return sh.git("rev-parse", "--abbrev-ref", "HEAD").strip()


def get_commit_hash(commit_spec):
    return sh.git("rev-parse", commit_spec).strip()


@click.command()
@click.argument("commit", type=str)
@click.argument("branch", type=str)
@click.option("--base", type=str, default="origin/master", help="Base branch to branch from")
@click.option("--push/--no-push", default=True, help="Push the feature branch")
@click.option("--new/--not-new", default=False, help="Make a new branch")
@click.option("--switch/--no-switch", default=False, help="Switch to the other branch")
@click.option("--mock/--real", default=False, help="Just print git commands")
def main(commit, branch, base, push, new, switch, mock):
    """ COMMIT: a commit range to be cherry-picked into BRANCH, e.g. HEAD^1 or HEAD..HEAD~1, or a hash range

        BRANCH: this branch will be rebased off of the base branch, e.g. myname/my-great-feature
    """
    # Mock git just prints the command which would be run
    if mock:
        git = mock_git
    else:
        git = real_git

    current_branch = get_current_branch()

    exists = branch_exists(branch)

    if exists and new:
        raise click.UsageError(f"Branch {branch} already exists. remove --new")

    if not exists and not new:
        raise click.UsageError(f"Branch {branch} must be created. use --new")

    try:
        click.echo(f"Currently on {current_branch}", err=True)

        # Resolve the commit name unless a hash was specified
        if not re.match(r"[0-9a-f]{40}", commit):
            commit = get_commit_hash(commit)

        if "\n^" in commit:
            commit = commit.replace("\n^", "^..")

        # Describe the actions to be performed
        push_msg = ""
        if push and not new:
            push_msg = " and force push"
        if push and new:
            push_msg = " and push upstream"
        branch_action = "create" if new else "hard reset"

        click.echo(f"Going to {branch_action} branch {branch} on {base} then cherry pick {commit}{push_msg}", err=True)
        click.echo(err=True)

        # Checkout or create the branch and reset to the the base branch
        if not exists:
            git("checkout", "-b", branch)
        else:
            git("checkout", branch)
        git("reset", "--hard", base)

        # Cherry pick the commit(s) into the branch
        git("cherry-pick", commit)

        # Push to origin
        if push:
            # Set upstream if necessary, otherwise force push
            if not exists:
                git("push", "--set-upstream", "origin", branch)
            else:
                git("push", "--force")
    finally:
        git("checkout", current_branch)
