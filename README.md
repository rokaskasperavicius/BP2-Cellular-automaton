# BP2 Cellular automaton

Recommended IDE - PyCharm Edu (https://www.jetbrains.com/pycharm-edu/)

## Setup process
1. Install git (https://git-scm.com/downloads).
2. Setup SSH access (ask Rokas because this is a bit complicated) (https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent, https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
3. In the terminal (command prompt for windows) do `git clone git@github.com:rokaskasperavicius/BP2-Cellular-automaton.git` - this clones the repository on your local machine.
4. Open the project using your IDE.

## Git commands
Github uses different branches - this is useful when the project has many developers.

The main branch is called `main`.

Command `git branch` says on which branch you are on.

`git pull` allows to pull the newest version of your branch from github (this will be needed when working not alone). This has to be done when somebody updates `main` branch!

`git checkout [branch name]` puts you on a specific branch.

`git checkout -b [new branch name]` creates a new branch (this should be done from the `main` branch)!

## Starting to work
1. `git checkout main`
2. `git pull`
3. `git checkout -b [new branch name]` (i.e. `git checkout -b daniel`)
 
## When you are done working on the script (push everything to github so everybody could see)
1. `git add .` - adds all files to they could be pushed
2. `git commit -m "[insert a message here]"` - add a message to your commit
3. `git push` - push the changes to the `main` branch (the terminal might throw another command you have to use for the first time you push)

Now you have pushed your code to github and can create a pull request against main branch :)