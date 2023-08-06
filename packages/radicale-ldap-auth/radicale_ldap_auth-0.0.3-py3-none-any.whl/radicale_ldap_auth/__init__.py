from radicale.auth import BaseAuth
from radicale.log import logger
import ldap

PLUGIN_CONFIG_SCHEMA = {
    "auth": {
    "ldap_url": {"value": "", "type": str},
    "ldap_port": {"value": "", "type": str},
    "ldap_user_postfix": {"value": "", "type": str}
        }
    }


class Auth(BaseAuth):
    def __init__(self, configuration):
        super().__init__(configuration.copy(PLUGIN_CONFIG_SCHEMA))

    def login(self, user, password):
        url = self.configuration.get("auth", "ldap_url")
        port = self.configuration.get("auth", "ldap_port")

        ldap_url = f'{url}:{port}'
        l = ldap.initialize(ldap_url)
        l.set_option(ldap.OPT_REFERRALS, 0)
        try:
            l.simple_bind_s(user, password)
        except ldap.INVALID_CREDENTIALS as error:
            logger.error(error)
            return ""
        except ldap.SERVER_DOWN:
            logger.error(f'LDAP SERVER_DOWN: {ldap_url}')
            return ""
        except ldap.LDAPError as error:
            if type(error.message) == dict and error.message.has_key('desc'):
                logger.error(f"Other LDAP error: {error.message['desc']}")
                return ""
            else:
                logger.error(f"Other LDAP error: {error}")
        finally:
            logger.info(f"LDAP login : {user}")
            l.unbind_s()
        return user.split('@')[0]

