from manim import *

class InterpolationNewton(Scene):
    def construct(self):
        # Titre
        title = Text("Méthode d’Interpolation de Newton").scale(1.2).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Présentation de la formule générale
        formula = MathTex(
            r"P_n(x) = \sum_{i=0}^n \beta_i \, \omega_i(x)"
        )
        formula.next_to(title, DOWN, buff=0.8)
        self.play(Write(formula))
        self.wait(2)

        # Explication de omega_i(x)
        omega_def = MathTex(
            r"\omega_i(x) = \prod_{j=0}^{i-1} (x - x_j), \quad \text{avec} \quad \omega_0(x)=1"
        )
        omega_def.next_to(formula, DOWN, buff=0.8)
        self.play(Write(omega_def))
        self.wait(3)

        # Présenter les points d'exemple
        points_text = Text("Exemple : points {(x_i, y_i)}").scale(0.8).to_edge(LEFT).shift(DOWN)
        self.play(Write(points_text))
        self.wait(1)

        # Définir les points
        points = [
            {"x": -1, "y": 2},
            {"x": 0, "y": 1},
            {"x": 1, "y": -1}
        ]

        # Afficher les points
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 3, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True}
        ).to_edge(RIGHT)

        # Labels
        labels = VGroup()
        for p in points:
            dot = Dot(point=axes.c2p(p["x"], p["y"]), color=YELLOW)
            label = MathTex(f"({p['x']},{p['y']})").next_to(dot, UP, buff=0.1)
            labels.add(VGroup(dot, label))
            self.play(Create(dot), Write(label))
        self.wait(1)

        self.play(Create(axes))
        self.wait(1)

        # Montrer les points sur l'axe
        self.play(*[Indicate(dot) for dot in labels[::2]])
        self.wait(1)

        # Calcul étape par étape des coefficients beta_i
        # Place all math expressions in a VGroup for vertical arrangement
        beta0 = MathTex(r"\beta_0 = y_0 = 2").scale(0.8)
        omega0 = MathTex(r"\omega_0(x)=1").scale(0.8)
        beta1_expr = MathTex(
            r"\beta_1 = \frac{y_1 - y_0}{x_1 - x_0} = \frac{" + str(y1) + " - " + str(y0) + "}{" + str(x1) + " - " + str(x0) + "} = -1"
        ).scale(0.8)
        omega1_eq = MathTex(r"\omega_1(x) = (x - x_0) = (x + 1)").scale(0.8)
        numerator = f"({y2} - {y1})/({x2} - {x0}) - ({y1} - {y0})/({x1} - {x0})"
        beta2_expr = MathTex(
            r"\beta_2 = \frac{" + numerator + "}{" + str(x2) + " - " + str(x0) + "}"
        ).scale(0.8)
        beta2_num = MathTex(r"\beta_2 \approx -0.5").scale(0.8)
        poly_expr = MathTex(
            r"P_2(x) = \beta_0 + \beta_1 (x - x_0) + \beta_2 (x - x_0)(x - x_1)"
        ).scale(0.8)

        # Arrange all math vertically, left side
        math_steps = VGroup(
            beta0,
            omega0,
            beta1_expr,
            omega1_eq,
            beta2_expr,
            beta2_num,
            poly_expr
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).to_edge(LEFT, buff=0.7)

        # Show each step one by one, keeping previous visible
        self.play(Write(beta0))
        self.wait(1)
        self.play(Write(omega0))
        self.wait(1)
        self.play(Write(beta1_expr))
        self.wait(1)
        self.play(Write(omega1_eq))
        self.wait(1)
        self.play(Write(beta2_expr))
        self.wait(1)
        self.play(Write(beta2_num))
        self.wait(1)
        self.play(Write(poly_expr))
        self.wait(2)

        # Illustration graphique
        # Now define P(x) with correct values
        def P(x):
            return y0 + beta1_value * (x - x0) + beta2_value * (x - x0) * (x - x1)

        # Tracer la courbe P(x)
        graph = axes.plot(lambda x: P(x), color=RED, x_range=[-2, 2])
        self.play(Create(graph))
        self.wait(2)

        # Montrer le polynôme sur l'axe
        label_poly = MathTex(r"P_2(x)").next_to(graph, UP)
        self.play(Write(label_poly))
        self.wait(2)

        # Résumé final
        conclusion = Text("Le polynôme d'interpolation de Newton est construit étape par étape.\n"
                          "Les coefficients sont calculés via les différences divisées.", font_size=20)
        conclusion.to_edge(DOWN)
        self.play(Transform(title, conclusion))
        self.wait(3)

        # Fin
        self.play(FadeOut(Group(title, axes, labels, graph, formula, omega_def, beta0, beta1_expr, omega1_eq, beta2_expr, beta2_num, poly_expr, label_poly, conclusion)))
        self.wait(1)
