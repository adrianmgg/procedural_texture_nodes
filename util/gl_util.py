from typing import Union
import gpu
from mathutils import Matrix
import gpu_extras


# TODO give this a better name
class OffscreenRendering:
    def __init__(self, width: int, height: int, samples: int = 0):
        self.width = width
        self.height = height
        self.samples = samples
        self._offscreen: Union[gpu.types.GPUOffScreen, None] = None

    def __enter__(self):
        self._offscreen = gpu.types.GPUOffScreen(self.width, self.height, self.samples)
        self._offscreen.bind()
        gpu.matrix.load_matrix(Matrix.Identity(4))
        gpu.matrix.load_projection_matrix(Matrix.Identity(4))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._offscreen.unbind()
        self._offscreen.free()


class OffscreenRender2DShader(OffscreenRendering):
    __vertex_shader = '''\
in vec2 pos;
in vec2 uv;

out vec2 uvInterp;

void main()
{
    uvInterp = uv;
    gl_Position = vec4(pos, 0.0, 1.0);
}
'''

    def __init__(self, width: int, height: int, fragment_shader: str, samples: int = 0):
        super().__init__(width, height, samples)
        self.shader = gpu.types.GPUShader(
            OffscreenRender2DShader.__vertex_shader,
            fragment_shader
        )
        self.batch: gpu.types.GPUBatch = gpu_extras.batch.batch_for_shader(
            self.shader,
            'TRI_FAN',
            {
                "pos": ((-1, -1), (1, -1), (1, 1), (-1, 1)),
                "uv": ((0, 0), (1, 0), (1, 1), (0, 1)),
            }
        )

    def draw_shader(self):
        self.batch.draw(self.shader)
