
class SecretKey():
    SECRET_KEY="JOQUERJ@J@"

class ConfigExternalObject(SecretKey):
    DEBUG=True
    MYSQL_HOST='192.168.1.200'
    MYSQL_USER='remoteuser'
    MYSQL_PASSWORD='1234'
    MYSQL_DB='Packed_company'

externalobject={
    "Config":ConfigExternalObject()
}
