![banner](./images/banner.png)

<p align="center">
  <a href="https://github.com/Game-K-Hack/dotclaude-analyzer/releases/latest"><img src="https://img.shields.io/github/v/release/Game-K-Hack/dotclaude-analyzer?label=Herunterladen&style=for-the-badge&logo=windows" alt="Herunterladen"></a>
</p>

[:fr: Français](./README.fr.md) | 
[:uk: English](../README.md) | 
[:kr: 한국어](./README.ko.md) | 
[:jp: 日本語](./README.ja.md) | 
[:cn: 中文](./README.zh.md) | 
[:it: Italiano](./README.it.md) | 
[:es: Español](./README.es.md) | 
[:ru: Русский](./README.ru.md) | 
**:de: Deutsch**

### DotClaude Analyzer

**DotClaude Analyzer** ist eine grafische Anwendung, die Ihren `.claude`-Ordner durchsucht, um Ihnen zu helfen, Ihre Aktivität mit Claude Code besser zu verstehen und zu nutzen.

Der Assistent ermöglicht es Ihnen:

- Ihre Einstellungen und Ihre Verbindung zu überprüfen;
- Ihre Projekte zu durchsuchen und alle Konversationen erneut zu lesen;
- alle von Claude erstellten oder geänderten Dateien aufzulisten;
- eine vollständige Version eines Projekts zu einem bestimmten Datum zu exportieren.

---

### Installation

```
git clone https://github.com/Game-K-Hack/dotclaude-analyzer.git
pip install -r requirements.txt
```

#### Starten der grafischen Oberfläche

```
python main.py
```

#### Build als EXE

```
pyinstaller --noconfirm build.spec
```

---

### Demonstration

![screenshot-1](./images/welcome.png)

Wählen Sie einen `.claude`-Ordner aus, der sich im `User`-Ordner befindet

![screenshot-2](./images/source.png)

Wählen Sie ein abzurufendes Projekt aus (Sie können seine Konversationen erneut lesen)

![screenshot-3](./images/conv.png)

Wählen Sie die Version der zu exportierenden Dateien aus

![screenshot-4](./images/files.png)
