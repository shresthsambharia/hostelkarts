from database import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    notificationId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    sentAt = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def sendNotification(user_id, notif_type, message):
        n = Notification(userId=user_id, type=notif_type, message=message)
        db.session.add(n)
        db.session.commit()
        return n
