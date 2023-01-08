from flask import current_app as app

class Cart:
    def __init__(self, id, uid, pid, quantity, time_added):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.time_added = time_added

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, quantity
FROM Carts
WHERE id = :id
''',
                              id=id)
        return Cart(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, quantity
FROM Carts
WHERE uid = :uid
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def add_product(uid, pid, quantity):
        try:
            rows = app.db.execute("""
        INSERT INTO Carts(uid, pid, quantity)
        VALUES(:uid, :pid, :quantity, :time_added)
        RETURNING id
        """,
                                  uid=uid,
                                  pid=pid,
                                  quantity=quantity,
                                  time_added=time_added)
            id = rows[0][0]
            return Cart.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None