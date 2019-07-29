# Readme.md

## Getting Started

### Prerequisites

- [ ] python 3.6 [download](https://www.python.org/downloads/)
- [ ] Docker [windows](https://docs.docker.com/docker-for-windows/install/) [macOS](https://docs.docker.com/docker-for-mac/) [Linux](https://docs.docker.com/install/linux/docker-ce/centos/)

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
$ docker run -d -p 8000:8000 -t minigame_template_dev
```

## API documentation

Gitbook Document [click here!](https://app.gitbook.com/@cocoa/s/cocoa-project/~/settings/share)
