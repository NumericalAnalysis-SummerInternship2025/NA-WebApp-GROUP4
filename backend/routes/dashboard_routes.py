from fastapi import APIRouter, HTTPException, Depends
from database import db_manager

router = APIRouter()

@router.get("/api/dashboard/stats/{enseignant_id}")
def get_dashboard_stats(enseignant_id: int):
    try:
        # --- Total Students ---
        # This query assumes a linking table between teachers, students, and modules.
        # The actual query will depend on the final schema for enrollments.
        students_query = """
            SELECT COUNT(DISTINCT e.id_utilisateur) as total_students
            FROM utilisateur e
            JOIN groupe_etudiant ge ON e.id_utilisateur = ge.id_etudiant
            JOIN groupe g ON ge.id_groupe = g.id_groupe
            WHERE g.id_enseignant = ? AND e.role = 'etudiant'
        """
        total_students_result = db_manager.execute_query(students_query, (enseignant_id,))
        total_students = total_students_result[0]['total_students'] if total_students_result else 0

        # --- Active Modules ---
        modules_query = "SELECT COUNT(id_module) as active_modules FROM module WHERE id_enseignant = ?"
        active_modules_result = db_manager.execute_query(modules_query, (enseignant_id,))
        active_modules = active_modules_result[0]['active_modules'] if active_modules_result else 0

        # --- Module Success Rate ---
        # This is a complex query and will be refined. It calculates avg score per module.
        success_rate_query = """
            SELECT m.id_module, m.nom as name, AVG(qs.score) as successRate
            FROM module m
            LEFT JOIN quiz q ON m.id_module = q.id_module
            LEFT JOIN quiz_score qs ON q.id_quiz = qs.id_quiz
            WHERE m.id_enseignant = ?
            GROUP BY m.id_module, m.nom
        """
        module_success_result = db_manager.execute_query(success_rate_query, (enseignant_id,))
        # Filter out modules with no success rate (None)
        module_success = [module for module in module_success_result if module['successRate'] is not None]


        # --- Assignments to Grade (Placeholder) ---
        # This will be implemented once assignment submissions are tracked.
        assignments_to_grade = 0 # Placeholder value

        return {
            "totalStudents": total_students,
            "activeModules": active_modules,
            "averageSuccessRate": (sum(m['successRate'] for m in module_success) / len(module_success)) if module_success else 0,
            "assignmentsToGrade": assignments_to_grade,
            "moduleSuccess": module_success
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard stats: {e}")
