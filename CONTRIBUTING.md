# Getting Started with TERMINALMONOPOLY

### Step 0: what you'll need
- Code editor of your choice (recommended: **VS Code**)
- Python installed in your system (minimum ver. **Python 3.10**)
- Git installed on your system
- The code documentation at DOCUMENTATION.md

### Step 1: forking a repository
![fork](https://github.com/user-attachments/assets/a71ea542-0236-4051-8076-07e414d0934c)

- [ ] Go to https://github.com/ufosc/TERMINALMONOPOLY
- [ ] Press the "fork" button in the top right
- [ ] (Feel free to "star" the repository as well at this point!)

![fork2](https://github.com/user-attachments/assets/4ae61df2-a32d-47d1-9fbd-ae62f3c2e011)
- [ ] Create a name for your fork (default is usually fine) and add a description
- [ ] Create fork

![uptodate](https://github.com/user-attachments/assets/1f7f6b34-a70c-41a9-8670-e8a15689c926)
- [ ] Ensure the newly created branch is up to date with ufosc/TERMINALMONOPOLY:main
- [ ] If not, press "sync fork"

### Step 2: cloning the fork
![vscode1](https://github.com/user-attachments/assets/7bff4df7-a0f8-42de-8cb3-47390742d8f9)
*Different code editors have different features, but most have Github integrations or extensions you can work with. If not, you can always use the command line commands listed here.*

![vscode2](https://github.com/user-attachments/assets/e61e57cd-3af2-4fca-9c17-57abb14d8ded)

- [ ] Navigate to a directory in your file system where you want to save everything. **cd "directory name"** to switch directories
- [ ] Clone git repository using code editor feature or in the command line: **git clone "URL to your newly created fork"** (no quotes)
- [ ] Once cloned, git pull using code editor or in the command line: **git pull** (no parameters). This ensures you are up to date.

![vscode3](https://github.com/user-attachments/assets/d79c9126-23a2-4e6d-85a6-5a941637157d)
### Step 3: working on a branch  
Create a new branch with a descriptive (but short) title regarding what you're working on
- [ ] Use code editor feature or command line: **git branch "name"** (no quotes)
- [ ] Additionally, you can always use **git branch** to view all your local branches
- [ ] To switch to your newly made branch, use **git checkout "name"**
Once you're working in the new branch, you can make new changes locally without messing up your main branch

## You're all set! Happy coding!

# Ready to submit your changes? How to submit a Pull Request

![image](https://github.com/user-attachments/assets/d73b5128-7014-4d4f-ae95-919246825060)
### Step 1: saving your files and staging
- [ ] Review all changed files and save them locally (ctrl+S)
- [ ] Run **git add .** to add all changed files to staging area. Alternatively, use **git add filename1 filename2 filenameN ...** to add only specific files.

![image](https://github.com/user-attachments/assets/2af3b513-2763-4f34-89e7-818bcfb30f14)
### Step 2: commit
There are multiple ways to use the commit command. 
- [ ] In the command line, use **git commit -m "message"** where the message parameter is less than 50 characters, and briefly describes the commit
Commit messages should be **descriptive** and **tell the history of the changes**. What is depicted here is NOT a good commit name.
See [here](https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/) for additional reading
- [ ] In vscode, you may also use the box in the top left to create a commit message, and you may commit with the checkmark.



### Step 3: sync fork and rebase
- [ ] Go to your remote github repository and press the "sync fork" button found here. This is *crucial* to ensure your code doesn't break code upstream. This updates your remote repository with any changes that may have occurred on the official ufosc repository. This might cause your code to change too, so you may need to carefully review the changes.
  It is *your* responsibility to ensure your new code doesn't conflict with code from upstream. 
- [ ] Once you sync your fork, return to your code editor and run **git checkout main** followed by **git pull**. I recommend checking out and pulling on your **main** branch, *not your development branch*. This updates your local files with the new stuff you just synced from the official repository.
- [ ] Then, especially if you're many commits behind the main branch, run **git checkout "branchname"** followed by run **git rebase main**.
- [ ] For a thorough explanation of why we're doing this, along with a demonstration, watch [this video](https://www.youtube.com/watch?v=f1wnYdLEpgI).
- [ ] Resolve any merge conflicts with the built-in merge editor or some other method.
- [ ] Then, run **git checkout main** followed by **git rebase "branchname"**.
  This whole process allows you to submit your changes in your main branch, instead of necessarily needing to publish your development branch. It makes the history more linear and readable. 

![vscode6](https://github.com/user-attachments/assets/b7043a88-39ce-4677-a570-d760a29c1cb9)
### Step 3: publish branch
- [ ] If this is a new branch, publish it using the button
- [ ] Publishing should automatically push, but if not move to step 4.

![vscode7](https://github.com/user-attachments/assets/d09c2c58-d502-4650-b869-db5f4e445011)
### Step 4: push
- [ ] In the command line, **git push** 
Pushing sends your local changes to the remote (your fork, on github.com). In the image, everything is up-to-date because of step 3. 

![fork3](https://github.com/user-attachments/assets/7a28c408-ea67-4d44-b2c0-1ba8d789bc01)
### Step 5: contribute
- [ ] On your own fork, you may see "compare and pull request" green button: you will do mini-pull request where you compare the previous code you have to your new code and save the new changes.
- [ ] Once you've updated your fork, you can press the contribute button to create a pull request for the main branch.
- [ ] Write a **thorough** and accurate description of your changes.
- [ ] If you were working on an issue #, add "fixes #N" where N is the issue number. Github should help auto populate this as well. See the following [https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue] 

## That's it! Your code will be reviewed by a tech lead and if approved, merged into the main branch. Congrats on your contribution!
