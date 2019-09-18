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

vec4 blend(vec4 color_1, vec4 color_2){
	return vec4(
		color_1.rgb * color_1.a + color_2.rgb * (1 - color_1.a),
		color_1.a + color_2.a * (1-color_2.a)
	);
}

vec4 blend_add(vec4 color_1, vec4 color_2){
	return vec4(
		color_1.rgb * color_1.a + color_2.rgb,
		color_1.a + color_2.a * (1-color_2.a)
	);
}


vec4 blend_subtract(vec4 color_1, vec4 color_2){
	return vec4(
		color_2.rgb - color_1.rgb * color_1.a,
		color_1.a + color_2.a * (1-color_2.a)
	);
}

vec4 blend_multiply(vec4 color_1, vec4 color_2){
	return vec4(
		color_1.rgb * color_2.rgb * color_2.a + color_2.rgb * (1 - color_1.a),
		color_1.a + color_2.a * (1-color_2.a)
	);
}