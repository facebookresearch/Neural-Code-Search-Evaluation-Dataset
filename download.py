#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""
Download the GitHub repositories specified in the download links file.

The downloading takes about 24 minutes to finish on a 24-core machine.
The downloaded files take up 7GB disk space in total.

Examples
--------
python3 download.py \
  --download_link_file data/android_repositories_download_links.txt \
  --project_path /tmp/projects/
"""

import argparse
import multiprocessing
import os
import urllib.error
import urllib.request
import zipfile

from tqdm import tqdm


def parallel_download(array, function, args=(), n_cores=None):
    if n_cores == 1:
        return [function(x, *args) for x in tqdm(array)]
    with tqdm(total=len(array)) as pbar:

        def update(*args):
            pbar.update()

        if n_cores is None:
            n_cores = multiprocessing.cpu_count()
        with multiprocessing.Pool(processes=n_cores) as pool:
            jobs = [
                pool.apply_async(function, (x, *args), callback=update) for x in array
            ]
            results = [job.get() for job in jobs]
        return results


def download_project(url, project_path):
    zip_url = url.strip()
    # get only username/projectname, replace / with @
    username_projectname = "/".join(zip_url.strip().split("/")[3:5])
    zipfile_name = username_projectname.replace("/", "@") + ".zip"
    zip_path = os.path.join(project_path, zipfile_name)
    try:
        urllib.request.urlretrieve(zip_url, zip_path)
    except urllib.error.URLError:
        return

    try:
        project_dir = os.path.join(project_path, username_projectname)
        with zipfile.ZipFile(zip_path, "r") as f:
            for file in f.infolist():
                if os.path.splitext(file.filename)[1] == ".java":
                    # copy to a new folder
                    dest_file = "/".join(file.filename.split("/")[1:])
                    dest_path = os.path.join(project_dir, dest_file)
                    dest_dir = "/".join(dest_path.split("/")[:-1])
                    # cannot use shutil here because we're copying bytes to non-bytes
                    content = f.read(file.filename)
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    with open(dest_path, "wb") as outfile:
                        outfile.write(content)
        os.remove(zip_path)
    except Exception:
        os.remove(zip_path)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--download_link_file",
        required=True,
        help="the path to the project download links file",
    )
    parser.add_argument(
        "--project_path",
        required=True,
        help="the directory to save the downloaded projects",
    )
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    if not os.path.exists(args.project_path):
        os.makedirs(args.project_path)
    with open(args.download_link_file, "r") as infile:
        urls = infile.readlines()

    # Download zip files and extract .java files
    parallel_download(urls, download_project, args=(args.project_path,))


if __name__ == "__main__":
    main()
