# No models defined. Only database setup is used in this project. 

from pydantic import BaseModel
from typing import Optional, List

class QuizQuestion(BaseModel):
    id: int
    enonce: str
    choix: List[str]
    bonnes_reponses: List[int]

class QuizAttemptQuestion(BaseModel):
    question_id: int
    selected_answers: List[int]

class QuizAttemptRequest(BaseModel):
    quiz_id: int
    user_id: int
    is_remedial: bool = False
    questions: List[QuizAttemptQuestion]

class QuizAttemptResponse(BaseModel):
    score: float
    passed: bool
    show_remedial: bool
    message: str

class Quiz(BaseModel):
    id: int
    titre: str
    id_module: int
    questions: List[QuizQuestion] = []

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    role: str  # 'etudiant', 'enseignant', 'admin'
    password: Optional[str] = None  # Only for creation

class Module(BaseModel):
    id: Optional[int] = None
    titre: str
    type: str
    description: Optional[str] = None
    contenu: Optional[str] = None
    id_enseignant: Optional[int] = None
    id_module: Optional[int] = None
    theorie: Optional[str] = None
    categorie: Optional[str] = None
    niveau: Optional[str] = None
    duree: Optional[str] = None
    objectifs: Optional[List[str]] = None

class Lesson(BaseModel):
    id: Optional[int] = None
    titre: str
    description: Optional[str] = None
    duree: Optional[str] = None
    niveau: Optional[str] = None
    contenu: str
    id_module: int
    id_enseignant: int
    ordre: Optional[int] = 0

class Exercise(BaseModel):
    id: Optional[int] = None
    question: str
    solution: str
    feedback: Optional[str] = None
    points: Optional[int] = 1
    id_module: Optional[int] = None
    id_lecon: Optional[int] = None
    id_enseignant: int
    tp: Optional[str] = None 

class CalendarEvent(BaseModel):
    id: Optional[int] = None
    title: str
    date: str # Using string to match frontend date input
    type: str # 'exam', 'assignment', 'reminder'
    id_enseignant: int