# SPDX-FileCopyrightText: © 2022–2023 Kevin Lu
# SPDX-Licence-Identifier: AGPL-3.0-or-later
from csv import DictWriter
import os
import sys

from ruamel.yaml import YAML


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <yaml_dir> <output.csv> [--with-pendulum]")

    _, yaml_dir, output_file, with_pendulum = sys.argv

    yaml = YAML()
    columns = ["konami_id", "name", "text"]
    if with_pendulum:
        columns += ["pendulum"]
    with open(output_file, "w") as csv_file:
        writer = DictWriter(csv_file, columns)
        writer.writeheader()
        for filename in os.listdir(yaml_dir):
            if filename.endswith(".yaml"):
                konami_id = int(os.path.splitext(filename)[0])
                filepath = os.path.join(yaml_dir, filename)
                if os.path.isfile(filepath):
                    with open(filepath) as file:
                        card = yaml.load(file)
                    writer.writerow({"konami_id": konami_id, **card})
