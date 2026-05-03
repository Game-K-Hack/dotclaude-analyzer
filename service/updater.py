import json
import re
from urllib.request import Request, urlopen

from PyQt5.QtCore import QObject, QThread, pyqtSignal

from service.version import __version__

RELEASES_API_URL = "https://api.github.com/repos/Game-K-Hack/dotclaude-analyzer/releases/latest"
RELEASES_PAGE_URL = "https://github.com/Game-K-Hack/dotclaude-analyzer/releases"


def _normalize(tag: str) -> tuple:
    tag = tag.strip().lstrip("vV")
    parts = re.split(r"[.\-+]", tag)
    out = []
    for p in parts:
        if p.isdigit():
            out.append((0, int(p)))
        else:
            out.append((1, p))
    return tuple(out)


def is_newer(remote: str, local: str) -> bool:
    if not remote or not local:
        return False
    if remote.lstrip("vV") == local.lstrip("vV"):
        return False
    try:
        return _normalize(remote) > _normalize(local)
    except Exception:
        return False


def fetch_latest_tag(timeout: float = 5.0) -> str | None:
    req = Request(RELEASES_API_URL, headers={"Accept": "application/vnd.github+json"})
    with urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("tag_name")


class UpdateChecker(QObject):
    update_available = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread = QThread(parent)
        self.moveToThread(self._thread)
        self._thread.started.connect(self._run)

    def start(self):
        self._thread.start()

    def _run(self):
        try:
            latest = fetch_latest_tag()
            if latest and is_newer(latest, __version__):
                self.update_available.emit(__version__, latest)
        except Exception:
            pass
        finally:
            self._thread.quit()
