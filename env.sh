# activate or create virtualenv project
VERSION=$1

if [[ -z "$VIRTUAL_ENV" ]]; then
    source /usr/local/bin/virtualenvwrapper.sh
fi

if [[ -z "$1" ]]; then
    VERSION=3
fi

# default env vars
ENV_NAME="rinasystems-$VERSION"
PYTHON_BIN="/usr/bin/python$VERSION"

if [ -n "$(lsvirtualenv | grep $ENV_NAME)" ]; then
    workon $ENV_NAME
else
    mkvirtualenv $ENV_NAME -p $PYTHON_BIN
    pip install -r requirements.txt
fi
