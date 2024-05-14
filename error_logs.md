### About

Recorded list of errors obtained in the process of developing this application.
Might be useful documentation for people looking to implement this app in their local
build.

- `ServerSelectionTimeoutError ... [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1006)`

**Error found in the following code**:
```Python
client = MongoClient(uri)
```

**Solution**:
```Python
client = MongoClient(uri, tlsCAFile=certifi.where())
```

When connecting to the DB, pymongo defaultly relies on the OS's root certificates. Certification verification
fails because OpenSSL does not have access to the root certificates / the certificates are out of date.

Source: [Link](https://www.mongodb.com/community/forums/t/serverselectiontimeouterror-ssl-certificate-verify-failed-trying-to-understand-the-origin-of-the-problem/115288)