from fastapi import FastAPI, HTTPException, Depends, status, Response, File, UploadFile, Form, Request
from pydantic import BaseModel
from typing import Optional
import re
from fastapi.staticfiles import StaticFiles
from typing import List
from models import User, Module, Lesson, Exercise, Quiz, QuizQuestion, QuizAttemptQuestion, QuizAttemptRequest, QuizAttemptResponse
from database import db_manager
import logging
from fastapi.middleware.cors import CORSMiddleware
import json
import hashlib
import secrets
from pydantic import BaseModel
import matplotlib
import os
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
import io
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

app = FastAPI()

# --- Import et inclusion des routers ---
from matrix_router import router as matrix_router
from routes.calendar_routes import router as calendar_router
from routes.dashboard_routes import router as dashboard_router

app.include_router(matrix_router)
app.include_router(calendar_router)
app.include_router(dashboard_router)

# Mount static files directory for videos
app.mount("/media", StaticFiles(directory="media"), name="media")

# Enable CORS for frontend domainet ycommuniquiou /accepter les rrequetttes https
# List of allowed origins (update with your frontend URL in production)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://192.168.1.16:8080",
    "http://192.168.1.16:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Authorization"],
    max_age=600,  # cache preflight request for 10 minutes
)

db_manager.create_tables()

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        salt, hash_value = hashed_password.split('$')
        hash_obj = hashlib.sha256((password + salt).encode())
        return hash_obj.hexdigest() == hash_value
    except:
        return False

@app.on_event("shutdown")
def shutdown_event():
    db_manager.close()

@app.post("/users", response_model=User)
def create_user(user: User):
    try:
        # Check if user already exists
        check_query = "SELECT * FROM utilisateur WHERE email = ?"
        existing_user = db_manager.execute_query(check_query, (user.email,))
        if existing_user:
            raise HTTPException(status_code=400, detail="Un utilisateur avec cet email existe déjà")
        
        # Hash the password
        if not user.password:
            raise HTTPException(status_code=400, detail="Password is required")
        hashed_password = hash_password(user.password)
        
        query = """
            INSERT INTO utilisateur (nom, email, mot_de_passe, role)
            VALUES (?, ?, ?, ?)
        """
        db_manager.execute_query(query, (user.name, user.email, hashed_password, user.role))
        # Fetch the created user
        get_query = "SELECT * FROM utilisateur WHERE email = ?"
        result = db_manager.execute_query(get_query, (user.email,))
        if result:
            row = result[0]
            return User(id=row['id_utilisateur'], name=row['nom'], email=row['email'], role=row['role'])
        else:
            raise HTTPException(status_code=500, detail="User creation failed")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail=str(e))

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/login")
def login_user(login_data: LoginRequest):
    try:
        # First check if user exists, regardless of active status
        query = "SELECT * FROM utilisateur WHERE email = ?"
        result = db_manager.execute_query(query, (login_data.email,))
        
        if not result:
            raise HTTPException(status_code=401, detail="Aucun compte trouvé avec cet email")
        
        user = result[0]
        
        # Check if user is active
        if user.get('actif') != 1:
            # If user exists but is inactive, activate them
            activate_query = "UPDATE utilisateur SET actif = 1 WHERE id_utilisateur = ?"
            db_manager.execute_query(activate_query, (user['id_utilisateur'],))
            
        # Verify password
        if not verify_password(login_data.password, user['mot_de_passe']):
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")
        
        # Update last login
        update_query = "UPDATE utilisateur SET derniere_connexion = CURRENT_TIMESTAMP WHERE id_utilisateur = ?"
        db_manager.execute_query(update_query, (user['id_utilisateur'],))
        
        return User(id=user['id_utilisateur'], name=user['nom'], email=user['email'], role=user['role'])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la connexion")

@app.get("/users", response_model=List[User])
def get_users():
    query = "SELECT * FROM utilisateur WHERE actif = 1"
    result = db_manager.execute_query(query)
    return [User(id=row['id_utilisateur'], name=row['nom'], email=row['email'], role=row['role']) for row in result]

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    query = "SELECT * FROM utilisateur WHERE id_utilisateur = ? AND actif = 1"
    result = db_manager.execute_query(query, (user_id,))
    if result:
        row = result[0]
        return User(id=row['id_utilisateur'], name=row['nom'], email=row['email'], role=row['role'])
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    query = "UPDATE utilisateur SET nom = ?, email = ?, role = ? WHERE id_utilisateur = ?"
    db_manager.execute_query(query, (user.name, user.email, user.role, user_id))
    # Fetch updated user
    get_query = "SELECT * FROM utilisateur WHERE id_utilisateur = ?"
    result = db_manager.execute_query(get_query, (user_id,))
    if result:
        row = result[0]
        return User(id=row['id_utilisateur'], name=row['nom'], email=row['email'], role=row['role'])
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    query = "UPDATE utilisateur SET actif = 0 WHERE id_utilisateur = ?"
    db_manager.execute_query(query, (user_id,))
    return {"message": "User deleted"}

# --- Module CRUD ---
@app.post("/modules", response_model=Module)
def create_module(module: Module):
    query = """
        INSERT INTO module (titre, type, description, contenu, id_enseignant, categorie, niveau, duree, objectifs)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    db_manager.execute_query(query, (module.titre, module.type, module.description, module.contenu, module.id_enseignant, json.dumps(module.categorie), module.niveau, module.duree, json.dumps(module.objectifs)))
    get_query = "SELECT * FROM module WHERE titre = ? AND id_enseignant = ? ORDER BY id_module DESC LIMIT 1"
    result = db_manager.execute_query(get_query, (module.titre, module.id_enseignant))
    if result:
        row = result[0]
        return Module(id=row['id_module'], titre=row['titre'], type=row['type'], description=row['description'], contenu=row['contenu'], id_enseignant=row['id_enseignant'], categorie=json.loads(row['categorie']), niveau=row['niveau'], duree=row['duree'], objectifs=json.loads(row['objectifs']))
    else:
        raise HTTPException(status_code=500, detail="Module creation failed")

def parse_module_row(row):
    """Helper function to parse a module row with proper null handling"""
    # Handle categorie as string (don't parse JSON)
    categorie = row.get('categorie')
    if categorie and isinstance(categorie, str) and categorie.startswith('['):
        try:
            categorie = json.loads(categorie)
            # Convert list to string if it's a list
            if isinstance(categorie, list):
                categorie = ', '.join(str(item) for item in categorie)
        except json.JSONDecodeError:
            pass  # Keep as is if not valid JSON
    
    # Handle objectifs as string (don't parse JSON)
    objectifs = row.get('objectifs')
    if objectifs and isinstance(objectifs, str) and objectifs.startswith('['):
        try:
            objectifs = json.loads(objectifs)
            # Ensure it's a list of strings
            if isinstance(objectifs, list):
                objectifs = [str(item) for item in objectifs]
            else:
                objectifs = [str(objectifs)]
        except json.JSONDecodeError:
            objectifs = [objectifs] if objectifs else []
    
    return Module(
        id=row['id_module'],
        titre=row['titre'],
        type=row['type'],
        description=row['description'],
        contenu=row['contenu'],
        id_enseignant=row['id_enseignant'],
        categorie=categorie if categorie is not None else "",
        niveau=row['niveau'],
        duree=row['duree'],
        objectifs=objectifs if objectifs is not None else []
    )

@app.get("/modules", response_model=List[dict])
def get_modules():
    query = """
    SELECT m.*, u.nom as enseignant_nom
    FROM module m
    LEFT JOIN utilisateur u ON m.id_enseignant = u.id_utilisateur
    WHERE m.actif = 1
    """
    result = db_manager.execute_query(query)
    modules = []
    for row in result:
        module = parse_module_row(row)
        module_dict = module.dict()
        module_dict['enseignant_nom'] = row.get('enseignant_nom')
        modules.append(module_dict)
    return modules

@app.get("/modules/{module_id}", response_model=Module)
def get_module(module_id: int):
    query = "SELECT * FROM module WHERE id_module = ? AND actif = 1"
    result = db_manager.execute_query(query, (module_id,))
    if result:
        return parse_module_row(result[0])
    else:
        raise HTTPException(status_code=404, detail="Module not found")

@app.put("/modules/{module_id}", response_model=Module)
def update_module(module_id: int, module: Module):
    query = "UPDATE module SET titre = ?, type = ?, description = ?, contenu = ?, id_enseignant = ?, categorie = ?, niveau = ?, duree = ?, objectifs = ? WHERE id_module = ?"
    db_manager.execute_query(query, (module.titre, module.type, module.description, module.contenu, module.id_enseignant, json.dumps(module.categorie), module.niveau, module.duree, json.dumps(module.objectifs), module_id))
    get_query = "SELECT * FROM module WHERE id_module = ?"
    result = db_manager.execute_query(get_query, (module_id,))
    if result:
        row = result[0]
        return Module(id=row['id_module'], titre=row['titre'], type=row['type'], description=row['description'], contenu=row['contenu'], id_enseignant=row['id_enseignant'], categorie=json.loads(row['categorie']), niveau=row['niveau'], duree=row['duree'], objectifs=json.loads(row['objectifs']))
    else:
        raise HTTPException(status_code=404, detail="Module not found")

@app.delete("/modules/{module_id}")
def delete_module(module_id: int):
    query = "UPDATE module SET actif = 0 WHERE id_module = ?"
    db_manager.execute_query(query, (module_id,))
    return {"message": "Module deleted"}

# --- Lesson CRUD ---
@app.post("/lessons", response_model=Lesson)
def create_lesson(lesson: Lesson):
    query = """
        INSERT INTO lecon (titre, description, duree, niveau, contenu, id_module, id_enseignant, ordre)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    db_manager.execute_query(query, (lesson.titre, lesson.description, lesson.duree, lesson.niveau, lesson.contenu, lesson.id_module, lesson.id_enseignant, lesson.ordre))
    get_query = "SELECT * FROM lecon WHERE titre = ? AND id_module = ? AND id_enseignant = ? ORDER BY id_lecon DESC LIMIT 1"
    result = db_manager.execute_query(get_query, (lesson.titre, lesson.id_module, lesson.id_enseignant))
    if result:
        row = result[0]
        return Lesson(id=row['id_lecon'], titre=row['titre'], description=row['description'], duree=row['duree'], niveau=row['niveau'], contenu=row['contenu'], id_module=row['id_module'], id_enseignant=row['id_enseignant'], ordre=row['ordre'])
    else:
        raise HTTPException(status_code=500, detail="Lesson creation failed")

@app.get("/lessons", response_model=List[Lesson])
def get_lessons():
    query = "SELECT * FROM lecon WHERE actif = 1"
    result = db_manager.execute_query(query)
    return [Lesson(id=row['id_lecon'], titre=row['titre'], description=row['description'], duree=row['duree'], niveau=row['niveau'], contenu=row['contenu'], id_module=row['id_module'], id_enseignant=row['id_enseignant'], ordre=row['ordre']) for row in result]

@app.get("/lessons/{lesson_id}", response_model=Lesson)
def get_lesson(lesson_id: int):
    query = "SELECT * FROM lecon WHERE id_lecon = ? AND actif = 1"
    result = db_manager.execute_query(query, (lesson_id,))
    if result:
        row = result[0]
        return Lesson(id=row['id_lecon'], titre=row['titre'], description=row['description'], duree=row['duree'], niveau=row['niveau'], contenu=row['contenu'], id_module=row['id_module'], id_enseignant=row['id_enseignant'], ordre=row['ordre'])
    else:
        raise HTTPException(status_code=404, detail="Lesson not found")

@app.put("/lessons/{lesson_id}", response_model=Lesson)
def update_lesson(lesson_id: int, lesson: Lesson):
    query = "UPDATE lecon SET titre = ?, description = ?, duree = ?, niveau = ?, contenu = ?, id_module = ?, id_enseignant = ?, ordre = ? WHERE id_lecon = ?"
    db_manager.execute_query(query, (lesson.titre, lesson.description, lesson.duree, lesson.niveau, lesson.contenu, lesson.id_module, lesson.id_enseignant, lesson.ordre, lesson_id))
    get_query = "SELECT * FROM lecon WHERE id_lecon = ?"
    result = db_manager.execute_query(get_query, (lesson_id,))
    if result:
        row = result[0]
        return Lesson(id=row['id_lecon'], titre=row['titre'], description=row['description'], duree=row['duree'], niveau=row['niveau'], contenu=row['contenu'], id_module=row['id_module'], id_enseignant=row['id_enseignant'], ordre=row['ordre'])
    else:
        raise HTTPException(status_code=404, detail="Lesson not found")

@app.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int):
    query = "UPDATE lecon SET actif = 0 WHERE id_lecon = ?"
    db_manager.execute_query(query, (lesson_id,))
    return {"message": "Lesson deleted"}

@app.get("/lessons/module/{module_id}", response_model=List[Lesson])
def get_lessons_by_module(module_id: int):
    query = "SELECT * FROM lecon WHERE id_module = ? AND actif = 1"
    result = db_manager.execute_query(query, (module_id,))
    return [Lesson(
        id=row['id_lecon'],
        titre=row['titre'],
        description=row['description'],
        duree=row['duree'],
        niveau=row['niveau'],
        contenu=row['contenu'],
        id_module=row['id_module'],
        id_enseignant=row['id_enseignant'],
        ordre=row['ordre']
    ) for row in result]

# --- Exercise CRUD ---
@app.post("/exercises", response_model=Exercise)
def create_exercise(exercise: Exercise):
    query = """
        INSERT INTO exercice (question, solution, feedback, points, id_module, id_lecon, id_enseignant, tp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    db_manager.execute_query(query, (
        exercise.question, exercise.solution, exercise.feedback, exercise.points,
        exercise.id_module, exercise.id_lecon, exercise.id_enseignant, exercise.tp
    ))
    get_query = "SELECT * FROM exercice WHERE question = ? AND id_enseignant = ? ORDER BY id_exercice DESC LIMIT 1"
    result = db_manager.execute_query(get_query, (exercise.question, exercise.id_enseignant))
    if result:
        row = result[0]
        return Exercise(
            id=row['id_exercice'], question=row['question'], solution=row['solution'],
            feedback=row['feedback'], points=row['points'],
            id_module=row['id_module'], id_lecon=row['id_lecon'], id_enseignant=row['id_enseignant'],
            tp=row.get('tp')
        )
    else:
        raise HTTPException(status_code=500, detail="Exercise creation failed")

@app.get("/exercises", response_model=List[Exercise])
def get_exercises():
    query = "SELECT * FROM exercice WHERE actif = 1"
    result = db_manager.execute_query(query)
    return [Exercise(
        id=row['id_exercice'], question=row['question'], solution=row['solution'],
        feedback=row['feedback'], points=row['points'],
        id_module=row['id_module'], id_lecon=row['id_lecon'], id_enseignant=row['id_enseignant'],
        tp=row.get('tp')
    ) for row in result]

@app.get("/exercises/filter", response_model=List[Exercise])
def get_exercises_by_chapter_tp(chapter: str = None, tp: str = None):
    query = "SELECT * FROM exercice WHERE actif = 1"
    params = []
    if chapter:
        query += " AND (question LIKE ? OR description LIKE ? OR instructions LIKE ?)"
        params.extend([f"%{chapter}%", f"%{chapter}%", f"%{chapter}%"])
    if tp:
        query += " AND tp = ?"
        params.append(tp)
    result = db_manager.execute_query(query, tuple(params))
    return [Exercise(
        id=row['id_exercice'], question=row['question'], solution=row['solution'],
        feedback=row['feedback'], points=row['points'],
        id_module=row['id_module'], id_lecon=row['id_lecon'], id_enseignant=row['id_enseignant'],
        tp=row.get('tp')
    ) for row in result]

@app.get("/exercises/{exercise_id}", response_model=Exercise)
def get_exercise(exercise_id: int):
    query = "SELECT * FROM exercice WHERE id_exercice = ? AND actif = 1"
    result = db_manager.execute_query(query, (exercise_id,))
    if result:
        row = result[0]
        return Exercise(
            id=row['id_exercice'], question=row['question'], solution=row['solution'],
            feedback=row['feedback'], points=row['points'],
            id_module=row['id_module'], id_lecon=row['id_lecon'], id_enseignant=row['id_enseignant'],
            tp=row.get('tp')
        )
    else:
        raise HTTPException(status_code=404, detail="Exercise not found")

@app.put("/exercises/{exercise_id}", response_model=Exercise)
def update_exercise(exercise_id: int, exercise: Exercise):
    query = "UPDATE exercice SET question = ?, solution = ?, feedback = ?, points = ?, id_module = ?, id_lecon = ?, id_enseignant = ?, tp = ? WHERE id_exercice = ?"
    db_manager.execute_query(query, (
        exercise.question, exercise.solution, exercise.feedback, exercise.points,
        exercise.id_module, exercise.id_lecon, exercise.id_enseignant, exercise.tp, exercise_id
    ))
    get_query = "SELECT * FROM exercice WHERE id_exercice = ?"
    result = db_manager.execute_query(get_query, (exercise_id,))
    if result:
        row = result[0]
        return Exercise(
            id=row['id_exercice'], question=row['question'], solution=row['solution'],
            feedback=row['feedback'], points=row['points'],
            id_module=row['id_module'], id_lecon=row['id_lecon'], id_enseignant=row['id_enseignant'],
            tp=row.get('tp')
        )
    else:
        raise HTTPException(status_code=404, detail="Exercise not found")

@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int):
    query = "UPDATE exercice SET actif = 0 WHERE id_exercice = ?"
    db_manager.execute_query(query, (exercise_id,))
    return {"message": "Exercise deleted"}

@app.get("/exercises/lesson/{lesson_id}", response_model=List[Exercise])
def get_exercises_by_lesson(lesson_id: int):
    query = "SELECT * FROM exercice WHERE id_lecon = ? AND actif = 1"
    result = db_manager.execute_query(query, (lesson_id,))
    return [Exercise(
        id=row['id_exercice'], question=row['question'], solution=row['solution'],
        feedback=row['feedback'], points=row['points'],
        id_module=row['id_module'], id_lecon=row['id_lecon'], id_enseignant=row['id_enseignant'],
        tp=row.get('tp')
    ) for row in result]

# --- Quiz CRUD ---
@app.post("/quizzes", response_model=Quiz)
def create_quiz(quiz: Quiz):
    query = """
        INSERT INTO quiz (titre, id_module)
        VALUES (?, ?)
    """
    db_manager.execute_query(query, (quiz.titre, quiz.id_module))
    get_query = "SELECT * FROM quiz WHERE titre = ? AND id_module = ? ORDER BY id_quiz DESC LIMIT 1"
    result = db_manager.execute_query(get_query, (quiz.titre, quiz.id_module))
    if not result:
        raise HTTPException(status_code=500, detail="Quiz creation failed")
    quiz_id = result[0]['id_quiz']
    # Insert questions
    for q in quiz.questions:
        db_manager.execute_query(
            "INSERT INTO quiz_question (id_quiz, enonce, choix, bonnes_reponses) VALUES (?, ?, ?, ?)",
            (quiz_id, q.enonce, json.dumps(q.choix), json.dumps(q.bonnes_reponses))
        )
    # Return full quiz with questions
    return get_quiz(quiz_id)

@app.get("/quizzes", response_model=List[Quiz])
def get_quizzes():
    query = "SELECT * FROM quiz WHERE actif = 1"
    result = db_manager.execute_query(query)
    quizzes = []
    for row in result:
        quiz_id = row['id_quiz']
        questions = db_manager.execute_query("SELECT * FROM quiz_question WHERE id_quiz = ?", (quiz_id,))
        questions = [QuizQuestion(id=q['id_question'], enonce=q['enonce'], choix=json.loads(q['choix']), bonnes_reponses=json.loads(q['bonnes_reponses'])) for q in questions]
        quizzes.append(Quiz(id=row['id_quiz'], titre=row['titre'], id_module=row['id_module'], questions=questions))
    return quizzes

@app.get("/quizzes/{quiz_id}", response_model=Quiz)
def get_quiz(quiz_id: int):
    query = "SELECT * FROM quiz WHERE id_quiz = ? AND actif = 1"
    result = db_manager.execute_query(query, (quiz_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Quiz not found")
    row = result[0]
    questions = db_manager.execute_query("SELECT * FROM quiz_question WHERE id_quiz = ?", (quiz_id,))
    questions = [QuizQuestion(id=q['id_question'], enonce=q['enonce'], choix=json.loads(q['choix']), bonnes_reponses=json.loads(q['bonnes_reponses'])) for q in questions]
    return Quiz(id=row['id_quiz'], titre=row['titre'], id_module=row['id_module'], questions=questions)

@app.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int):
    db_manager.execute_query("UPDATE quiz SET actif = 0 WHERE id_quiz = ?", (quiz_id,))
    return {"message": "Quiz deleted"}

@app.get("/quizzes/module/{id_module}", response_model=List[Quiz])
def get_quizzes_by_module(id_module: int):
    query = "SELECT * FROM quiz WHERE id_module = ?"
    result = db_manager.execute_query(query, (id_module,))
    return [Quiz(**row) for row in result]

@app.post("/quizzes/submit", response_model=QuizAttemptResponse)
def submit_quiz_attempt(attempt: QuizAttemptRequest):
    # Get the quiz with all questions
    quiz_query = "SELECT * FROM quiz WHERE id_quiz = ?"
    quiz_result = db_manager.execute_query(quiz_query, (attempt.quiz_id,))
    if not quiz_result:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get all questions for this quiz
    questions_query = "SELECT * FROM quiz_question WHERE id_quiz = ?"
    questions_result = db_manager.execute_query(questions_query, (attempt.quiz_id,))
    questions = [{
        'id': q['id_question'],
        'correct_answers': json.loads(q['bonnes_reponses']),
        'points': 1.0  # Each question is worth 1 point
    } for q in questions_result]
    
    # Calculate score
    total_questions = len(questions)
    if total_questions == 0:
        raise HTTPException(status_code=400, detail="Quiz has no questions")
    
    correct_answers = 0
    for q in questions:
        user_attempt = next((a for a in attempt.questions if a.question_id == q['id']), None)
        if user_attempt and set(user_attempt.selected_answers) == set(q['correct_answers']):
            correct_answers += 1
    
    score = (correct_answers / total_questions) * 100
    passed = score >= 50  # 50% passing threshold
    
    # Check if this is a remedial attempt
    if not attempt.is_remedial:
        # For regular attempts, save the score
        insert_query = """
            INSERT INTO score_quiz (id_utilisateur, id_quiz, score, passed)
            VALUES (?, ?, ?, ?)
        """
        db_manager.execute_query(
            insert_query,
            (attempt.user_id, attempt.quiz_id, score, passed)
        )
    
    # Check if we should show remedial questions
    show_remedial = False
    message = "Quiz completed successfully!"
    
    if not passed and not attempt.is_remedial:
        # Check if there are any remedial questions available
        # In a real implementation, you would check for remedial questions here
        # For now, we'll assume there are remedial questions available
        show_remedial = True
        message = "You didn't pass the quiz. Would you like to try some remedial questions?"
    
    return QuizAttemptResponse(
        score=score,
        passed=passed,
        show_remedial=show_remedial,
        message=message
    )

@app.get("/quizzes/user/{user_id}/module/{module_id}", response_model=List[dict])
def get_user_quiz_progress(user_id: int, module_id: int):
    """
    Get user's quiz progress for a specific module.
    Returns a list of quizzes with their completion status and scores.
    """
    # Get all quizzes for the module
    quizzes_query = """
        SELECT q.id_quiz, q.titre, sq.score, sq.passed, sq.date_passage
        FROM quiz q
        LEFT JOIN score_quiz sq ON q.id_quiz = sq.id_quiz AND sq.id_utilisateur = ?
        WHERE q.id_module = ?
        ORDER BY q.id_quiz
    """
    result = db_manager.execute_query(quizzes_query, (user_id, module_id))
    
    # Format the response
    quizzes = []
    for row in result:
        quizzes.append({
            'quiz_id': row['id_quiz'],
            'title': row['titre'],
            'score': row['score'],
            'passed': bool(row['passed']) if row['passed'] is not None else False,
            'completed': row['score'] is not None,
            'date_attempted': row['date_passage']
        })
    
    return quizzes

# --- Video Progress Tracking ---
@app.post("/progress/video")
def track_video_progress(progress_data: dict):
    """
    Track video watching progress for a user.
    Expected data: user_id, lesson_id, progress_percentage (0-100)
    """
    try:
        user_id = progress_data.get('user_id')
        lesson_id = progress_data.get('lesson_id')
        progress_percentage = progress_data.get('progress_percentage')
        
        if not all([user_id, lesson_id, progress_percentage is not None]):
            raise HTTPException(status_code=400, detail="Missing required fields: user_id, lesson_id, progress_percentage")
        
        # Check if progress entry already exists
        check_query = """
            SELECT * FROM progression_etudiant
            WHERE id_etudiant = ? AND id_lecon = ?
        """
        existing = db_manager.execute_query(check_query, (user_id, lesson_id))
        
        if existing:
            # Update existing progress
            update_query = """
                UPDATE progression_etudiant
                SET score = ?, temps_passe = ?
                WHERE id_etudiant = ? AND id_lecon = ?
            """
            db_manager.execute_query(update_query, (progress_percentage, 0, user_id, lesson_id))
        else:
            # Create new progress entry
            insert_query = """
                INSERT INTO progression_etudiant
                (id_etudiant, id_lecon, statut, score, temps_passe)
                VALUES (?, ?, 'en_cours', ?, 0)
            """
            db_manager.execute_query(insert_query, (user_id, lesson_id, progress_percentage))
        
        return {"message": "Video progress tracked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking video progress: {str(e)}")

@app.get("/progress/module/{user_id}/{module_id}")
def get_module_progress(user_id: int, module_id: int):
    """
    Calculate overall module progress based on video watching (70%) and quiz scores (30%).
    Progress is calculated as:
    - 70%: Average progress of watching Manim videos by the user
    - 30%: Average quiz scores for the module
    """
    try:
        # Get total number of videos in the module
        total_videos_query = """
            SELECT COUNT(*) as total_videos
            FROM lecon 
            WHERE id_module = ? 
            AND (contenu LIKE '%"type":"video"%' OR contenu LIKE '%"type":"video_manim"%')
        """
        total_videos_result = db_manager.execute_query(total_videos_query, (module_id,))
        total_videos = total_videos_result[0]['total_videos'] if total_videos_result else 0
        
        # Get user's video progress
        video_progress_query = """
            SELECT l.id_lecon, pe.score
            FROM lecon l
            LEFT JOIN progression_etudiant pe ON l.id_lecon = pe.id_lecon AND pe.id_etudiant = ?
            WHERE l.id_module = ? 
            AND (l.contenu LIKE '%"type":"video"%' OR l.contenu LIKE '%"type":"video_manim"%')
        """
        video_progress_result = db_manager.execute_query(video_progress_query, (user_id, module_id))
        
        # Calculate average progress and count watched videos
        total_progress = 0
        watched_videos = 0
        video_count = 0
        
        for row in video_progress_result:
            video_count += 1
            progress = row['score'] or 0
            total_progress += progress
            if progress >= 90:  # Consider video as watched if progress >= 90%
                watched_videos += 1
        
        avg_video_progress = (total_progress / video_count) if video_count > 0 else 0
        
        # Get total number of quizzes in the module
        quizzes_query = """
            SELECT COUNT(*) as total_quizzes
            FROM quiz q
            WHERE q.id_module = ?
        """
        quizzes_result = db_manager.execute_query(quizzes_query, (module_id,))
        total_quizzes = quizzes_result[0]['total_quizzes'] if quizzes_result else 0
        
        # Get user's quiz scores for this module
        quiz_scores_query = """
            SELECT AVG(sq.score) as avg_score
            FROM score_quiz sq
            JOIN quiz q ON sq.id_quiz = q.id_quiz
            WHERE sq.id_utilisateur = ? AND q.id_module = ?
        """
        quiz_scores_result = db_manager.execute_query(quiz_scores_query, (user_id, module_id))
        avg_quiz_score = quiz_scores_result[0]['avg_score'] if quiz_scores_result and quiz_scores_result[0]['avg_score'] else 0
        
        # Calculate overall progress (70% videos + 30% quizzes)
        overall_progress = (avg_video_progress * 0.7) + (avg_quiz_score * 0.3)
        
        return {
            "overall_progress": overall_progress,
            "video_progress": avg_video_progress,
            "quiz_score": avg_quiz_score,
            "total_videos": total_videos,
            "watched_videos": watched_videos,
            "total_quizzes": total_quizzes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating module progress: {str(e)}")

class PlotRequest(BaseModel):
    code: str

@app.post("/plot")
def plot_python_code(request: PlotRequest):
    # Redirect stdout/stderr to capture errors
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        # Prepare a restricted namespace
        allowed_builtins = {'__builtins__': {}}
        safe_globals = {
            "plt": plt,
            "np": np,
        }
        # Execute the code
        exec(request.code, {**allowed_builtins, **safe_globals})
        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Response(content=buf.read(), media_type="image/png")
    except Exception as e:
        error_output = sys.stdout.getvalue() + sys.stderr.getvalue() + str(e)
        return Response(content=f"Error in code execution:\n{error_output}", media_type="text/plain", status_code=400)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

# --- Mode Examen : chapitres et exercices démo ---
@app.get("/chapters/")
async def get_chapters():
    return ["Algèbre linéaire", "Analyse", "Probabilités", "Statistiques"]

# Servir les fichiers statiques (vidéos)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "media")), name="static")

# Pydantic models for the new endpoint
class LinearSystemRequest(BaseModel):
    eq1: str
    eq2: str
    user_id: Optional[int] = None

class Solution(BaseModel):
    x: float
    y: float

class LinearSystemResponse(BaseModel):
    solution: Optional[Solution]
    solution_type: str  # 'unique', 'none', 'infinite', 'invalid'
    coeffs1: Optional[dict]
    coeffs2: Optional[dict]

# Helper function to parse equations
def parse_equation(eq: str) -> Optional[dict]:
    # This regex is designed to be more robust for y = mx + b format
    # It handles missing coefficients, signs, and spaces
    match = re.match(r"y\s*=\s*(-?(?:\d*\.\d+|\d+)?)\s*\*?\s*x\s*([+\-]\s*(?:\d*\.\d+|\d+))?", eq.strip())
    if not match:
        return None

    m_str, b_str = match.groups()

    # Determine slope (m)
    if m_str is None or m_str == '+':
        m = 1.0
    elif m_str == '-':
        m = -1.0
    elif m_str == '':
        # This case can happen if the equation is just 'y=x...'
        m = 1.0
    else:
        try:
            m = float(m_str)
        except ValueError:
            return None # Invalid number for slope

    # Determine y-intercept (b)
    if b_str is None:
        b = 0.0
    else:
        try:
            b = float(b_str.replace(' ', ''))
        except ValueError:
            return None # Invalid number for intercept

    return {"m": m, "b": b}

@app.post("/api/solve-linear-system", response_model=LinearSystemResponse)
def solve_linear_system(request: LinearSystemRequest):
    coeffs1 = parse_equation(request.eq1)
    coeffs2 = parse_equation(request.eq2)

    response = {}

    if not coeffs1 or not coeffs2:
        response = {"solution": None, "solution_type": "invalid", "coeffs1": coeffs1, "coeffs2": coeffs2}

    m1, b1 = coeffs1['m'], coeffs1['b']
    m2, b2 = coeffs2['m'], coeffs2['b']

    # Using a small tolerance for floating point comparison
    if abs(m1 - m2) < 1e-9:
        if abs(b1 - b2) < 1e-9:
            return {"solution": None, "solution_type": "infinite", "coeffs1": coeffs1, "coeffs2": coeffs2}
        else:
            return {"solution": None, "solution_type": "none", "coeffs1": coeffs1, "coeffs2": coeffs2}
    else:
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        response = {"solution": {"x": x, "y": y}, "solution_type": "unique", "coeffs1": coeffs1, "coeffs2": coeffs2}

    # Save to history if user_id is provided and solution is not invalid
    if request.user_id and response["solution_type"] != 'invalid':
        try:
            db_manager.execute_query(
                "INSERT INTO linear_system_history (id_utilisateur, equation1, equation2, solution_type, solution_x, solution_y) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    request.user_id,
                    request.eq1,
                    request.eq2,
                    response['solution_type'],
                    response['solution']['x'] if response['solution'] else None,
                    response['solution']['y'] if response['solution'] else None,
                )
            )
        except Exception as e:
            logger.error(f"Failed to save history: {e}") # Log error but don't fail the request

    return response


@app.get("/api/history/linear-system/{user_id}")
def get_user_history(user_id: int):
    try:
        history = db_manager.execute_query("SELECT * FROM linear_system_history WHERE id_utilisateur = ? ORDER BY timestamp DESC", (user_id,))
        return history
    except Exception as e:
        logger.error(f"Error fetching history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch history")

@app.delete("/api/history/linear-system/{user_id}")
def delete_user_history(user_id: int):
    try:
        db_manager.execute_query("DELETE FROM linear_system_history WHERE id_utilisateur = ?", (user_id,))
        return {"message": "History cleared successfully"}
    except Exception as e:
        logger.error(f"Error deleting history for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear history")


@app.get("/api/manim-videos")
def get_manim_videos():
    videos_dir = "media/videos"
    video_data = []
    if not os.path.isdir(videos_dir):
        raise HTTPException(status_code=404, detail="Videos directory not found")

    categories = sorted([d for d in os.listdir(videos_dir) if os.path.isdir(os.path.join(videos_dir, d))])

    for category in categories:
        category_path = os.path.join(videos_dir, category)
        videos = []
        # We only look in the 1080p60 subdirectory for final videos
        specific_path = os.path.join(category_path, "1080p60")
        if os.path.isdir(specific_path):
            for filename in sorted(os.listdir(specific_path)):
                if filename.endswith(".mp4"):
                    # Construct the URL path
                    url_path = f"/media/videos/{category}/1080p60/{filename}".replace('\\', '/')
                    videos.append({"name": filename, "url": url_path})
        
        if videos:
            video_data.append({"category": category, "videos": videos})
    
    return video_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
