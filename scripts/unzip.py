#!/usr/bin/env python3

import argparse
import zipfile
import os
import sys
from os.path import dirname, abspath

def unzip_file(zip_path: str):
    """
    Unzips a specified ZIP file to a target directory.

    Args:
        zip_path (str): The path to the input ZIP file.
        extract_dir (str): The directory where the contents will be extracted.
    """
    if not os.path.exists(zip_path):
        print(f"Error: Input file not found at '{zip_path}'")
        sys.exit(1)
    
    parent_dir = dirname(dirname(abspath(__file__)))
    print(f"Starting extraction of '{zip_path}'...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(parent_dir)
    
    print(f"Successfully unzipped '{zip_path}'")


def main():
    """
    Main function to parse arguments and call the unzip utility.
    """
    parser = argparse.ArgumentParser(
        description="A Python script to unzip a file with an optional custom name.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        default='data.zip',
        help="Path to the input ZIP file to be unzipped.\n(Default: data.zip)"
    )

    args = parser.parse_args()
    unzip_file(args.input)

if __name__ == "__main__":
    main()
