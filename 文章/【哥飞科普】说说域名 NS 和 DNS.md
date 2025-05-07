> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/65ZhVxcn_3j-MRb66iu6BQ)

大家好，我是哥飞。  

最近好多第一次注册域名，第一次使用 Cloudflare 和 Vercel 的朋友在域名解析上面产生了一些疑问，所以今天哥飞写篇文章来给大家讲一讲 NS 和 DNS 。

今天不是写论文，所以哥飞会基于自己的理解，尽量用浅显易懂的语言来描述，如果万一哪里有错误，还请大家在评论区补充说明。  

我们先从服务器聊起，每一台服务器都有一个 IP 地址，默认情况下，我们可以使用 IP 地址来访问服务器资源。  

但是 IP 地址太长了，很多人记不住，后来就有了域名，域名也可以理解为 IP 的别名。

每一个域名就相当于一个门牌号，把门牌号和服务器 IP 绑定到一起，用户通过域名也可以访问服务器资源。

管理域名和服务器 IP 对应关系的系统，就是域名系统，英文名 Domain Name System，简写为 DNS 。  

DNS 主要作用就是是把容易记忆的域名与不好记忆的 IP 地址给关联起来。

DNS 是全球分布式数据库系统，人人都可以搭建，并且对外提供 DNS 服务。

NS 是 Name Server 的简写，中文名是名称服务器。

NS 是 DNS 系统的其中一部分，如果你想对外提供 DNS 服务，就需要有一个 NS，用来让你的用户可以管理域名与 IP 的对应关系。

域名有域名注册局（Domain Registry）和域名注册商（Domain Registrar）的区分，每一个域名后缀都由一个域名注册局管理。

一般域名注册局不直接对外提供域名注册服务，而是由域名注册商提供域名注册服务。

一个域名注册商会跟多个域名注册局合作，这样就可以提供多种域名后缀的域名注册服务。  

一般域名注册商都会提供 NS ，大家注册的域名，默认的 NS 就是域名注册商的。  

所以我们如果要配置 DNS 解析记录，可以直接在域名注册商后台找到 DNS 管理，去添加或者修改解析记录。

但如果我们使用 Cloudflare 的服务，Cloudflare 会要求域名必须要用 Cloudflare 的 NS 。  

所以我们需要去 Cloudflare 后台添加一个域名，然后把 Cloudflare 给我们的 NS 填写到域名注册商的后台。

一旦你填写的新的 NS 生效了，在任意一个 Whois 查询服务里都能够查询到，如我们查一下 SoraWebui.com 的 Whois 信息。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LBrX00GQeics07oUpDPnUfhF28gKbYOnAcNVW5ACV1q3PlGLZQtibpVaGicNscNflxx4nbicCyibEa3J8MXkmOBTibeA/640?wx_fmt=png&from=appmsg)

可以看到上面显示 DNS 服务由 Cloudflare 提供，所以 NS 设置的是 Cloudflare 的服务器。

再看下 Google.com 可以看到 DNS 服务是谷歌自己做的，这也是为了保证服务的稳定性，不会受制于人。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LBrX00GQeics07oUpDPnUfhF28gKbYOnARicu2ZhmtXfEGRlxibelWicicprDbicxnHPkbKf5blZuDBr9wF7dWG7bktA/640?wx_fmt=png&from=appmsg)

当我们查询 Whois 信息发现 DNS 已经切换为 Cloudflare 的了，那就说明新的 NS 生效了，就可以去 Cloudflare 设置 DNS 解析记录。

在左侧菜单栏就可以找到 DNS 的 Records ，也就是 DNS 解析记录。  

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LBrX00GQeics07oUpDPnUfhF28gKbYOnAdWUJCy9yiaFmdp7p3pxVeMEu5Fibx9pPfTvQH5e3CveJgKPJgF66WUGA/640?wx_fmt=png&from=appmsg)

点进去，就能够看到所有解析记录。可以在这里添加新记录，修改旧记录，删除记录。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LBrX00GQeics07oUpDPnUfhF28gKbYOnA5ZKnjVpoCtibliaS0Lzb8663huBPXsjbDr8eqRZiaYF8pS9Bjv1tW3jpg/640?wx_fmt=png&from=appmsg)

你可能会为，上面要添加解析信息是哪里来的呢？

这就要看你的代码部署在哪里，如果部署在你自己的服务器里，上面就填写你自己服务器的 IP 地址。

我们这个服务是部署在 Vercel 上的，所以需要填写 Vercel 的 IP 和域名信息，分别是一个 A 记录，一个 CNAME 记录。

A 记录里直接填写 IP 地址，CNAME 记录里填写一个域名。

其实两者都表示某一个 IP 地址，只不过 A 记录写死了 IP 地址，而 CNAME 是别名，目前指向某个 IP 地址，下次 Vercel 可以改为另一个 IP 地址，而不需要通知我们修改。

这里哥飞举个例子大家就明白了。

假设哥飞有一台服务器，里边部署了 10 个网站，对应 10 个域名。

哥飞就需要去每一个域名的 DNS 解析里分别添加一条 A 记录，写死这台服务器的 IP 地址。

后面某一天，因为某种原因，这台服务器坏了，哥飞把所有 10 个网站代码迁移到了第二台服务器，之后要去修改 10 个域名的解析记录，总共要改 10 次，才能把全部域名修改完成。  

但假如一开始，哥飞就配置了某个子域名通过 A 记录指向了第一台服务器，然后 10 个网站都通过 CNAME 记录指向到了这个子域名。

那么当哥飞要把 10 个网站迁移到第二台服务器时，只需要去修改那个子域名的 A 记录，把第一台服务器的 IP 地址改为第二台服务器 IP 地址。

剩下 10 个网站因为是通过 CNAME 指向到那个子域名的，所以都不需要修改。

这里还需要解释一下，如果你的一台服务器里只有一个网站，那么你在 DNS 里把域名指向到了这台服务器，就能够访问到这台服务器的这个默认网站。

但假如你一台服务器有 10 个网站，你就需要用到 Nginx 的虚拟主机，通过配置虚拟主机来绑定域名与你 10 个网站代码目录的对应关系。

如果不配置的话，你的 10 个域名很可能都会打开同一个网站。  

回来说 Vercel ，因为 Vercel 一台服务器也会有很多个网站，所以我们需要在 Vercel 的每一个项目后台绑定域名。

填写我们想要绑定的域名之后，Vercel 就会告诉我们需要配置的 DNS 解析记录有哪些，一般会给一个 A 记录，一个 CNAME 记录。  

我们要做的就是去 Cloudflare 找到这个域名，打开 DNS 管理界面，填写新的解析记录。

如果你的解析记录已经存在相同的，会提示冲突，你就需要判断之前已经存在的记录是否需要，如果不需要就删除即可。  

好了，以上就是今天的科普内容。  

想要跟着哥飞学 SEO，做网站赚美元吗？

欢迎加入哥飞的付费社群 “哥飞的朋友们”。  

社群目前暂时是微信群形态，有一个配套的网站，已上线第一版，社群内朋友可见。

社群主要面向技术开发者、产品经理、设计师等人群，大家一起讨论独立开发、出海产品、流量获取、流量变现等话题。

社群讨论的话题主要是围绕着网站来的，用网站来承接流量，然后变现。

 那么就要考虑做什么网站，所以需要去挖掘需求。

然后去搞流量，可以是 SEO，也可以是发帖宣传推广，还可以是付费软文。

有了流量之后就得考虑如何变现，可以是广告变现，也可以是联盟导购，更可以直接向用户收费。

社群目前超过 1000 人，新的一期开始了，这期哥飞将带着大家实战，每个月都会安排任务，推着大家前进，让大家能够赚钱。

目前 888 元优惠价已经结束，前两天已经正式涨价为 999 元了。

社群按照 365 天计时，也就是你今天加入后，明年今日到期。

前两期讨论很活跃，行动很迅速，大家已经做了上百个产品了。 

有的几人小团队已经用几个月时间从零开始做到了月收入 4 万美元以上，还有的单人实现了月收入几千美元。

这个社群 7 月 2 号开始运营的，到今天 7 个多月时间里，主要讨论了以下话题：

1、建站基础，如何快速做一个网站；

2、SEO 基础，如何优化网站；

3、推广基础，如何宣传推广网站；

4、运营基础，如何运营好一个网站；

5、Adsense 基础，如何靠谷歌 Adsense 赚广告费；

6、一些工具使用经验分享，如 Semrush 分析别的网站流量和出入站链接，Similarweb 如何看流量；

7、基于 Semrush、Similarweb 等工具，如何去发掘新需求，发现新网站；

8、实战经验，如何去抓住新词热词做网站，从搜索引擎获取流量。

以上所有讨论都沉淀到了社群配套网站 web.cafe 上，所以第三期大家一进群就可以看到前两期的精华内容，以及其他更多相关话题。

欢迎加哥飞微信 qiayue 加入社群大家一起出海赚美元。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/LBrX00GQeicv24nb20ZrM7niaIBxv5QynWqOtclGh4ApYjVM5exp1niaK9pOLIOswYu2jU0zczI2Hx2bdfAo1Fwow/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)