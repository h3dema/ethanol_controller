#!/bin/bash
PYCOMPILE=`which pycompile`
if [ -z "$PYCOMPILE" ]; then
    echo "Didn't find pycompile"
    exit 0
fi

DIRS=`echo */`

PYTHON_VERSION="2.7"

for d in $DIRS; do
    # echo "$PYCOMPILE -q -V \"$PYTHON_VERSION\" \"$d*.py\""
    $PYCOMPILE -q -V "$PYTHON_VERSION" "$d/*.py"
done