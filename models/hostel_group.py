from database import db

student_groups = db.Table('student_groups',
    db.Column('student_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('hostel_groups.groupId'), primary_key=True)
)

class HostelGroup(db.Model):
    __tablename__ = 'hostel_groups'
    groupId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    
    students = db.relationship('Student', secondary=student_groups, backref=db.backref('groups', lazy='dynamic'))