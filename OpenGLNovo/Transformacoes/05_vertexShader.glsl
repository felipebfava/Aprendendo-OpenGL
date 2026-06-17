// arquivo 05_vertexShader.glsl
#version 460

uniform mat4 modelMatrix; //matriz translacao

//declarações de entrada e saída
layout(location = 0) in vec2 a_pos;
layout(location = 1) in vec2 a_textCoord;

out vec2 textCoord;

void main(){
    textCoord = a_textCoord;
    gl_Position = modelMatrix * vec4(a_pos, 0.0, 1.0); //vec4 para vec2
}
