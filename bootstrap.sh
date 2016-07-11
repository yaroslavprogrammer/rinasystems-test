# os deps
sudo apt-get install redis-server python-pip python-dev
sudo pip install virtualenvwrapper

# python deps
source env.sh
pip install -r requirements.txt
python -m nltk.downloader punkt

# project deps
mkdir -p taskcelery/db

# wget file
# ungzip it
