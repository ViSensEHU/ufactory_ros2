function [robot, p_fun, J_fun, T_fun, a2_val, T2_offset_val, T3_offset_val] = model()

    % Parámetros geométricos
    T2_offset_val = deg2rad(-79.34995);
    T3_offset_val = deg2rad(79.34995);
    a2_val        = 0.28948866; % metros

    % Construcción del robot (DH modificado)
    L1 = Link([0 0.267 0      0      0 0], 'modified');             % Eslabón 1
    L2 = Link([0 0     0     -pi/2   0 T2_offset_val], 'modified'); % Eslabón 2
    L3 = Link([0 0     a2_val 0      0 T3_offset_val], 'modified'); % Eslabón 3
    L4 = Link([0 0.3425 0.0775 -pi/2 0 0], 'modified');             % Eslabón 4
    L5 = Link([0 0     0      pi/2   0 0], 'modified');             % Eslabón 5
    L6 = Link([0 0.097 0.076 -pi/2   0 0], 'modified');             % Eslabón 6

    % Crear el robot
    robot = SerialLink([L1 L2 L3 L4 L5 L6], 'name', 'xArm6');
    
    % Definir los límites articulares
    robot.qlim = deg2rad([
        -360   360   % q1
        -117   116   % q2
        -219   10    % q3
        -360   360   % q4
        -97    180   % q5
        -360   360   % q6
    ]);

    % Parámetros dinámicos
    robot.links(1).m = 2.177;
    robot.links(1).r = [0.00015 0.02724 -0.01357];
    robot.links(1).I = [0.005433 0.004684 0.0031118 9.864e-06 -2.68e-05 -0.000826936];
    
    robot.links(2).m = 2.011;
    robot.links(2).r = [0.0367 -0.22088 0.03356];
    robot.links(2).I = [0.0271342 0.0053854 0.0262093 0.004736 0.00068673 -0.0047834];
    
    robot.links(3).m = 1.725;
    robot.links(3).r = [0.06977 0.1135 0.01163];
    robot.links(3).I = [0.006085 0.0036652 0.0057045 -0.0015 0.0009558 0.0018091];
    
    robot.links(4).m = 1.211;
    robot.links(4).r = [-0.0002 0.02 -0.026];
    robot.links(4).I = [0.0046981 0.0042541 0.00123664 -6.486e-06 -1.404e-05 -0.0002877];
    
    robot.links(5).m = 1.206;
    robot.links(5).r = [0.06387 0.02928 0.0035];
    robot.links(5).I = [0.0013483 0.00175694 0.002207 -0.00042677 0.00028758 0.0001244];
    
    robot.links(6).m = 0.170;
    robot.links(6).r = [0 -0.00677 -0.01098];
    robot.links(6).I = [9.3e-05 5.87e-05 0.000132 0 0 -3.6e-06];

    for i = 1:6
        robot.links(i).G  = 1;
        robot.links(i).Jm = 0;
        robot.links(i).B  = 0;
        robot.links(i).Tc = [0 0];
    end

    % Generación de funciones numéricas
    syms q1 q2 q3 q4 q5 q6 real

    % Transformaciones simbólicas
    T01 = L1.A(q1).T;
    T12 = L2.A(q2).T;
    T23 = L3.A(q3).T;
    T34 = L4.A(q4).T;
    T45 = L5.A(q5).T;
    T56 = L6.A(q6).T;

    T06 = simplify(T01*T12*T23*T34*T45*T56);
    p06 = T06(1:3,4);
    Jv  = jacobian(p06, [q1 q2 q3 q4 q5 q6]);

    % Funciones numéricas
    p_fun = matlabFunction(p06, 'Vars', {q1,q2,q3,q4,q5,q6});
    J_fun = matlabFunction(Jv,  'Vars', {q1,q2,q3,q4,q5,q6});
    T_fun = matlabFunction(T06, 'Vars', {q1,q2,q3,q4,q5,q6});

end
