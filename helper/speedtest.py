import asyncio
import json
import logging
import shutil
import subprocess
import time

logger = logging.getLogger(__name__)

# A full test saturates the link for several seconds; running it on every status
# page view would hurt the very traffic it reports on.
CACHE_TTL = 600
TEST_TIMEOUT = 120


class SpeedResult:
    __slots__ = ("speed", "ping", "server", "measured_at")

    def __init__(self, speed=None, ping=None, server=None):
        self.speed = speed  # download Mbps or None when the test failed
        self.ping = ping    # ms or None
        self.server = server
        self.measured_at = time.time()

    def label(self) -> str:
        return f"{self.speed:.2f} Mbps" if self.speed is not None else "N/A"

    def is_fresh(self) -> bool:
        return time.time() - self.measured_at < CACHE_TTL


_result: SpeedResult | None = None
_lock = asyncio.Lock()


def _run_cmd(cmd):
    return subprocess.check_output(cmd, timeout=TEST_TIMEOUT)


def _run_official() -> dict:
    out = _run_cmd([shutil.which("speedtest"), "--accept-license", "--accept-gdpr", "-f", "json"])
    data = json.loads(out)
    # Official CLI: download.bandwidth is bytes/sec, ping.latency is ms.
    return {
        "speed": data["download"]["bandwidth"] * 8 / 1_000_000,
        "ping": data.get("ping", {}).get("latency"),
        "server": (data.get("server") or {}).get("name"),
    }


def _run_speedtest_cli() -> dict:
    out = _run_cmd([shutil.which("speedtest-cli"), "--json"])
    data = json.loads(out)
    # speedtest-cli: download is bits/sec already.
    return {
        "speed": data["download"] / 1_000_000,
        "ping": data.get("ping"),
        "server": (data.get("server") or {}).get("name"),
    }


def _is_official(path: str | None) -> bool:
    if not path:
        return False
    try:
        out = subprocess.check_output(
            [path, "--version"], timeout=10, stderr=subprocess.STDOUT
        ).decode(errors="ignore")
        return "ookla" in out.lower()
    except Exception:
        return False  # shortcut: version probe failed -> treat as unofficial


def _run_sync() -> SpeedResult:
    official = shutil.which("speedtest")
    cli = shutil.which("speedtest-cli")
    runners = []
    if _is_official(official):
        runners.append(_run_official)
    elif official and official != cli:
        # `speedtest` exists but isn't Ookla (often a speedtest-cli alias):
        # skip it, the --accept-license flags would just fail noisily.
        logger.debug("speedtest: ignoring non-Ookla binary at %s", official)
    if cli or (official and not runners):
        runners.append(_run_speedtest_cli)
    if not runners:
        logger.warning("speedtest: no Ookla client found (install 'speedtest' or 'speedtest-cli')")
        return SpeedResult()

    for runner in runners:
        try:
            return SpeedResult(**runner())
        except Exception as e:
            logger.warning("speedtest: %s failed: %s", runner.__name__, e)
    return SpeedResult()


async def network_speed() -> SpeedResult:
    """Latest Ookla download result, refreshed at most every CACHE_TTL seconds."""
    global _result
    if _result is not None and _result.is_fresh():
        return _result
    async with _lock:
        if _result is not None and _result.is_fresh():
            return _result
        _result = await asyncio.to_thread(_run_sync)
        return _result


async def network_speed_label() -> str:
    'Like "33.60 Mbps (Server)" or "N/A"; never raises.'
    result = await network_speed()
    label = result.label()
    if result.server:
        label += f" ({result.server})"
    return label
