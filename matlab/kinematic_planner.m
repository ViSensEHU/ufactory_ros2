function [Q_des, dQ_des, ddQ_des, t, P, T_final] = kinematic_planner( ...
    robot, p_fun, J_fun, T_fun, q_init, p_goal_m, vel_max, acc_max)

    % Límites articulares (en deg)
    q_min = robot.qlim(:,1);
    q_max = robot.qlim(:,2);
    q_mid = (q_min + q_max)/2;

    %  Verificación de alcanzabilidad
    reach_max_m = 0.7; % 700 mm
    if norm(p_goal_m) > reach_max_m
        fprintf('Objetivo fuera del alcance -> NO realizable\n');
        Q_des = []; dQ_des = []; ddQ_des = []; t = []; P = []; T_final = [];
        return
    end

    % IK numérica
    tol     = 1e-6; 
    maxIter = 80; 
    K       = 0.005;

    q_goal = newtonIK(p_goal_m, q_init, p_fun, J_fun, ...
                      q_min, q_max, q_mid, K, tol, maxIter);

    if any(isnan(q_goal))
        error('IK no encontró solución válida.');
    end

    % Trayectoria quíntica base + escalado
    n  = 300;
    T0 = 1.0;                   % tiempo base mínimo (se reescala luego)
    t0 = linspace(0, T0, n);

    % Quíntica base entre q_init y q_goal
    Q0 = quinticTraj(q_init.', q_goal.', T0, t0);

    % Escalado óptimo de tiempo para cumplir vel/acc (estilo TOTG)
    [Q_des, t, T_final] = scale_traj(Q0, t0, vel_max, acc_max);

    % Derivadas numéricas
    dt      = t(2) - t(1);
    dQ_des  = diff(Q_des) / dt;
    ddQ_des = diff(dQ_des) / dt;

    % Trayectoria cartesiana del efector
    P = zeros(numel(t), 3);
    for k = 1:numel(t)
        Tnow   = T_fun(Q_des(k,1), Q_des(k,2), Q_des(k,3), ...
                       Q_des(k,4), Q_des(k,5), Q_des(k,6));
        p_m    = Tnow(1:3,4);     % metros
        P(k,:) = (p_m * 1000).';  % mm para graficar
    end

end

% Funciones auxiliares
function q_sol = newtonIK(p_d_m, q_seed, p_fun, J_fun, ...
                          q_min, q_max, q_mid, K, tol, maxIter)

    qk = q_seed(:);
    for it = 1:maxIter %#ok<NASGU>
        p_now_m = p_fun(qk(1), qk(2), qk(3), qk(4), qk(5), qk(6));
        J_now   = J_fun(qk(1), qk(2), qk(3), qk(4), qk(5), qk(6));

        e = p_d_m - p_now_m;
        if norm(e) < tol, break; end

        gradH = 2 * (qk - q_mid) ./ ((q_max - q_min).^2);
        dq    = pinv(J_now) * e - K * gradH;

        qk = qk + dq;
    end
    q_sol = qk;
end

function Q = quinticTraj(q0, qf, T, t)
    n = numel(t); 
    Q = zeros(n, numel(q0));
    for i = 1:numel(q0)
        a0 = q0(i); a1 = 0; a2 = 0;
        a3 = 10*(qf(i)-q0(i))/T^3;
        a4 = -15*(qf(i)-q0(i))/T^4;
        a5 = 6*(qf(i)-q0(i))/T^5;
        Q(:,i) = a0 + a1*t + a2*t.^2 + a3*t.^3 + a4*t.^4 + a5*t.^5;
    end
end

function [Q_out, t_out, T_scaled] = scale_traj(Q, t, vel_max, acc_max)
    dt  = t(2) - t(1);
    dQ  = diff(Q)/dt;
    ddQ = diff(dQ)/dt;

    % Factor mínimo de escalado para cumplir límites
    scale_v = max(max(abs(dQ)  ./ vel_max));
    scale_a = max(max(abs(ddQ) ./ acc_max));
    scale   = max([1, scale_v, sqrt(scale_a)]);

    if scale > 1
        T_scaled = t(end) * scale;
        t_out    = linspace(0, T_scaled, numel(t));

        Q_out = zeros(size(Q));
        q0    = Q(1,:); 
        qf    = Q(end,:);
        for i = 1:size(Q,2)
            a0 = q0(i); a1 = 0; a2 = 0;
            a3 = 10*(qf(i)-q0(i))/T_scaled^3;
            a4 = -15*(qf(i)-q0(i))/T_scaled^4;
            a5 = 6*(qf(i)-q0(i))/T_scaled^5;
            Q_out(:,i) = a0 + a1*t_out + a2*t_out.^2 + a3*t_out.^3 + ...
                         a4*t_out.^4 + a5*t_out.^5;
        end
    else
        Q_out   = Q; 
        t_out   = t; 
        T_scaled = t(end);
    end
end
