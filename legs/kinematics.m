clc; clear all; close all;

syms t_1 t_2 t_3 a_0 a_1 a_2 a_3 alpha_0
T_B0 = transMatrix(a_0, alpha_0, 0, t_1);
T_01 = transMatrix(0, 0, 0, t_1);
T_12 = transMatrix(a_1,-sym(pi)/2,0,t_2);
T_23 = transMatrix(a_2,0,0,t_3);
T_3f = transMatrix(a_3,0,0,0);

T_02 = simplify(T_01*T_12);
T_03 = simplify(T_01*T_12*T_23);
T_0f = simplify(T_01*T_12*T_23*T_3f);

P = T_0f(1:3,4);
simplify(expand((sqrt(P(1)^2+P(2)^2) - a_1)^2+P(3)^2))


function T = transMatrix(a, alpha, d, theta)
    T = [cos(theta) -sin(theta) 0 a;...
         sin(theta)*cos(alpha) cos(theta)*cos(alpha) -sin(alpha) -sin(alpha)*d;...
         sin(theta)*sin(alpha) cos(theta)*sin(alpha) cos(alpha) cos(alpha)*d;...
         0 0 0 1];
end