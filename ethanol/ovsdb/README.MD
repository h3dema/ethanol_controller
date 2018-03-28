# Comments

There is a lot to be done in this module yet.
Only some functions are ok.

# Using this module


```python

from pox.ethanol.ovsdb.ovsdb import Ovsdb

ovs = Ovsdb()
if not ovs.connect():
    print "Cannot connect to database"
    sys.exit(0)

db_list = ovs.list_dbs()
db_name = db_list['result'][0]
```
