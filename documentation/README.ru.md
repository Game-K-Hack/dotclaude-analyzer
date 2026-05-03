![banner](./images/banner.png)

<p align="center">
  <a href="https://github.com/Game-K-Hack/dotclaude-analyzer/releases/latest"><img src="https://img.shields.io/github/v/release/Game-K-Hack/dotclaude-analyzer?label=%D0%A1%D0%BA%D0%B0%D1%87%D0%B0%D1%82%D1%8C&style=for-the-badge&logo=windows" alt="Скачать"></a>
</p>

[:fr: Français](./README.fr.md) | 
[:uk: English](../README.md) | 
[:kr: 한국어](./README.ko.md) | 
[:jp: 日本語](./README.ja.md) | 
[:cn: 中文](./README.zh.md) | 
[:it: Italiano](./README.it.md) | 
[:es: Español](./README.es.md) | 
**:ru: Русский** | 
[:de: Deutsch](./README.de.md)

### DotClaude Analyzer

**DotClaude Analyzer** — это графическое приложение, которое исследует вашу папку `.claude`, чтобы помочь вам лучше понимать и использовать вашу активность с Claude Code.

Помощник позволяет:

- проверять ваши настройки и подключение;
- просматривать ваши проекты и перечитывать все их беседы;
- перечислять все файлы, созданные или изменённые Claude;
- экспортировать полную версию проекта на заданную дату.

---

### Установка

```
git clone https://github.com/Game-K-Hack/dotclaude-analyzer.git
pip install -r requirements.txt
```

#### Запуск графического интерфейса

```
python main.py
```

#### Сборка в EXE

```
pyinstaller --noconfirm build.spec
```

---

### Демонстрация

![screenshot-1](./images/welcome.png)

Выберите папку `.claude`, находящуюся в папке `User`

![screenshot-2](./images/source.png)

Выберите проект для получения (вы можете перечитать его беседы)

![screenshot-3](./images/conv.png)

Выберите версию файлов для экспорта

![screenshot-4](./images/files.png)
