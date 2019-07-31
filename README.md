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

## Run server

```text
python3 minigame/manage.py runserver
```

## Serveo deploy server

```text
ssh -o ServerAliveInterval=60 -R 80:127.0.0.1:8000 serveo.net
```

## Download word db

은진님께서 보내주신 worddb를 다운받아 직접 파일에 넣어주셔야 합니다.
위치는 총 2개의 minigame 폴더가 존재하는데(상위, 하위)
상위의 minigame 폴더에 넣어주시면 됩니다.

## make tables(sync db)

```text
python3 minigame/manage.py makemigrations
python3 minigame/manage.py --run-syncdb
```

## find tables(sync db)

```text
python3 minigame/manage.py dbshell
```

## move file in api_datebot_words to initial_sound_quiz_words and word_chain_words

특정 테이블만 참조하게 하는 방법이 있는 것 같은데, 그 방법을 찾지못해 일단은 각 파일에서 참조하는 테이블안으로 데이터를 옮겨주어야합니다..

```text
insert into initial*sound_quiz_words select * from api*datebot_words
insert into word_chain_words select * from api_datebot_words
```

## API documentation(ignore)

Gitbook Document [click here!](https://app.gitbook.com/@cocoa/s/cocoa-project/~/settings/share)
