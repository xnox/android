#! /usr/bin/python3
import apt_pkg
import apt
import aptsources.sourceslist
import os
import tempfile

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', type=str, nargs='*')
    parser.add_argument('--src', type=str, nargs='*')
    parser.add_argument('--bin', type=str, nargs='*')
    args = parser.parse_args()

    apt_pkg.init_config()
    apt_pkg.init_system()
    apt_pkg.config.set("Dir", os.getcwd())

    if len(args.init):
        sources = aptsources.sourceslist.SourcesList()
        sources.add("deb", args.init[0], args.init[1], ["main", "restricted", "universe", "multiverse"], architectures=['armhf'])
        sources.add("deb-src", args.init[0], args.init[1], ["main", "restricted", "universe", "multiverse"])
        sources.save()
        cache = apt.Cache(rootdir=os.getcwd())
        cache.update()

    cache = apt.Cache(rootdir=os.getcwd())
    for package in args.bin:
        for dep in cache[package].candidate.dependencies[0]:
            if dep.name.startswith('linux-image'):
                cache[dep.name].candidate.fetch_binary()

    for package in args.src:
        cache[package].candidate.fetch_source()
                
if __name__ == '__main__':
    main()

