s/^Listen 443/Listen 0.0.0.0:8443/
s/_default_:443/_default_:8443/
s!^(\s*CustomLog)\s+\S+!\1 |/usr/bin/cat!
s!^(\s*TransferLog)\s+\S+!\1 |/usr/bin/cat!
s!^(\s*ErrorLog)\s+\S+!\1 |/usr/bin/cat!
