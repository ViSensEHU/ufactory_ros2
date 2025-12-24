function [Q_torque, dQ_torque, ddQ_torque, t_torque, tau_all, tau_peak_final, k_opt, did_retime] = ...
    dynamic_replanner(robot, Q_des, dQ_des, ddQ_des, t, tau_max)

    % Ajuste de longitudes
    % ddQ tiene N-2 muestras --> recortamos todo a esa longitud
    Ndd = size(ddQ_des,1);
    Q_des   = Q_des(1:Ndd,:);
    dQ_des  = dQ_des(1:Ndd,:);
    ddQ_des = ddQ_des(1:Ndd,:);
    t       = t(1:Ndd);

    grav = [0;0;-9.81];

    % Parámetros de búsqueda
    k_low = 1.0;      
    k_high = 8.0;     
    tol = 1e-3;       
    max_iter = 20;

    %  Función interna para evaluar torque con factor k
    function [tau_peak, tau_all, t_new, dQ_new, ddQ_new] = ...
            eval_tau(robot, Q, dQ, ddQ, t, k, grav)

        % Escalado temporal
        t_new  = t * k;
        dQ_new = dQ / k;
        ddQ_new = ddQ / (k^2);

        % Evaluación del torque
        N = size(Q,1);
        tau_all = zeros(N,6);
        for j = 1:N
            tau_all(j,:) = robot.rne(Q(j,:), dQ_new(j,:), ddQ_new(j,:), grav);
        end

        tau_peak = max(abs(tau_all),[],1);
    end

    %  Evaluar torque original (k = 1)
    [tau_peak, ~, ~, ~, ~] = eval_tau(robot, Q_des, dQ_des, ddQ_des, t, 1.0, grav);

    %  Caso 1: no hay retiming
    if all(tau_peak <= tau_max)
        disp('La trayectoria original ya cumple límites de par.');
        k_opt = 1.0;

        % Evaluar torque original para graficarlo SIEMPRE
        [tau_peak_final, tau_all, t_torque, dQ_torque, ddQ_torque] = ...
            eval_tau(robot, Q_des, dQ_des, ddQ_des, t, 1.0, grav);

        Q_torque = Q_des;
        did_retime = false;
        return;
    end

    %  Caso 2: sí hay retiming
    disp('Buscando factor de escalado óptimo...');

    for iter = 1:max_iter
        k_mid = (k_low + k_high) / 2;

        tau_peak_mid = eval_tau(robot, Q_des, dQ_des, ddQ_des, t, k_mid, grav);

        if all(tau_peak_mid <= tau_max)
            k_high = k_mid;   % podemos reducir k
        else
            k_low = k_mid;    % necesitamos aumentar k
        end

        if abs(k_high - k_low) < tol
            break;
        end
    end

    k_opt = k_high;

    % Construir trayectoria final
    [tau_peak_final, tau_all, t_torque, dQ_torque, ddQ_torque] = ...
        eval_tau(robot, Q_des, dQ_des, ddQ_des, t, k_opt, grav);

    Q_torque = Q_des;
    did_retime = true;

    % Impresiones SOLO si hubo retiming
    fprintf('\n=== RESULTADOS DEL RETIMING ===\n');
    fprintf('Factor de escalado óptimo k = %.4f\n', k_opt);
    fprintf('Nuevo tiempo total de trayectoria: %.4f s\n', t_torque(end));
    fprintf('Tau máximo por articulación después del retiming:\n');
    disp(tau_peak_final);

end
