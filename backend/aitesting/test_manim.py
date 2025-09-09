from manim import *

class TestScene(Scene):
    def construct(self):
        # Create a simple title
        title = Text("Math Test", font_size=48)
        title.to_edge(UP)
        
        # Create a simple equation
        equation = MathTex("x^2 + 2x + 1 = (x + 1)^2")
        equation.scale(1.5)
        
        # Add animations
        self.play(Write(title))
        self.wait(1)
        self.play(Write(equation))
        self.wait(2)
