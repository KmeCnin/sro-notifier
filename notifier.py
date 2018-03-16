from bs4 import BeautifulSoup
from bs4.diagnose import diagnose

from src import config
from src import manager
from src import padlock
from src import update_kills
from src import update_chars

padlock.lock()
try:
    update_kills.update()
    update_chars.update()
finally:
    padlock.unlock()