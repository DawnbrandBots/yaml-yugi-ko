# SPDX-FileCopyrightText: © 2022 Kevin Lu
# SPDX-Licence-Identifier: AGPL-3.0-or-later
import os
import sqlite3
import sys

from ruamel.yaml import YAML


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <yaml_dir> <output.db3>")

    _, yaml_dir, output_file = sys.argv

    yaml = YAML()
    with sqlite3.connect(output_file) as db:
        cursor = db.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS card_text (
    konami_id INTEGER NOT NULL,
    card_name TEXT NOT NULL,
    card_text TEXT NOT NULL,
    pendulum TEXT
)""")
    for filename in os.listdir(yaml_dir):
        if filename.endswith(".yaml"):
            konami_id = os.path.splitext(filename)[0]
            filepath = os.path.join(yaml_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath) as file:
                    card = yaml.load(file)
                cursor.execute("INSERT INTO card_text VALUES (?, ?, ?, ?)",
                               (konami_id, card["name"], card["text"], card.get("pendulum")))
        db.commit()
