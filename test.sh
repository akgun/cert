#!/bin/bash
set -x

nose2 -v --with-coverage --coverage cert --coverage-report html --coverage-report xml

set +e
pylint cert -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt
set -e
