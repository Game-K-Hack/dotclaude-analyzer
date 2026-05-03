![banner](./images/banner.png)

<p align="center">
  <a href="https://github.com/Game-K-Hack/dotclaude-analyzer/releases/latest"><img src="https://img.shields.io/github/v/release/Game-K-Hack/dotclaude-analyzer?label=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&style=for-the-badge&logo=windows" alt="다운로드"></a>
</p>

[:fr: Français](./README.fr.md) | 
[:uk: English](../README.md) | 
**:kr: 한국어** | 
[:jp: 日本語](./README.ja.md) | 
[:cn: 中文](./README.zh.md) | 
[:it: Italiano](./README.it.md) | 
[:es: Español](./README.es.md) | 
[:ru: Русский](./README.ru.md) | 
[:de: Deutsch](./README.de.md)

### DotClaude Analyzer

**DotClaude Analyzer**는 `.claude` 폴더를 탐색하여 Claude Code와 함께한 활동을 더 잘 이해하고 활용할 수 있도록 도와주는 그래픽 애플리케이션입니다.

이 어시스턴트를 통해 다음 작업을 할 수 있습니다:

- 설정 및 연결 정보 확인하기;
- 프로젝트를 탐색하고 모든 대화 내용을 다시 읽기;
- Claude가 생성하거나 수정한 모든 파일 나열하기;
- 특정 날짜의 프로젝트 전체 버전 내보내기.

---

### 설치

```
git clone https://github.com/Game-K-Hack/dotclaude-analyzer.git
pip install -r requirements.txt
```

#### 그래픽 인터페이스 실행

```
python main.py
```

#### EXE 빌드

```
pyinstaller --noconfirm build.spec
```

---

### 데모

![screenshot-1](./images/welcome.png)

`User` 폴더에 있는 `.claude` 폴더 선택

![screenshot-2](./images/source.png)

가져올 프로젝트 선택 (대화 내용을 다시 읽을 수 있습니다)

![screenshot-3](./images/conv.png)

내보낼 파일의 버전 선택

![screenshot-4](./images/files.png)
