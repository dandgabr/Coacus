export const vertex = `#version 300 es
out vec2 uv;
void main() {
  vec2 corner = vec2(float((gl_VertexID << 1) & 2), float(gl_VertexID & 2));
  uv = corner;
  gl_Position = vec4(corner * 2.0 - 1.0, 0.0, 1.0);
}`

const fragment = `#version 300 es
precision highp float;
in vec2 uv;
out vec4 color;
`

export const feedback = fragment + `
uniform sampler2D lastState;
uniform vec2 cell;
uniform float dt;
uniform vec4 impulse;
uniform float strength;

void main() {
  // Keep a solid one-texel wall and never sample across it.
  if (any(lessThan(uv, cell)) || any(greaterThan(uv, 1.0 - cell))) {
    color = vec4(0.0);
    return;
  }

  vec2 velocity = texture(lastState, uv).rg;
  vec2 source = clamp(uv - velocity * dt, cell * 0.5, 1.0 - cell * 0.5);
  vec3 state = texture(lastState, source).rgb * exp(-dt * vec3(2.4, 2.4, 1.6));

  vec2 offset = uv - impulse.xy;
  vec2 aspect = vec2(cell.y / cell.x, 1.0);
  float weight = strength * exp(-dot(offset * aspect, offset * aspect) / 0.004);
  vec2 swirl = vec2(-offset.y, offset.x) * 3.0;
  state.xy = clamp(state.xy + (impulse.zw + swirl) * weight, -0.8, 0.8);
  state.z = min(1.0, state.z + 0.76 * weight);

  // Dampen the normal component near the wall.
  vec2 distanceToWall = min(uv, 1.0 - uv);
  state.xy *= smoothstep(cell, cell * 4.0, distanceToWall);
  color = vec4(state, 0.0);
}
`

export const ink = fragment + `
uniform sampler2D lastState;
void main() {
  float dye = texture(lastState, uv).b;
  vec3 paper = mix(vec3(0.025, 0.055, 0.085), vec3(0.065, 0.105, 0.14), uv.y);
  vec3 pigment = mix(vec3(0.13, 0.55, 0.68), vec3(0.78, 0.96, 0.84), dye);
  color = vec4(mix(paper, pigment, sqrt(dye)), 1.0);
}
`

export const image = fragment + `
uniform int scene;
uniform float aspect;

void main() {
  bool tide = scene == 0;
  vec3 sky = tide ? vec3(17.0, 35.0, 61.0) / 255.0 : vec3(61.0, 28.0, 51.0) / 255.0;
  vec3 ridge = tide ? vec3(0.18, 0.48, 0.55) : vec3(0.83, 0.41, 0.36);
  vec3 foreground = tide ? vec3(0.07, 0.27, 0.37) : vec3(0.40, 0.19, 0.30);
  vec2 center = vec2(tide ? 0.27 : 0.73, 0.68);
  float orb = 1.0 - smoothstep(0.112, 0.12, length((uv - center) * vec2(aspect, 1.0)));
  float farHill = 0.33 + 0.14 * sin(uv.x * 5.2 + float(scene) * 2.8);
  float nearHill = 0.23 + 0.09 * cos(uv.x * 7.0 - float(scene) * 2.1);
  vec3 landscape = mix(sky, tide ? vec3(0.85, 0.97, 0.93) : vec3(1.0, 0.82, 0.49), orb);
  landscape = mix(landscape, ridge, 1.0 - smoothstep(farHill - 0.004, farHill + 0.004, uv.y));
  landscape = mix(landscape, foreground, 1.0 - smoothstep(nearHill - 0.004, nearHill + 0.004, uv.y));
  color = vec4(landscape, 1.0);
}
`

export const composite = fragment + `
uniform sampler2D fromImage;
uniform sampler2D toImage;
uniform float progress;
void main() {
  float edge = uv.x + 0.06 * sin(uv.y * 14.0);
  float amount = smoothstep(-0.025, 0.025, mix(-0.09, 1.09, progress) - edge);
  color = mix(texture(fromImage, uv), texture(toImage, uv), amount);
}
`
