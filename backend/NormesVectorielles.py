from manim import *
import numpy as np

# Configuration globale
config.frame_rate = 30
config.pixel_height = 720
config.pixel_width = 1280

class IntroductionNormes(Scene):
    def construct(self):
        # Titre principal avec animation
        title = Text("Introduction aux Normes Vectorielles", 
                    font_size=48, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title, run_time=2))
        
        # Question principale
        question = Text("Comment mesurer la taille d'un vecteur ?", 
                       font_size=32, color=WHITE)
        question.next_to(title, DOWN, buff=0.8)
        self.play(FadeIn(question, shift=UP))
        self.wait(2)
        
        # Transition vers la démonstration
        self.play(FadeOut(question))
        
        # Créer un système de coordonnées
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": GRAY, "stroke_width": 2}
        )
        
        # Étiquettes des axes
        x_label = axes.get_x_axis_label("x_1", color=WHITE)
        y_label = axes.get_y_axis_label("x_2", color=WHITE)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Vecteur exemple
        vector_coords = [3, 2]
        vector = Arrow(axes.c2p(0, 0), axes.c2p(*vector_coords), 
                      color=YELLOW, stroke_width=6, buff=0)
        vector_label = MathTex(r"\vec{v} = \begin{pmatrix} 3 \\ 2 \end{pmatrix}", 
                              color=YELLOW, font_size=32)
        vector_label.next_to(axes.c2p(*vector_coords), UR, buff=0.3)
        
        self.play(Create(vector), Write(vector_label))
        self.wait(1)
        
        # Narration text
        narration = Text("Les normes vectorielles nous donnent différentes manières de le faire.", 
                        font_size=24, color=WHITE)
        narration.to_edge(DOWN)
        self.play(Write(narration))
        self.wait(2)
        
        # NORME 1 (Manhattan) - Chemin en escalier
        self.play(FadeOut(narration))
        
        norme1_title = Text("Norme 1 (Manhattan)", font_size=28, color=GREEN, weight=BOLD)
        norme1_title.to_edge(LEFT).shift(UP * 2)
        self.play(Write(norme1_title))
        
        # Dessiner le chemin en escalier
        horizontal_line = Line(axes.c2p(0, 0), axes.c2p(3, 0), color=GREEN, stroke_width=4)
        vertical_line = Line(axes.c2p(3, 0), axes.c2p(3, 2), color=GREEN, stroke_width=4)
        
        self.play(Create(horizontal_line), run_time=1.5)
        self.play(Create(vertical_line), run_time=1.5)
        
        # Formule et calcul
        norme1_formula = MathTex(r"||\vec{v}||_1 = |x_1| + |x_2| = |3| + |2| = 5", 
                                color=GREEN, font_size=24)
        norme1_formula.next_to(norme1_title, DOWN, buff=0.3)
        self.play(Write(norme1_formula))
        self.wait(2)
        
        # NORME 2 (Euclidienne) - Distance directe avec cercle
        norme2_title = Text("Norme 2 (Euclidienne)", font_size=28, color=RED, weight=BOLD)
        norme2_title.next_to(norme1_formula, DOWN, buff=0.8)
        self.play(Write(norme2_title))
        
        # Cercle centré à l'origine
        norme2_value = np.sqrt(3**2 + 2**2)
        circle = Circle(radius=axes.x_axis.unit_size * norme2_value, color=RED, stroke_width=3)
        circle.move_to(axes.c2p(0, 0))
        
        # Point sur le cercle
        point_on_circle = Dot(axes.c2p(*vector_coords), color=RED, radius=0.08)
        
        self.play(Create(circle), Create(point_on_circle))
        
        # Formule et calcul
        norme2_formula = MathTex(r"||\vec{v}||_2 = \sqrt{x_1^2 + x_2^2} = \sqrt{3^2 + 2^2} = \sqrt{13} \approx 3.6", 
                                color=RED, font_size=24)
        norme2_formula.next_to(norme2_title, DOWN, buff=0.3)
        self.play(Write(norme2_formula))
        self.wait(2)
        
        # NORME ∞ (Max) - Carré avec composante maximale
        norme_inf_title = Text("Norme ∞ (Maximum)", font_size=28, color=PURPLE, weight=BOLD)
        norme_inf_title.next_to(norme2_formula, DOWN, buff=0.8)
        self.play(Write(norme_inf_title))
        
        # Carré encadrant
        square_size = 3  # max(|3|, |2|) = 3
        square = Rectangle(width=axes.x_axis.unit_size * square_size * 2, 
                          height=axes.x_axis.unit_size * square_size * 2, 
                          color=PURPLE, stroke_width=3)
        square.move_to(axes.c2p(square_size/2, square_size/2))
        
        # Lignes de grille pour montrer les composantes
        max_line_x = DashedLine(axes.c2p(0, 0), axes.c2p(3, 0), color=PURPLE, stroke_width=2)
        max_line_y = DashedLine(axes.c2p(0, 0), axes.c2p(0, 2), color=PURPLE, stroke_width=2)
        
        self.play(Create(square), Create(max_line_x), Create(max_line_y))
        
        # Formule et calcul
        norme_inf_formula = MathTex(r"||\vec{v}||_\infty = \max\{|x_1|, |x_2|\} = \max\{|3|, |2|\} = 3", 
                                   color=PURPLE, font_size=24)
        norme_inf_formula.next_to(norme_inf_title, DOWN, buff=0.3)
        self.play(Write(norme_inf_formula))
        self.wait(3)
        
        # Fade out tout pour la transition
        self.play(FadeOut(Group(*self.mobjects)))

class DemonstrationNouvelleNorme(Scene):
    def construct(self):
        # Titre
        title = Text("Démonstration d'une Nouvelle Norme", 
                    font_size=42, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Définition de la norme
        norme_def = MathTex(r"||\vec{X}|| = |x_1 + x_2| + |x_1|", 
                           font_size=36, color=YELLOW)
        norme_def.next_to(title, DOWN, buff=0.5)
        self.play(Write(norme_def))
        
        # Vecteur exemple
        vector_example = MathTex(r"\vec{X} = \begin{pmatrix} x_1 \\ x_2 \end{pmatrix}", 
                                font_size=32, color=WHITE)
        vector_example.next_to(norme_def, DOWN, buff=0.5)
        self.play(Write(vector_example))
        self.wait(1)
        
        # Étape 1: Positivité
        step1_title = Text("1. Définie Positivité", font_size=32, color=GREEN, weight=BOLD)
        step1_title.next_to(vector_example, DOWN, buff=0.8)
        self.play(Write(step1_title))
        
        step1_proof = VGroup(
            MathTex(r"||\vec{X}|| = 0 \Leftrightarrow |x_1 + x_2| + |x_1| = 0", color=WHITE),
            MathTex(r"\Leftrightarrow |x_1 + x_2| = 0 \text{ et } |x_1| = 0", color=WHITE),
            MathTex(r"\Leftrightarrow x_1 + x_2 = 0 \text{ et } x_1 = 0", color=WHITE),
            MathTex(r"\Leftrightarrow x_1 = 0 \text{ et } x_2 = 0", color=WHITE),
            MathTex(r"\Leftrightarrow \vec{X} = \vec{0}", color=GREEN)
        )
        step1_proof.arrange(DOWN, buff=0.2)
        step1_proof.next_to(step1_title, DOWN, buff=0.3)
        
        for line in step1_proof:
            self.play(Write(line), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        self.play(FadeOut(step1_title), FadeOut(step1_proof))
        
        # Étape 2: Homogénéité
        step2_title = Text("2. Homogénéité", font_size=32, color=RED, weight=BOLD)
        step2_title.next_to(vector_example, DOWN, buff=0.8)
        self.play(Write(step2_title))
        
        step2_proof = VGroup(
            MathTex(r"||\lambda \vec{X}|| = |\lambda x_1 + \lambda x_2| + |\lambda x_1|", color=WHITE),
            MathTex(r"= |\lambda| \cdot |x_1 + x_2| + |\lambda| \cdot |x_1|", color=WHITE),
            MathTex(r"= |\lambda| \cdot (|x_1 + x_2| + |x_1|)", color=WHITE),
            MathTex(r"= |\lambda| \cdot ||\vec{X}||", color=RED)
        )
        step2_proof.arrange(DOWN, buff=0.2)
        step2_proof.next_to(step2_title, DOWN, buff=0.3)
        
        for line in step2_proof:
            self.play(Write(line), run_time=1)
            self.wait(0.5)
        
        self.wait(2)
        self.play(FadeOut(step2_title), FadeOut(step2_proof))
        
        # Étape 3: Inégalité triangulaire
        step3_title = Text("3. Inégalité Triangulaire", font_size=32, color=PURPLE, weight=BOLD)
        step3_title.next_to(vector_example, DOWN, buff=0.8)
        self.play(Write(step3_title))
        
        step3_proof = VGroup(
            MathTex(r"||\vec{X} + \vec{Y}|| = |(x_1 + y_1) + (x_2 + y_2)| + |x_1 + y_1|", color=WHITE),
            MathTex(r"\leq |x_1 + x_2| + |y_1 + y_2| + |x_1| + |y_1|", color=WHITE),
            MathTex(r"= (|x_1 + x_2| + |x_1|) + (|y_1 + y_2| + |y_1|)", color=WHITE),
            MathTex(r"= ||\vec{X}|| + ||\vec{Y}||", color=PURPLE)
        )
        step3_proof.arrange(DOWN, buff=0.2)
        step3_proof.next_to(step3_title, DOWN, buff=0.3)
        
        for line in step3_proof:
            self.play(Write(line), run_time=1)
            self.wait(0.5)
        
        # Conclusion
        conclusion = Text("✓ C'est bien une norme !", font_size=32, color=GREEN, weight=BOLD)
        conclusion.next_to(step3_proof, DOWN, buff=0.8)
        self.play(Write(conclusion))
        
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))

class NormesMatriciellesSubordonnees(Scene):
    def construct(self):
        # Titre
        title = Text("Normes Matricielles Subordonnées", 
                    font_size=42, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Narration
        narration = Text("Comment une matrice transforme des vecteurs ?\nLa norme matricielle mesure l'étirement maximal.", 
                        font_size=24, color=WHITE)
        narration.next_to(title, DOWN, buff=0.5)
        self.play(Write(narration))
        self.wait(2)
        
        # Créer un système de coordonnées
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY}
        )
        axes.to_edge(LEFT)
        
        self.play(Create(axes))
        
        # Cercle unité
        unit_circle = Circle(radius=axes.x_axis.unit_size, color=BLUE, stroke_width=3)
        unit_circle.move_to(axes.c2p(0, 0))
        
        circle_label = Text("Cercle unité", font_size=20, color=BLUE)
        circle_label.next_to(unit_circle, DOWN, buff=0.3)
        
        self.play(Create(unit_circle), Write(circle_label))
        
        # Matrice exemple
        matrix_A = MathTex(r"A = \begin{pmatrix} -1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & -1 \end{pmatrix}", 
                          font_size=32, color=WHITE)
        matrix_A.to_edge(RIGHT).shift(UP * 2)
        self.play(Write(matrix_A))
        
        # Transformation du cercle (pour une matrice 2x2, on montre la projection)
        # Ici on montre conceptuellement l'effet de la matrice
        transform_circle = Circle(radius=axes.x_axis.unit_size, color=RED, stroke_width=3)
        transform_circle.move_to(axes.c2p(0, 0))
        
        # Animation de transformation
        self.play(Transform(unit_circle, transform_circle))
        
        # Calcul de la norme
        norm_calc = MathTex(r"||A||_\infty = \max_{1 \leq i \leq 3} \sum_{j=1}^{3} |a_{ij}|", 
                           font_size=24, color=WHITE)
        norm_calc.next_to(matrix_A, DOWN, buff=0.5)
        self.play(Write(norm_calc))
        
        # Résultat
        result = MathTex(r"||A||_\infty = \max\{|-1|, |1|, |-1|\} = 1", 
                        font_size=28, color=GREEN)
        result.next_to(norm_calc, DOWN, buff=0.5)
        self.play(Write(result))
        
        # Définition formelle
        definition = MathTex(r"||A|| = \sup_{||x|| = 1} ||Ax||", 
                            font_size=32, color=YELLOW)
        definition.next_to(result, DOWN, buff=0.8)
        self.play(Write(definition))
        
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))

class RayonSpectralValeursPropres(Scene):
    def construct(self):
        # Titre
        title = Text("Rayon Spectral et Valeurs Propres", 
                    font_size=42, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Narration
        narration = Text("Le rayon spectral est le max des |λ|, où λ est une valeur propre.", 
                        font_size=24, color=WHITE)
        narration.next_to(title, DOWN, buff=0.5)
        self.play(Write(narration))
        self.wait(2)
        
        # Définition
        definition = MathTex(r"\rho(A) = \max\{|\lambda| : \lambda \text{ valeur propre de } A\}", 
                            font_size=32, color=YELLOW)
        definition.next_to(narration, DOWN, buff=0.8)
        self.play(Write(definition))
        
        # Exemple
        example_title = Text("Exemple :", font_size=28, color=GREEN, weight=BOLD)
        example_title.next_to(definition, DOWN, buff=0.8)
        self.play(Write(example_title))
        
        # Matrice
        matrix_A = MathTex(r"A = \begin{pmatrix} 1 & 2 & 0 \\ -1 & 3 & 0 \\ 0 & 0 & -1 \end{pmatrix}", 
                          font_size=32, color=WHITE)
        matrix_A.next_to(example_title, DOWN, buff=0.5)
        self.play(Write(matrix_A))
        
        # Calcul du polynôme caractéristique
        poly_title = Text("Polynôme caractéristique :", font_size=24, color=WHITE)
        poly_title.next_to(matrix_A, DOWN, buff=0.8)
        self.play(Write(poly_title))
        
        # Déterminant
        det_matrix = MathTex(r"\det(A - \lambda I) = \begin{vmatrix} 1-\lambda & 2 & 0 \\ -1 & 3-\lambda & 0 \\ 0 & 0 & -1-\lambda \end{vmatrix}", 
                            font_size=24, color=WHITE)
        det_matrix.next_to(poly_title, DOWN, buff=0.3)
        self.play(Write(det_matrix))
        
        # Calcul par étapes
        calc_step1 = MathTex(r"= (-1-\lambda) \begin{vmatrix} 1-\lambda & 2 \\ -1 & 3-\lambda \end{vmatrix}", 
                            font_size=24, color=WHITE)
        calc_step1.next_to(det_matrix, DOWN, buff=0.3)
        self.play(Write(calc_step1))
        
        calc_step2 = MathTex(r"= (-1-\lambda)(\lambda^2 - 4\lambda + 5)", 
                            font_size=24, color=WHITE)
        calc_step2.next_to(calc_step1, DOWN, buff=0.3)
        self.play(Write(calc_step2))
        
        # Analyse des racines
        analysis = Text("λ² - 4λ + 5 n'a pas de solutions réelles (Δ < 0)", 
                       font_size=20, color=ORANGE)
        analysis.next_to(calc_step2, DOWN, buff=0.3)
        self.play(Write(analysis))
        
        # Résultat final
        result = MathTex(r"\rho(A) = \max\{|-1|\} = 1", 
                        font_size=32, color=GREEN)
        result.next_to(analysis, DOWN, buff=0.5)
        self.play(Write(result))
        
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))

class ComparaisonNormes(Scene):
    def construct(self):
        # Titre
        title = Text("Comparaison des Normes", 
                    font_size=42, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Question
        question = Text("Pourquoi choisir une norme plutôt qu'une autre ?", 
                       font_size=28, color=WHITE)
        question.next_to(title, DOWN, buff=0.5)
        self.play(Write(question))
        self.wait(1)
        
        # Créer un tableau de comparaison
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 4, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY}
        )
        axes.to_edge(LEFT)
        self.play(Create(axes))
        
        # Vecteur exemple
        vector_coords = [3, 2]
        vector = Arrow(axes.c2p(0, 0), axes.c2p(*vector_coords), 
                      color=YELLOW, stroke_width=6, buff=0)
        vector_label = MathTex(r"\vec{v} = \begin{pmatrix} 3 \\ 2 \end{pmatrix}", 
                              color=YELLOW)
        vector_label.next_to(axes.c2p(*vector_coords), UR)
        
        self.play(Create(vector), Write(vector_label))
        
        # Tableau des résultats
        table_title = Text("Résultats :", font_size=24, color=WHITE, weight=BOLD)
        table_title.to_edge(RIGHT).shift(UP * 2)
        self.play(Write(table_title))
        
        # Résultats pour chaque norme
        results = VGroup(
            MathTex(r"||v||_1 = 5", color=GREEN),
            MathTex(r"||v||_2 = \sqrt{13} \approx 3.6", color=RED),
            MathTex(r"||v||_\infty = 3", color=PURPLE)
        )
        results.arrange(DOWN, buff=0.5)
        results.next_to(table_title, DOWN, buff=0.5)
        
        for result in results:
            self.play(Write(result))
            self.wait(0.5)
        
        # Applications
        applications_title = Text("Applications :", font_size=24, color=WHITE, weight=BOLD)
        applications_title.next_to(results, DOWN, buff=0.8)
        self.play(Write(applications_title))
        
        applications = VGroup(
            Text("• Optimisation", font_size=20, color=GREEN),
            Text("• Analyse d'erreur", font_size=20, color=RED),
            Text("• Convergence", font_size=20, color=PURPLE),
            Text("• Stabilité numérique", font_size=20, color=ORANGE)
        )
        applications.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        applications.next_to(applications_title, DOWN, buff=0.3)
        
        for app in applications:
            self.play(Write(app))
            self.wait(0.5)
        
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))

class ContreExempleNormeNonSubordonnee(Scene):
    def construct(self):
        # Titre
        title = Text("Contre-exemple : Norme Non-Subordonnée", 
                    font_size=40, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Narration
        narration = Text("Attention ! Toutes les normes matricielles ne sont pas subordonnées !", 
                        font_size=24, color=RED, weight=BOLD)
        narration.next_to(title, DOWN, buff=0.5)
        self.play(Write(narration))
        self.wait(2)
        
        # Définition d'une norme non-subordonnée
        example_title = Text("Exemple de norme non-subordonnée :", font_size=28, color=YELLOW)
        example_title.next_to(narration, DOWN, buff=0.8)
        self.play(Write(example_title))
        
        # Norme de Frobenius
        frobenius_norm = MathTex(r"||A||_F = \sqrt{\sum_{i,j} |a_{ij}|^2}", 
                                font_size=32, color=WHITE)
        frobenius_norm.next_to(example_title, DOWN, buff=0.5)
        self.play(Write(frobenius_norm))
        
        # Contre-exemple
        counterexample_title = Text("Contre-exemple où ||AB|| > ||A|| ||B|| :", 
                                   font_size=24, color=RED)
        counterexample_title.next_to(frobenius_norm, DOWN, buff=0.8)
        self.play(Write(counterexample_title))
        
        # Matrices
        matrix_A = MathTex(r"A = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}", 
                          font_size=28, color=WHITE)
        matrix_B = MathTex(r"B = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}", 
                          font_size=28, color=WHITE)
        
        matrices = VGroup(matrix_A, matrix_B)
        matrices.arrange(RIGHT, buff=1)
        matrices.next_to(counterexample_title, DOWN, buff=0.5)
        self.play(Write(matrices))
        
        # Calcul du produit
        product = MathTex(r"AB = \begin{pmatrix} 1 & 1 \\ 0 & 0 \end{pmatrix}", 
                         font_size=28, color=WHITE)
        product.next_to(matrices, DOWN, buff=0.5)
        self.play(Write(product))
        
        # Calculs des normes
        norm_calculations = VGroup(
            MathTex(r"||A||_F = 1", color=GREEN),
            MathTex(r"||B||_F = 2", color=GREEN),
            MathTex(r"||AB||_F = \sqrt{2}", color=RED),
            MathTex(r"||A||_F \cdot ||B||_F = 2", color=GREEN)
        )
        norm_calculations.arrange(DOWN, buff=0.3)
        norm_calculations.next_to(product, DOWN, buff=0.5)
        
        for calc in norm_calculations:
            self.play(Write(calc))
            self.wait(0.5)
        
        # Conclusion
        conclusion = MathTex(r"\sqrt{2} \not\leq 2 \text{ mais } \sqrt{2} \approx 1.41 < 2", 
                            font_size=24, color=ORANGE)
        conclusion.next_to(norm_calculations, DOWN, buff=0.5)
        self.play(Write(conclusion))
        
        # Message final
        final_message = Text("La norme de Frobenius EST subordonnée !\nCeci était juste un exemple pédagogique.", 
                           font_size=20, color=GRAY)
        final_message.next_to(conclusion, DOWN, buff=0.5)
        self.play(Write(final_message))
        
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))

class ConclusionComplete(Scene):
    def construct(self):
        # Titre final
        title = Text("Récapitulatif : Normes Vectorielles et Matricielles", 
                    font_size=40, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Points clés avec animations
        points = [
            ("Normes vectorielles", "Mesurent la 'taille' des vecteurs", GREEN),
            ("Trois normes usuelles", "||·||₁, ||·||₂, ||·||∞", RED),
            ("Normes matricielles", "Mesurent l'amplification maximale", PURPLE),
            ("Rayon spectral", "Lié aux valeurs propres", ORANGE),
            ("Applications", "Analyse numérique, optimisation", YELLOW)
        ]
        
        point_objects = []
        for i, (titre, description, color) in enumerate(points):
            # Titre du point
            point_title = Text(titre, font_size=24, color=color, weight=BOLD)
            point_desc = Text(description, font_size=20, color=WHITE)
            
            point_group = VGroup(point_title, point_desc)
            point_group.arrange(DOWN, buff=0.1)
            
            if i == 0:
                point_group.next_to(title, DOWN, buff=1)
            else:
                point_group.next_to(point_objects[-1], DOWN, buff=0.5)
            
            point_objects.append(point_group)
            self.play(Write(point_group))
            self.wait(0.8)
        
        #