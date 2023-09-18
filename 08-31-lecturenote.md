### 도커의 탄생

잘 돌고 있는 서버를 업그레이드도, 다운그레이드도 할 수 없는 상태…\
→ 가상환경 탄생

Hypervisor (MS, VBox, )\
하나의 하트웨어 위에 여러개의 가상환경, 그 가상환경 위에서 앱을 띄우겠다\
but 모든 가상환경마다 os 깔고, 개발환경 구축해야 함\
→ 오버헤드 발생\
app 여러 개 깔고 사용하지만 앱이 서로를 간섭하지 않게 함 (샌드박스 격리)

컨테이너의 장점
: 생성, 개발, 배포를 자유롭게 하겠다\
윈도우에서 개발해서 잘 돌아가던 서비스를 클라우드에 올리니 안 되는 상황을 막음\
클라우드에도 환경 구축하면 되겠지만, 컨테이너로 이미지를 잘 만들어두면 편함\
컨테이너 리눅스 커널

---

### 도커 이미지와 컨테이너

도커 이미지 : 결과물\
도커 컨테이너 : 결과물을 실행하여 실체화된 결과

이미지를 배포하면 컨테이너\
배포한 이미지를 pull하여 실행시키면(run) 컨테이너 생성 가능\
이미지를 가져오기 위한 [dockerhub](https://hub.docker.com/)

---

### 우분투에 도커 설치

```bash
sudo apt install docker.io -y
systemctl status docker
sudo docker version
```

client - server\
docker라는 명령어 자체가 클라이언트 소프트웨어\
mysql도 클라이언트가 있음..\
커널사이드에 도커 엔진이 존재함

```bash
sudo docker # sudo 명령어를 사용하는 것은 보안성이 떨어짐
sudo usermod -aG docker sangeun
newgrp docker
docker version

docker run hello-world # docker run = docker pull + docker create + docker start
docker images # 이미지에 hello-world 뜸

docker ps -a

docker pull ubuntu:<태그>
docker pull ubuntu:20.04
```

![Untitled (1)](https://github.com/sangeun99/sesac-docker/assets/63828057/100ad978-df8d-4590-b0de-d5b2816310d9)

container 4개 확인 가능\
태그를 안 넣으면…\
`docker pull ubuntu:latest`가 최신 버전을 의미하지는 않음 (글자를 가져오는 것)


```bash
docker pull ubuntu:16.04
docker create ubuntu:16.04
docker start 62884bb9dbbf
```

컨테이너를 시작한다? 우분투를 시작한다?\
가상머신일 때는 부팅이라는 프로세스를 거켜 GUI로 로그인 창을 띄워준다\
원격 접속하기 위한.. 명령어를 입출력하기 위한… 터미널을 실행하기를 기대하고 있는 것임

bash라고 부르는 바이너리 실행파일\
bash라는 터미널을 주는 것임\
-i interactive\
-t tty (터미널)

```bash
docker run -it ubuntu:18.04 # 도커 컨테이너 안에 들어와있는 상태
```

도커 컨테이너 안에서 만든 파일 등은 도커 컨테이너가 종료되면 사라짐\
`docker start -i 6cfcc8745ff3` 를 통해 종료된 컨테이너에 다시 들어온다면 만든 환경이 그대로 있음\
컨테이너 안은 완전히 격리된 별도의 공간임.. 파일시스템, 프로세스, 사용자 등등등\
OS를 구동할 때 필요한 모든 내용들을 포함한 격리된 환경

컨테이너 내에서 돌아가는 프로세스를 확인하면 자신의 컨테이너 내의 프로세스만 확인 가능 (호스트에서 `docker ps`를 확인하면 모든 컨테이너 확인 가능)

명령어 : ps / ps aux \
`docker ps` \
원래 프로세스를 확인하는 명령어가 아니기에 새로운 명령어 생김 \
`docker container ls` \
`docker container ls -a`

---

### !! 컨테이너 및 이미지 지우기

```bash
docker rm e3405316324c
docker rm e34 # 정도만 쳐도 알아서 지워줌 (한 글자도 unique하면 지워줌)
docker rm intelligent_robinson # 이름 이용 시 풀매치 필요 - tab 완성 가능

docker ps -aq # 아이디만 뽑아서 쓸 수 있음
docker rm $(docker ps -aq) # 리눅스의 명령어 기능.. 모든 컨테이너 지우기

docker rmi ubuntu:16.04
docker rmi $(docker images -q)
```

docker.io/library

---

### !! nginx 컨테이너 띄우기

```bash
docker run -d nginx
docker exec -it f473 bash # 돌고 있는 컨테이너 안에 들어와봄
curl localhost # 컨테이너에 돌고 있는 웹서버 확인
```

실행하는 것이 바로 종료되는 것인데 종료를 원치 않으면 -it \
실행하는 것이 foreground process 상태로 있으면 -d (daemon 상태로 돌아라) \
만약 bash가 없는 서버가 있다면 보통 shell이 있음 \
`docker exec -it <컨테이너ID> shel`l \
의미 없는 nginx.. 격리된 공간 안에 웹서버가 존재하고 있음 \
격리된 공간에서 내부/외부를 연결할 수 있을까?

```bash
docker run -d -p <호스트>:<컨테이너> nginx # -p: port binding
docker run -d -p 81:80 nginx
```

http://192.168.56.101:81/

우분투 안에서 돌고 있는 컨테이너 안에서 돌고 있는 거임

```bash
find / -name index.html 2> /dev/null # index.html을 찾고 권한 없는 파일은 /dev/null로 보냄
```

cat /etc/*-release : 격리된 환경 안의 OS를 확인하는 명령어

---

### !! Database를 도커에서 돌려보자

VM과는 다른 개념으로 실제로 OS가 구동되지는 않음\
우분투 리눅스 환경 내에서 모든 애플리케이션 구동되는 형태

```bash
docker run -d mysql
docker logs df55
# 기본 계정의 암호가 없는 문제 발생

# 도커의 환경변수를 통해서 다양한 변수값 설정 가능
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=sesac1234 mysql 
docker run -d -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=1 mysql 
docker run -d -p 3306:3306 -e MYSQL_RANDOM_ROOT_PASSWORD=1 mysql 
```

도커 디버깅 방법\
(1) `docker exec -it <cont-id> bash`를 통해 들어가서 확인\
(2) `docker logs <cont-id>` 로그를 통해 확인

```bash
mysql -h 127.0.0.1 -u root -p
```

상태를 가지고 있지 않는 것이 컨테이너화를 하기에 좋은 애플리케이션임

신중하게 관리하지 않으면 상태가 날아갈 수 있다 \
별도의 저장소에 컨텐츠(상태=state)를 저장하는 공간이 필요함

두 가지 기법.. \
(1) 호스트패스 바인딩 → 호스트가 있는 경로를 통해 \
(2) 볼륨 바인딩

-v라는 옵션으로 호스트패스를 연결해주겠다.. 

```bash
docker run
-d
-p 3306:3306
-v <호스트경로>:<컨테이너경로> # 호스트경로는 full path
-e MYSQL_ALLOW_EMPTY_PASSWORD=1
mysql 

docker run -d -p 3306:3306 -v /home/sangeun/my-database:/var/lib/mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=1 mysql

# 바인딩 이후 우분투에서 mysql 접속
mysql -h 127.0.0.1 -u root
```

![Untitled](https://github.com/sangeun99/sesac-docker/assets/63828057/15d663e9-90e1-4dfb-81d5-91301c469147)


문제점: 내 파일인데 내가 권한이 없음

```bash
docker volume create my-sesac-db
docker volume ls

docker volume rm my-sesac-db # 추후 볼륨 삭제 시 이용

docker run -d -p 3306:3306 -v my-sesac-db:/var/lib/mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=1 --name my-db mysql
# 로컬에는 존재하지 않고 도커가 관리하는 어딘가에 있음
```

```bash
create database sesac;
use sesac;
create table users(id integer, username varchar(200));
insert into users values (1, 'users');
select * from users;
```

도커를 지우고 다시 생성해도 그대로 연결하면 살아있는 것을 확인할 수 있음

```bash
docker info # 그럼 이 데이터베이스는 어디서 지워질까??
```

Docker Root Dir: /var/lib/docker \
실무적으로는 EBS 새로 생성하고 /data → EBS 연결 (mount) \
/data/docker \
/data/docker_dir

```bash
docker system df
```

도커 디스크 관리 필요 \
안 쓰는 것은 지워야 함 → `docker volume prune` \
볼륨 안에 있다고 안전한 것은 아님! prune을 써서 공간을 확보할 수는 있지만 데이터베이스를 날릴 수도…