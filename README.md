![banner](./documentation/images/banner.png)

<p align="center">
  <a href="https://github.com/Game-K-Hack/dotclaude-analyzer/releases/latest"><img src="https://img.shields.io/github/v/release/Game-K-Hack/dotclaude-analyzer?label=Download&style=for-the-badge&logo=windows" alt="Download"></a>
</p>

[:fr: Français](./documentation/README.fr.md) | 
**:uk: English** | 
[:kr: 한국어](./documentation/README.ko.md) | 
[:jp: 日本語](./documentation/README.ja.md) | 
[:cn: 中文](./documentation/README.zh.md) | 
[:it: Italiano](./documentation/README.it.md) | 
[:es: Español](./documentation/README.es.md) | 
[:ru: Русский](./documentation/README.ru.md) | 
[:de: Deutsch](./documentation/README.de.md)

### DotClaude Analyzer

**DotClaude Analyzer** is a graphical application that explores your `.claude` folder to help you better understand and leverage your activity with Claude Code.

The assistant allows you to:

- inspect your settings and connection;
- browse your projects and reread all of their conversations;
- list every file created or modified by Claude;
- export a full version of a project at a given date.

---

### Installation

```
git clone https://github.com/Game-K-Hack/dotclaude-analyzer.git
pip install -r requirements.txt
```

#### Launching the graphical interface

```
python main.py
```

#### Building the EXE

```
pyinstaller --noconfirm build.spec
```

---

### Demo

![screenshot-1](./documentation/images/welcome.png)

Select a `.claude` folder located in the `User` folder

![screenshot-2](./documentation/images/source.png)

Select a project to retrieve (you can reread its conversations)

![screenshot-3](./documentation/images/conv.png)

Select the version of the files to export

![screenshot-4](./documentation/images/files.png)

![](https://dawn-wave-6f61.hack-h.workers.dev/?project=github%2Fdotclaude-analyzer)
