import appdirs
import platform
import sys
import os

app_name = "PolarAttack"

APP_DIR = appdirs.user_data_dir(app_name, roaming=True, appauthor=False)
CACHE_DIR =appdirs.user_cache_dir(app_name, appauthor=False)
LOG_DIR = appdirs.user_log_dir(app_name, appauthor=False)

SETTINGS = os.path.join(APP_DIR, "settings.json")

def resource_path(relative_path):
    """
    Return an absolute path to a resource. Works both when running from source
    and when running from a PyInstaller bundle (onefile or onefolder), or inside
    a macOS .app bundle produced by PyInstaller.

    Behavior:
    - If running frozen (PyInstaller), try a set of likely extraction/Resources
      locations (sys._MEIPASS, _internal, Contents/Resources, Contents/Resources/_internal).
      Return the first location where the resource exists (or the first candidate
      when dealing with directories).
    - Otherwise (not frozen) return the joined path relative to the current working
      directory (typical development layout).
    """
    # Running in a PyInstaller bundle?
    if getattr(sys, "frozen", False):
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        # Common PyInstaller extraction/layout locations (best-effort checks)
        candidates = [
            base_path,
            os.path.join(base_path, "_internal"),
            os.path.join(base_path, "Contents", "Resources"),
            os.path.join(base_path, "Contents", "Resources", "_internal"),
        ]
        # If relative_path is empty, return the first existing base directory
        if not relative_path:
            for p in candidates:
                if os.path.isdir(p):
                    return p
            return base_path
        # Try candidate locations for the resource
        for p in candidates:
            candidate = os.path.join(p, relative_path)
            if os.path.exists(candidate):
                return candidate
        # Fallback: return joined path with base_path even if file doesn't yet exist
        return os.path.join(base_path, relative_path)
    else:
        # Running from source (development): use project cwd
        return os.path.join(os.path.abspath("."), relative_path)


def chromium_path():
    """
    Return a tuple (chrome_binary_path, chromedriver_path) suitable for Selenium.
    The function attempts several locations (bundle resources, bundled chromium, system chrome)
    to be robust for:
      - development run
      - PyInstaller one-folder and one-file bundles
      - macOS .app bundles
      - Windows one-folder bundles

    It prefers bundled binaries (via resource_path) when available, otherwise falls back
    to system-installed chrome/chromium via shutil.which, and finally returns the
    resource_path fallback (which may be non-existent if not bundled).
    """
    from shutil import which

    system = platform.system()
    # macOS (Darwin)
    if system == "Darwin":
        chrome_candidates = [
            resource_path("chromium_mac/Chromium.app/Contents/MacOS/Chromium"),
            resource_path("Chromium.app/Contents/MacOS/Chromium"),
            # allow a path named chrome as a fallback in some setups
            resource_path("chromium_mac/Chromium"),
            resource_path("chrome"),
        ]
        driver_candidates = [
            resource_path("chromedriver"),                # unix-style bundled chromedriver
            resource_path("chromedriver.exe"),            # fallback if misnamed
        ]
        # prefer a bundled chrome if present
        chrome = None
        for c in chrome_candidates:
            if c and os.path.exists(c):
                chrome = c
                break
        if chrome is None:
            # try system installations
            chrome = which("chromium") or which("chromium-browser") or which("google-chrome") or which("chrome")
        # prefer bundled chromedriver if present, otherwise use resource fallback
        driver = None
        for d in driver_candidates:
            if d and os.path.exists(d):
                driver = d
                break
        if driver is None:
            driver = resource_path("chromedriver")
        return chrome, driver

    # Windows and other platforms
    else:
        # Windows typical bundled chromium path
        chrome_candidate = resource_path("chromium_win\\chrome.exe")
        driver_candidate = resource_path("chromedriver.exe")
        chrome = chrome_candidate if chrome_candidate and os.path.exists(chrome_candidate) else None
        if chrome is None:
            # try system-installed chrome executables
            chrome = which("chrome") or which("chrome.exe") or which("msedge") or which("google-chrome")
        # driver
        driver = driver_candidate if driver_candidate and os.path.exists(driver_candidate) else resource_path("chromedriver.exe")
        return chrome, driver

def sep()-> str:
    if platform.system() == "Windows":
        return '\\'
    else:
        return '/'
