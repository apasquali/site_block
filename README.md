# Domain Blocklist Collection

This directory contains a set of domain blocklist files in plain-text .domains format. Each file holds one domain per line and is organized by category.

## Included files

- [antimalware.domains](antimalware.domains)
- [base.domains](base.domains)
- [cryptocurrency.domains](cryptocurrency.domains)
- [dhs-ais.domains](dhs-ais.domains)
- [high.domains](high.domains)
- [scambling.domains](scambling.domains)
- [site_block.domains](site_block.domains)

## Intended use

These lists are intended for filtering, monitoring, or threat-intelligence workflows that rely on flat domain lists.

## Validation rules

Entries should be valid domain names and are checked by the CI workflow. The rules include:
- length between 4 and 255 characters
- only letters, numbers, dots, underscores, and hyphens
- no leading/trailing dot or hyphen
- at least one dot
- no consecutive dots
- no hyphen-before-dot sequence
- valid public TLDs (https://data.iana.org/TLD/tlds-alpha-by-domain.txt), with .onion allowed

## Notes

- The files are simple text-based blocklists.
- Use them with tools that accept domain lists in .domains format.
- Please review [LICENSE](LICENSE) for licensing terms.
- change
