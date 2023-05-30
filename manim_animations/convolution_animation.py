from manim import *
import numpy as np


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(GREEN, opacity=0.5)
        self.play(Create(circle))


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        square = Square()
        square.rotate(PI / 4)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class AnimateSquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(ReplacementTransform(square, circle))
        self.play(FadeOut(square))
        self.play(circle.animate.set_fill(PINK, opacity=0.5))


class Convolution(Scene):
    def construct(self):
        square_length = 3

        square = Square(side_length=square_length)
        # resize the square to half of its original size
        # get top left corner of the square

        v_line_1 = Line(
            [-square_length / 6, square_length / 2, 0],
            [-square_length / 6, -square_length / 2, 0],
        )
        v_line_2 = Line(
            [square_length / 6, square_length / 2, 0],
            [square_length / 6, -square_length / 2, 0],
        )
        h_line_1 = Line(
            [-square_length / 2, square_length / 6, 0],
            [square_length / 2, square_length / 6, 0],
        )
        h_line_2 = Line(
            [-square_length / 2, -square_length / 6, 0],
            [square_length / 2, -square_length / 6, 0],
        )

        # move the square to a specific x,y position
        self.play(Create(square))
        self.play(Create(v_line_1), run_time=0.2)
        self.play(Create(v_line_2), run_time=0.2)
        self.play(Create(h_line_1), run_time=0.2)
        self.play(Create(h_line_2), run_time=0.2)

        kernel = VGroup(square, v_line_1, v_line_2, h_line_1, h_line_2)

        # reduce the size of the square
        self.play(kernel.animate.scale(0.3))
        self.play(kernel.animate.move_to([-3, 3, 0]))

        n_points_w = 3
        n_points_h = 3
        x = np.arange(-n_points_w, n_points_w, 1)
        y = np.arange(n_points_h, -n_points_h, -1)

        xm, ym = np.meshgrid(x, y, indexing="xy")

        xm = xm.ravel()
        ym = ym.ravel()

        tot_points = 2 * n_points_w * 2 * n_points_h

        for i in range(tot_points):
            self.play(kernel.animate.move_to([xm[i], ym[i], 0]), run_time=0.2)
