from __future__ import annotations

import re
import urllib.request
from pathlib import Path
from typing import List, Tuple


def load_tlds() -> set[str]:
    tld_url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    with urllib.request.urlopen(tld_url, timeout=20) as response:
        text = response.read().decode("utf-8")

    tlds = set()
    for line in text.splitlines():
        line = line.strip().upper()
        if line and not line.startswith("#"):
            tlds.add(line)
    return tlds


def validate_domain(domain: str, tlds: set[str] | None = None) -> List[str]:
    if tlds is None:
        tlds = load_tlds()

    domain = domain.strip()
    if not domain or domain.startswith("#"):
        return []

    errors: List[str] = []

    if not 4 <= len(domain) <= 255:
        errors.append("length")

    if not re.fullmatch(r"[A-Za-z0-9._-]+", domain):
        errors.append("characters")

    if domain.startswith(".") or domain.endswith("."):
        errors.append("dot-bounds")

    if domain.startswith("-") or domain.endswith("-"):
        errors.append("hyphen-bounds")

    if domain.count(".") < 1:
        errors.append("missing-dot")

    if ".." in domain:
        errors.append("consecutive-dots")

    if "-." in domain:
        errors.append("hyphen-dot")

    labels = domain.split(".")
    if len(labels) < 2:
        errors.append("missing-labels")
    else:
        tld = labels[-1].upper()
        if tld != "ONION" and tld not in tlds:
            errors.append("tld")

    return errors


def iter_domain_files(root: Path | None = None) -> List[Path]:
    if root is None:
        root = Path(__file__).resolve().parent
    return sorted(root.glob("*.domains"))


def find_invalid_domains(root: Path | None = None) -> List[Tuple[Path, int, str, List[str]]]:
    if root is None:
        root = Path(__file__).resolve().parent
    tlds = load_tlds()
    invalid: List[Tuple[Path, int, str, List[str]]] = []

    for path in iter_domain_files(root):
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                domain = raw_line.strip()
                if not domain:
                    continue
                errors = validate_domain(domain, tlds)
                if errors:
                    invalid.append((path, line_number, domain, errors))

    return invalid


if __name__ == "__main__":
    invalid = find_invalid_domains()
    if invalid:
        print(f"Found {len(invalid)} invalid domain entries:")
        for path, line_number, domain, errors in invalid:
            print(f"{path.name}:{line_number}: {domain} -> {', '.join(errors)}")
        raise SystemExit(1)

    print("All domain entries passed validation.")
