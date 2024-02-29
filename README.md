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

### Usage of the translation files

**[`ocg-override.csv`](./ocg-override.csv)**

- OCG cards with outdated or incorrect Korean errata on the official database
- OCG cards that are missing Korean ruby text in their names on the official database

The pipeline will match cards based on `konami_id`. You may specify other identifiers for reference,
but they will be ignored. Once a card is matched, any of `name`, `text`, or `pendulum` that are not
blank will replace existing data from other sources.

`name` should have ruby text annotated using HTML markup, e.g. `<ruby>BF<rt>블랙 페더</rt></ruby>－극북의 블리자드`.
If a card is not a Pendulum Monster or has no Pendulum Effect, leave `pendulum` empty.
It will be ignored anyway.

**[`ocg-prerelease.csv`](./ocg-prerelease.csv)**

- OCG cards not yet released in Korea and thus not on the Korean official database yet

The pipeline will match cards based on `yugipedia_page_id`. You may specify other identifiers for
reference, but they will be ignored. If text from the Korean official database is found, the row
will be ignored, and may be automatically flagged for removal. The same guidelines for `name` and
`pendulum` apply.

**[`rush-override.csv`](./rush-override.csv)**

- Rush Duel cards with outdated or incorrect Korean errata on the official database
- Rush Duel cards that are missing Korean ruby text in their names on the official database

The pipeline will match cards based on `konami_id`. You may specify other identifiers for reference,
but they will be ignored.

The columns correspond to the [YAML Yugi schema for Rush Duel cards](https://github.com/DawnbrandBots/api-v8-definitions/blob/master/rush.ts).
If a column does not apply to the type of card, leave it blank, as it will be ignored anyway.

Required columns:
- All: `name` should have ruby text annotated using HTML markup like `ocg-override.csv`
- Spell/Trap: `requirement` and `effect`.
- Main Deck Effect Monster: `requirement` and `effect`. Do not specify the effect type in `effect`.
  Fill in `summoning_condition` if needed, e.g. Maximum Monsters, Cyber Dragon.
- Fusion Effect Monster: `materials`, `requirement`, and `effect`. Do not specify the effect type in `effect`.
- Non-Effect Monster: `non_effect_monster_text`. This means the flavour text for Normal Monsters and
  the `materials` for Fusion Non-Effect Monsters.

**[`rush-prerelease.csv`](./rush-prerelease.csv)**

- Rush Duel cards not yet released in Korea and thus not on the Korean official database yet

The pipeline will match cards based on `yugipedia_page_id`. You may specify other identifiers for
reference, but they will be ignored. If text from the Korean official database is found, the row
will be ignored, and may be automatically flagged for removal. The same guidelines for columns apply.
