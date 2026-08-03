from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from validate_domains import find_invalid_domains, validate_domain


def test_validate_domain_rejects_invalid_examples():
    assert validate_domain("example.com") == []
    assert validate_domain("-example.com") != []
    assert validate_domain("example-.com") != []
    assert validate_domain("example..com") != []
    assert validate_domain("example.com.") != []
    assert validate_domain("example") != []
    assert validate_domain("exa_mple.com") == []
    assert validate_domain("example.c") != []
    assert validate_domain("example.onion") == []
    assert validate_domain("my_domain.example.com") == []


def test_all_domains_in_blocklists_are_valid():
    root = Path(__file__).resolve().parents[1]
    invalid = find_invalid_domains(root)
    assert not invalid, (
        "Found invalid domains:\n"
        + "\n".join(
            f"{path.name}:{line}: {domain} -> {', '.join(errors)}"
            for path, line, domain, errors in invalid[:20]
        )
    )
