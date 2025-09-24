import json
import math
import os
from typing import List


def split_json_array(input_path: str, output_dir: str, records_per_file: int = 500) -> List[str]:
    """
    Split a large JSON array file into multiple smaller JSON files, each
    containing up to records_per_file entries. Returns the list of output paths.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "r") as f:
        data = json.load(f)

    total = len(data)
    num_files = math.ceil(total / records_per_file)
    output_paths: List[str] = []

    for i in range(num_files):
        start = i * records_per_file
        end = min(start + records_per_file, total)
        chunk = data[start:end]
        out_path = os.path.join(output_dir, f"counties_part_{i+1:04d}.json")
        with open(out_path, "w") as out_f:
            json.dump(chunk, out_f)
        output_paths.append(out_path)

    return output_paths


if __name__ == "__main__":
    INPUT = "Preprocessing/Raw_Data/us-county-boundaries.json"
    OUTPUT_DIR = "Preprocessing/Raw_Data/us-county-boundaries-chunks"
    split_json_array(INPUT, OUTPUT_DIR, records_per_file=500)


