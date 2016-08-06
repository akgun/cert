#!/bin/bash
set -e

cmd=$1

case $cmd in
    build) exec pyinstaller --onefile main.spec ;;
    test) exec python3 -m unittest discover tests ;;
esac

exec "$@"
