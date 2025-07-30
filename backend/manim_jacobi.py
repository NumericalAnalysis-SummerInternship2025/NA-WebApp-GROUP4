from manim import *
import numpy as np

class JacobiMethodAnimation(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content_objects = []
        # Définition des couleurs
        self.PRIMARY_COLOR = BLUE
        self.SECONDARY_COLOR = GREEN
        self.HIGHLIGHT_COLOR = YELLOW
        self.ERROR_COLOR = RED

    def construct(self):
        # Les couleurs sont maintenant définies dans __init__
        
        # Titre principal persistant avec position sécurisée
        self.main_title = Text("Méthode de Jacobi", font_size=36, color=self.PRIMARY_COLOR)
        self.main_title.to_edge(UP, buff=0.8)
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
        """Introduction avec caractéristiques de Jacobi"""
        intro = VGroup(
            Text("Méthode itérative simultanée", font_size=26),
            Text("Utilise TOUTES les valeurs de l'itération précédente", font_size=22, color=self.HIGHLIGHT_COLOR),
            Text("Ax = b", font_size=32, color=self.PRIMARY_COLOR)
        ).arrange(DOWN, buff=0.7)
        intro.move_to(self.content_bounds.get_center())
        
        self.play(FadeIn(intro))
        self.wait(3)
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
        content.move_to(self.content_bounds.get_center())
        
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
        matrix_A.move_to(self.content_bounds.get_center() + UP * 1.5)
        
        self.play(Write(matrix_A))
        self.wait(1)
        self.add_to_content(matrix_A)
        
        
        
        # Décomposition avec matrices plus petites pour éviter le débordement
        matrix_D = MathTex(r"D = \begin{bmatrix} 5 & 0 & 0 \\ 0 & 6 & 0 \\ 0 & 0 & 4 \end{bmatrix}", 
                          color=RED, font_size=18)
        matrix_E = MathTex(r"E = \begin{bmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 2 & 1 & 0 \end{bmatrix}", 
                          color=GREEN, font_size=18)
        matrix_F = MathTex(r"F = \begin{bmatrix} 0 & 2 & -1 \\ 0 & 0 & -3 \\ 0 & 0 & 0 \end{bmatrix}", 
                          color=BLUE, font_size=18)
        
        decomp = VGroup(matrix_D, matrix_E, matrix_F).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        decomp.move_to(self.content_bounds.get_center() + DOWN * 1)
        
        for matrix in decomp:
            self.play(Write(matrix))
            self.wait(0.8)
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
        
        # Vérifications avec calculs détaillés
        check1 = MathTex(r"\text{Ligne 1: } |5| > |2| + |-1| \Rightarrow 5 > 3", color=GREEN, font_size=22)
        check2 = MathTex(r"\text{Ligne 2: } |6| > |1| + |-3| \Rightarrow 6 > 4", color=GREEN, font_size=22)
        check3 = MathTex(r"\text{Ligne 3: } |4| > |2| + |1| \Rightarrow 4 > 3", color=GREEN, font_size=22)
        
        # Utiliser du texte simple pour les checkmarks
        checkmark1 = Text("OK", font_size=18, color=GREEN)
        checkmark2 = Text("OK", font_size=18, color=GREEN)
        checkmark3 = Text("OK", font_size=18, color=GREEN)
        
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
        
        conclusion = Text("Convergence assurée pour Jacobi", font_size=26, color=GREEN)
        conclusion.move_to(self.content_bounds.get_center() + DOWN * 2)
        self.play(Write(conclusion))
        self.wait(2)
        self.add_to_content(conclusion)

    def show_algorithm(self):
        """Algorithme de Jacobi avec explications"""
        self.clear_content()
        
        section_title = Text("4. Algorithme de Jacobi", font_size=22, color=self.PRIMARY_COLOR)
        section_title.next_to(self.main_title, DOWN, buff=0.5)
        section_title.to_edge(LEFT, buff=1)
        self.play(Write(section_title))
        self.add_to_content(section_title)
        
        # Formule générale centrée
        general_formula = MathTex(
            r"x_i^{(k+1)} = \frac{1}{a_{ii}} \left( b_i - \sum_{j \neq i} a_{ij} x_j^{(k)} \right)",
            font_size=24,
            color=self.HIGHLIGHT_COLOR
        )
        general_formula.move_to(self.content_bounds.get_center() + UP * 1.8)
        
        self.play(Write(general_formula))
        self.wait(2)
        self.add_to_content(general_formula)
        
       
        
        # Formules spécifiques centrées
        formula1 = MathTex(r"x_1^{(k+1)} = \frac{1}{5}(6 - 2x_2^{(k)} + x_3^{(k)})", color=RED, font_size=22)
        formula2 = MathTex(r"x_2^{(k+1)} = \frac{1}{6}(4 - x_1^{(k)} + 3x_3^{(k)})", color=GREEN, font_size=22)
        formula3 = MathTex(r"x_3^{(k+1)} = \frac{1}{4}(2 - 2x_1^{(k)} - x_2^{(k)})", color=BLUE, font_size=22)
        
        formulas = VGroup(formula1, formula2, formula3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        formulas.move_to(self.content_bounds.get_center() + DOWN * 0.5)
        
        for formula in [formula1, formula2, formula3]:
            self.play(Write(formula))
            self.wait(1)
            self.add_to_content(formula)

    def execute_iterations(self):
        """Exécute les itérations avec calculs détaillés"""
        self.clear_content()
        
        section_title = Text("5. Calcul des itérations", font_size=22, color=self.PRIMARY_COLOR)
        section_title.next_to(self.main_title, DOWN, buff=0.5)
        section_title.to_edge(LEFT, buff=1)
        self.play(Write(section_title))
        self.add_to_content(section_title)
        
        # En-têtes avec espacement calculé - utiliser Text partout
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
        
        # Données des itérations (calculs plus précis)
        iterations = [
            ("0", "0.0000", "0.0000", "0.0000", "-"),
            ("1", "1.2000", "0.6667", "0.5000", "1.456"),
            ("2", "0.9333", "0.4556", "-0.0833", "0.598"),
            ("3", "1.0278", "0.4815", "-0.1065", "0.112"),
            ("4", "0.9917", "0.4417", "-0.1021", "0.045"),
            ("5", "1.0028", "0.4469", "-0.1135", "0.018"),
            ("6", "0.9989", "0.4440", "-0.1097", "0.007")
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
            row.move_to(headers.get_center() + DOWN * (0.4 + i * 0.3))
            table_rows.append(row)
            
            if k == "0":
                self.play(Write(row), run_time=0.8)
            else:
                # Animation pour montrer le calcul simultané
                calc_note = Text(f"Calcul simultané avec les valeurs k={int(k)-1}", 
                               font_size=16, color=ORANGE)
                calc_note.move_to(self.content_bounds.get_center() + DOWN * 2.5)
                self.play(Write(calc_note))
                self.play(Write(row), run_time=1)
                self.play(FadeOut(calc_note))
            
            self.wait(0.4)
            self.add_to_content(row)
        
        # Note sur la convergence avec position sécurisée
        if table_rows:
            convergence_note = Text(
                "Jacobi converge plus lentement mais sûrement !",
                font_size=20,
                color=GREEN
            )
            convergence_note.next_to(table_rows[-1], DOWN, buff=0.8)
            self.play(Write(convergence_note))
            self.wait(2)
            self.add_to_content(convergence_note)

    def execute_iterations(self):
        self.clear_content()
        title = Text("Exécution des Itérations", font_size=28, color=self.PRIMARY_COLOR)
        title.next_to(self.main_title, DOWN, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Données d'exemple pour l'itération
        iterations = [
            {"k": 0, "x1": 0.0000, "x2": 0.0000, "x3": 0.0000, "error": "-"},
            {"k": 1, "x1": 0.7500, "x2": -0.4000, "x3": 0.6667, "error": 1.1667},
            {"k": 2, "x1": 0.6833, "x2": -0.2833, "x3": 0.6083, "error": 0.1583},
            {"k": 3, "x1": 0.6688, "x2": -0.2583, "x3": 0.6104, "error": 0.0250},
            {"k": 4, "x1": 0.6619, "x2": -0.2560, "x3": 0.6019, "error": 0.0085}
        ]
        
        # Création du tableau
        table = self.create_iteration_table(iterations)
        table.next_to(title, DOWN, buff=1)
        
        # Animation du tableau
        self.play(Create(table.get_horizontal_lines()),
                 Create(table.get_vertical_lines()))
        self.play(Write(table.get_entries()[:5]))  # En-têtes
        
        # Animation des itérations une par une
        for i in range(1, len(iterations)):
            start_idx = 5 + (i-1)*5  # 5 entêtes + (i-1)*5 valeurs par ligne
            end_idx = start_idx + 5
            self.play(Write(table.get_entries()[start_idx:end_idx]))
            self.wait(0.5)
        
        self.wait(2)
        
        # Affichage de la solution finale
        final_solution = VGroup(
            Text("Solution finale (approchée) :", font_size=26, color=self.SECONDARY_COLOR),
            MathTex(r"x_1 \approx 0.662", font_size=28, color=WHITE),
            MathTex(r"x_2 \approx -0.256", font_size=28, color=WHITE),
            MathTex(r"x_3 \approx 0.602", font_size=28, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        final_solution.next_to(table, DOWN, buff=1)
        final_solution.to_edge(LEFT, buff=1.5)
        
        self.play(Write(final_solution[0]))
        self.wait(0.5)
        for sol in final_solution[1:]:
            self.play(Write(sol))
            self.wait(0.3)
            
        self.wait(2)
        self.add_to_content(title, table, final_solution)
    
    def create_iteration_table(self, iterations):
        # En-têtes
        headers = ["k", "x₁", "x₂", "x₃", "Erreur"]
        
        # Préparation des données
        table_data = [headers]
        for it in iterations:
            row = [
                str(it["k"]),
                f"{it['x1']:.4f}",
                f"{it['x2']:.4f}",
                f"{it['x3']:.4f}",
                str(it["error"]) if it["error"] == "-" else f"{it['error']:.4f}"
            ]
            table_data.append(row)
        
        # Création du tableau avec Table()
        table = Table(
            table_data,
            include_outer_lines=True,
            arrange_in_grid_config={"cell_alignment": RIGHT}
        )
        
        # Mise en forme
        table.scale(0.6)
        
        # Style des cellules
        for i, color in enumerate([YELLOW, BLUE, BLUE, BLUE, RED]):
            table.add_highlighted_cell((1, i+1), color=color)
        
        return table
    
    