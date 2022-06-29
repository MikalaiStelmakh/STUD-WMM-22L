from math import radians
import moderngl
from numpy import float32
from pyrr import Matrix44, Vector4

from base_window import BaseWindowConfig


class RobotWindow(BaseWindowConfig):

    def __init__(self, **kwargs):
        super(RobotWindow, self).__init__(**kwargs)
        self.color_head = Vector4((1.0, 1.0, 1.0, 1.0))
        self.color_body = Vector4((0.0, 0.0, 0.0, 1.0))
        self.color_hand = Vector4((1.0, 0.5, 0.0, 1.0))
        self.color_leg = Vector4((0.5, 0.3, 0.1, 1.0))


    def model_load(self):
        self.sphere = self.load_scene("sphere.obj")
        self.cube = self.load_scene("cube.obj")
        self.vao_sphere = self.sphere.root_nodes[0].mesh.vao.instance(self.program)
        self.vao_cube = self.cube.root_nodes[0].mesh.vao.instance(self.program)

    def init_shaders_variables(self):
        self.obj_color = self.program["obj_color"]
        self.pvm_matrix = self.program["pvm_matrix"]


    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.8, 0.8, 0.8, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (-20.0, -15.0, 5.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
        )
        # Head
        self.create_sphere(self.calc_pvm_matrix(projection, lookat, Matrix44.from_translation((0.0, 0.0, 5.0))),
                           self.color_head.astype("f4"))
        # Body
        self.create_cube(self.calc_pvm_matrix(
                            projection, lookat,
                            Matrix44.from_translation((0.0, 0.0, 2.0)) * Matrix44.from_scale((1.0, 1.0, 2.0))
                            ),
                         self.color_body.astype("f4"))
        # Right hand
        self.create_cube(self.calc_pvm_matrix(
                            projection, lookat,
                            (Matrix44.from_translation((0.0, -3.0, 3.0)) * Matrix44.from_x_rotation(radians(45)) *
                             Matrix44.from_scale((0.5, 0.5, 1.25)))
                            ),
                        self.color_hand.astype("f4"))
        # Left hand
        self.create_cube(self.calc_pvm_matrix(
                            projection, lookat,
                            (Matrix44.from_translation((0.0, 3.0, 3.0)) * Matrix44.from_x_rotation(radians(-45)) *
                             Matrix44.from_scale((0.5, 0.5, 1.25)))
                            ),
                        self.color_hand.astype("f4"))
        # Right leg
        self.create_cube(self.calc_pvm_matrix(
                            projection, lookat,
                            (Matrix44.from_translation((0.0, -2.0, -1.5)) * Matrix44.from_x_rotation(radians(30)) *
                             Matrix44.from_scale((0.5, 0.5, 1.75)))
                            ),
                        self.color_leg.astype("f4"))
        # Left leg
        self.create_cube(self.calc_pvm_matrix(
                    projection, lookat,
                    (Matrix44.from_translation((0.0, 2.0, -1.5)) * Matrix44.from_x_rotation(radians(-30)) *
                        Matrix44.from_scale((0.5, 0.5, 1.75)))
                    ),
                self.color_leg.astype("f4"))

    def calc_pvm_matrix(self, projection: Matrix44, lookat: Matrix44,
                             model_matrix: Matrix44) -> Matrix44:
        return projection * lookat * model_matrix

    def create_cube(self, pvm_matrix: Matrix44, color: float32) -> None:
        self.pvm_matrix.write(pvm_matrix.astype("f4"))
        self.obj_color.write(color)
        self.vao_cube.render()

    def create_sphere(self, pvm_matrix: Matrix44, color: float32) -> None:
        self.pvm_matrix.write(pvm_matrix.astype("f4"))
        self.obj_color.write(color)
        self.vao_sphere.render()
