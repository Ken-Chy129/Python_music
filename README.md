> 介绍

基于**GUI界面**、**爬虫**、**数据处理**、**可视化展示**和**数据库存储**实现的可进行音乐搜索、音乐播放、音乐下载、音乐收藏、歌词下载、歌曲信息保存、当前热门歌曲查看、当前热门歌手、数据分析查看的一款软件

> 环境说明

计算机系统版本：Windows10

python版本：Python3.9

编辑器：Pycharm2021.1.2

> 界面预览

**登录页**：输入账号密码后点击Register进行注册，注册成功后数据会同步至数据库，随后即可输入该账号密码登录进入主界面

![登录](https://img-blog.csdnimg.cn/dafbf7008d364c5393064751f6012afa.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5b6X6L-H5LiU6L-H55qE5YuH6ICFeQ==,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

![登录2](https://img-blog.csdnimg.cn/aa48c0704abb4c87955601287f70b82a.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5b6X6L-H5LiU6L-H55qE5YuH6ICFeQ==,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

**主界面**：

![主界面](https://img-blog.csdnimg.cn/af83fc99068a4940bef91e4c1bc8b136.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5b6X6L-H5LiU6L-H55qE5YuH6ICFeQ==,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

**爬虫数据展示**：

![爬虫数据展示](https://img-blog.csdnimg.cn/e2e162ed20b34bcc9d234f024a610f1e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5b6X6L-H5LiU6L-H55qE5YuH6ICFeQ==,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

**数据分析展示**：

![image-20211217161817352](https://img-blog.csdnimg.cn/a44d346dccbe482bbfb3947d73f9a97b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5b6X6L-H5LiU6L-H55qE5YuH6ICFeQ==,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

![热门歌手歌曲量占比饼图](https://img-blog.csdnimg.cn/7ae6a729860d426cbe56f95684c326b1.jpg?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5b6X6L-H5LiU6L-H55qE5YuH6ICFeQ==,size_14,color_FFFFFF,t_70,g_se,x_16#pic_center)

**数据库展示：**

![数据库](https://img-blog.csdnimg.cn/7d5838b18073444bab0bfa6987faa9a2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5b6X6L-H5LiU6L-H55qE5YuH6ICFeQ==,size_11,color_FFFFFF,t_70,g_se,x_16#pic_center)

> 代码说明

具体代码功能与实现可以前往https://ken-chy129.blog.csdn.net/article/details/121876876进行查看

> 软件说明

1. 程序中分为两个类，分别对应两个GUI界面
2. 注册登录界面登录成功会传递当前登录的用户名以调用主界面
3. 进入主界面会自动调用search函数（默认search(“陈奕迅”)）爬取歌曲信息并展示，可以通过在界面上的搜索框进行搜索其他歌手或歌曲
4. 点击搜索结果的歌名可以进行音乐播放，当播放结束会自动进入下一首，知道列表播放结束提示暂无下一首
5. 可以点击进度条上的按钮实现上一首，播放/暂停，下一首的功能
6. 点击右边执行操作即可实现相应的功能
7. 点击左侧我的下载和我的收藏可以查看当前用户收藏和下载过的歌曲
8. 点击左侧联系与帮助可以进入CSDN查看开发的流程，访问作者个人博客等

>使用须知

1. 在使用之前得确保本地有相应的数据库和表，否则会出现数据库连接失败的情况
   - `host='localhost', user='root', password='129496', db='pyhomework'`（也可以更改数据库连接部分的代码为自己的用户名和密码）
   - 项目中已附带对应的建表的sql语句
2. 在进入主页面之前必须保证联网状态，因为进入主界面会自动触发爬虫搜索功能，需要联网否则会因连接超时而报错
3. 启动前需要先安装好依赖的包

