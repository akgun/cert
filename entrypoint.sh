#!/bin/bash
set -e

cmd=$1

case $cmd in
    build)
        rm -rf build/ dist/
        exec pyinstaller --onefile main.spec
    ;;
    test)
        exec nosetests \
                --with-coverage \
                    --cover-erase --cover-package cert --cover-html --cover-html-dir=build/coverage
    ;;
esac

exec "$@"
