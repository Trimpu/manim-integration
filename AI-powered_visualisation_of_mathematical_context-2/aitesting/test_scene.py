from manim import *

class HelloMathScene(Scene):
    def construct(self):
        text = Text("Hello, Math!")
        self.play(Write(text))
        self.wait(2)