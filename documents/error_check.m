clc; clear all; close all;

data = csvread('data_close_loop_object20230117-212712.csv', 2);
temp = data(:,1);
ref = data(:,2);
u = data(:,3);
e = data(:,4);
t = 1:430;
t = t';

avg_res = mean(e(119:219));
result = avg_res/0.26 