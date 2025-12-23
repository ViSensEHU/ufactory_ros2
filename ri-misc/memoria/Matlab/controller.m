function [q_real_hist, dq_real_hist, tau_hist] = controller( ...
        robot, Q_des, dQ_des, ddQ_des, t, grav, Kp, Kd, Ki)

    N  = size(Q_des,1);
    dt = t(2) - t(1);

    % ===============================
    % Ajuste de longitudes
    % ===============================
    Ndd = size(ddQ_des,1);
    
    Q_des   = Q_des(1:Ndd,:);
    dQ_des  = dQ_des(1:Ndd,:);
    ddQ_des = ddQ_des(1:Ndd,:);
    t       = t(1:Ndd);
    
    N = Ndd;


    % Históricos
    q_real_hist  = zeros(N,6);
    dq_real_hist = zeros(N,6);
    tau_hist     = zeros(N,6);

    % Estado inicial
    q_real  = Q_des(1,:);
    dq_real = dQ_des(1,:);

    % Integral del error
    e_int = zeros(1,6);

    % Perturbación externa (torque)
    %tau_pert = @(k) 0.5 * sin(0.1*k) * ones(1,6);
    tau_pert = @(k) 0.2 * randn(1,6);

    robot.gravity = grav(:).';

    for k = 1:N

        % ======== Señales deseadas ========
        q_d   = Q_des(k,:);
        dq_d  = dQ_des(k,:);
        ddq_d = ddQ_des(k,:);

        % ======== Error ========
        e    = q_d  - q_real;
        edot = dq_d - dq_real;
        e_int = e_int + e*dt;

        % ======== PID ========
        ddq_ref = ddq_d + Kp.*e + Kd.*edot + Ki.*e_int;

        % ======== Torque PID ========
        tau_pid = robot.rne(q_real, dq_real, ddq_ref);

        % ======== Perturbación física ========
        tau_total = tau_pid + tau_pert(k);

        % ======== Dinámica directa ========
        M = robot.inertia(q_real);
        C = robot.coriolis(q_real, dq_real);
        g = robot.gravload(q_real);

        ddq_real = M \ (tau_total' - C*dq_real' - g');

        % ======== Integración ========
        dq_real = dq_real + ddq_real'*dt;
        q_real  = q_real  + dq_real*dt;

        % ======== Guardar ========
        q_real_hist(k,:)  = q_real;
        dq_real_hist(k,:) = dq_real;
        tau_hist(k,:)     = tau_total;
    end

    %% ================================
    %  GRÁFICAS
    % ================================
    figure;
    plot(t, Q_des, '--', 'LineWidth', 1.2); hold on;
    plot(t, q_real_hist, 'LineWidth', 1.4);
    title('Trayectorias deseadas vs reales (todas las articulaciones)');
    xlabel('Tiempo [s]'); ylabel('Ángulo [rad]');
    legend('q1_d','q2_d','q3_d','q4_d','q5_d','q6_d', ...
           'q1_r','q2_r','q3_r','q4_r','q5_r','q6_r');
    grid on;

    % Una figura por articulación
    for j = 1:6
        figure;
        plot(t, Q_des(:,j), '--', 'LineWidth', 1.2); hold on;
        plot(t, q_real_hist(:,j), 'LineWidth', 1.4);
        title(['Trayectoria - Articulación ', num2str(j)]);
        xlabel('Tiempo [s]'); ylabel('Ángulo [rad]');
        legend('Deseada','Real');
        grid on;
    end

end
