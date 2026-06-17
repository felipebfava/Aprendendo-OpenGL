// arquivo 01_vertexShader.glsl
//vertex shader é a primeira parada no pipeline, ela recebe os atributos dos vertices

//declarando a versão de GLSL
#version 330 core

//declarações de entrada e saída
layout(location = 0) in vec2 a_pos; //vec2 - vetor 2d tipo float

//não uso a cor no vertexShader, somente passo o atributo ao fragmentShader
layout(location = 1) in vec3 a_color; //vec3 - vetor 3d tipo float

//comunicacao do vertexShader ao fragmentShader
//o vertexShader passa os valores(atributos) da cor a cada vertice.
//Porem o fragmentShader passa os valores para pixels, fazendo interpolacao linear

out vec3 f_color;

void main(){
    gl_Position = vec4(a_pos, 0.0, 1.0); //vec4 para vec2
    f_color = a_color;
}
