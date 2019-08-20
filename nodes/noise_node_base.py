import bgl
import bpy
from gpu_extras.presets import draw_circle_2d

from .. import categories
from .. import events
from ..base_types.node import ProceduralTextureNode
from ..data import buffer as buffer_manager
from ..registration import register_node
from ..sockets.buffer_socket import BufferSocket
from ..util.gl_util import OffscreenRender2DShader


def dimensions_changed(node: 'NoiseNodeBase', context: bpy.types.Context):
    buffer_manager.replace_instance(
        key=node.buffer_id,
        buffer_type=bgl.GL_BYTE,
        dimensions=4 * node.image_width * node.image_height
    )
    events.node_property_update(node, context)


def noise_node(idname, label, fragment_shader):
    @register_node(category=categories.noise_nodes)
    class NoiseNodeBase(ProceduralTextureNode):
        bl_idname = idname
        bl_label = label
        image_width: bpy.props.IntProperty(default=1024, min=1, update=dimensions_changed)
        image_height: bpy.props.IntProperty(default=1024, min=1, update=dimensions_changed)

        buffer_id: bpy.props.IntProperty(default=-1)

        def __init_subclass__(cls, **kwargs):
            cls.__annotations__['image_width'] = NoiseNodeBase.__annotations__['image_width']
            cls.__annotations__['image_height'] = NoiseNodeBase.__annotations__['image_height']

        def init(self, context: bpy.types.Context):
            self.buffer_id = buffer_manager.new_instance(
                buffer_type=bgl.GL_BYTE,
                dimensions=4 * self.image_width * self.image_height
            )
            self.outputs.new(BufferSocket.bl_idname, name='Output')
            super().init_post()

        def draw_buttons(self, context, layout):
            layout.prop(self, 'image_width', text='Width')
            layout.prop(self, 'image_height', text='Height')

        def recalculateOutputs(self):
            buffer_output: BufferSocket = self.outputs.get('Output')
            buffer_output.set_buffer_id(self.buffer_id)
            buffer_output.width = self.image_width
            buffer_output.height = self.image_height
            if self.buffer_id is not -1:
                with OffscreenRender2DShader(self.image_width, self.image_height, fragment_shader=fragment_shader) \
                        as offscreen:
                    offscreen.draw_shader()

                    buffer = buffer_manager.get_instance(self.buffer_id)
                    bgl.glReadBuffer(bgl.GL_BACK)
                    bgl.glReadPixels(0, 0, self.image_width, self.image_height, bgl.GL_RGBA, bgl.GL_UNSIGNED_BYTE,
                                     buffer)

        def free(self):
            buffer_manager.free_instance(self.buffer_id)


noise_node(
    idname='ProceduralTexture_Node_Noise_Perlin',
    label='Perlin Noise',
    fragment_shader='''
    #define M_PI 3.14159265358979323846
in vec2 uvInterp;

float rand(vec2 c){
    return fract(sin(dot(c.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

float noise(vec2 p, float freq ){
    float unit = 1.0/freq;
    vec2 ij = floor(p/unit);
    vec2 xy = mod(p,unit)/unit;
    //xy = 3.*xy*xy-2.*xy*xy*xy;
    xy = .5*(1.-cos(M_PI*xy));
    float a = rand((ij+vec2(0.,0.)));
    float b = rand((ij+vec2(1.,0.)));
    float c = rand((ij+vec2(0.,1.)));
    float d = rand((ij+vec2(1.,1.)));
    float x1 = mix(a, b, xy.x);
    float x2 = mix(c, d, xy.x);
    return mix(x1, x2, xy.y);
}

float pNoise(vec2 p, int res){
    float persistance = .5;
    float n = 0.;
    float normK = 0.;
    float f = 4.;
    float amp = 1.;
    int iCount = 0;
    for (int i = 0; i<50; i++){
        n+=amp*noise(p, f);
        f*=2.;
        normK+=amp;
        amp*=persistance;
        if (iCount == res) break;
        iCount++;
    }
    float nf = n/normK;
    return nf*nf*nf*nf;
}

void main(){
    float value = pNoise(uvInterp, 2);
    gl_FragColor = vec4(value, value, value, 1.0);
}
''')
