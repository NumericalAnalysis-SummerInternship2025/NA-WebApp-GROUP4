from manim import *
import numpy as np

class InterpolationClean(Scene):
    def construct(self):
        # Configuration couleurs propres
        self.bg_color = "#0F0F23"
        self.primary_color = "#00D4FF"
        self.secondary_color = "#FF6B6B"
        self.accent_color = "#4ECDC4"
        self.text_color = "#FFFFFF"
        self.grid_color = "#2A2A3A"
        
        # ÉTAPE 1: Titre principal - Simple et clair
        self.show_title()
        
        # ÉTAPE 2: Données - Tableau propre
        self.show_data_clean()
        
        # ÉTAPE 3: Graphique - Un seul élément à la fois
        self.show_graph_step_by_step()
        
        # ÉTAPE 4: Résultats - Comparaison claire
        self.show_results_comparison()
        
        # ÉTAPE 5: Conclusion
        self.show_final_conclusion()
    
    def show_title(self):
        """Titre principal simple et direct"""
        main_title = Text("INTERPOLATION", 
                         font_size=56, 
                         color=self.primary_color, 
                         weight=BOLD)
        
        subtitle = Text("Méthodes numériques d'approximation", 
                       font_size=28, 
                       color=self.text_color)
        subtitle.next_to(main_title, DOWN, buff=0.5)
        
        title_group = VGroup(main_title, subtitle)
        
        self.play(Write(main_title, run_time=1.5))
        self.play(Write(subtitle, run_time=1))
        self.wait(1.5)
        self.play(FadeOut(title_group))
    
    def show_data_clean(self):
        """Données présentées clairement"""
        data_title = Text("DONNÉES EXPÉRIMENTALES", 
                         font_size=40, 
                         color=self.accent_color, 
                         weight=BOLD)
        data_title.to_edge(UP, buff=1)
        
        # Tableau simple et lisible
        table_data = [
            ["Temps (s)", "Vitesse (m/s)"],
            ["0", "2.00"],
            ["10", "1.89"],
            ["20", "1.72"],
            ["30", "1.44"]
        ]
        
        table = Table(
            table_data,
            include_outer_lines=True,
            v_buff=0.6,
            h_buff=1.2,
            line_config={"color": self.text_color, "stroke_width": 2}
        ).scale(0.9)
        
        # Style du tableau
        for i in range(len(table_data)):
            for j in range(len(table_data[i])):
                cell = table.get_cell((i+1, j+1))
                if i == 0:  # En-tête
                    cell.set_fill(color=self.primary_color, opacity=0.8)
                    cell.set_color(WHITE)
                else:  # Données
                    cell.set_fill(color=self.grid_color, opacity=0.2)
                    cell.set_color(self.text_color)
        
        table.next_to(data_title, DOWN, buff=1)
        
        self.play(Write(data_title))
        self.play(Create(table, run_time=2))
        self.wait(2)
        self.play(FadeOut(data_title, table))
    
    def show_graph_step_by_step(self):
        """Graphique construit étape par étape"""
        # Titre de section
        graph_title = Text("VISUALISATION GRAPHIQUE", 
                          font_size=36, 
                          color=self.primary_color, 
                          weight=BOLD)
        graph_title.to_edge(UP, buff=0.5)
        
        self.play(Write(graph_title))
        
        # Axes propres et simples
        axes = Axes(
            x_range=[0, 35, 5],
            y_range=[1.3, 2.1, 0.2],
            axis_config={
                "include_numbers": True, 
                "font_size": 24, 
                "color": self.text_color
            },
            tips=True
        ).scale(0.9).center().shift(DOWN * 0.3)
        
        # Labels des axes - bien espacés
        x_label = Text("Temps (s)", font_size=28, color=self.text_color)
        x_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.5)
        
        y_label = Text("Vitesse (m/s)", font_size=28, color=self.text_color)
        y_label.rotate(90 * DEGREES)
        y_label.next_to(axes.y_axis.get_end(), UP, buff=0.5)
        
        self.play(Create(axes))
        self.play(Write(x_label), Write(y_label))
        
        # Points de données - UN PAR UN
        points = [(0, 2), (10, 1.89), (20, 1.72), (30, 1.44)]
        colors = [self.primary_color, self.accent_color, self.secondary_color, "#FFD93D"]
        
        dots = VGroup()
        
        for i, ((x, y), color) in enumerate(zip(points, colors)):
            dot = Dot(axes.c2p(x, y), color=color, radius=0.1)
            
            # Label PROPRE - bien positionné
            if i < 2:
                label_pos = UP
                buff_val = 0.4
            else:
                label_pos = DOWN
                buff_val = 0.4
            
            label = Text(f"({x}, {y})", font_size=20, color=color)
            label.next_to(dot, label_pos, buff=buff_val)
            
            dots.add(dot)
            
            self.play(Create(dot), Write(label), run_time=0.8)
        
        self.wait(1)
        
        # INTERPOLATION LINÉAIRE - Section dédiée
        self.show_linear_interpolation_clean(axes, graph_title)
        
        # INTERPOLATION POLYNOMIALE - Section dédiée
        self.show_polynomial_interpolation_clean(axes, graph_title)
        
        # Nettoyage
        self.play(FadeOut(*self.mobjects))
    
    def show_linear_interpolation_clean(self, axes, graph_title):
        """Interpolation linéaire - Section dédiée"""
        # Nouveau titre de section
        linear_title = Text("INTERPOLATION LINÉAIRE", 
                           font_size=32, 
                           color=self.secondary_color, 
                           weight=BOLD)
        linear_title.next_to(graph_title, DOWN, buff=0.3)
        
        self.play(Write(linear_title))
        
        # Ligne d'interpolation simple
        linear_func = lambda t: 1.89 + (1.72 - 1.89) * (t - 10) / (20 - 10)
        linear_graph = axes.plot(
            linear_func, 
            x_range=[10, 20], 
            color=self.secondary_color,
            stroke_width=6
        )
        
        self.play(Create(linear_graph, run_time=2))
        
        # Point d'interpolation t=15 - SEUL
        t_test = 15
        y_linear = linear_func(t_test)
        
        # Point visible
        test_point = Dot(axes.c2p(t_test, y_linear), 
                        color=WHITE, 
                        radius=0.12)
        
        # Formule CLAIRE et LISIBLE
        formula_text = f"V(15) = {y_linear:.3f} m/s"
        formula = Text(formula_text, 
                      font_size=28, 
                      color=WHITE,
                      weight=BOLD)
        formula.to_corner(DR, buff=1)
        
        self.play(Create(test_point))
        self.play(Write(formula))
        self.wait(2)
        
        # Nettoyage de cette section
        self.play(FadeOut(linear_title, linear_graph, test_point, formula))
    
    def show_polynomial_interpolation_clean(self, axes, graph_title):
        """Interpolation polynomiale - Section dédiée"""
        # Nouveau titre de section
        poly_title = Text("INTERPOLATION POLYNOMIALE", 
                         font_size=32, 
                         color=self.accent_color, 
                         weight=BOLD)
        poly_title.next_to(graph_title, DOWN, buff=0.3)
        
        self.play(Write(poly_title))
        
        # Courbe polynomiale
        poly_func = lambda t: -0.000357 * t**2 - 0.013643 * t + 1.978571
        poly_graph = axes.plot(
            poly_func, 
            x_range=[0, 30], 
            color=self.accent_color,
            stroke_width=6
        )
        
        self.play(Create(poly_graph, run_time=3))
        
        # Point d'interpolation t=15
        t_test = 15
        y_poly = poly_func(t_test)
        
        test_point = Dot(axes.c2p(t_test, y_poly), 
                        color=WHITE, 
                        radius=0.12)
        
        # Formule CLAIRE
        formula_text = f"V(15) = {y_poly:.3f} m/s"
        formula = Text(formula_text, 
                      font_size=28, 
                      color=WHITE,
                      weight=BOLD)
        formula.to_corner(DR, buff=1)
        
        self.play(Create(test_point))
        self.play(Write(formula))
        self.wait(2)
        
        # Nettoyage de cette section
        self.play(FadeOut(poly_title, poly_graph, test_point, formula))
    
    def show_results_comparison(self):
        """Comparaison des résultats - CLAIRE"""
        title = Text("COMPARAISON DES RÉSULTATS", 
                    font_size=40, 
                    color=self.primary_color, 
                    weight=BOLD)
        title.to_edge(UP, buff=1)
        
        # Résultats en colonnes PROPRES
        results = [
            ["Méthode", "Résultat pour V(15)"],
            ["Linéaire", "1.805 m/s"],
            ["Polynomiale", "1.694 m/s"],
            ["Différence", "0.111 m/s"]
        ]
        
        results_table = Table(
            results,
            include_outer_lines=True,
            v_buff=0.8,
            h_buff=1.5,
            line_config={"color": self.text_color, "stroke_width": 3}
        ).scale(1.1)
        
        # Style du tableau
        for i in range(len(results)):
            for j in range(len(results[i])):
                cell = results_table.get_cell((i+1, j+1))
                if i == 0:
                    cell.set_fill(color=self.primary_color, opacity=0.8)
                    cell.set_color(WHITE)
                elif i == 1:
                    cell.set_fill(color=self.secondary_color, opacity=0.3)
                    cell.set_color(self.text_color)
                elif i == 2:
                    cell.set_fill(color=self.accent_color, opacity=0.3)
                    cell.set_color(self.text_color)
                else:
                    cell.set_fill(color="#FFD93D", opacity=0.3)
                    cell.set_color(self.text_color)
        
        results_table.next_to(title, DOWN, buff=1)
        
        self.play(Write(title))
        self.play(Create(results_table, run_time=2))
        self.wait(3)
        self.play(FadeOut(title, results_table))
    
    def show_final_conclusion(self):
        """Conclusion finale - SIMPLE"""
        conclusion_title = Text("CONCLUSION", 
                               font_size=48, 
                               color=self.primary_color, 
                               weight=BOLD)
        conclusion_title.to_edge(UP, buff=1)
        
        # Points clés - ESPACÉS
        points = [
            "✓ Interpolation linéaire : Simple et rapide",
            "✓ Interpolation polynomiale : Plus précise",
            "✓ Choix selon le contexte d'application"
        ]
        
        conclusion_group = VGroup()
        for i, point in enumerate(points):
            text = Text(point, 
                       font_size=32, 
                       color=self.text_color)
            text.next_to(conclusion_title, DOWN, buff=1 + i * 1.2)
            conclusion_group.add(text)
        
        self.play(Write(conclusion_title))
        
        for text in conclusion_group:
            self.play(Write(text), run_time=1.5)
        
        self.wait(3)
        
        # Fin propre
        self.play(FadeOut(conclusion_title, conclusion_group))
        
        final_text = Text("FIN", 
                         font_size=64, 
                         color=self.primary_color, 
                         weight=BOLD)
        self.play(Write(final_text))
        self.wait(2)
        self.play(FadeOut(final_text))