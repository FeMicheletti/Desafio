from pathlib import Path
from datetime import datetime, timezone


def _safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)


def save_artifacts(driver, test_name: str, out_dir: str = "artifacts"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    base = f"{_safe_name(test_name)}_{ts}"

    png_path = Path(out_dir) / f"{base}.png"
    html_path = Path(out_dir) / f"{base}.html"

    driver.save_screenshot(str(png_path))
    html_path.write_text(driver.page_source, encoding="utf-8")

    return str(png_path), str(html_path)
