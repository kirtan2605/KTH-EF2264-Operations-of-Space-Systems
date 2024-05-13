clc
clear
close all

data = load('LOS_visibility_data_v1.mat');


set(groot, 'DefaultTextInterpreter', 'latex')
set(groot, 'DefaultLegendInterpreter', 'latex')
set(groot, 'DefaultAxesTickLabelInterpreter', 'latex')



% Define start and end datetime
startDateTime = datetime(2023, 1, 1, 0, 0, 0); % 1st Jan 2023, 00:00:00
endDateTime = datetime(2023, 1, 31, 0, 0, 0); % 30th Jan 2023, 23:59:00

% Generate datetime vector with 1 minute timestep
dateTimeVector = startDateTime:minutes(1):endDateTime;


%% Waterfall Plot

% Define the color map
colors = [0 1 0; 1 0 0]; % Green for 0, Red for 1
% since we want to avoid Starlink Satellites in LOS
v_min = 0;
v_max = 1;
levels = [v_min, v_max];

% Plot the matrix
imagesc(data.LOS_visibility_data);
colormap(colors);
caxis([v_min v_max]);

% Create a custom color bar with ticks and tick labels
cb = colorbar;
set(cb, 'Ticks', levels);
set(cb, 'TickLabels', {'Low', 'High'});

% Create a custom colorbar
c = colorbar;
c.Ticks = [];
c.TickLabels = {'Not Visible', 'Visible'};

set(c,'YTickLabel', []);
hYLabel = ylabel(c, 'Not Visible                          Visible');     
set(hYLabel,'Rotation',90);

% Specify y-axis ticks
yticks(linspace(1, size(data.LOS_visibility_data, 1), 5)); % Evenly spaced ticks
yticklabels({'1 Jan', '8 Jan', '15 Jan', '22 Jan', '30 Jan'}); % Specify the labels for the ticks
ax=gca;
ax.FontSize = 15;


% Set axis labels
xlabel('Starlink Satellie Number');
%ylabel('Date');
title('Starlink Satellite Line-of-Sight Visibility 2023');


%% Number of visible satellites plot
% Calculate the sum of elements in each row
row_sums = sum(data.LOS_visibility_data, 2); % Dimension 2 represents summing along rows

% Plot the sums
figure;
plot(dateTimeVector, row_sums, 'LineWidth', 2);
ylabel('Number of Satellites');
title('Number of Visible Starlink Satellites');
grid on;
grid minor
ax=gca;
ax.FontSize = 15;
