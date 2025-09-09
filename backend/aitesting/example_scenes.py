"""
Example: Manual Manim Scene
This shows what kind of code the AI generates for mathematical visualizations.
You can run this directly to see a sample output without needing GitHub AI.
"""

from manim import *

class PythagoreanTheoremExample(Scene):
    def construct(self):
        # Title
        title = Text("Pythagorean Theorem", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Create a right triangle
        triangle = Polygon(
            [0, 0, 0],      # Origin
            [3, 0, 0],      # Right side (3 units)
            [0, 4, 0],      # Up side (4 units)
            color=WHITE,
            fill_opacity=0.3,
            fill_color=BLUE
        )
        triangle.move_to(ORIGIN).shift(DOWN*0.5)
        
        # Draw the triangle
        self.play(Create(triangle))
        self.wait(1)
        
        # Label the sides
        a_label = MathTex("a = 3", color=GREEN).next_to(triangle, DOWN).shift(RIGHT*1.5)
        b_label = MathTex("b = 4", color=GREEN).next_to(triangle, LEFT).shift(UP*2)
        c_label = MathTex("c = ?", color=RED).next_to(triangle, RIGHT).shift(UP*0.5 + LEFT*0.5)
        
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(2)
        
        # Show the theorem
        theorem = MathTex("a^2 + b^2 = c^2", font_size=36, color=YELLOW)
        theorem.to_edge(DOWN).shift(UP*2)
        self.play(Write(theorem))
        self.wait(2)
        
        # Substitute values
        substitution = MathTex("3^2 + 4^2 = c^2", font_size=36, color=YELLOW)
        substitution.next_to(theorem, DOWN)
        self.play(Write(substitution))
        self.wait(1)
        
        # Calculate
        calculation = MathTex("9 + 16 = c^2", font_size=36, color=YELLOW)
        calculation.next_to(substitution, DOWN)
        self.play(Write(calculation))
        self.wait(1)
        
        # Final result
        result = MathTex("25 = c^2", font_size=36, color=YELLOW)
        result.next_to(calculation, DOWN)
        self.play(Write(result))
        self.wait(1)
        
        # Answer
        answer = MathTex("c = 5", font_size=36, color=GREEN)
        answer.next_to(result, DOWN)
        self.play(Write(answer))
        
        # Update the c label
        new_c_label = MathTex("c = 5", color=GREEN).next_to(triangle, RIGHT).shift(UP*0.5 + LEFT*0.5)
        self.play(Transform(c_label, new_c_label))
        
        # Add visual squares to show areas
        square_a = Square(side_length=1, color=RED, fill_opacity=0.5).next_to(triangle, DOWN).shift(LEFT*2)
        square_a_label = MathTex("a^2 = 9", font_size=24).next_to(square_a, DOWN)
        
        square_b = Square(side_length=1.33, color=GREEN, fill_opacity=0.5).next_to(square_a, RIGHT).shift(RIGHT*0.5)
        square_b_label = MathTex("b^2 = 16", font_size=24).next_to(square_b, DOWN)
        
        square_c = Square(side_length=1.67, color=BLUE, fill_opacity=0.5).next_to(square_b, RIGHT).shift(RIGHT*0.5)
        square_c_label = MathTex("c^2 = 25", font_size=24).next_to(square_c, DOWN)
        
        self.play(
            Create(square_a), Write(square_a_label),
            Create(square_b), Write(square_b_label),
            Create(square_c), Write(square_c_label)
        )
        
        self.wait(3)
        
        # Conclusion
        conclusion = Text("The Pythagorean Theorem proved!", font_size=32, color=GOLD)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)


class QuadraticFunctionExample(Scene):
    def construct(self):
        # Title
        title = Text("Quadratic Functions", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 8, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": WHITE},
            tips=False
        )
        axes.center()
        
        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        
        # General form
        general_form = MathTex("f(x) = ax^2 + bx + c", font_size=36, color=YELLOW)
        general_form.to_corner(UL).shift(DOWN*0.5)
        self.play(Write(general_form))
        self.wait(1)
        
        # Specific example
        specific = MathTex("f(x) = x^2 - 2x + 1", font_size=32, color=GREEN)
        specific.next_to(general_form, DOWN)
        self.play(Write(specific))
        self.wait(1)
        
        # Create the parabola
        parabola = axes.plot(lambda x: x**2 - 2*x + 1, color=BLUE, x_range=[-2, 4])
        self.play(Create(parabola))
        self.wait(1)
        
        # Mark the vertex
        vertex_point = axes.coords_to_point(1, 0)
        vertex_dot = Dot(vertex_point, color=RED, radius=0.1)
        vertex_label = MathTex("Vertex (1, 0)", font_size=24, color=RED)
        vertex_label.next_to(vertex_dot, DOWN + RIGHT)
        
        self.play(Create(vertex_dot), Write(vertex_label))
        self.wait(1)
        
        # Show vertex formula
        vertex_formula = MathTex("Vertex: x = -\\frac{b}{2a}", font_size=28, color=ORANGE)
        vertex_formula.to_corner(UR).shift(DOWN*1)
        self.play(Write(vertex_formula))
        
        # Calculate vertex
        vertex_calc = MathTex("x = -\\frac{(-2)}{2(1)} = 1", font_size=24, color=ORANGE)
        vertex_calc.next_to(vertex_formula, DOWN)
        self.play(Write(vertex_calc))
        self.wait(2)
        
        # Show direction of opening
        direction = Text("Opens upward (a > 0)", font_size=24, color=PURPLE)
        direction.to_corner(DR)
        self.play(Write(direction))
        self.wait(2)


if __name__ == "__main__":
    # This is how you would render these scenes manually
    # Run: manim example_scenes.py PythagoreanTheoremExample --medium_quality
    # Run: manim example_scenes.py QuadraticFunctionExample --medium_quality
    print("Example Manim scenes for mathematical visualization")
    print("To render:")
    print("1. D:/VSCODE/aitesting/.venv/Scripts/python.exe -m manim example_scenes.py PythagoreanTheoremExample --medium_quality")
    print("2. D:/VSCODE/aitesting/.venv/Scripts/python.exe -m manim example_scenes.py QuadraticFunctionExample --medium_quality")
