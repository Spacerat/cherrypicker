# Cherrypicker

Cherrypicker lets you easily create or update a branch to contain one or more commits which exist on your current branch. Install with:

    pip3 install git+https://github.com/evenco/cherrypicker

## Why?

If you're working on a PR and decide that you would like to change some library code which could be committed independantly, this tool lets you:

- Make that change in one commit
- Create a PR on `origin/master` containing _just that commit_ and push it to github with a single command, without leaving your current branch.

## Basic example

Cherrypick the last two commits into a new branch called `joe/myfeature`, then push the branch upstream and return to master:

    cherrypicker HEAD~1..HEAD joe/myfeature --new --push --mock


## Show me the workflow!

I'm on a big feature branch and make some change:

    cherrypicker> touch myfeature
    cherrypicker> git add myfeature & git commit -m "added a feature"

    [master 205f4c4] added a feature
    1 file changed, 0 insertions(+), 0 deletions(-)
    create mode 100644 myfeature
    Job 1, 'git add myfeature &' has ended

Then I do some more work:

    cherrypicker> touch some_other_work
    cherrypicker> git add some_other_work & git commit -m "did some other work"

    [master 82f5344] did some other work
    1 file changed, 0 insertions(+), 0 deletions(-)
    create mode 100644 some_other_work
    Job 1, 'git add some_other_work &' has ended

I realise that `myfeature` would actually make a good PR by itself, so I throw it on a branch:

    cherrypicker> cherrypicker HEAD~1 joe/myfeature --new

    Currently on master
    Going to create branch joe/myfeature on origin/master then cherry pick 205f4c4d0fae9070ce06f9ae6ea728729bf57f60 and push upstream

    /usr/local/bin/git checkout -b joe/myfeature
    /usr/local/bin/git reset --hard origin/master
    /usr/local/bin/git cherry-pick 205f4c4d0fae9070ce06f9ae6ea728729bf57f60
    /usr/local/bin/git push --set-upstream origin joe/myfeature
    /usr/local/bin/git checkout master

Let's see what that branch looks like:

    cherrypicker> git checkout joe/myfeature

    Switched to branch 'joe/myfeature'
    Your branch is up to date with 'origin/joe/myfeature'.
    cherrypicker> git log
    commit 40ae0e60699593bc877f02c472e1bac0aecb6f11 (HEAD -> joe/myfeature, origin/joe/myfeature)
    Author: Joseph Atkins-Turkish <joe@teameven.com>
    Date:   Wed Mar 20 10:00:43 2019 -0700

        added a feature

    commit c9d9df3906e851764f7f919918bfe89a75fe0c02 (origin/master)
    Author: Joseph Atkins-Turkish <joe@teameven.com>
    Date:   Wed Mar 20 09:58:48 2019 -0700

        Initial commit
    cherrypicker>


## Cherrypicking a range of commits into a branch

Cherrypicker will resolve branch specs such as `HEAD~1..HEAD` on your _current branch_, so that they can be cherrypicked into the target branch.

    cherrypicker> cherrypicker HEAD~1..HEAD joe/myfeature --mock --push
    Currently on master
    Going to hard reset branch joe/myfeature on origin/master then cherry pick a172a1d046b8b6500e82e72dd7e42625bcb0fa58^..61594f3b1b60fc9cc05d55c315c9f51ccb765a92 and force push

    /usr/local/bin/git checkout joe/myfeature
    /usr/local/bin/git reset --hard origin/master
    /usr/local/bin/git cherry-pick a172a1d046b8b6500e82e72dd7e42625bcb0fa58^..61594f3b1b60fc9cc05d55c315c9f51ccb765a92
    /usr/local/bin/git push --force
    /usr/local/bin/git checkout master


## Updating a feature branch

If you want to make changes to a PR without making its branch diverge, you can interactively rebase and then push the changes back up with this tool.


    cherrypicker> git rebase -i origin/master

Change the command to `edit` or `e` for the commit you want to modify:

    Stopped at 205f4c4...  added a feature
    You can amend the commit now, with

    git commit --amend

    Once you are satisfied with your changes, run

    git rebase --continue

    cherrypicker> echo "code!" > myfeature
    cherrypicker> git commit myfeature --amend --no-edit

    [detached HEAD 61594f3] added a feature
    Date: Wed Mar 20 10:00:43 2019 -0700
    1 file changed, 1 insertion(+)
    create mode 100644 myfeature
    cherrypicker> git rebase --continue
    Successfully rebased and updated refs/heads/master.

Now reset the feature branch to contain this updated version of the change:

    cherrypicker> cherrypicker HEAD~1 joe/myfeature

    Currently on master
    Going to hard reset branch joe/myfeature on origin/master then cherry pick 61594f3b1b60fc9cc05d55c315c9f51ccb765a92 and force push

    /usr/local/bin/git checkout joe/myfeature
    /usr/local/bin/git reset --hard origin/master
    /usr/local/bin/git cherry-pick 61594f3b1b60fc9cc05d55c315c9f51ccb765a92
    /usr/local/bin/git push --force
    /usr/local/bin/git checkout master
    cherrypicker>
