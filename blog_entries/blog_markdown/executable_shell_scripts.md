# Executable shell scripts
Even though this can easily be found online, I find it useful to have together several of the things I usually use when making shell scripts that I use over and over again.

To begin with we should select a folder where to store all the scripts we will create, say `sh_scripts` under your home directory:

```bash
mkdir -p ~/sh_scripts
```

Now you can create a `.sh` file. Here I make use of `code` (Visual Studio Code) but using your preferred editor makes no
 difference. 
```bash
code example.sh
```

In the editor you may now write the lines you would like to aoutomate. I'll make a silly example (it is not recommended
to do something like this with git):
```bash
#!/bin/bash
git status
git pull
git add .

echo "Wrtie commit message: "
read commit_msg
git commit -m '${commit_msg}'

git push
```

If you run this within a git folder, this sh script shows the current status of your current local branch,
pulls changes, asks for a commit message, commits for you and pushes in an automated way. Again, this is not
recommended.

Now we need to change the mode of our `example.sh` shell script with

```bash
chmod +x example.sh
```