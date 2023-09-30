import cantools
from candb import CANDBC

candb = CANDBC('./sample.dbc')

candb.show_messages()
candb.show_signals()
candb.show_receivers()
candb.show_ecus()
candb.show_counts()
candb.dump_signals()
