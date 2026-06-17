// arquivo 05_fragmentShader.glsl
#version 460


uniform sampler2D u_tex;

in vec2 textCoord;

out vec4 fragColor;

void main(){
    vec4 color = texture(u_tex, textCoord);
    fragColor = color;
    // fragColor = vec4(1, 0, 0, 1.0); //cor padrão teste
}
