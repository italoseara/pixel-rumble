#ifdef GL_ES
precision mediump float;
#endif

uniform sampler2D u_texture;
uniform vec2 u_resolution;
uniform float u_radius;   // 0.0 to 1.0, vignette radius
uniform float u_softness; // 0.0 to 1.0, vignette softness

varying vec2 v_texCoord;

void main() {
    vec2 uv = v_texCoord;
    vec2 position = (uv - 0.5) * u_resolution / min(u_resolution.x, u_resolution.y);
    float dist = length(position);

    float vignette = smoothstep(u_radius, u_radius - u_softness, dist);

    vec4 color = texture2D(u_texture, uv);
    color.rgb *= vignette;

    gl_FragColor = color;
}