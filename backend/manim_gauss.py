from manim import *

class ImprovedGaussPivotAnimation(Scene):
    def construct(self):
        # Title
        title = Text("Élimination de Gauss avec Pivot Partiel", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.5)

        self.play(Write(title))
        self.wait(0.5)

        # Initial matrix
        matrix_title = Text("Matrice augmentée :", font_size=24, color=GREEN)
        matrix_title.shift(UP * 1.5)

        initial_matrix = MathTex(
            r"\begin{bmatrix} 2 & 1 & -1 & | & 8 \\ -3 & -1 & 2 & | & -11 \\ -2 & 1 & 2 & | & -3 \end{bmatrix}",
            font_size=28
        ).next_to(matrix_title, DOWN, buff=0.3)

        self.play(Write(matrix_title), Write(initial_matrix))
        self.wait(0.5)

        # Step 1: Pivot search
        step1_text = Text("ÉTAPE 1 : Recherche du pivot (colonne 1)", font_size=19, color=BLUE)
        step1_text.to_edge(DOWN, buff=0.5)

        self.play(Write(step1_text))
        self.wait(0.5)

        # Highlight first column and find maximum
        col1_highlight = VGroup(
            SurroundingRectangle(initial_matrix.get_part_by_tex("2"), color=YELLOW, buff=0.1),
            SurroundingRectangle(initial_matrix.get_part_by_tex("-3"), color=YELLOW, buff=0.1),
            SurroundingRectangle(initial_matrix.get_part_by_tex("-2"), color=YELLOW, buff=0.1)
        )

        max_text = Text("Maximum : |-3| = 3", font_size=20, color=RED).next_to(initial_matrix, DOWN, buff=0.5)
        exchange_text = Text("Échange : L₁ ↔ L₂", font_size=20, color=RED).next_to(max_text, DOWN, buff=0.3)

        self.play(Create(col1_highlight), Write(max_text), Write(exchange_text))
        self.wait(0.5)

        # New matrix after swap
        swapped_matrix = MathTex(
            r"\begin{bmatrix} -3 & -1 & 2 & | & -11 \\ 2 & 1 & -1 & | & 8 \\ -2 & 1 & 2 & | & -3 \end{bmatrix}",
            font_size=28
        ).move_to(initial_matrix.get_center())

        self.play(Transform(initial_matrix, swapped_matrix), FadeOut(col1_highlight, max_text, exchange_text))
        self.wait(0.5)

        # Step 2: Elimination
        step2_text = Text("ÉTAPE 2 : Élimination (colonne 1)", font_size=19, color=BLUE)
        step2_text.move_to(step1_text.get_center())

        self.play(Transform(step1_text, step2_text))
        self.wait(0.5)

        # Highlight pivot
        pivot_rect = SurroundingRectangle(initial_matrix.get_part_by_tex("-3"), color=GREEN, buff=0.1)
        pivot_label = Text("Pivot", font_size=18, color=GREEN).next_to(pivot_rect, UP, buff=0.1)

        self.play(Create(pivot_rect), Write(pivot_label))
        self.wait(0.5)

        # Multipliers
        multipliers = VGroup(
            MathTex(r"m_{21} = \frac{2}{-3} = -\frac{2}{3}", font_size=20, color=ORANGE),
            MathTex(r"m_{31} = \frac{-2}{-3} = \frac{2}{3}", font_size=20, color=ORANGE)
        ).arrange(DOWN, buff=0.2).next_to(initial_matrix, DOWN, buff=1)

        self.play(Write(multipliers))
        self.wait(0.5)

        # Row operations
        operations = VGroup(
            MathTex(r"L_2 \leftarrow L_2 - (-\frac{2}{3})L_1", font_size=20, color=PURPLE),
            MathTex(r"L_3 \leftarrow L_3 - \frac{2}{3}L_1", font_size=20, color=PURPLE)
        ).arrange(DOWN, buff=0.2).next_to(multipliers, DOWN, buff=0.3)

        self.play(Write(operations))
        self.wait(0.5)

        # New matrix after elimination
        eliminated_matrix = MathTex(
            r"\begin{bmatrix} -3 & -1 & 2 & | & -11 \\ 0 & \frac{1}{3} & \frac{1}{3} & | & \frac{2}{3} \\ 0 & \frac{5}{3} & \frac{10}{3} & | & \frac{19}{3} \end{bmatrix}",
            font_size=28
        ).move_to(initial_matrix.get_center())

        self.play(Transform(initial_matrix, eliminated_matrix), FadeOut(pivot_rect, pivot_label, multipliers, operations))
        self.wait(0.5)

        # Step 3: Second column pivot
        step3_text = Text("ÉTAPE 3 : Pivot dans la colonne 2", font_size=19, color=BLUE)
        step3_text.move_to(step1_text.get_center())

        self.play(Transform(step1_text, step3_text))
        self.wait(0.5)

        # Compare pivots
        comparison = Text("Comparaison : |1/3| = 0.33 vs |5/3| = 1.67", font_size=20, color=YELLOW)
        best_pivot = Text("Meilleur pivot : 5/3 (déjà en position)", font_size=20, color=GREEN)
        pivot_group = VGroup(comparison, best_pivot).arrange(DOWN, buff=0.2).next_to(initial_matrix, DOWN, buff=0.5)

        self.play(Write(pivot_group))
        self.wait(0.5)

        # Final multiplier and operation
        final_mult = MathTex(r"m_{32} = \frac{\frac{1}{3}}{\frac{5}{3}} = \frac{1}{5}", font_size=20, color=ORANGE)
        final_op = MathTex(r"L_3 \leftarrow L_3 - \frac{1}{5}L_2", font_size=20, color=PURPLE)
        final_group = VGroup(final_mult, final_op).arrange(DOWN, buff=0.2).next_to(pivot_group, DOWN, buff=0.3)

        self.play(Write(final_group))
        self.wait(0.5)

        # Final matrix
        final_matrix = MathTex(
            r"\begin{bmatrix} -3 & -1 & 2 & | & -11 \\ 0 & \frac{1}{3} & \frac{1}{3} & | & \frac{2}{3} \\ 0 & 0 & \frac{8}{3} & | & \frac{8}{3} \end{bmatrix}",
            font_size=28
        ).move_to(initial_matrix.get_center())

        self.play(Transform(initial_matrix, final_matrix), FadeOut(pivot_group, final_group))
        self.wait(0.5)

        # Step 4: Back substitution
        step4_text = Text("ÉTAPE 4 : Substitution arrière", font_size=19, color=BLUE)
        step4_text.move_to(step1_text.get_center())

        self.play(Transform(step1_text, step4_text))
        self.wait(0.5)

        # Solutions
        solutions = VGroup(
            MathTex(r"z = \frac{8/3}{8/3} = 1", font_size=20, color=GREEN),
            MathTex(r"y = \frac{2/3 - (1/3)(1)}{1/3} = 1", font_size=20, color=GREEN),
            MathTex(r"x = \frac{-11 - (-1)(1) - 2(1)}{-3} = 4", font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.2).next_to(initial_matrix, DOWN, buff=0.5)

        self.play(Write(solutions))
        self.wait(0.5)

        # Final solution
        final_solution = MathTex(r"\boxed{x = 4, \, y = 1, \, z = 1}", font_size=24, color=RED)
        final_solution.next_to(solutions, DOWN, buff=0.3)

        self.play(Write(final_solution))
        self.wait(1)

        # Fade out and final message
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob is not title], run_time=1)
        final_message = Text("Méthode terminée !", font_size=36, color=BLUE)
        self.play(Write(final_message))
        self.wait(2)