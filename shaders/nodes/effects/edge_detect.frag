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

uniform sampler2D input_image;

layout(location = 0) out vec4 out_color;

void main(){
	//https://en.wikipedia.org/wiki/Sobel_operator#Formulation
	vec3 gx = convolveRGB(mat3(-1, 0, 1, -2, 0, 2, -1, 0, 1)/8, input_image, uv);
	vec3 gy = convolveRGB(mat3(-1, -2, -1, 0, 0, 0, 1, 2, 1)/8, input_image, uv);
	out_color = vec4(sqrt(gx * gx + gy * gy), 1);
}
