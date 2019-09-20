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

vec3 convolveRGB(mat3x3 kernel, sampler2D image, vec2 uv){
	vec3 accumulate = vec3(0);
	vec2 size = 1.0 / textureSize(image, 0);
	for(int x = -1; x <= 1; x++){
		for(int y = -1; y <= 1; y++){
			accumulate += kernel[x+1][y+1] * texture(image, uv + vec2(x,y) * size).rgb;
		}
	}
	return accumulate;
}

vec4 convolveRGBA(mat3x3 kernel, sampler2D image, vec2 uv){
	vec4 accumulate = vec4(0);
	vec2 size = 1.0 / textureSize(image, 0);
	for(int x = -1; x <= 1; x++){
		for(int y = -1; y <= 1; y++){
			accumulate += kernel[x+1][y+1] * texture(image, uv + vec2(x,y) * size);
		}
	}
	return accumulate;
}
