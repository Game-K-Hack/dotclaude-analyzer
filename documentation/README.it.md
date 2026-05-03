![banner](./images/banner.png)

<p align="center">
  <a href="https://github.com/Game-K-Hack/dotclaude-analyzer/releases/latest"><img src="https://img.shields.io/github/v/release/Game-K-Hack/dotclaude-analyzer?label=Scarica&style=for-the-badge&logo=windows" alt="Scarica"></a>
</p>

[:fr: Français](./README.fr.md) | 
[:uk: English](../README.md) | 
[:kr: 한국어](./README.ko.md) | 
[:jp: 日本語](./README.ja.md) | 
[:cn: 中文](./README.zh.md) | 
**:it: Italiano** | 
[:es: Español](./README.es.md) | 
[:ru: Русский](./README.ru.md) | 
[:de: Deutsch](./README.de.md)

### DotClaude Analyzer

**DotClaude Analyzer** è un'applicazione grafica che esplora la tua cartella `.claude` per aiutarti a comprendere e sfruttare meglio la tua attività con Claude Code.

L'assistente ti permette di:

- ispezionare le tue impostazioni e la tua connessione;
- sfogliare i tuoi progetti e rileggere tutte le loro conversazioni;
- elencare tutti i file creati o modificati da Claude;
- esportare una versione completa di un progetto a una data specifica.

---

### Installazione

```
git clone https://github.com/Game-K-Hack/dotclaude-analyzer.git
pip install -r requirements.txt
```

#### Avvio dell'interfaccia grafica

```
python main.py
```

#### Build in EXE

```
pyinstaller --noconfirm build.spec
```

---

### Dimostrazione

![screenshot-1](./images/welcome.png)

Seleziona una cartella `.claude` situata nella cartella `User`

![screenshot-2](./images/source.png)

Seleziona un progetto da recuperare (puoi rileggere le sue conversazioni)

![screenshot-3](./images/conv.png)

Seleziona la versione dei file da esportare

![screenshot-4](./images/files.png)
