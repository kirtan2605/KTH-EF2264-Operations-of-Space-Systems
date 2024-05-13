clc
clear
close all

load("interSat_distances.mat")
load("LOS_visibility_data_v1.mat")


set(groot, 'DefaultTextInterpreter', 'latex')
set(groot, 'DefaultLegendInterpreter', 'latex')
set(groot, 'DefaultAxesTickLabelInterpreter', 'latex')

% Define start and end datetime
startDateTime = datetime(2023, 1, 1, 0, 0, 0); % 1st Jan 2023, 00:00:00
endDateTime = datetime(2023, 1, 31, 0, 0, 0); % 30th Jan 2023, 23:59:00

% Generate datetime vector with 1 minute timestep
dateTimeVector = startDateTime:minutes(1):endDateTime;



LOS_visible_distances = LOS_visibility_data.*interSatdistancesdata;

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
