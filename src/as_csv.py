# SPDX-FileCopyrightText: © 2022 Kevin Lu
# SPDX-Licence-Identifier: AGPL-3.0-or-later
from csv import DictWriter
import os
import sys

from ruamel.yaml import YAML


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <yaml_dir> <output.csv>")

    _, yaml_dir, output_file = sys.argv

    yaml = YAML()
    with open(output_file, "w") as csv_file:
        writer = DictWriter(csv_file, ["konami_id", "name", "text", "pendulum"])
        for filename in os.listdir(yaml_dir):
            if filename.endswith(".yaml"):
                konami_id = int(os.path.splitext(filename)[0])
                filepath = os.path.join(yaml_dir, filename)
                if os.path.isfile(filepath):
                    with open(filepath) as file:
                        card = yaml.load(file)
                    writer.writerow({"konami_id": konami_id, **card})
