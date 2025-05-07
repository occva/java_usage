> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [www.guai.win](https://www.guai.win/notes/0003/new-vps)

> 主要从性能测试、安全配置、基本应用、常用工具这些方面切入，争取让小白也能轻松上手

拿到新机器，咱们二话不说，先 ping 一下 IP，能否连通。连不通的话，可能是被封锁了，新机一般可以免费换 IP，换完接着 ping。

连通后看看延迟和丢包，延迟太大就得考虑。可能这个机房，它不适合你。

大家的地区，运营商，节点线路都不大一样，别人吹上天也没用，冷暖自知。

能接受的话，就 ssh 上去，开始跑测试脚本，是骡子是马，还得看数据。跑完测试觉得机子不行，应该还能赶在截止时间之前退单退款。

_有些鸡贼的商家，使用流量超过 10G，就不给退单退款，这种就别跑测速了。_

测速脚本一跑，几十个 GB 就没了，到时候退不了，只能砸自己手里。

· · ·

一、脚本测试
------

先别急着装什么面板，测完性能再说，直接上脚本。

### 1. yabs 脚本

yabs 是一个比较常用的综合测试脚本，权威性比较高，一般用来看最后的 cpu 得分。

```
wget -qO- yabs.sh | bash 
```

### 2. bench.sh 一键测试脚本

bench.sh 也是一个综合测试脚本，历史比较久，大佬一直在维护。

原作者链接：[github.com/teddysun/across](https://github.com/teddysun/across/blob/master/bench.sh)

```
wget -qO- bench.sh | bash 
```

### 3. 线路测试

besttrace 是专门测试回国线路的脚本，可以看到连接国内几大城市的节点线路和对应延迟。

```
wget -qO- git.io/besttrace | bash 
```

### 4. 网速测试

network-speed，测试 vps 到全球的连接速度，节点比较多，`比较耗流量`，成功测完得 20G 往上。

```
wget -qO- network-speed.xyz | bash 
```

### 5. 硬盘测试

这条测试是调用系统的命令，看看到底是 HDD、SSD 还是 NVME 硬盘。

```
dd if=/dev/zero of=256 bs=64K count=4K oflag=dsync 
```

测试结果参考：1-2M/s 的是 HDD；20-30M/s 是普通的 SSD；80M/s 以上的是好机子。

### 6. 内存超售检测

部分商家会超售内存，可以用该脚本检测。

至于 CPU、带宽的超售，这个就比较稀松平常了，只能看大家的口碑和商家的良心。

（脚本的安全性未知，建议看完重装系统部分，再决定要不要跑。）

```
curl https://raw.githubusercontent.com/uselibrary/memoryCheck/main/memoryCheck.sh | bash 
```

### 7. 流媒体解锁和 OpenAI 解锁测试

检测 VPS 的 IP，能否用来开通流媒体、OpenAI 等订阅服务。（同上，脚本安全性未知。）

```
bash <(curl -L -s https://netflix.dad/detect-script) 
```

### 8. IP 检测

如果对 IP 这个比较看重，怪文再推荐两个小工具，简单调查一下手上的 IP。

#### 1) IP 位置

[whatismyipaddress.com](https://whatismyipaddress.com/)

whatismyipaddress 这个网站可以查到你 VPS 的 IP 所在地，数据比较精准。

#### 2) IP 纯净度

[scamalytics.com](https://scamalytics.com/ip)

scamalytics 这个网站会返回一个分数和一个风险等级，欺诈风险分数一般低于 50 就好。

当然，分数越低越好，0 分最好。

_scamalytics 可以查到 IP 的纯净程度，这点很重要！_

IP 越干净，越容易通过流媒体等服务的订阅风控，也不容易弹 Google 和 Cloudflare 的人机验证弹窗，和影响浏览体验的过渡页，代理翻墙的时候体验会更好。

比如：注册 OpenAI 账号、开通 Plus 订阅，都是很看重 IP 欺诈分的，分数太高的话，申请 API 和 Plus 可能不给通过。

当然，也可以选择其他方式进行代偿，比如套 wrap，或者用其他优质节点开通服务，后面换回原 IP 继续用，这种绕开方式基本没啥问题，除非原 IP 被墙了。

· · ·

二、更新系统
------

### 1. 重装系统

**建议先跑完测试脚本，再重装系统，也是为了规避脚本的安全性问题。可别以为大家用的脚本就很安全哦，咱还是别轻信外部脚本比较好。**

有些人喜欢跑各种整合过的一键脚本，也不看脚本里面写的啥，难搞......

一般来说，VPS 厂商给你装的默认操作系统，很可能不是你想要的发行版或者版本号，建议用厂商的面板重新安装一下系统。

不太建议自己深度定制 diy，装些商家没有提供的系统，容易被抓到把柄，被删机了也很难退款。

#### 系统的选择

服务器端发行版选择很多：Debian，Ubuntu，Rocky Linux，AlmaLinux，Fedora 等等，甚至 CentOS，OpenSUSE Leap 都行，选自己熟悉的就好。

关于各个发行版的特点和取舍，这里先占个坑，后面来填吧。

反正有条件的直接上 Red Hat Enterprise Linux（RHEL）就好，免费的哪有这个好啊。

Ubuntu 因为资料好找，使用起来方便，稳定性也不错，所以怪文也一直用 Ubuntu。

但自从 Canonical 往 Ubuntu 22.04.3 LTS 里面塞广告，有些广告还无法被移除，吃相有点难看，这种行径和国内厂商有得一拼了。

目前还在寻找平替，因为系统还没换，下面的 shell 命令，基本都是基于 Ubuntu 的版本。

如果装的是 Fedora 和 RHEL 系的发行版，比如 CentOS 之类的，请将下面命令中的 `apt` 用 `yum` 替换。

### 2. 更新应用列表、升级软件

```
apt update && apt upgrade && apt full-upgrade && apt autoremove 
```

### 3. 安装基础工具包（按需安装）

```
apt install vim curl unzip ufw 
```

· · ·

三、安全配置
------

小白最容易忽略的就是安全配置，`弱密码`什么的就不说了，说一下核心的配置。

### 1. 添加新用户

不建议每次都用 root 账号登录，可以用 root 创建新用户，并给它 root 权限比较好。

首先，添加新用户，并自动创建对应的组，然后根据提示设置密码：

```
adduser 新用户名 
```

设置新密码之后，继续。除了用户名，其他敲回车默认即可。

添加新用户到 sudo 用户组，就可以使用 sudo 命令了：

```
usermod -aG sudo 新用户名 
```

```
// 相关补充
exit            // 用户退出登录
passwd p        // 重设密码 
```

### 2. 修改 SSH 登录端口

更改端口前，建议把 22 端口先添加上。等 ssh 能通过其他端口连接后，再注释掉 22 端口。

先打开配置文件：

```
vim /etc/ssh/sshd_config 
```

找到这行：

> Port 22

然后在后面追加想要的端口号：

> Port 端口号

端口号的范围是 0 到 65535，数字别超了，而且还要避开常用的端口。

加完端口号，重启 SSHD 服务，让配置生效：

```
systemctl restart sshd.service 
```

如遇到 ssh 连接总自己断开，还可以继续添加添加配置：

> ClientAliveInterval 30
> 
> ClientAliveCountMax 6

### 3. SSH 免密登录

Windows 用户在 /.ssh 目录生成公钥和私钥：

```
ssh-keygen 
```

然后在 vps 上的生成用户的公钥和私钥：

```
ssh-keygen 
```

ssh 目录下面创建名为 authorized_keys 的文件，把 Win 上的公钥复制进 authorized_keys 文件：

```
cd /当前用户目录/.ssh
vim authorized_keys 
```

然后给 authorized_keys 文件设置权限：

```
chmod 600 /当前用户目录/.ssh/authorized_keys 
```

再重启 ssh：

```
systemctl restart sshd 
```

最后，在本地测试配置是否成功：

```
ssh 用户名@IP 
```

在本地的 SSH 工具里配置一下登录凭证，就可以免密登录了。

### 4. 限制 root 用户直接 ssh 登录或者密码登录

修改配置文件：

```
vim /etc/ssh/sshd_config 
```

加入内容（限制 root 用户直接 ssh 登录，换言之，后面得用新用户登录）：

> PermitRootLogin no

如果只是想限制 root 用户密码登录，只能用密钥登录，则需要修改配置文件内容为：

> PermitRootLogin without-password

使修改生效：

```
systemctl restart sshd 
```

修改文件权限，把 .ssh 目录设为 700：

```
chmod 700 /root/.ssh 
```

### 5. 启用防火墙

检查防火墙的状态：

```
ufw status verbose 
```

查看所有可用的应用程序配置：

```
ufw app list 
```

查找指定配置文件包含的防火墙规则：

```
ufw app info 'Nginx Full' 
```

启用防火墙之前，先允许 ssh 应用的默认端口：

```
ufw allow ssh 
```

如果 ssh 监听的是其他端口，就打开那个端口，允许外部访问：

```
ufw allow 端口 
```

还可以指定访问的协议：

```
ufw allow 端口/协议 
```

启用防火墙（启用之前一定要保证，SSH 的端口已经开了，不然登出之后，就登不进来了！）

```
ufw enable 
```

删除防火墙规则：

```
ufw delete allow 端口/tcp
ufw delete 防火墙规则编号 
```

关闭防火墙（规则和配置会保留）：

```
ufw disable 
```

重置防火墙设置并停止（配置会重置）：

```
ufw reset 
```

· · ·

四、基本配置
------

### 1. 设置时区

先看下系统的时区：

```
timedatectl show 
```

再按需修改，下面是按东八区的代号修改：

```
timedatectl set-timezone Asia/Shanghai 
```

### 2. 修改登录欢迎语（可选项）

Ubuntu 20.04 登录总提示 New release '22.04.3 LTS' available，如果不想升级，可以关掉登录后的动态消息。

```
vim /etc/pam.d/sshd 
```

然后注释掉下面这两行：

> session optional pam_motd.so motd=/run/motd.dynamic
> 
> session optional pam_motd.so noupdate

Ubuntu 22.04 每次登录都弹个很长的欢迎语，里面还有广告，难受。

好消息是，动态消息也可以像上面 Ubuntu 20.04 那样彻底禁止掉。

坏消息是，其他夹在 apt 命令中的广告就不那么好弄了。

不想完全关闭动态消息的话，也有些能做的事，比如欢迎语里面的 K8S 推广内容倒是可以手动关闭。

```
vim /etc/default/motd-news 
```

把文件里的 ENABLED=1 改成 ENABLED=0 就行。

### 3. 装面板（可选项）

如果手上的机器多，或者对命令行终端不感冒，也可以考虑装个面板，比如：1Panel、宝塔之类的。

面板安装和使用，又可以写一篇长文了，有需要的手动搜一下吧。

· · ·

五、科学配置（可选项）
-----------

### 1. BBR 加速

如果系统不支持 BBR2 或者 BBR Plus，配置 BBR 加速就行了。

```
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p 
```

验证是否成功：

```
sysctl net.ipv4.tcp_available_congestion_control
lsmod | grep bbr 
```

如果系统支持 BBR2 或者 BBR Plus 的话，可以用一键脚本装内核，开启 BBR2，至于安全性，那就不清楚了。

### 2. WARP

WARP 是 Cloudflare 提供的网络流量安全及加速服务，它基于 WireGuard，能够帮你通过连接到 Cloudflare 的边缘节点，实现隐私保护及链路优化。

### 3. WireGuard

如果要用 WARP，那肯定要装 WireGuard。

WARP 的安装，又可以写一篇博文了，有需要的手动搜一下吧。

### 4. V2Ray

这个之前整过，就写出来把，用的是官方脚本：[https://github.com/v2fly/fhs-install-v2ray](https://github.com/v2fly/fhs-install-v2ray)

V2Ray 的安装倒是很简单：

```
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh) 
```

安装后就可以启动了，但是建议先改下配置文件。（配置内容根据官方的模板，做下调整就好）

```
vim /usr/local/etc/v2ray/config.json 
```

改好配置后，先启动测试下：

```
systemctl daemon-reload
systemctl start v2ray 
```

查看服务状态：

```
systemctl status v2ray 
```

开机自启，让系统启动时引导 v2ray 启动：

```
sudo systemctl enable v2ray 
```

反悔了，不让系统启动时引导 v2ray 启动：

```
systemctl disable v2ray 
```

停止服务：

```
systemctl stop v2ray 
```

重新加载：

```
systemctl reload v2ray 
```

v2ray 默认的配置路径：

> /usr/local/etc/v2ray/config.json

v2ray 默认的日志路径：

> /var/log/v2ray/access.log
> 
> /var/log/v2ray/error.log

当然，如果嫌手动配置麻烦的话，也可以选择一键安装和引导配置的脚本，比如下面的这个（安全性未知）：

```
bash <(wget -qO- -o- https://git.io/v2ray.sh) 
```

· · ·

六、推荐软件（可选项）
-----------

### 1. Docker 安装

现在干点啥都喜欢上 Docker，服务基本都扔 Docker 里面了，有需要的建议先安上，挺省心的。

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh 
```

看看安装是否成功：

```
docker 
```

补充一下，这个脚本是官方的，会自动安装 Docker Compose 组件，调用命令是：`docker compose`。

如果看到别人用的命令是 docker-compose，那替换成 `docker compose` 就好，不必再装一个 docker-compose。

### 2. Nginx 安装

把 Nginx 放 Docker 当然也可以，但是对于这种入口级别的中间件，个人还是习惯用原生的。

安装非常的简单：

```
apt install nginx 
```

看看成功没有：

```
nginx -V 
```

启动 Nginx：

```
systemctl daemon-reload
systemctl start nginx 
```

测一下：在浏览器通过 ip 加 80 端口访问，是否是 Nginx 默认欢迎页。

配置的话，一般直接去 /etc/nginx/conf.d 添加个文件，配一下就好了。

有静态网站，可以直接扔 /var/www/ 里面，也很方便。

Nginx 的维护，基本靠系统控制命令就能实现：

查看服务状态：

```
systemctl status nginx 
```

如果只修改了配置，Nginx 可以在不中断服务的情况下热加载，这个很好用：

```
systemctl reload nginx 
```

开启自启，让系统启动时引导 Nginx 启动：

```
systemctl enable nginx 
```

反悔了，不让系统启动时引导 Nginx 启动：

```
systemctl disable nginx 
```

停用 nginx：

```
systemctl stop nginx 
```

### 3. Nvm 安装

Node.js 也是火的不行，经常看到一些开源工具，都是放在 Node 里面跑。

有需要的也可以装上，但不建议直接装 Node.js，因为版本问题什么的太操心了，直接上 Nvm 更方便。

还有一点非常的坑，Node.js 对用户的权限要求有点变态，个人建议用 root 用户安装，启动也是。之前只用其他用户 sudo 安装，结果各种问题。

从 Github 拉取官方正式版：

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash 
```

安装 Nvm：

```
source ~/.bashrc 
```

再用 Nvm 安装 Node.js：

```
nvm install node 
```

看看安装成功没有：

```
nvm --version
node --version
npm --version 
```

后面就可以 npm 一把梭了，当然也可以装 yarn 和 pm2，看个人喜好。

· · ·

七、小结
----

最后，终于来到最关键的部分了。其实上面这些整备的过程，一个脚本就可以搞定。

可以说是一次编写，多次运行，以后拿到新 VPS，直接复制过去就能跑。

整备的脚本，发个出来，给大家做个参考吧：

#### 1) 软件更新

```
apt update && apt upgrade && apt full-upgrade && apt autoremove 
```

如果不想一直蹲那儿按确认，可以强制自动确认（风险还是有的，自己权衡吧）：

```
apt update -y && apt upgrade -y && apt full-upgrade -y && apt autoremove -y 
```

#### 2) 创建和运行脚本

把脚本复制进去（参考脚本在后面，往下翻）：

```
vi ready.sh 
```

给执行权限：

```
chmod +x ready.sh 
```

运行脚本：

```
source ready.sh 
```

脚本 ready.sh 的参考内容如下：

```
#!/bin/bash










apt install ufw curl unzip




user
password="密码"
useradd -m -s /bin/bash -G sudo "$username"


echo "$username:$password" | chpasswd




sed -i '/#Port 22/a Port 22\nPort 端口号' /etc/ssh/sshd_config


systemctl restart sshd




public_key="本地公钥"


ssh-keygen


cat <<EOF > /当前用户目录/.ssh/authorized_keys
$public_key
EOF


chmod 600 /当前用户目录/.ssh/authorized_keys
systemctl restart sshd





file="/etc/ssh/sshd_config"
search="PermitRootLogin yes"
replace="PermitRootLogin without-password"
sed -i "s/$search/$replace/" "$file"


chmod 700 /当前用户目录/.ssh
systemctl restart sshd





ufw allow ssh
ufw allow 22
ufw allow 端口号


ufw enable



timedatectl set-timezone 时区



echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p 
```

跑完脚本验证一下配置，比如：新用户登录，root 用户无密码登录等，没问题就可以开始装应用干活了。

· · ·

七、相关
----

### 补充说明

如果是境内 VPS，有些额外的坑：可能需要镜像网站才能访问某些服务。

### 订阅通知

**后面还会有几篇 VPS、VPN 相关的的长文，可以订阅怪文的 [Telegram 电报（纸飞机）](https://t.me/guaiwin) 或者 [推特](https://x.com/guaiwin) 获取更新通知哦。**

### 相关资源