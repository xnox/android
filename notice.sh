#!/bin/sh

notice_one () {
    BASE=$(dirname $1)
    NOTICE=${BASE}/NOTICE
    echo
    echo "Files: ${BASE}"
    grep Copyright ${NOTICE} | head -n1 | sed 's/^/Copyright: /'
    echo "License:"
    sed 's/^/ /;s/\(^\s*$\)/ ./' ${NOTICE}
}

if [ -n "$1" ]; then
    notice_one "$1"
else
    for project in $(find . -name 'NOTICE'); do
	notice_one "$project"
    done
fi
