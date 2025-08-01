#!/usr/bin/env python3
"""
Migration script to convert frontend examData to backend exercises
"""

import requests
import json
import time

# Backend API URL
BASE_URL = "http://localhost:8000"

# Teacher ID (from the users list)
ID_ENSEIGNANT = 2

# The examData from your frontend (converted to backend format)
exam_data = {
    "Chapitre 1": {
        "TP1": [
            {
                "question": """Exercice 1 : Méthode de Gauss (8 points)
Partie I

a) Soit la matrice :
A = | 2  2 -1 |
    | 0  4  1 |
    | 1 -1  3 |
Calculer det(A). Conclure sur l'existence et l'unicité de la solution de AX = b.""",
                "solution": "det(A)=2(|4|-1|1 3|)-0(|2-1-1 3|)+1(|2 4-1 1|)=2(12+1)+1(2+4)=32",
                "feedback": "Attendu : calcul détaillé du déterminant, conclusion sur l'unicité.",
                "points": 2,
                "tp": "TP1"
            },
            {
                "question": """b) Résoudre le système AX = b avec b = (1, 3, -4) en utilisant la méthode de Gauss.""",
                "solution": "X=(1,0,-1)",
                "feedback": "Attendu : Triangularisation complète, solution par remontée, X=(1,0,-1).",
                "points": 4,
                "tp": "TP1"
            },
            {
                "question": """Exercice 2 : Méthodes Itératives (8 points)
Partie II

a) Vérifier que A est à diagonale strictement dominante.""",
                "solution": "A est à diagonale strictement dominante",
                "feedback": "Attendu : justification ligne par ligne.",
                "points": 2,
                "tp": "TP1"
            },
            {
                "question": """b) Écrire les schémas itératifs de Jacobi pour AX = b.""",
                "solution": "x1(k+1)=(1- x3(k))/2, x2(k+1)=(3-2x1(k)+x3(k))/4, x3(k+1)=(-4+x1(k)-x2(k))/3",
                "feedback": "Attendu : Formules exactes Jacobi.",
                "points": 1.5,
                "tp": "TP1"
            },
            {
                "question": """b) Écrire les schémas itératifs de Gauss-Seidel pour AX = b.""",
                "solution": "x1(k+1)=(1- x3(k))/2, x2(k+1)=(3-2x1(k+1)+x3(k))/4, x3(k+1)=(-4+x1(k+1)-x2(k+1))/3",
                "feedback": "Attendu : Formules exactes Gauss-Seidel.",
                "points": 1.5,
                "tp": "TP1"
            },
            {
                "question": """c) Calculer X(1) et X(2) pour chaque méthode avec X(0) = (1,0,0).""",
                "solution": "XJ(1)=(0.5,0.25,-1), XJ(2)=(1,0.25,-0.25), XGS(1)=(0.5,0.25,-0.333), XGS(2)=(1.166,-0.125,-0.555)",
                "feedback": "Attendu : résultats numériques pour Jacobi et Gauss-Seidel.",
                "points": 3,
                "tp": "TP1"
            },
            {
                "question": """Exercice 3 : Décomposition LU (4 points)
Pour A = | 3  1  0 |
         | 4  2  2 |
         | -2 1 6 |
vérifier que A admet une décomposition LU.""",
                "solution": "A admet une décomposition LU",
                "feedback": "Attendu : vérification des mineurs principaux non nuls.",
                "points": 2,
                "tp": "TP1"
            },
            {
                "question": """Résoudre A2X = b en utilisant la décomposition LU.""",
                "solution": "Y=A^-1b, X=A^-1Y",
                "feedback": "Attendu : Solution intermédiaire Y=A^-1b puis X=A^-1Y.",
                "points": 2,
                "tp": "TP1"
            }
        ],
        "TP2": [
            {
                "question": """Exercice 4 : Interpolation de Lagrange (6 points)
Soit les points (0,1), (1,3), (2,2). Calculer le polynôme d'interpolation de Lagrange.""",
                "solution": "P(x) = -0.5x² + 2.5x + 1",
                "feedback": "Attendu : polynôme exact de degré 2.",
                "points": 3,
                "tp": "TP2"
            }
        ],
        "TP3": []
    },
    "Chapitre 2": {
        "TP1": [],
        "TP2": [],
        "TP3": []
    },
    "Chapitre 3": {
        "TP1": [],
        "TP2": [],
        "TP3": []
    }
}

def create_exercise(exercise_data):
    """Create an exercise via the backend API"""
    url = f"{BASE_URL}/exercises"
    
    # Prepare the exercise data
    exercise = {
        "question": exercise_data["question"],
        "solution": exercise_data["solution"],
        "feedback": exercise_data["feedback"],
        "points": exercise_data["points"],
        "id_enseignant": ID_ENSEIGNANT,
        "tp": exercise_data["tp"],
        "id_module": None,  # Will be set later if needed
        "id_lecon": None    # Will be set later if needed
    }
    
    try:
        response = requests.post(url, json=exercise)
        if response.status_code == 200:
            created_exercise = response.json()
            print(f"✅ Created exercise {created_exercise['id']}: {exercise_data['question'][:50]}...")
            return created_exercise
        else:
            print(f"❌ Failed to create exercise: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating exercise: {e}")
        return None

def migrate_exam_data():
    """Migrate all exam data to the backend"""
    print("🚀 Starting migration of exam data to backend...")
    print(f"📝 Using teacher ID: {ID_ENSEIGNANT}")
    print("-" * 50)
    
    total_exercises = 0
    created_exercises = 0
    
    # Count total exercises
    for chapter, tps in exam_data.items():
        for tp, exercises in tps.items():
            total_exercises += len(exercises)
    
    print(f"📊 Found {total_exercises} exercises to migrate")
    print("-" * 50)
    
    # Migrate exercises
    for chapter, tps in exam_data.items():
        print(f"\n📚 Processing {chapter}:")
        for tp, exercises in tps.items():
            if exercises:
                print(f"  📋 {tp}: {len(exercises)} exercises")
                for exercise in exercises:
                    if create_exercise(exercise):
                        created_exercises += 1
                    time.sleep(0.1)  # Small delay to avoid overwhelming the server
            else:
                print(f"  📋 {tp}: No exercises")
    
    print("-" * 50)
    print(f"✅ Migration completed!")
    print(f"📊 Created {created_exercises}/{total_exercises} exercises")
    
    if created_exercises < total_exercises:
        print(f"⚠️  {total_exercises - created_exercises} exercises failed to create")
    else:
        print("🎉 All exercises migrated successfully!")

if __name__ == "__main__":
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            print("✅ Backend is running")
            migrate_exam_data()
        else:
            print("❌ Backend is not responding properly")
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Please make sure the backend is running on http://localhost:8000") 