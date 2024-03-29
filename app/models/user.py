from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            print(rows[0][1:])
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, balance)
VALUES(:email, :password, :firstname, :lastname, :balance)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname, balance = 0)
            id = rows[0][0]
            return User.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
    


    @staticmethod
    def updatebalance(id, amount):
        try:
            app.db.execute("""
UPDATE Users
SET balance = :amount + balance
WHERE id = :id
RETURNING balance
""",
                                  id = id,
                                  amount = amount)
            return True
        except Exception as e:
            # likely email already in use; better error checking and
            # reporting needed
            return None



    @staticmethod
    def update(id, email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
UPDATE Users
SET email = :email, password = :password, firstname = :firstname, lastname= :lastname
WHERE id = :id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname)
            return User.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None
