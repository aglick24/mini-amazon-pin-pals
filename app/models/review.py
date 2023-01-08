from flask import current_app as app


class Review:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.rating = rating
        self.review = Review
        self.date_time = date_time

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT uid, pid, rating, review, date_time
FROM Reviews
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT id, pid, rating, review, date_time
FROM Reviews
WHERE uid = :uid
ORDER BY date_time DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]
