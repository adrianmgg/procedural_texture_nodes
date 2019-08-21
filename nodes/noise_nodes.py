import bpy
import gpu

from .. import categories
from .. import events
from ..base_types.shader_node import ShaderNode
from ..registration import register_node

# TODO gl_FragColor is deprecated


@register_node(category=categories.noise_nodes)
class PerlinNoiseNode(ShaderNode):
    bl_idname = 'ProceduralTexture_Node_Noise_Perlin'
    bl_label = 'Perlin Noise'

    # shader from https://gist.github.com/patriciogonzalezvivo/670c22f3966e662d2f83
    fragment_shader = '''
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
'''


@register_node(category=categories.noise_nodes)
class FBMNoiseNode(ShaderNode):
    bl_idname = 'ProceduralTexture_Node_Noise_FBM'
    bl_label = 'FBM Noise'

    num_octaves: bpy.props.IntProperty(default=5, min=1, update=events.node_property_update)

    def add_shader_inputs(self, shader: gpu.types.GPUShader):
        super().add_shader_inputs(shader)
        shader.uniform_int('octaves', self.num_octaves)

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, 'num_octaves', text='Octaves')

    # shader from https://www.shadertoy.com/view/4dS3Wd
    fragment_shader = '''
uniform int octaves;

in vec2 uvInterp;

float hash(vec2 p) { return fract(1e4 * sin(17.0 * p.x + p.y * 0.1) * (0.1 + abs(sin(p.y * 13.0 + p.x)))); }

float noise(vec2 x) {
    vec2 i = floor(x);
    vec2 f = fract(x);
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

float fbm(vec2 x) {
    float v = 0.0;
    float a = 0.5;
    vec2 shift = vec2(100);
    mat2 rot = mat2(cos(0.5), sin(0.5), -sin(0.5), cos(0.50));
    for (int i = 0; i < octaves; ++i) {
        v += a * noise(x);
        x = rot * x * 2.0 + shift;
        a *= 0.5;
    }
    return v;
}

void main(){
    float value = fbm(uvInterp);
    gl_FragColor = vec4(value, value, value, 1.0);
}
'''


@register_node(category=categories.noise_nodes)
class Cells(ShaderNode):
    bl_idname = 'ProceduralTexture_Node_Noise_Cells'
    bl_label = 'Cells'

    scale: bpy.props.FloatProperty(default=1, update=events.node_property_update)

    def add_shader_inputs(self, shader: gpu.types.GPUShader):
        super().add_shader_inputs(shader)
        shader.uniform_float('scale', self.scale)

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, 'scale', text='Scale')

    fragment_shader = '''\
//
//  Wombat
//  An efficient texture-free GLSL procedural noise library
//  Source: https://github.com/BrianSharpe/Wombat
//  Derived from: https://github.com/BrianSharpe/GPU-Noise-Lib
//
//  I'm not one for copyrights.  Use the code however you wish.
//  All I ask is that credit be given back to the blog or myself when appropriate.
//  And also to let me know if you come up with any changes, improvements, thoughts or interesting uses for this stuff. :)
//  Thanks!
//
//  Brian Sharpe
//  brisharpe CIRCLE_A yahoo DOT com
//  http://briansharpe.wordpress.com
//  https://github.com/BrianSharpe
//

//
//  This represents a modified version of Stefan Gustavson's work at http://www.itn.liu.se/~stegu/GLSL-cellular
//  The noise is optimized to use a 2x2 search window instead of 3x3
//  Modifications are...
//  - faster random number generation
//  - analytical final normalization
//  - random point offset is restricted to prevent artifacts
//

//
//  Cellular Noise 2D Deriv
//  Return value range of 0.0->1.0, with format vec3( value, xderiv, yderiv )
//
vec3 Cellular2D_Deriv( vec2 P )
{
    //  https://github.com/BrianSharpe/Wombat/blob/master/Cellular2D_Deriv.glsl

    //  establish our grid cell and unit position
    vec2 Pi = floor(P);
    vec2 Pf = P - Pi;

    //  calculate the hash
    vec4 Pt = vec4( Pi.xy, Pi.xy + 1.0 );
    Pt = Pt - floor(Pt * ( 1.0 / 71.0 )) * 71.0;
    Pt += vec2( 26.0, 161.0 ).xyxy;
    Pt *= Pt;
    Pt = Pt.xzxz * Pt.yyww;
    vec4 hash_x = fract( Pt * ( 1.0 / 951.135664 ) );
    vec4 hash_y = fract( Pt * ( 1.0 / 642.949883 ) );

    //  generate the 4 points
    hash_x = hash_x * 2.0 - 1.0;
    hash_y = hash_y * 2.0 - 1.0;
    const float JITTER_WINDOW = 0.25;   // 0.25 will guarentee no artifacts
    hash_x = ( ( hash_x * hash_x * hash_x ) - sign( hash_x ) ) * JITTER_WINDOW + vec4( 0.0, 1.0, 0.0, 1.0 );
    hash_y = ( ( hash_y * hash_y * hash_y ) - sign( hash_y ) ) * JITTER_WINDOW + vec4( 0.0, 0.0, 1.0, 1.0 );

    //	return the closest squared distance + derivatives ( thanks to Jonathan Dupuy )
    vec4 dx = Pf.xxxx - hash_x;
    vec4 dy = Pf.yyyy - hash_y;
    vec4 d = dx * dx + dy * dy;
    vec3 t1 = d.x < d.y ? vec3( d.x, dx.x, dy.x ) : vec3( d.y, dx.y, dy.y );
    vec3 t2 = d.z < d.w ? vec3( d.z, dx.z, dy.z ) : vec3( d.w, dx.w, dy.w );
    return ( t1.x < t2.x ? t1 : t2 ) * vec3( 1.0, 2.0, 2.0 ) * ( 1.0 / 1.125 ); // return a value scaled to 0.0->1.0
}

in vec2 uvInterp;

uniform float scale;

layout(location = 0) out vec4 frag_color;

void main(){
    vec2 uv_scaled = ((uvInterp-.5)*2)*scale;
    frag_color = vec4(Cellular2D_Deriv(uv_scaled), 1.0);
}
'''