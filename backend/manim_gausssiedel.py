from manim import *
import numpy as np

class GaussSeidelMethodAnimation(Scene):
    def construct(self):
        # Configuration des couleurs
        self.PRIMARY_COLOR = BLUE
        self.SECONDARY_COLOR = GREEN
        self.HIGHLIGHT_COLOR = YELLOW
        self.ERROR_COLOR = RED
        
        # Titre principal persistant avec position sécurisée
        self.main_title = Text("Méthode de Gauss-Seidel", font_size=36, color=self.PRIMARY_COLOR)
        self.main_title.to_edge(UP, buff=0.8)  # Plus d'espace pour éviter les collisions
        self.play(Write(self.main_title))
        self.wait(1)

        # Zone de contenu avec limites définies
        self.content_bounds = Rectangle(width=12, height=5.5, stroke_opacity=0)
        self.content_bounds.next_to(self.main_title, DOWN, buff=0.5)

        # Liste pour tracker les objets de contenu
        self.content_objects = []

        # Exécuter les sections
        self.show_introduction()
        self.present_system()
        self.show_matrix_decomposition()
        self.check_convergence()
        self.show_algorithm()
        self.execute_iterations()
        self.show_conclusion()

    def clear_content(self):
        """Nettoie la zone de contenu de manière sécurisée"""
        if hasattr(self, 'content_objects') and self.content_objects:
            # Filter out None objects and objects that might have been removed
            valid_objects = [obj for obj in self.content_objects if obj is not None and obj in self.mobjects]
            if valid_objects:
                self.play(FadeOut(*valid_objects), run_time=0.5)
            self.content_objects = []

    def add_to_content(self, *mobjects):
        """Ajoute des objets à la liste de contenu"""
        for mob in mobjects:
            self.content_objects.append(mob)

    def show_introduction(self):
        """Introduction simple et claire"""
        intro = VGroup(
            Text("Résolution itérative de systèmes linéaires", font_size=24),
            Text("Ax = b", font_size=32, color=self.HIGHLIGHT_COLOR)
        ).arrange(DOWN, buff=0.8)
        intro.move_to(self.content_bounds.get_center())
        
        self.play(FadeIn(intro))
        self.wait(2)
        self.play(FadeOut(intro))

    def present_system(self):
        """Présente le système avec positionnement sécurisé"""
        self.clear_content()
        
        # Titre de section avec position relative au titre principal
        section_title = Text("1. Système à résoudre", font_size=22, color=self.PRIMARY_COLOR)
        section_title.next_to(self.main_title, DOWN, buff=0.5)
        section_title.to_edge(LEFT, buff=1)
        self.play(Write(section_title))
        self.add_to_content(section_title)
        
        # Système d'équations avec formatage LaTeX sécurisé
        system_text = VGroup(
            MathTex(r"5x_1 + 2x_2 - x_3 = 6", font_size=28),
            MathTex(r"x_1 + 6x_2 - 3x_3 = 4", font_size=28),
            MathTex(r"2x_1 + x_2 + 4x_3 = 2", font_size=28)
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        arrow = MathTex(r"\Rightarrow", font_size=36)
        
        # Forme matricielle avec espacement approprié
        matrix_form = MathTex(
            r"\begin{bmatrix}"
            r"5 & 2 & -1 \\"
            r"1 & 6 & -3 \\"
            r"2 & 1 & 4"
            r"\end{bmatrix}"
            r"\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}"
            r"= \begin{bmatrix} 6 \\ 4 \\ 2 \end{bmatrix}",
            font_size=24
        )
        
        # Arrangement avec espacement adaptatif
        content = VGroup(system_text, arrow, matrix_form).arrange(RIGHT, buff=0.8)
        content.next_to(section_title, DOWN, buff=0.8)
        content.move_to(self.content_bounds.get_center() + DOWN * 0.5)
        
        self.play(Write(system_text))
        self.wait(1)
        self.play(Write(arrow))
        self.wait(0.5)
        self.play(Write(matrix_form))
        self.wait(2)
        
        self.add_to_content(system_text, arrow, matrix_form)

    def show_matrix_decomposition(self):
        """Décomposition matricielle avec gestion d'erreurs"""
        self.clear_content()
        
        section_title = Text("2. Décomposition A = D - E - F", font_size=22, color=self.PRIMARY_COLOR)
        section_title.next_to(self.main_title, DOWN, buff=0.5)
        section_title.to_edge(LEFT, buff=1)
        self.play(Write(section_title))
        self.add_to_content(section_title)
        
        # Matrice A centrée
        matrix_A = MathTex(
            r"A = \begin{bmatrix}"
            r"5 & 2 & -1 \\"
            r"1 & 6 & -3 \\"
            r"2 & 1 & 4"
            r"\end{bmatrix}",
            font_size=28
        )
        matrix_A.move_to(self.content_bounds.get_center() + UP * 1.2)
        
        self.play(Write(matrix_A))
        self.wait(1)
        self.add_to_content(matrix_A)
        
        # Décomposition centrée
        matrix_D = MathTex(r"D = \begin{bmatrix} 5 & 0 & 0 \\ 0 & 6 & 0 \\ 0 & 0 & 4 \end{bmatrix}", 
                          color=RED, font_size=20)
        matrix_E = MathTex(r"E = \begin{bmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 2 & 1 & 0 \end{bmatrix}", 
                          color=GREEN, font_size=20)
        matrix_F = MathTex(r"F = \begin{bmatrix} 0 & 2 & -1 \\ 0 & 0 & -3 \\ 0 & 0 & 0 \end{bmatrix}", 
                          color=BLUE, font_size=20)
        
        decomp = VGroup(matrix_D, matrix_E, matrix_F).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        decomp.move_to(self.content_bounds.get_center() + DOWN * 0.8)
        
        for matrix in decomp:
            self.play(Write(matrix))
            self.wait(1)
            self.add_to_content(matrix)
        
        self.wait(1)

    def check_convergence(self):
        """Vérification de convergence avec gestion des symboles"""
        self.clear_content()
        
        section_title = Text("3. Condition de convergence", font_size=22, color=self.PRIMARY_COLOR)
        section_title.next_to(self.main_title, DOWN, buff=0.5)
        section_title.to_edge(LEFT, buff=1)
        self.play(Write(section_title))
        self.add_to_content(section_title)
        
        # Condition centrée
        condition_text = Text("Diagonale strictement dominante:", font_size=24)
        condition_formula = MathTex(r"|a_{ii}| > \sum_{j \neq i} |a_{ij}|", font_size=28, color=self.HIGHLIGHT_COLOR)
        
        condition_group = VGroup(condition_text, condition_formula).arrange(DOWN, buff=0.5)
        condition_group.move_to(self.content_bounds.get_center() + UP * 1.5)
        
        self.play(Write(condition_group))
        self.wait(1)
        self.add_to_content(condition_group)
        
        # Vérifications avec symboles simples - éviter les caractères problématiques
        check1 = MathTex(r"|5| > |2| + |-1| \Rightarrow 5 > 3", color=GREEN, font_size=24)
        check2 = MathTex(r"|6| > |1| + |-3| \Rightarrow 6 > 4", color=GREEN, font_size=24)  
        check3 = MathTex(r"|4| > |2| + |1| \Rightarrow 4 > 3", color=GREEN, font_size=24)
        
        # Utiliser du texte simple pour les checkmarks
        checkmark1 = Text("OK", font_size=20, color=GREEN)
        checkmark2 = Text("OK", font_size=20, color=GREEN)
        checkmark3 = Text("OK", font_size=20, color=GREEN)
        
        checks = VGroup(
            VGroup(check1, checkmark1).arrange(RIGHT, buff=0.3),
            VGroup(check2, checkmark2).arrange(RIGHT, buff=0.3),
            VGroup(check3, checkmark3).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        checks.move_to(self.content_bounds.get_center() + DOWN * 0.2)
        
        for check in checks:
            self.play(Write(check))
            self.wait(0.8)
            self.add_to_content(check)
        
        conclusion = Text("Convergence garantie", font_size=28, color=GREEN)
        conclusion.move_to(self.content_bounds.get_center() + DOWN * 2)
        self.play(Write(conclusion))
        self.wait(2)
        self.add_to_content(conclusion)

    def show_algorithm(self):
        """Algorithme avec formatage amélioré"""
        self.clear_content()
        
        section_title = Text("4. Formules itératives", font_size=22, color=self.PRIMARY_COLOR)
        section_title.next_to(self.main_title, DOWN, buff=0.5)
        section_title.to_edge(LEFT, buff=1)
        self.play(Write(section_title))
        self.add_to_content(section_title)
        
        # Formules avec indices LaTeX appropriés
        formula1 = MathTex(r"x_1^{(k+1)} = \frac{1}{5}(6 - 2x_2^{(k)} + x_3^{(k)})", color=RED, font_size=24)
        formula2 = MathTex(r"x_2^{(k+1)} = \frac{1}{6}(4 - x_1^{(k+1)} + 3x_3^{(k)})", color=GREEN, font_size=24)
        formula3 = MathTex(r"x_3^{(k+1)} = \frac{1}{4}(2 - 2x_1^{(k+1)} - x_2^{(k+1)})", color=BLUE, font_size=24)
        
        formulas = VGroup(formula1, formula2, formula3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        formulas.next_to(section_title, DOWN, buff=0.8)
        formulas.move_to(self.content_bounds.get_center())
        
        for formula in [formula1, formula2, formula3]:
            self.play(Write(formula))
            self.wait(1)
            self.add_to_content(formula)
        
        note = Text("Calcul séquentiel : utilise les valeurs déjà calculées", 
                   font_size=20, color=self.HIGHLIGHT_COLOR)
        note.next_to(formulas, DOWN, buff=0.8)
        self.play(Write(note))
        self.wait(2)
        self.add_to_content(note)

    def execute_iterations(self):
        """Itérations avec tableau sécurisé"""
        self.clear_content()
        
        section_title = Text("5. Calcul des itérations", font_size=22, color=self.PRIMARY_COLOR)
        section_title.next_to(self.main_title, DOWN, buff=0.5)
        section_title.to_edge(LEFT, buff=1)
        self.play(Write(section_title))
        self.add_to_content(section_title)
        
        # En-têtes avec espacement calculé - utiliser Text partout pour éviter les erreurs LaTeX
        headers = VGroup(
            Text("k", font_size=20, color=self.HIGHLIGHT_COLOR),
            Text("x1", font_size=20, color=RED),
            Text("x2", font_size=20, color=GREEN), 
            Text("x3", font_size=20, color=BLUE),
            Text("Erreur", font_size=18, color=self.ERROR_COLOR)
        ).arrange(RIGHT, buff=1.0)
        headers.next_to(section_title, DOWN, buff=0.8)
        
        self.play(Write(headers))
        self.add_to_content(headers)
        
        # Données des itérations
        iterations = [
            ("0", "0.0000", "0.0000", "0.0000", "-"),
            ("1", "1.2000", "0.4667", "-0.2167", "1.456"),
            ("2", "0.9700", "0.3967", "-0.0842", "0.274"),
            ("3", "1.0245", "0.4538", "-0.1257", "0.081"),
            ("4", "0.9933", "0.4383", "-0.1062", "0.034"),
            ("5", "1.0022", "0.4457", "-0.1130", "0.012")
        ]
        
        # Afficher les itérations une par une avec positionnement absolu
        table_rows = []
        for i, (k, x1, x2, x3, err) in enumerate(iterations):
            row = VGroup(
                Text(k, font_size=18),
                Text(x1, font_size=18, color=RED),
                Text(x2, font_size=18, color=GREEN),
                Text(x3, font_size=18, color=BLUE),
                Text(err, font_size=16, color=self.ERROR_COLOR)
            ).arrange(RIGHT, buff=1.0)
            
            # Position absolue pour éviter les erreurs de positionnement
            row.move_to(headers.get_center() + DOWN * (0.4 + i * 0.35))
            table_rows.append(row)
            
            self.play(Write(row), run_time=0.6)
            self.wait(0.3)
            self.add_to_content(row)
        
        # Solution finale avec position sécurisée
        if table_rows:  # Vérifier que la table existe
            solution = Text("Solution convergée !", font_size=24, color=GREEN)
            solution.next_to(table_rows[-1], DOWN, buff=0.8)
            self.play(Write(solution))
            self.wait(2)
            self.add_to_content(solution)

    def show_conclusion(self):
        """Conclusion avec nettoyage final"""
        self.clear_content()
        
        conclusion_title = Text("Résumé", font_size=28, color=self.PRIMARY_COLOR)
        conclusion_title.next_to(self.main_title, DOWN, buff=0.5)
        self.play(Write(conclusion_title))
        self.add_to_content(conclusion_title)
        
        points = VGroup(
            Text("• Méthode itérative efficace", font_size=22),
            Text("• Converge si diagonale dominante", font_size=22),
            Text("• Plus rapide que Jacobi", font_size=22),
            Text("• Calcul séquentiel des composantes", font_size=22)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        points.next_to(conclusion_title, DOWN, buff=1)
        
        for point in points:
            self.play(Write(point), run_time=0.8)
            self.wait(0.4)
            self.add_to_content(point)
        
        final_text = Text("Fin de la présentation", font_size=24, color=self.HIGHLIGHT_COLOR)
        final_text.next_to(points, DOWN, buff=1)
        self.play(Write(final_text))
        self.wait(3)
        self.add_to_content(final_text)
        
        # CORRECTION : Ajout du nettoyage final pour faire disparaître le résumé
        self.clear_content()
        self.wait(1)