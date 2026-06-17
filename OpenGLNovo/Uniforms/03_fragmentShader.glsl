#version 460

//crio o uniform
// uniform vec3 color; //maneira antiga antes da versão 4.6.0

layout(location = 0) uniform vec3 color;

out vec4 fragColor;

void main(){
    fragColor = vec4(color, 1.0); //rgb + opacidade/transparencia
}
