# YAML Yugi (한국어)

The [YAML Yugi](https://github.com/DawnbrandBots/yaml-yugi) project aims to create a comprehensive, machine-readable,
human-editable database of the _Yu-Gi-Oh! Trading Card Game_ and _Official Card Game_.

## Proposal

This repository will become the central source of community translations of Yu-Gi-Oh cards in Korean.
This includes the following categories of OCG and Rush Duel cards:
- cards not yet released in Korea (e.g. OCG cards before print, TCG world premiere cards)
- cards with outdated or incorrect errata on the official database
- cards that are missing ruby text in their names on the official database

The community translations will be combined with text from the official database for ingest into YAML Yugi.
This will be used by downstream data consumers like Bastion.
Additionally, this will organize the translations in a presentable format for eventual inclusion in
Yugipedia, which is currently lacking in Korean content.
Since this repository will become the central source of Korean translations, CDBs will be generated
by YAML Yugi, replacing manual management, as Git stores SQLite files poorly.

There will be at least two files hosting community translations here. These will be in CSV format
so they are text files that store well in Git and display well on GitHub, and easily import into
spreadsheet software. One file will contain translations for prereleases, mapped based on Yugipedia
page ID; the other will contain corrections for the official database, whether for the card text or
adding card name ruby text, mapped based on Konami ID. Rush Duel content may be kept in separate files
or the same files as the OCG, as there is no overlap in identifiers.

Pending any response from [Weblate](https://github.com/WeblateOrg/weblate/discussions/9616), we
could adopt this software to aid in collaborative translation while staying in sync with the repository.
I did not find an adequate two-way synchronization solution between GitHub and Google Sheets.

This repository could expand in the future to cover additional content, such as:
- updating old cards for modern effect syntax
- unofficial cards exclusive to the anime, manga, or video games
