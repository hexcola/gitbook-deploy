# GitBook Deploy

## Goal

Simplify deploy `gitbook-cli` generated static files to github pages.

> The steps looks complicated, actually it's simple. 

## Requirements

* `gitbook-cli`
* `python 2.7`
* `git`


## How to use

### Create a new repository on GitHub and clone it to local

```bash
# clone repository to local
$ git clone https://github.com/<your_name>/<your_project>.git

# switch to project directory
$ cd <your_project>

# use current directory as gitbook root
$ gitbook init
```

### Add .gitignore file

```bash 
_book

# we'll discuss it later.
.deploy 
```

### Commit the project 

```bash 
$ git add .
$ git commit -m "initial upload"
$ git push
```

### Initialize gh-pages branch

```bash
$ git checkout -b gh-pages
$ git push -u origin gh-pages
$ git checkout master
```

### Clone remote gh-pages to local and rename it as '.deploy'

```bash
git clone -b gh-pages https://github.com/<your_name>/<your_project>.git .deploy
```

then copy `gb-config.yml` and `gb-deploy.py` to the root folder, after that, your project directory should look like this:

```tree
<your_project>
    |_  .deploy
    |_  gb-config.yml
    |_  gb-deploy.py
    |_  README.md
    |_  SUMMARY.md
```

### Config `gb-config.yml` file 

It's straightforward.

### Try

```bash
# use gitbook to generate static files, all of them will put under _book
$ gitbook build

# after previous operation, your directory structure should looks like this.
<your_project>
    |_  _book
    |_  .deploy
    |_  gb-config.yml
    |_  gb-deploy.py
    |_  README.md
    |_  SUMMARY.md

# deploy it files to your branch
$ gb-deploy.py
```


## TO-DO

make a gitbook helper

* `gb-helper init https://github.com/<your_name>/<your_project>.git`
* `gb-helper build`
* `gh-helper deploy`