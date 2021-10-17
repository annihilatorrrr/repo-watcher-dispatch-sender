# repo-watcher-dispatch-sender

<p align='center'>
  <img src="https://img.shields.io/github/forks/DivideProjects/repo-watcher-dispatch-sender?style=flat-square" alt="Forks">
  <img src="https://img.shields.io/github/stars/DivideProjects/repo-watcher-dispatch-sender?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/issues/DivideProjects/repo-watcher-dispatch-sender?style=flat-square" alt="Issues">
  <img src="https://img.shields.io/github/license/DivideProjects/repo-watcher-dispatch-sender?style=flat-square" alt="LICENSE">
  <img src="https://img.shields.io/github/contributors/DivideProjects/repo-watcher-dispatch-sender?style=flat-square" alt="Contributors">
  <img src="https://img.shields.io/github/repo-size/DivideProjects/repo-watcher-dispatch-sender?style=flat-square" alt="Repo Size">
  <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/DivideProjects/repo-watcher-dispatch-sender&amp;title=Profile%20Views" alt="Views">
</p>

<p align='center'>
  <a href="https://www.python.org/" alt="made-with-python"> <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square&logo=python&color=blue" /> </a>
  <a href="https://github.com/DivideProjects/repo-watcher-dispatch-sender" alt="Docker Pulls"> <img src="https://img.shields.io/docker/pulls/divideprojects/repo-watcher-dispatch-sender.svg" /> </a>
  <a href="https://hub.docker.com/r/divideprojects/repo-watcher-dispatch-sender" alt="Docker Image Version"> <img src="https://img.shields.io/docker/v/divideprojects/repo-watcher-dispatch-sender/latest?label=docker%20image%20ver." /> </a>
  <a href="https://deepsource.io/gh/DivideProjects/repo-watcher-dispatch-sender/?ref=repository-badge"><img src="https://static.deepsource.io/deepsource-badge-light-mini.svg" alt="DeepSource"></a>
</p>

<p align='center'>
  <a href="https://t.me/DivideProjects"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&amp;logo=telegram&amp;logoColor=white" alt="Join us on Telegram"></a></br></br>

</p>

This app is used to send a `repository_dispatch` event to the destination repo set in [config.py](/src/config.py) or Environmental Variables whenver a commit is made on the upstream repo.

This setup is for my own use, please fork and make your own if you want :D

Give this repo a :star: if you like it or it helps you!

## How to use?

### Set the Environmental Variables or [config.py](/src/config.py) file

It's really not difficult to set this up, you just need to define the variables in [config file](/src/config.py), the varibales include the following:

 - **GH_PAT**: Github Personal Access Token with `repo` access to the destination repo. Cause you know, you can't trigger any workflow anywhere except the ones you have acess to :p
 - **REPOSITORY_PAIR**: The main stuff, this tells the script about source and destination repo, the source repo is the one we check commits for, destination is for sending the `repository_dispatch` to it. It should be in this format: `<source>:<branch>:<destination>`, the source and destination should be in this format: `<github_user/repo>`, Example: `<divkix/proxygrab@main:octocat/proxygrab>`
 - **TIME_PERIOD**: The time after which script should sleep for, i.e. wait before running again. It is not recommented to set it to less than **30**, default is 60 minutes
 - **SLEEP_TIME**: The time before performing another action after one has been done, i.e. wait time between 2 consecutive requests. It is not recommented to set it to **0**, default is 1 minute
 - **EVENT_TYPE**: The event which should be sent in `repository_dispatch`, read more here: [docs.github.com](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#repository_dispatch)
 - **DB_URI**: MongoDB URL for database usage of bot.

### Choose how you want to run it

You can run it in several different ways, one of the easiest might be to use heroku.

Another option is to locally run it on you pc as it is or using docker.

Docker images can be found here: [ghcr.io](https://github.com/DivideProjects/repo-watcher-dispatch-sender/pkgs/container/repo-watcher-dispatch-sender) or [Docker Hub](https://hub.docker.com/r/divideprojects/repo-watcher-dispatch-sender)

You can even easily build your own docker images using the provided dockerfiles!


### Running using docker

You can easily use the docker image like this:

```sh 
docker run -e GH_PAT="<your GH PAT>" -e REPOSITORY_PAIR="<repo pairs>" -e TIME_PERIOD=60 -e SLEEP_TIME=1 -e EVENT_TYPE="<name of event you want to send>" -e DB_URI="<mongo db uri>" divideprojects/repo-watcher-dispatch-sender:latest
```

or

```sh 
docker run -e GH_PAT="<your GH PAT>" -e REPOSITORY_PAIR="<repo pairs>" -e TIME_PERIOD=60 -e SLEEP_TIME=1 -e EVENT_TYPE="<name of event you want to send>" -e DB_URI="<mongo db uri>" ghcr.io/divideprojects/repo-watcher-dispatch-sender:latest
```

These is absolutely no difference between the 2 commands above, you can use any, the first one fetched image from [docker hub](https://hub.docker.com/r/divideprojects/repo-watcher-dispatch-sender) while other one gets the image from [ghcr.io](https://github.com/DivideProjects/repo-watcher-dispatch-sender/pkgs/container/repo-watcher-dispatch-sender)

# What is the use of this?

It can be whatever you want it to do, you can use it trigger automatic builds, tests, builds, and a lot of things...

# FAQ

Some general questions you might stumble upon

### Why can't I trigger to a specific branch on destination repo?

It's not really needed most of time, if you stiff want this feature we'll be happy to merge your pull request for it :)

### Why should `SLEEP_TIME` should not be set to 0?

Every API has limitations, and so is the case with Github, it has a soft-limit of 60 api calls per hour, so we need to make sure that we don't hit the limits.
