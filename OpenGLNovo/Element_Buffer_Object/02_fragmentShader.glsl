// arquivo 01_fragmentShader.glsl
//declarando a versão de GLSL
#version 330 core

out vec4 fragColor;
in vec3 f_color; //a variavel cor está vindo do vertexShader

void main(){
    fragColor = vec4(f_color, 1.0); //rgb + opacidade/transparencia
}
