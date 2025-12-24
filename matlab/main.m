clear; clc; close all;

% Modelo del robot
[robot, p_fun, J_fun, T_fun, a2_val, T2_offset_val, T3_offset_val] = model();
robot.plot([0 0 0 0 0 0]);

%  Entrada usuario
dlg = inputdlg( ...
    {'Articulaciones actuales [q1 q2 q3 q4 q5 q6] en grados (matemático):', ...
     'Posición final del efector [x y z] en mm:'}, ...
    'Entrada de movimiento', [1 70], {'0 0 0 0 0 0', '350 150 250'});

if isempty(dlg)
    q0_deg    = input('Introduce [q1 q2 q3 q4 q5 q6] en grados (matemático): ');
    p_goal_mm = input('Introduce [x y z] en mm para la posición final del efector: ');
else
    q0_deg    = str2num(dlg{1}); %#ok<ST2NM>
    p_goal_mm = str2num(dlg{2}); %#ok<ST2NM>
end

assert(numel(q0_deg)==6);
assert(numel(p_goal_mm)==3);

q_init   = deg2rad(q0_deg(:));   % rad
p_goal_m = p_goal_mm(:) / 1000;  % m

grav = [0; 0; -9.81];

% Planificador de trayectoria con escalado replanificación 
% para cumplir los límites
vel_max = deg2rad([180 180 180 180 180 180]); % rad/s
acc_max = deg2rad([1500 1500 1500 1500 1500 1500]); % rad/s^2
tau_max = [50 50 40 12 12 8]; % Nm

[Q_des, dQ_des, ddQ_des, t, P, T_final] = kinematic_planner( ...
    robot, p_fun, J_fun, T_fun, q_init, p_goal_m, vel_max, acc_max);

[Q_torque, dQ_torque, ddQ_torque, t_torque, tau_all, tau_peak_final, k_opt] = ...
    dynamic_replanner(robot, Q_des, dQ_des, ddQ_des, t, tau_max);

% Controlador PID
Kp = [100 100 100 10 4 2];
Kd = [20 20 20 20 15 5];
Ki = [0 0 0 0 0 0];

[q_real, dq_real, tau_hist] = controller(robot, Q_des, dQ_des, ddQ_des, t, grav, Kp, Kd, Ki);


%  Impresión de estados inicial/final y máximos
% 1) Posición articular inicial (ya en q_init)
q_init_rad = q_init(:).';
q_init_deg = rad2deg(q_init_rad);

% 2) Posición cartesiana inicial
T_init = T_fun(q_init(1), q_init(2), q_init(3), ...
               q_init(4), q_init(5), q_init(6));
p_init_m  = T_init(1:3,4);
p_init_mm = p_init_m.' * 1000;

% 3) Posición articular final (tomamos la final tras retiming)
q_final_rad = Q_torque(end,:);
q_final_deg = rad2deg(q_final_rad);

% 4) Posición cartesiana final
T_final_fk = T_fun(q_final_rad(1), q_final_rad(2), q_final_rad(3), ...
                   q_final_rad(4), q_final_rad(5), q_final_rad(6));
p_final_m  = T_final_fk(1:3,4);
p_final_mm = p_final_m.' * 1000;

% 5) Tiempo total de trayectoria (tras retiming por torque)
T_traj = t_torque(end);

% 6) Máximos reales
vel_peak = max(abs(dQ_torque), [], 1);
acc_peak = max(abs(ddQ_torque), [], 1);
tau_peak = max(abs(tau_all), [], 1);

fprintf('\n========================================\n');
fprintf('          RESUMEN DE LA TRAYECTORIA\n');
fprintf('========================================\n');

fprintf('\nTiempo total de trayectoria (tras torque): %.4f s\n', T_traj);

fprintf('\nPosición articular inicial [rad]:\n');
disp(q_init_rad);
fprintf('Posición articular inicial [deg]:\n');
disp(q_init_deg);

fprintf('Posición cartesiana inicial [mm]:\n');
disp(p_init_mm);

fprintf('\nPosición articular final [rad]:\n');
disp(q_final_rad);
fprintf('Posición articular final [deg]:\n');
disp(q_final_deg);

fprintf('Posición cartesiana final [mm]:\n');
disp(p_final_mm);

% Máximos reales
vel_peak = max(abs(dQ_torque), [], 1);
acc_peak = max(abs(ddQ_torque), [], 1);
tau_peak = max(abs(tau_all), [], 1);

fprintf('\n==============================\n');
fprintf('   MÁXIMOS DE LA TRAYECTORIA\n');
fprintf('==============================\n');

fprintf('Velocidades máximas alcanzadas en trayectoria calculada [rad/s]:\n');
disp(vel_peak);
fprintf('\nVelocidades máximas teóricas [rad/s]:\n');
disp(vel_max);

fprintf('Aceleraciones máximas alcanzadas en trayectoria calculada [rad/s^2]:\n');
disp(acc_peak);
fprintf('\nAceleraciones máximas teóricas [rad/s^2]:\n');
disp(acc_max);

fprintf('Torques máximos alcanzados en trayectoria calculada [Nm]:\n');
disp(tau_peak);
fprintf('\nTorques máximos teóricos [Nm]:\n');
disp(tau_max);

fprintf('==============================\n\n');

% Gráficas completas
% 1) Trayectoria articular óptima
figure;
plot(t_torque, Q_torque, 'LineWidth', 1.4);
title('Trayectoria articular óptima (Q\_torque)');
xlabel('Tiempo [s]');
ylabel('q [rad]');
grid on;
legend('q1','q2','q3','q4','q5','q6');

% 2) Velocidades articulares
figure;
plot(t_torque, dQ_torque, 'LineWidth', 1.4);
title('Velocidades articulares óptimas');
xlabel('Tiempo [s]');
ylabel('dq/dt [rad/s]');
grid on;
legend('dq1','dq2','dq3','dq4','dq5','dq6');

% 3) Aceleraciones articulares
figure;
plot(t_torque, ddQ_torque, 'LineWidth', 1.4);
title('Aceleraciones articulares óptimas');
xlabel('Tiempo [s]');
ylabel('d^2q/dt^2 [rad/s^2]');
grid on;
legend('ddq1','ddq2','ddq3','ddq4','ddq5','ddq6');

% 4) Trayectoria cartesiana
figure;
plot3(P(:,1), P(:,2), P(:,3), 'LineWidth', 1.5);
grid on;
xlabel('X [mm]');
ylabel('Y [mm]');
zlabel('Z [mm]');
title('Trayectoria cartesiana (quintic)');

% 5) Par articular a lo largo del tiempo
%{
figure;
plot(t_torque, tau_all, 'LineWidth', 1.4);
title('Par articular \tau(t)');
xlabel('Tiempo [s]');
ylabel('Torque [Nm]');
grid on;
legend('tau1','tau2','tau3','tau4','tau5','tau6');

% Límites de par
hold on;
for i = 1:6
    yline( tau_max(i), '--', 'Color', [0.5 0.5 0.5]);
    yline(-tau_max(i), '--', 'Color', [0.5 0.5 0.5]);
end
hold off;
%}
figure;
plot(t_torque, tau_all, 'LineWidth', 1.4);
title('Par articular \tau(t)');
xlabel('Tiempo [s]');
ylabel('Torque [Nm]');
grid on;
legend('tau1','tau2','tau3','tau4','tau5','tau6');

