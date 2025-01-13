from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    user_skills = db.relationship('UserSkills', backref='owner', lazy=True)  # Changed to 'owner'

    def __repr__(self):
        return f"<User {self.username}>"

class UserSkills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    xp = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<UserSkill {self.user_id}-{self.skill_id}>"


class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    xp_reward = db.Column(db.Integer, default=10)

    def __repr__(self):
        return f"<Quest {self.title}>"

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    skills = db.relationship('Skill', backref='area', lazy=True)

    def __repr__(self):
        return f"<Area {self.name}>"


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Skill {self.name}>"
