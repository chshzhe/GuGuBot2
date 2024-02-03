# GuGuBot2

## How to start

1. generate project using `nb create` .
2. create your plugin using `nb plugin create` .
3. writing your plugins under `src/plugins` folder.
4. run your bot using `nb run` .

## 部署方法

### 配置Shamrock（类似go-cqhttp的作用）

> 考虑到 MuMu12 模拟器对 `Magisk` 和 `LSPosed` 暂时[还不支持](https://forum.libfekit.so/d/60-mumu12mo-ni-qi-an-zhuang-magiskhe-lsposed/3)，此处展示基于 `LSPatch` 的配置方案。
> 
> 其特点参看[OpenShamrock指南](https://whitechi73.github.io/OpenShamrock/guide/getting-started.html#%E6%97%A0-root-%E7%8E%AF%E5%A2%83)

1. 安装 MuMU12 模拟器，记得打开MuMU12模拟器的可写系统盘和 Root 权限。为了长期运行，建议打开后台保活。
![可写系统盘权限](IMG/img-1.png)
![Root权限和保活](IMG/img-2.png)

2. 从[LSPatch](https://github.com/LSPosed/LSPatch)下载最新 `release` 的 `LSPatch` ，并安装到模拟器中。

3. 从[OpenShamrock](https://github.com/whitechi73/OpenShamrock)的 `Action` 下载最新开发版 `Shamrock` ，注意下载带有 `all` 字样的版本，如 `Shamrock-v1.0.7.r253.81be383-all.zip` ，并安装到模拟器中。

4. 参考[此页面](https://whitechi73.github.io/OpenShamrock/guide/faq.html#%E6%94%AF%E6%8C%81%E7%9A%84qq%E7%89%88%E6%9C%AC)给出的支持的 QQ 版本，选择最新即可，在[这里](https://qq.cn.uptodown.com/android/versions)选择对应的版本下载，在 MuMu 模拟器安装即可。

5. 在 `LSPatch` 中用 `Shamrock` 修补 QQ 。
     - 打开 `LSPatch` 并在管理页面选择 ` + ` 新建修补，可以选择从存储目录选择 QQAPK 或者直接使用已经安装过的 QQ 
     - 修补模式默认且应该优先选择本地模式，这样方便直接更新 `Shamrock` 模块而不用重新修补，缺点是需要 `LSPatch` 保持后台运行 
     - 其他配置保持默认，然后点击开始修补，修补完成后会提示安装(如果已经安装会提示卸载)，或者手动替换安装。
     - 安装 `Shamrock` 模块后在管理页面点击修补好的 QQ ，选择模块作用域勾选上 `Shamrock` 模块然后保存 
     - 启动 `Shamrock` 并重新启动 QQ 客户端 
     - 此时 `Shamrock` 会显示已激活。
     - 登录 `Bot` 账号，然后在 `Shamrock - 状态` 勾选 `强制平板模式` ，方便安卓手机登录监看。

### 安装GUGUBot2

1. `git clone` 本项目，进入项目根目录，创建虚拟环境并安装依赖
   ```shell
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. 安装脚手架，参看[Nonebot2文档](https://nonebot.dev/docs/quick-start#%E5%AE%89%E8%A3%85%E8%84%9A%E6%89%8B%E6%9E%B6)

3. 安装 `NoneBot2`、`OneBot` 适配器和 `APScheduler` 插件
   ```
   pip install nonebot2[fastapi]
   nb adapter install nonebot-adapter-onebot
   nb plugin install nonebot-plugin-apscheduler
   ```
4. 运行 Bot 服务，但此时尚未配置模拟器和本机的通信，因此无法接收消息。
   ```
   nb run
   ```