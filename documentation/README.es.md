![banner](./images/banner.png)

<p align="center">
  <a href="https://github.com/Game-K-Hack/dotclaude-analyzer/releases/latest"><img src="https://img.shields.io/github/v/release/Game-K-Hack/dotclaude-analyzer?label=Descargar&style=for-the-badge&logo=windows" alt="Descargar"></a>
</p>

[:fr: Français](./README.fr.md) | 
[:uk: English](../README.md) | 
[:kr: 한국어](./README.ko.md) | 
[:jp: 日本語](./README.ja.md) | 
[:cn: 中文](./README.zh.md) | 
[:it: Italiano](./README.it.md) | 
**:es: Español** | 
[:ru: Русский](./README.ru.md) | 
[:de: Deutsch](./README.de.md)

### DotClaude Analyzer

**DotClaude Analyzer** es una aplicación gráfica que explora tu carpeta `.claude` para ayudarte a comprender y aprovechar mejor tu actividad con Claude Code.

El asistente te permite:

- inspeccionar tus parámetros y tu conexión;
- recorrer tus proyectos y releer todas sus conversaciones;
- listar todos los archivos creados o modificados por Claude;
- exportar una versión completa de un proyecto en una fecha determinada.

---

### Instalación

```
git clone https://github.com/Game-K-Hack/dotclaude-analyzer.git
pip install -r requirements.txt
```

#### Iniciar la interfaz gráfica

```
python main.py
```

#### Compilar como EXE

```
pyinstaller --noconfirm build.spec
```

---

### Demostración

![screenshot-1](./images/welcome.png)

Selecciona una carpeta `.claude` ubicada en la carpeta `User`

![screenshot-2](./images/source.png)

Selecciona un proyecto a recuperar (puedes releer sus conversaciones)

![screenshot-3](./images/conv.png)

Selecciona la versión de los archivos a exportar

![screenshot-4](./images/files.png)
