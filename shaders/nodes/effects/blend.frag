/*
 * Copyright (C) 2019 Adrian Guerra
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see https://www.gnu.org/licenses/.
 */

in vec2 uv;

uniform int blend_mode;
#define BLEND_MODE_NORMAL 0
#define BLEND_MODE_ADD 1
#define BLEND_MODE_SUBTRACT 2
#define BLEND_MODE_MULTIPLY 3

uniform sampler2D input_image_1;
uniform sampler2D input_image_2;

layout(location = 0) out vec4 out_color;

void main(){
	vec4 color_1 = texture2D(input_image_1, uv);
	vec4 color_2 = texture2D(input_image_2, uv);

	switch (blend_mode){
		case BLEND_MODE_NORMAL:
			out_color = vec4(
				color_1.rgb * color_1.a + color_2.rgb * (1 - color_1.a),
				color_1.a + color_2.a * (1-color_2.a)
			);
			return;
		case BLEND_MODE_ADD:
			out_color = vec4(
				color_1.rgb * color_1.a + color_2.rgb,
				color_1.a + color_2.a * (1-color_2.a)
			);
			return;
		case BLEND_MODE_SUBTRACT:
			out_color = vec4(
				color_2.rgb - color_1.rgb * color_1.a,
				color_1.a + color_2.a * (1-color_2.a)
			);
			return;
		case BLEND_MODE_MULTIPLY:
			out_color = vec4(
				color_1.rgb * color_2.rgb * color_2.a + color_2.rgb * (1 - color_1.a),
				color_1.a + color_2.a * (1-color_2.a)
			);
			return;
	}
}
