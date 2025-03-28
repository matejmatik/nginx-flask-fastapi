from bcrypt import hashpw
from flask_login import UserMixin

"""
import bcrypt

# Defining the password (must be bytes!)
password = b'GeekPassword'

# Adding the salt to password
salt = bcrypt.gensalt()

# Hashing the password
hashed = bcrypt.hashpw(password, salt)

"""

AUTHENTICATED_USER_LIST = {
    "matej.pirnat@bisol-energija.si": {
        "id": 1,
        "email": "matej.pirnat@bisol-energija.si",
        "password": b"$2b$12$6R0XSowfJZDRmsEHtEW0XOOS0GMa6ZkLWDuBmlv6KlwcMvwqVI1Wa",
        "name": "Matej Pirnat",
        "is_admin": True,
        "is_active": True,
    },
    "ziga.meznar@bisol-energija.si": {
        "id": 2,
        "email": "ziga.meznar@bisol-energija.si",
        "password": b"$2b$12$6R0XSowfJZDRmsEHtEW0XOozkEdUM6SGKDKtStKjUFA06FKtxQxmm",
        "name": "Žiga Mežnar",
        "is_admin": True,
        "is_active": True,
    },
    "marko.haluzan@bisol-energija.si": {
        "id": 3,
        "email": "marko.haluzan@bisol-energija.si",
        "password": b"$2b$12$6R0XSowfJZDRmsEHtEW0XOo1gJOF.7zLlBq9SYql2GJoRxu.CuMSK",
        "name": "Marko Halužan",
        "is_admin": True,
        "is_active": True,
    },
    "matej.mencin@bisol-energija.si": {
        "id": 4,
        "email": "matej.mencin@bisol-energija.si",
        "password": b"$2b$12$FwvM0KnG2mNMvPiFR5hTNeZmDXZZH71oMOHV4htvj.XI4d1zKtT2y",
        "name": "Matej Mencin",
        "is_admin": True,
        "is_active": True,
    },
    "sara.rajacic@bisol-energija.si": {
        "id": 5,
        "email": "sara.rajacic@bisol-energija.si",
        "password": b"$2b$12$wmnvwQLxqv4wVCCy3jp4w.yqSW3IRW/Mur9MkIkOG7OIaWWmGimFa",
        "name": "Sara Rajačič",
        "is_admin": True,
        "is_active": True,
    },
    "alojz.meznar@bisol-energija.si": {
        "id": 6,
        "email": "alojz.meznar@bisol-energija.si",
        "password": b"$2b$12$oHtSYP3UwDh.muyjiS.fDOxNuN7a6kTVHaz6Ouh4g2OT7VD/4DY2a",
        "name": "Alojz Mežnar",
        "is_admin": True,
        "is_active": True,
    },
    "vito.zaloznik@bisol-energija.si": {
        "id": 7,
        "email": "vito.zaloznik@bisol-energija.si",
        "password": b"$2b$12$oHtSYP3UwDh.muyjiS.fDO.Mivx5VH2lPM0T.PM8LGYioVydPPY5y",
        "name": "Vito Založnik",
        "is_admin": True,
        "is_active": True,
    },
    "luka.grum@bisol-energija.si": {
        "id": 8,
        "email": "luka.grum@bisol-energija.si",
        "password": b"$2b$12$MqOU4RT6OUbiFA9LATGtUuAs4Wc.eZzcBTU/Amb8TcrTB01IJXyqm",
        "name": "Luka Grum",
        "is_admin": True,
        "is_active": True,
    },
}


class User(UserMixin):
    _id = None
    email = None
    password = None
    name = None
    is_admin = None
    is_active = None
    is_anonymous = None
    is_authenticated = None

    def __init__(
        self,
        _id=None,
        email=None,
        password=None,
        name=None,
        is_admin=None,
        is_active=None,
    ):
        self._id = _id
        self.email = email
        self.password = password
        self.name = name
        self.is_admin = is_admin
        self.is_active = is_active
        self.is_anonymous = False
        self.is_authenticated = True

    def query_users(self, email):
        for user in AUTHENTICATED_USER_LIST.values():
            if user["email"] == email:
                return User(
                    _id=user["id"],
                    email=user["email"],
                    password=user["password"],
                    name=user["name"],
                    is_admin=user["is_admin"],
                    is_active=user["is_active"],
                )
        return None

    def get_id(self):
        return self.email

    def __repr__(self):
        return f"<User {self.email}>"


def validate_user_password(user: User, password: str) -> bool:
    return hashpw(password.encode("utf-8"), user.password) == user.password
