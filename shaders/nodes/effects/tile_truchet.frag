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
uniform sampler2D input_image;

layout(location = 0) out vec4 out_color;

void main(){
	vec2 cell = floor(uv * scale);
	vec2 cell_uv = fract(uv * scale);

	float angle = M_HALF_PI * floor(hash2to1(cell) * 4);
	cell_uv *= rotation2d(angle);

	out_color = texture2D(input_image, cell_uv);
}
