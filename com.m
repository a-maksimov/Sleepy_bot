clc;
clear;

s = serial('COM7');
format shortG

set(s,'BaudRate',9600);
fopen(s);

fileID = fopen('temperature.csv','w');
fprintf(fileID,'Count,Temperature1,Temperature2,Humidity\n');

pause('on')
 i = 1;
 while i < 86400
    data = fscanf(s,'%g %g %g',[3 86400]);
    data = data';
    disp([i data]);
    fprintf(fileID,'%i,%.1f,%.1f,%.1f\n',i,data(1,1),data(1,2),data(1,3));
    i = i + 1;
 end

fclose(fileID);

fclose(s);

delete(instrfindall); % https://www.mathworks.com/matlabcentral/answers/65946-error-refreshing-com-ports

clear s