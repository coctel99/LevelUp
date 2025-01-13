from app import app, db
from app.models import User, Area, Skill, UserSkills

def create_db():
    with app.app_context():
        db.create_all()  # Creates all the tables defined in the models
        print("Database and tables created successfully!")

if __name__ == "__main__":
    create_db()
