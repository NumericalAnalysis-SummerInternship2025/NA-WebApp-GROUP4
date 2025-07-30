from manim import *

class LUDecompositionAnimation(Scene):
    def construct(self):
        # Ajout de l'audio
        self.add_sound("assets/sounds/lu2.mp3")
        
        # Configuration des couleurs pour différents éléments
        primary_color = BLUE
        secondary_color = GREEN
        highlight_color = YELLOW
        solution_color = RED
        
        # Titre principal
        title = Text("Décomposition LU - Méthode Complète", font_size=36)
        title.set_color(primary_color)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.scale(0.7).to_edge(UP))
        
        # Introduction du problème
        intro_text = Text("Résolvons le système d'équations linéaires:", font_size=24)
        intro_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(intro_text))
        self.wait(1)
        
        # Système d'équations original
        system = MathTex(
            r"\begin{cases}"
            r"3x_1 + x_2 + x_3 = 1 \\"
            r"x_1 - 3x_2 + x_3 = -3 \\"
            r"x_1 + x_2 - 3x_3 = 1"
            r"\end{cases}"
        ).scale(0.8)
        system.next_to(intro_text, DOWN, buff=0.8)
        self.play(Write(system))
        self.wait(2)
        
        # Transformation en forme matricielle
        matrix_text = Text("Forme matricielle: AX = b", font_size=24)
        matrix_text.next_to(system, DOWN, buff=0.8)
        self.play(Write(matrix_text))
        
        matrix_form = MathTex(
            r"\begin{pmatrix}"
            r"3 & 1 & 1 \\"
            r"1 & -3 & 1 \\"
            r"1 & 1 & -3"
            r"\end{pmatrix}"
            r"\begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}"
            r"= \begin{pmatrix} 1 \\ -3 \\ 1 \end{pmatrix}"
        ).scale(0.8)
        matrix_form.next_to(matrix_text, DOWN, buff=0.5)
        self.play(Write(matrix_form))
        self.wait(3)
        
        # Nettoyage de l'écran
        self.play(
            FadeOut(intro_text), FadeOut(system), 
            FadeOut(matrix_text), FadeOut(matrix_form)
        )
        
        # ÉTAPE 1: Explication de la décomposition LU
        step1_title = Text("ÉTAPE 1: Comprendre la décomposition LU", font_size=28)
        step1_title.set_color(primary_color)
        step1_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(step1_title))
        
        explanation = Text("A = L × U", font_size=24)
        explanation.next_to(step1_title, DOWN, buff=0.5)
        self.play(Write(explanation))
        
        # Explication des matrices L et U
        l_explanation = Text("L: Matrice triangulaire inférieure", font_size=20)
        l_explanation.next_to(explanation, DOWN, buff=0.3).shift(LEFT * 2)
        u_explanation = Text("U: Matrice triangulaire supérieure", font_size=20)
        u_explanation.next_to(explanation, DOWN, buff=0.3).shift(RIGHT * 2)
        
        self.play(Write(l_explanation), Write(u_explanation))
        self.wait(2)
        
        # Montrer la forme générale
        general_form = MathTex(
            r"A = \begin{pmatrix}"
            r"l_{11} & 0 & 0 \\"
            r"l_{21} & l_{22} & 0 \\"
            r"l_{31} & l_{32} & l_{33}"
            r"\end{pmatrix}"
            r"\begin{pmatrix}"
            r"u_{11} & u_{12} & u_{13} \\"
            r"0 & u_{22} & u_{23} \\"
            r"0 & 0 & u_{33}"
            r"\end{pmatrix}"
        ).scale(0.7)
        general_form.next_to(u_explanation, DOWN, buff=0.8)
        self.play(Write(general_form))
        self.wait(3)
        
        # Nettoyage
        self.play(
            FadeOut(step1_title), FadeOut(explanation),
            FadeOut(l_explanation), FadeOut(u_explanation),
            FadeOut(general_form)
        )
        
        # ÉTAPE 2: Calcul de la décomposition LU
        step2_title = Text("ÉTAPE 2: Calculer L et U", font_size=28)
        step2_title.set_color(primary_color)
        step2_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(step2_title))
        
        # Matrice A originale
        original_a = MathTex(
            r"A = \begin{pmatrix}"
            r"3 & 1 & 1 \\"
            r"1 & -3 & 1 \\"
            r"1 & 1 & -3"
            r"\end{pmatrix}"
        ).scale(0.8)
        original_a.next_to(step2_title, DOWN, buff=0.8)
        self.play(Write(original_a))
        self.wait(1)
        
        # Processus d'élimination de Gauss (simplifié pour l'animation)
        process_text = Text("Utilisation de l'élimination de Gauss avec pivots partiels", font_size=20)
        process_text.next_to(original_a, DOWN, buff=0.5)
        self.play(Write(process_text))
        self.wait(2)
        
        # Résultat de la décomposition
        lu_result = MathTex(
            r"L = \begin{pmatrix}"
            r"1 & 0 & 0 \\"
            r"\frac{1}{3} & 1 & 0 \\"
            r"\frac{1}{3} & \frac{2}{10} & 1"
            r"\end{pmatrix}"
            r", \quad U = \begin{pmatrix}"
            r"3 & 1 & 1 \\"
            r"0 & -\frac{10}{3} & \frac{2}{3} \\"
            r"0 & 0 & -\frac{8}{3}"
            r"\end{pmatrix}"
        ).scale(0.6)
        lu_result.next_to(process_text, DOWN, buff=0.8)
        self.play(Write(lu_result))
        self.wait(3)
        
        # Nettoyage
        self.play(
            FadeOut(step2_title), FadeOut(original_a),
            FadeOut(process_text), FadeOut(lu_result)
        )
        
        # ÉTAPE 3: Résolution de LY = b (Substitution avant)
        step3_title = Text("ÉTAPE 3: Résoudre LY = b (Substitution avant)", font_size=26)
        step3_title.set_color(secondary_color)
        step3_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(step3_title))
        
        # Équation LY = b
        ly_system = MathTex(
            r"\begin{pmatrix}"
            r"1 & 0 & 0 \\"
            r"\frac{1}{3} & 1 & 0 \\"
            r"\frac{1}{3} & \frac{2}{10} & 1"
            r"\end{pmatrix}"
            r"\begin{pmatrix} y_1 \\ y_2 \\ y_3 \end{pmatrix}"
            r"= \begin{pmatrix} 1 \\ -3 \\ 1 \end{pmatrix}"
        ).scale(0.6)
        ly_system.next_to(step3_title, DOWN, buff=0.4)
        self.play(Write(ly_system))
        self.wait(1)
        
        # Calculs étape par étape
        calc_text = Text("Calculs:", font_size=20)
        calc_text.next_to(ly_system, DOWN, buff=0.3)
        self.play(Write(calc_text))
        
        # y1 = 1
        y1_calc = MathTex(r"y_1 = 1").scale(0.7)
        y1_calc.next_to(calc_text, DOWN, buff=0.2)
        self.play(Write(y1_calc))
        self.wait(1)
        
        # y2 = -3 - (1/3)*1 = -10/3
        y2_calc = MathTex(r"y_2 = -3 - \frac{1}{3} \times 1 = -\frac{10}{3}").scale(0.6)
        y2_calc.next_to(y1_calc, DOWN, buff=0.2)
        self.play(Write(y2_calc))
        self.wait(1)
        
        # y3 calculé correctement
        y3_calc = MathTex(r"y_3 = 1 - \frac{1}{3} - \frac{2}{10} \times (-\frac{10}{3}) = 0").scale(0.5)
        y3_calc.next_to(y2_calc, DOWN, buff=0.2)
        self.play(Write(y3_calc))
        self.wait(2)
        
        # Solution Y
        y_solution = MathTex(
            r"Y = \begin{pmatrix} 1 \\ -\frac{10}{3} \\ 0 \end{pmatrix}"
        ).scale(0.7)
        y_solution.next_to(y3_calc, DOWN, buff=0.3)
        y_solution.set_color(solution_color)
        self.play(Write(y_solution))
        self.wait(2)
        
        # Nettoyage
        self.play(
            FadeOut(step3_title), FadeOut(ly_system),
            FadeOut(calc_text), FadeOut(y1_calc),
            FadeOut(y2_calc), FadeOut(y3_calc), FadeOut(y_solution)
        )
        
        # ÉTAPE 4: Résolution de UX = Y (Substitution arrière)
        step4_title = Text("ÉTAPE 4: Résoudre UX = Y (Substitution arrière)", font_size=26)
        step4_title.set_color(secondary_color)
        step4_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(step4_title))
        
        # Équation UX = Y
        ux_system = MathTex(
            r"\begin{pmatrix}"
            r"3 & 1 & 1 \\"
            r"0 & -\frac{10}{3} & \frac{2}{3} \\"
            r"0 & 0 & -\frac{8}{3}"
            r"\end{pmatrix}"
            r"\begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}"
            r"= \begin{pmatrix} 1 \\ -\frac{10}{3} \\ 0 \end{pmatrix}"
        ).scale(0.6)
        ux_system.next_to(step4_title, DOWN, buff=0.4)
        self.play(Write(ux_system))
        self.wait(1)
        
        # Calculs de substitution arrière
        back_calc_text = Text("Calculs:", font_size=20)
        back_calc_text.next_to(ux_system, DOWN, buff=0.3)
        self.play(Write(back_calc_text))
        
        # x3 = 0 / (-8/3) = 0
        x3_calc = MathTex(r"x_3 = \frac{0}{-\frac{8}{3}} = 0").scale(0.7)
        x3_calc.next_to(back_calc_text, DOWN, buff=0.2)
        self.play(Write(x3_calc))
        self.wait(1)
        
        # x2 = (-10/3 - (2/3)*0) / (-10/3) = 1
        x2_calc = MathTex(r"x_2 = \frac{-\frac{10}{3}}{-\frac{10}{3}} = 1").scale(0.6)
        x2_calc.next_to(x3_calc, DOWN, buff=0.2)
        self.play(Write(x2_calc))
        self.wait(1)
        
        # x1 = (1 - 1*1 - 1*0) / 3 = 0
        x1_calc = MathTex(r"x_1 = \frac{1 - 1 - 0}{3} = 0").scale(0.6)
        x1_calc.next_to(x2_calc, DOWN, buff=0.2)
        self.play(Write(x1_calc))
        self.wait(2)
        
        # Solution finale
        final_solution = MathTex(
            r"X = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}"
        ).scale(0.8)
        final_solution.next_to(x1_calc, DOWN, buff=0.1)
        final_solution.set_color(solution_color)
        self.play(Write(final_solution))
        self.wait(1)
        
        # Encadrer la solution
        solution_box = SurroundingRectangle(final_solution, color=solution_color, buff=0.1)
        self.play(Create(solution_box))
        self.wait(1)
        
        # Vérification
        verification_text = Text("Solution: x₁ = 0, x₂ = 1, x₃ = 0", font_size=18)
        verification_text.next_to(solution_box, DOWN, buff=0.1)
        verification_text.set_color(highlight_color)
        self.play(Write(verification_text))
        self.wait(1)
        
        # Résumé final
        self.play(
            FadeOut(step4_title), FadeOut(ux_system),
            FadeOut(back_calc_text), FadeOut(x3_calc),
            FadeOut(x2_calc), FadeOut(x1_calc),
            FadeOut(final_solution), FadeOut(solution_box),
            FadeOut(verification_text)
        )
        
        summary_title = Text("Résumé de la méthode LU", font_size=28)
        summary_title.set_color(primary_color)
        summary_title.next_to(title, DOWN, buff=0.5)
        
        summary_steps = VGroup(
            Text("1. Décomposer A = LU", font_size=20),
            Text("2. Résoudre LY = b (substitution avant)", font_size=20),
            Text("3. Résoudre UX = Y (substitution arrière)", font_size=20)
        ).arrange(DOWN, buff=0.3)
        summary_steps.next_to(summary_title, DOWN, buff=0.8)
        
        self.play(Write(summary_title))
        self.play(Write(summary_steps))
        self.wait(2)
        
        # Avantages de la méthode
        advantages_text = Text("Avantages: Efficace pour résoudre plusieurs systèmes avec la même matrice A", 
                              font_size=18)
        advantages_text.next_to(summary_steps, DOWN, buff=0.8)
        self.play(Write(advantages_text))
        self.wait(3)
        
        # Fin de l'animation
        self.play(
            FadeOut(summary_title),
            FadeOut(summary_steps), 
            FadeOut(advantages_text),
            FadeOut(title)
        )
        
        # Message final
        final_message = Text("Merci pour votre attention!", font_size=36)
        final_message.set_color(primary_color)
        self.play(Write(final_message))
        self.wait(2)
        self.play(FadeOut(final_message))