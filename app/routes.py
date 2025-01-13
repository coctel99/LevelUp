from flask import request, jsonify
from app import app, db
from app.models import User, Quest, UserSkills, Skill, Area


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"User {username} created!"}), 201


@app.route('/user/<int:user_id>', methods=['GET', 'PUT'])
def get_update_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return jsonify({
            "id": user.id,
            "username": user.username,
            "level": user.level,
            "xp": user.xp
        })
    elif request.method == 'PUT':
        data = request.get_json()
        user.xp += data.get('xp', 0)
        user.level = user.xp // 100 + 1  # Level up every 100 XP
        db.session.commit()
        return jsonify({
            "message": "User updated",
            "xp": user.xp,
            "level": user.level
        })


@app.route('/area', methods=['POST'])
def create_area():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Area name is required"}), 400

    area = Area(name=name, description=description)
    db.session.add(area)
    db.session.commit()
    return jsonify({"message": f"Area {name} created!"}), 201


@app.route('/skill', methods=['POST'])
def create_skill():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    area_id = data.get('area_id')

    if not name or not area_id:
        return jsonify({"error": "Skill name and area ID are required"}), 400

    skill = Skill(name=name, description=description, area_id=area_id)
    db.session.add(skill)
    db.session.commit()
    return jsonify({"message": f"Skill {name} created!"}), 201


@app.route('/user_skill', methods=['POST'])
def assign_user_skill():
    data = request.get_json()
    user_id = data.get('user_id')
    skill_id = data.get('skill_id')

    user_skill = UserSkills.query.filter_by(user_id=user_id, skill_id=skill_id).first()
    if not user_skill:
        user_skill = UserSkills(user_id=user_id, skill_id=skill_id)

    user_skill.xp += 10  # Example XP gain
    if user_skill.xp >= 100:
        user_skill.level += 1
        user_skill.xp = 0  # Reset XP after level-up

    db.session.add(user_skill)
    db.session.commit()
    return jsonify({"message": f"User skill updated: {user_skill.skill.name} level {user_skill.level}"}), 200


@app.route('/user/<int:user_id>/skills', methods=['GET'])
def get_user_skills(user_id):
    user = User.query.get_or_404(user_id)

    # Retrieve all user skills with related skill names and areas
    user_skills = UserSkills.query.filter_by(user_id=user_id).join(Skill).join(Area).all()

    skills_data = []
    for user_skill in user_skills:
        skill_info = {
            "skill_name": user_skill.skill.name,
            "area_name": user_skill.skill.area.name,
            "level": user_skill.level,
            "xp": user_skill.xp
        }
        skills_data.append(skill_info)

    return jsonify({
        "user_id": user_id,
        "skills": skills_data
    })


@app.route('/user/<int:user_id>/skills/area/<int:area_id>', methods=['GET'])
def get_user_skills_by_area(user_id, area_id):
    user = User.query.get_or_404(user_id)
    area = Area.query.get_or_404(area_id)

    # Retrieve all user skills within the given area
    user_skills = UserSkills.query.filter_by(user_id=user_id).join(Skill).filter(Skill.area_id == area_id).all()

    skills_data = []
    for user_skill in user_skills:
        skill_info = {
            "skill_name": user_skill.skill.name,
            "level": user_skill.level,
            "xp": user_skill.xp
        }
        skills_data.append(skill_info)

    return jsonify({
        "user_id": user_id,
        "area": area.name,
        "skills": skills_data
    })



@app.route('/quest', methods=['POST'])
def create_quest():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    xp_reward = data.get('xp_reward', 10)

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    quest = Quest(title=title, description=description, xp_reward=xp_reward)
    db.session.add(quest)
    db.session.commit()
    return jsonify({"message": f"Quest {title} created!"}), 201


@app.route('/quest/<int:quest_id>', methods=['GET'])
def get_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    return jsonify({
        "id": quest.id,
        "title": quest.title,
        "description": quest.description,
        "xp_reward": quest.xp_reward
    })

