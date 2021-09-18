clc; clear; close all;

ox = 0;
oy = 0;
oz = -0.16;

time = 20;
pathTime = linspace(-1,1,time+1);
pathTime2 = linspace(-1,1,2*time+1);

pathX = [];
pathY = [];
pathZ = [];

pathX = sin(-pi*pathTime/2);
pathY = 0*pathX;
pathZ = cos(pi*pathTime/2);
pathX(end)=[];
pathY(end)=[];
pathZ(end)=[];

pathX = 0.06*[pathX pathTime2];
pathY = 0*pathX+0.1;
pathZ = 0.05*[pathZ 0*pathTime2];
pathX(end)=[];
pathY(end)=[];
pathZ(end)=[];

pathX = pathX + ox;
pathY = pathY + oy;
pathZ = pathZ + oz;

scatter3(ox,oy,oz);
hold on;
scatter3(pathX, pathY,pathZ);
grid on;
daspect([1,1,1]);

points = [[0.1,0,-0.17],
					 [0.0998,-0.007,-0.17],
					 [0.0995,-0.014,-0.17],
					 [0.0989,-0.021,-0.17],
					 [0.098,-0.028,-0.17],
					 [0.097,-0.035,-0.17],
					 [0.096,-0.042,-0.17],

					 [0.094,-0.049,-0.17],
					 [0.097,-0.035,-0.17+0.015],
					 [0.0989,-0.021,-0.17+0.026],
					 [0.0998,-0.007,-0.17+0.031],
					 [0.0998,0.007,-0.17+0.031],
					 [0.0989,0.021,-0.17+0.026],
					 [0.097,0.035,-0.17+0.015],

					 [0.094,0.049,-0.17],
					 [0.096,0.042,-0.17],
					 [0.097,0.035,-0.17],
					 [0.098,0.028,-0.17],
					 [0.0989,0.021,-0.17],
					 [0.0995,0.014,-0.17],
					 [0.0998,0.007,-0.17]]

scatter3(points(:,1),points(:,2),points(:,3));

sweepAngle = 30;
circleX = .1*cos(deg2rad(sweepAngle*pathTime2));
circleY = .1*sin(deg2rad(sweepAngle*pathTime2));
circleZ = 0*pathTime2;
circleX(end) = [];
circleY(end) = [];
circleZ(end) = [];
arcX = 0*pathTime+abs(circleX(1));
arcY = abs(circleY(1))*sin(-pi*pathTime/2);
arcZ = 0.05*cos(-pi*pathTime/2);
arcX(end) = [];
arcY(end) = [];
arcZ(end) = [];

turnX = [circleX arcX];
turnY = [circleY arcY];
turnZ = [circleZ arcZ]+oz;
scatter3(turnX,turnY,turnZ);

forward = [pathX' pathY' pathZ'];
forward = circshift(flip(forward,1),2*time+1);

turn = [turnX', turnY', turnZ'];
turn = circshift(flip(turn,1),time+1);

disp(sprintf('Forward'));
for i=[1:time*3]
    disp(sprintf("  - [%f, %f, %f]",forward(i,:)));
end

disp(sprintf('Turn'));

for i=[1:time*3]
    disp(sprintf("  - [%f, %f, %f]",turn(i,:)));
end
         
