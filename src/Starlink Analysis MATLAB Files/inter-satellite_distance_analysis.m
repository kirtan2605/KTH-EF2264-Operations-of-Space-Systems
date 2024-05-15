clc
clear
close all

load("interSat_distances_data_v1.mat")
load("LOS_visibility_data_v1.mat")


set(groot, 'DefaultTextInterpreter', 'latex')
set(groot, 'DefaultLegendInterpreter', 'latex')
set(groot, 'DefaultAxesTickLabelInterpreter', 'latex')

% Define start and end datetime
startDateTime = datetime(2023, 1, 1, 0, 0, 0); % 1st Jan 2023, 00:00:00
endDateTime = datetime(2023, 1, 31, 0, 0, 0); % 30th Jan 2023, 23:59:00

% Generate datetime vector with 1 minute timestep
dateTimeVector = startDateTime:minutes(1):endDateTime;

LOS_visible_distances = LOS_visibility_data_v1.*interSat_distances_data_v1;

% Replace zeros with inf, so that they dont get counted as minimum distances
LOS_visible_distances(LOS_visible_distances == 0) = inf;

% Find minimum value in each row

min_visibleSat_distance =  min(LOS_visible_distances, [], 2);

% Plot the sums
figure;
plot(dateTimeVector, min_visibleSat_distance/1000, 'LineWidth', 2);
ylabel('Minimum Distance [km]');
title('Minimum Distance of Visible Starlink Satellite');
grid on;
grid minor
ax=gca;
ax.FontSize = 15;



%% Visible Satellite Distance Heatmap

% Replace int with -1 as a placeholder for no visibility,
LOS_visible_distances(LOS_visible_distances == inf) = -1;

% Create heatmap
imagesc(LOS_visible_distances/1000);    % in km

% Define start and end datetime
startDateTime = datetime(2023, 1, 1, 0, 0, 0); % 1st Jan 2023, 00:00:00
endDateTime = datetime(2023, 1, 31, 0, 0, 0); % 30th Jan 2023, 23:59:00

% Generate datetime vector with 1 minute timestep
dateTimeVector = startDateTime:minutes(1):endDateTime;

% Customize the colormap
cmap = colormap;
cmap(1,:) = [1 1 1]; % Set the first color to white for NaN values
colormap(cmap);
% Add colorbar for reference
colorbar;

% Specify y-axis ticks
yticks(linspace(1, size(LOS_visibility_data_v1, 1), 5)); % Evenly spaced ticks
yticklabels({'1 Jan', '8 Jan', '15 Jan', '22 Jan', '30 Jan'}); % Specify the labels for the ticks
ax=gca;
ax.FontSize = 18;


% Set axis labels
xlabel('Starlink Satellie Number');
title('Inter-satellite Distance [km] 2023');


% create a new pair of axes inside current figure
axes('position',[.60 .65 .25 .25])
box on % put box around new pair of axes
%indexOfInterest = (XDates < '06-Dec-2023 06:19:00') & (XDates > '05-Dec-2023 23:19:00');
% Create heatmap
imagesc(LOS_visible_distances(1:200, 1:17)/1000);    % in km
yticks('');
xticks('auto');
xtickangle(45);
grid on
grid minor
axis tight
axes2=gca;
axes2.FontSize = 18;
