from manim import *
import numpy as np
import cv2
import scipy.signal as signal

# remember
# in manim the width of the screen is 14.22
# the height of the screen is 8
# this means that one unit in manim is 1920/14.22 = 135.03 pixels

# the image is 32x32 pixels
# a unit is 135.03 pixels
# so to make the image 4 units wide we need to scale it by 135.03*4 = 540.12
# and divide by the initial width of the image (32)
IMG_SCALE = ((1920 / 14.22) * 4) / 32

# the kernel is 1x1 unit
# we have to consider that now une unit contains 8 pixels of the original image (32/4)
# so the kernel is 8x8 pixels
# we want the kernel to be 3x3 pixels
# so we have to scale it by 3/8
KERNEL_SCALE = 3 / 8


class Convolution(Scene):
    def construct(self):
        img = cv2.imread("cifar_example.png")

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        laplacian = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])

        convolved_image = signal.convolve2d(img, laplacian, mode="valid")

        # normalize convolved image to be between 0 and 255
        convolved_image = (convolved_image - np.min(convolved_image)) / (
            np.max(convolved_image) - np.min(convolved_image)
        )
        convolved_image = convolved_image * 255
        convolved_image = convolved_image.ravel()

        # plane = NumberPlane()
        # self.add(plane)

        # make the image a manim object

        img = ImageMobject(img)
        img.scale(IMG_SCALE)
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])

        square_length = 1

        square = Square(side_length=square_length, color=RED)

        v_line_1 = Line(
            [-square_length / 6, square_length / 2, 0],
            [-square_length / 6, -square_length / 2, 0],
            color=RED,
        )
        v_line_2 = Line(
            [square_length / 6, square_length / 2, 0],
            [square_length / 6, -square_length / 2, 0],
            color=RED,
        )
        h_line_1 = Line(
            [-square_length / 2, square_length / 6, 0],
            [square_length / 2, square_length / 6, 0],
            color=RED,
        )
        h_line_2 = Line(
            [-square_length / 2, -square_length / 6, 0],
            [square_length / 2, -square_length / 6, 0],
            color=RED,
        )

        # move the square to a specific x,y position
        self.play(FadeIn(img))

        self.play(img.animate.move_to([-3, 0, 0]))

        self.play(Create(square))
        self.play(Create(v_line_1), run_time=0.2)
        self.play(Create(v_line_2), run_time=0.2)
        self.play(Create(h_line_1), run_time=0.2)
        self.play(Create(h_line_2), run_time=0.2)

        kernel = VGroup(square, v_line_1, v_line_2, h_line_1, h_line_2)
        kernel.set_color(RED)
        # reduce the size of the square
        self.play(kernel.animate.scale(KERNEL_SCALE))
        self.play(
            kernel.animate.move_to(
                img.get_corner(UL)
                + [kernel.get_width() / 2, -kernel.get_height() / 2, 0]
            )
        )

        x = np.arange(
            -5 + kernel.get_width() / 2,
            -1 - kernel.get_width() / 3,
            kernel.get_width() / 3,
        )
        y = np.arange(
            2 - kernel.get_width() / 2,
            -2 + kernel.get_width() / 3,
            -kernel.get_width() / 3,
        )

        n_points_w = len(x)
        n_points_h = len(y)

        xm, ym = np.meshgrid(x, y, indexing="xy")

        xm = xm.ravel()
        ym = ym.ravel()

        tot_points = n_points_w * n_points_h

        for i in range(tot_points):
            color = convolved_image[i] / 255
            color = [color, color, color]
            color = rgb_to_color(color)

            pixel = Square(
                side_length=kernel.get_width() / 3,
                color=color,
                fill_opacity=1,
                stroke_width=0,
            )

            self.play(
                (kernel.animate.move_to([xm[i], ym[i], 0])),
                run_time=0.015,
            )

            pixel.set_fill(color=color, opacity=1)
            pixel.move_to(kernel.get_center() + [6, 0, 0])

            self.play(Create(pixel), run_time=0.015)

        color = convolved_image[-1] / 255
        color = [color, color, color]
        color = rgb_to_color(color)

        pixel = Square(
            side_length=kernel.get_width() / 3,
            color=color,
            fill_opacity=1,
            stroke_width=0,
        )

        pixel.set_fill(color=color, opacity=1)
        pixel.move_to(kernel.get_center() + [6 + kernel.get_width() / 3, 0, 0])
        self.play(Create(pixel), run_time=0.015)
