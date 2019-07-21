# Readme.md

## Getting Started

### Prerequisites

* [ ] python 3.6 [download](https://www.python.org/downloads/)
* [ ] Docker [windows](https://docs.docker.com/docker-for-windows/install/) [macOS](https://docs.docker.com/docker-for-mac/) [Linux](https://docs.docker.com/install/linux/docker-ce/centos/)

### Running

#### Build docker image

```bash
$ docker build . -t minigame_template_dev -f Dockerfile_dev
```

```
Successfully built <ImageId>
Successfully tagged minigame_template_dev:latest
```

#### Run docker image

```text
$ docker run -d -p 923:923 -t minigame_template_dev
```

