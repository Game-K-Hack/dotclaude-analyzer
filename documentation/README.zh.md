![banner](./images/banner.png)

<p align="center">
  <a href="https://github.com/Game-K-Hack/dotclaude-analyzer/releases/latest"><img src="https://img.shields.io/github/v/release/Game-K-Hack/dotclaude-analyzer?label=%E4%B8%8B%E8%BD%BD&style=for-the-badge&logo=windows" alt="下载"></a>
</p>

[:fr: Français](./README.fr.md) | 
[:uk: English](../README.md) | 
[:kr: 한국어](./README.ko.md) | 
[:jp: 日本語](./README.ja.md) | 
**:cn: 中文** | 
[:it: Italiano](./README.it.md) | 
[:es: Español](./README.es.md) | 
[:ru: Русский](./README.ru.md) | 
[:de: Deutsch](./README.de.md)

### DotClaude Analyzer

**DotClaude Analyzer** 是一个图形化应用程序,可探索您的 `.claude` 文件夹,帮助您更好地理解和利用您在 Claude Code 中的活动。

该助手允许您:

- 查看您的设置和连接信息;
- 浏览您的项目并重新阅读所有对话;
- 列出 Claude 创建或修改的所有文件;
- 导出指定日期的项目完整版本。

---

### 安装

```
git clone https://github.com/Game-K-Hack/dotclaude-analyzer.git
pip install -r requirements.txt
```

#### 启动图形界面

```
python main.py
```

#### 构建 EXE

```
pyinstaller --noconfirm build.spec
```

---

### 演示

![screenshot-1](./images/welcome.png)

选择位于 `User` 文件夹中的 `.claude` 文件夹

![screenshot-2](./images/source.png)

选择要获取的项目(您可以重新阅读这些对话)

![screenshot-3](./images/conv.png)

选择要导出的文件版本

![screenshot-4](./images/files.png)
