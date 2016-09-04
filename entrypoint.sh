#!/bin/bash
set -e

cmd=$1

case $cmd in
    build)
        rm -rf build/ dist/
        exec pyinstaller --onefile main.spec
    ;;
esac

exec "$@"
