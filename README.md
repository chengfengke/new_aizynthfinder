

**注意事项：开发时请勿将new_aizynthfinder包整个提交至git，提交前请运行git status进行检查**

**注意事项：开发时请勿将new_aizynthfinder包整个提交至git，提交前请运行git status进行检查**

**注意事项：开发时请勿将new_aizynthfinder包整个提交至git，提交前请运行git status进行检查**



# aizynthfinder-web（开发中）

基于aizynthfinder化学逆合成算法包制作的web网站的前后端代码仓库





## 前端 - aizynthfinder-web-frontend

### 技术选型

- HTML + CSS + JavaScript 三件套
- React
- Ant Design组件库
- Umi
- Ant Design Pro 脚手架



### 基本页面

#### 用户登录页

<img src="images/image-20240228040431631.png" height="400" style="float:left;">

#### 欢迎页

<img src="images/image-20240228040511349.png" height="400" style="float:left;">

#### 逆合成分析页

<img src="images/image-20240228185310364.png" height="400" style="float:left;">

## 后端 - aizynthfinder-web-backend

### 技术选型

- Python + Flask







## 快速开始

1. 将项目克隆至本地

```bash
git clone https://github.com/nx-xn2002/aizynthfinder-web.git
```

2. 安装相关依赖

安装最新LTS版本的node.js以便运行前端项目 https://nodejs.org/en

在命令行更新当前npm至最新版本

3. 配置并启动前端项目

在idea、webstorm或pycharm等ide中，打开`aizynthfinder-web/aizynthfinder-web-frontend`文件夹，前端项目文件夹如图所示

<img src="images/image-20240302145112299.png" height="500" style="float:left;">

在当前`aizynthfinder-web-frontend`目录下，命令行运行`npm install`指令安装依赖

运行完毕后，运行`package.json`文件中的`start`命令启动前端

![image-20240302145719677](images/image-20240302145719677.png)

启动成功可在浏览器看到以下页面

<img src="images/image-20240302150829448.png" height="300" style="float:left;">

4. 配置并启动后端

在外部其他目录下，运行拉取后端依赖包

```bash
git clone https://github.com/chengfengke/new_aizynthfinder.git
```

然后在包目录下运行拉取大文件

```bash
git lfs pull
```

完成后，为避免项目中出现冲突，请将当前拉取到的`new_aizynthfinder`文件夹内的`.git`隐藏文件夹删除并重新创建一个名为`.git`的文件夹

严格完成以上步骤后，将当前文件夹拖入`aizynthfinder-web`文件夹中，然后在pycharm中打开`aizynthfinder-web/new_aizynthfinder`文件夹

请使用`new_aizynthfinder`的虚拟环境运行该项目，另外，请通过`pip install`指令下载`flask_cors`和`flask`包

在`aizynthfinder-web-backend/Config.py`文件中，配置当前前端的路径

接下来，启动`new_aizynthfinder/aizynthfinder-web-backend/app.py`即可

5. 在浏览器中使用默认账号密码admin尝试进行登录，若成功，则前后端配置启动完毕



