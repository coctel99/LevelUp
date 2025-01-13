import requests
import json

# Base URL for the Flask app
BASE_URL = 'http://127.0.0.1:5000'

# 1. Create a new user
def create_user(username):
    url = f'{BASE_URL}/user'
    response = requests.post(url, json={'username': username})
    print(f"Create User Response: {response.status_code}")
    print(response.json())

# 2. Create a new area
def create_area(name, description):
    url = f'{BASE_URL}/area'
    response = requests.post(url, json={'name': name, 'description': description})
    print(f"Create Area Response: {response.status_code}")
    print(response.json())

# 3. Create a new skill for an area
def create_skill(name, description, area_id):
    url = f'{BASE_URL}/skill'
    response = requests.post(url, json={'name': name, 'description': description, 'area_id': area_id})
    print(f"Create Skill Response: {response.status_code}")
    print(response.json())

# 4. Assign XP to a user’s skill
def assign_user_skill(user_id, skill_id):
    url = f'{BASE_URL}/user_skill'
    response = requests.post(url, json={'user_id': user_id, 'skill_id': skill_id})
    print(f"Assign Skill to User Response: {response.status_code}")
    print(response.json())

# 5. Get all skills for a user across all areas
def get_user_skills(user_id):
    url = f'{BASE_URL}/user/{user_id}/skills'
    response = requests.get(url)
    print(f"Get User Skills Response: {response.status_code}")
    print(response.json())

# 6. Get user skills in a specific area
def get_user_skills_by_area(user_id, area_id):
    url = f'{BASE_URL}/user/{user_id}/skills/area/{area_id}'
    response = requests.get(url)
    print(f"Get User Skills by Area Response: {response.status_code}")
    print(response.json())

# Test the endpoints
if __name__ == "__main__":
    # Step 1: Create a new user
    create_user("player1")

    # Step 2: Create areas (e.g., Physical Health)
    create_area("Physical Health", "Developing strength, stamina, and fitness.")

    # Step 3: Create skills under Physical Health
    create_skill("Strength", "Build muscle and physical strength.", area_id=1)
    create_skill("Stamina", "Increase endurance and energy.", area_id=1)

    # Step 4: Assign skills and XP to user
    assign_user_skill(user_id=1, skill_id=1)  # Assign Strength to user
    assign_user_skill(user_id=1, skill_id=2)  # Assign Stamina to user

    # Step 5: Get all skills for user
    get_user_skills(user_id=1)

    # Step 6: Get user skills in a specific area (e.g., Physical Health)
    get_user_skills_by_area(user_id=1, area_id=1)
