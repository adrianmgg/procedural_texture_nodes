//https://www.shadertoy.com/view/4djSRW
// Hash without Sine
// Creative Commons Attribution-ShareAlike 4.0 International Public License
// Created by David Hoskins.

// *** Change these to suit your range of random numbers..

// *** Use this for integer stepped ranges, ie Value-Noise/Perlin noise functions.
//#define HASHSCALE1 .1031
//#define HASHSCALE3 vec3(.1031, .1030, .0973)
//#define HASHSCALE4 vec4(.1031, .1030, .0973, .1099)

// For smaller input rangers like audio tick or 0-1 UVs use these...
#define HASHSCALE1 443.8975
#define HASHSCALE3 vec3(443.897, 441.423, 437.195)
#define HASHSCALE4 vec4(443.897, 441.423, 437.195, 444.129)


float hash1to1(float p) {
	vec3 p3 = fract(vec3(p) * HASHSCALE1);
	p3 += dot(p3, p3.yzx + 19.19);
	return fract((p3.x + p3.y) * p3.z);
}

float hash2to1(vec2 p) {
	vec3 p3 = fract(vec3(p.xyx) * HASHSCALE1);
	p3 += dot(p3, p3.yzx + 19.19);
	return fract((p3.x + p3.y) * p3.z);
}

float hash3to1(vec3 p3) {
	p3 = fract(p3 * HASHSCALE1);
	p3 += dot(p3, p3.yzx + 19.19);
	return fract((p3.x + p3.y) * p3.z);
}

vec2 hash1to2(float p) {
	vec3 p3 = fract(vec3(p) * HASHSCALE3);
	p3 += dot(p3, p3.yzx + 19.19);
	return fract((p3.xx + p3.yz) * p3.zy);
}

vec2 hash2to2(vec2 p) {
	vec3 p3 = fract(vec3(p.xyx) * HASHSCALE3);
	p3 += dot(p3, p3.yzx + 19.19);
	return fract((p3.xx + p3.yz) * p3.zy);
}

vec2 hash3to2(vec3 p3) {
	p3 = fract(p3 * HASHSCALE3);
	p3 += dot(p3, p3.yzx + 19.19);
	return fract((p3.xx + p3.yz) * p3.zy);
}

vec3 hash1to3(float p) {
	vec3 p3 = fract(vec3(p) * HASHSCALE3);
	p3 += dot(p3, p3.yzx + 19.19);
	return fract((p3.xxy + p3.yzz) * p3.zyx); 
}

vec3 hash2to3(vec2 p) {
	vec3 p3 = fract(vec3(p.xyx) * HASHSCALE3);
	p3 += dot(p3, p3.yxz + 19.19);
	return fract((p3.xxy + p3.yzz) * p3.zyx);
}

vec3 hash3to3(vec3 p3) {
	p3 = fract(p3 * HASHSCALE3);
	p3 += dot(p3, p3.yxz + 19.19);
	return fract((p3.xxy + p3.yxx) * p3.zyx);
}

vec4 hash1to4(float p) {
	vec4 p4 = fract(vec4(p) * HASHSCALE4);
	p4 += dot(p4, p4.wzxy + 19.19);
	return fract((p4.xxyz + p4.yzzw) * p4.zywx); 
}

vec4 hash2to4(vec2 p) {
	vec4 p4 = fract(vec4(p.xyxy) * HASHSCALE4);
	p4 += dot(p4, p4.wzxy + 19.19);
	return fract((p4.xxyz + p4.yzzw) * p4.zywx);
}

vec4 hash3to4(vec3 p) {
	vec4 p4 = fract(vec4(p.xyzx) * HASHSCALE4);
	p4 += dot(p4, p4.wzxy + 19.19);
	return fract((p4.xxyz + p4.yzzw) * p4.zywx);
}

vec4 hash4to4(vec4 p4) {
	p4 = fract(p4 * HASHSCALE4);
	p4 += dot(p4, p4.wzxy + 19.19);
	return fract((p4.xxyz + p4.yzzw) * p4.zywx);
}
