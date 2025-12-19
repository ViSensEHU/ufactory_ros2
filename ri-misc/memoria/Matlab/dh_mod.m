clear; clc;
syms q1 q2 q3 q4 q5 q6 a2 T2_offset T3_offset real
pi2 = sym(pi)/2;

% Link([theta d a alpha sigma offset], 'modified')
L1_link = Link([0     267    0      0        0  0], 'modified');       
L2_link = Link([0     0      0     -pi2      0  T2_offset], 'modified'); 
L3_link = Link([0     0      a2     0        0  T3_offset], 'modified');
L4_link = Link([0     342.5  77.5  -pi2      0  0], 'modified');  
L5_link = Link([0     0      0      pi2      0  0], 'modified');   
L6_link = Link([0     97     76    -pi2      0  0], 'modified'); 

robot = SerialLink([L1_link L2_link L3_link L4_link L5_link L6_link], ...
                   'name', 'xArm6', 'modified');

robot.plot([0 0 0 0 0 0]);

q = [q1 q2 q3 q4 q5 q6];

T01 = simplify(L1_link.A(q1).T);
T12 = simplify(L2_link.A(q2).T);
T23 = simplify(L3_link.A(q3).T);
T34 = simplify(L4_link.A(q4).T);
T45 = simplify(L5_link.A(q5).T);
T56 = simplify(L6_link.A(q6).T);

T06_sym = simplify(T01 * T12 * T23 * T34 * T45 * T56);

% Sustitución numérica (q_i=0 y offsets reales)
S.q1 = 0; S.q2 = 0; S.q3 = 0; S.q4 = 0; S.q5 = 0; S.q6 = 0;
S.a2 = 289.48866;
S.T2_offset = deg2rad(-79.34995);
S.T3_offset = deg2rad(79.34995);

T06_num = vpa(subs(T06_sym, S), 10);
disp(T06_num);

