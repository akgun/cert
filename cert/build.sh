#!/bin/bash
set -e

. ./venv/bin/activate
pyinstaller --onefile main.spec
