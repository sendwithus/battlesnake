# Getting Started Guide

This guide will show you how to get up and running with the NodeJS starter snake on Heroku.


### Services to Sign Up For

- [Heroku](https://heroku.com)
- [Github](https://github.com)
- [Cloud9](https://c9.io) (recommended for Windows users)


### Fork Python Snake on Github

Navigate to [Python Snake](https://github.com/sendwithus/battlesnake-python) and click the `Fork`
button in the top right.

![Fork Repo](/static/img/setup/fork.png)

This will create a copy in your Github account that you can modify.


## Edit some Code and Deploy

This will be easiest on a Unix system (Linux or Mac). If you're on Windows, we recommend following
along with a [Cloud9 Workspace](https://c9.io) which will give you a free Linux environment.


### Basic Requirements

Things to install (follow instructions in the links below):

- [Git](https://git-scm.com/) for versioning and deploying code
- [Heroku Toolbelt](https://toolbelt.heroku.com/) for deployment


### Setup Heroku

_NOTE: Apart form these docs, Heroku has a great tutorial for
[getting started with Python](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)._

First, clone Python Snake codebase to your machine.

![Clone Github Repo](/static/img/setup/clone.png)

```bash
git clone https://github.com/<USERNAME>/battlesnake-python
```

Log in to the [Heroku Toolbelt](https://toolbelt.heroku.com/).

```bash
heroku login
```

Create a heroku app with a creative name of your choosing. We'll be using `battlesnake-tutorial` for
this tutorial.

```bash
heroku create battlesnake-tutorial
```

Deploy to Heroku using Git. Simply `git push` to the `heroku` remote.

```bash
git push heroku master
```

Copy the URL from the output above and open it in your browser (`heroku open` also does this).

![Viewing your Snake](/static/img/setup/success.png)


### Debugging your Snake

You can see the logs from your Heroku app by running the following command.

```bash
heroku logs -t
```

![Viewing Heroku Logs](/static/img/setup/logs.png)


## Making Changes

You can also push to github instead of Heroku by pushing to the `origin` remote.

```bash
git add -A                            # Add your changes
git commit -m "I changed some stuff"  # Commit your changes
git push heroku master                # Deploy to Heroku

git push origin master                # Push to Github (if you want)
```
