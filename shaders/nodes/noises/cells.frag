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

uniform int scale;

uniform int coloring_mode;
#define COLORING_MODE_INTENSITY 0
#define COLORING_MODE_CELLS 1

layout(location = 0) out vec4 out_color;

vec2 random2(vec2 p) {
	return fract(sin(vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3))))*43758.5453);
}

void main(){
	vec2 grid_pos = uv * scale;

	ivec2 cell = ivec2(floor(grid_pos));

	vec2 closest_point;
	float closest_point_distance = 10;

	for (int x = -1; x <= 1; x++){
		for (int y = -1; y <= 1; y++){
			ivec2 test_cell = cell + ivec2(x, y);
			ivec2 foo = cell + ivec2(x, y);
			if (foo.x < 0) foo.x = scale - 1;
			else if (foo.x >= scale) foo.x = 0;
			if (foo.y < 0) foo.y = scale - 1;
			else if (foo.y >= scale) foo.y = 0;
			vec2 test_point = test_cell + random2(foo);
			float dist = distance(grid_pos, test_point);
			if (dist < closest_point_distance){
				closest_point_distance = dist;
				closest_point = test_point;
			}
		}
	}

	switch (coloring_mode){
		case COLORING_MODE_INTENSITY:
		out_color = vec4(vec3(closest_point_distance), 1);
		break;
		case COLORING_MODE_CELLS:
		out_color = vec4(random2(closest_point), 0, 1);
		break;
	}
}