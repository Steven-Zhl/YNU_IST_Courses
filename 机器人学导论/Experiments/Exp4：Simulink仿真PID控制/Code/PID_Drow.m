clear all
close all
clc

G = tf(1, [2 1]); % 传递函数1：1/(2*s + 1)
G_2 = tf(3, [2 1]); % 传递函数2：3/(2*s + 1)
% Kp的作用
for Kp = 0:0.1:3
    G1 = Kp;
    sys = feedback(G1 * G * G_2, 1); % 单位负反馈系统
    step(sys);
    title(" ");
    xlabel("t", "Interpreter", "latex");
    ylabel("u(s)", "Interpreter", "latex");
    text(0.5, 0.9, "Kp="+num2str(Kp), "Interpreter", "latex", "Units", "normalized");
    text(0.5, 0.8, "$K_i=0$", "Interpreter", "latex", "Units", "normalized");
    text(0.5, 0.7, "$K_d=0$", "Interpreter", "latex", "Units", "normalized");
    axis([0 10 0 1.6]);
    pause(0.01);
end

% Ki的作用
Kp = 3;
for Ki = 0:0.05:1
    G1 = tf([Kp Ki], [1 0]); % 比例-积分控制 (Kp*s + Ki) / s
    sys = feedback(G1 * G * G_2, 1); % 单位负反馈系统
    step(sys);
    title(" ");
    xlabel("t", "Interpreter", "latex");
    ylabel("u(s)", "Interpreter", "latex");
    text(0.5, 0.9, "$K_p=3$", "Interpreter", "latex", "Units", "normalized");
    text(0.5, 0.8, "Ki="+num2str(Ki), "Interpreter", "latex", "Units", "normalized");
    text(0.5, 0.7, "$K_d=0$", "Interpreter", "latex", "Units", "normalized");
    axis([0 10 0 1.6]);
    pause(0.01);
end

% Kd的作用
Kp = 3;
Ki = 1;
for Kd = 0:0.1:2
    G1 = tf([Kd, Kp, Ki], [1 0]); % PID控制 (kd*s^2 + Kp*s + Ki) / s
    sys = feedback(G1 * G * G_2, 1); % 单位负反馈系统
    step(sys);
    title(" ");
    xlabel("t", "Interpreter", "latex");
    ylabel("u(s)", "Interpreter", "latex");
    text(0.5, 0.9, "$K_p=3$", "Interpreter", "latex", "Units", "normalized");
    text(0.5, 0.8, "$K_i=1$", "Interpreter", "latex", "Units", "normalized");
    text(0.5, 0.7, "Kd="+num2str(Kd), "Interpreter", "latex", "Units", "normalized");
    axis([0 10 0 1.6]);
    pause(0.01);
end
