clear all;
clc;

% Define the coordinates of the satellites over time
MATS_coords = load("Satellite_positions/MATS.txt"); % [x1, y1, z1] coordinates over time
Starlink_coords = load("Satellite_positions/Starlink_006.txt"); % [x2, y2, z2] coordinates over time

% convert distances to km
MATS_coords = MATS_coords/1000;
Starlink_coords = Starlink_coords/1000;


% Define the binary vector indicating the time steps to display the line of sight
LOS_visibility_data = load("LOS_visibility_data_v1.mat");
line_of_sight_steps = LOS_visibility_data.LOS_visibility_data_v1(:,6); % Binary vector of the same length as the coordinates
LOS_MATS_coords = line_of_sight_steps.*MATS_coords;
LOS_Starlink_coords = line_of_sight_steps.*Starlink_coords;


% Create a figure
figure;
hold on;
grid on;
xlabel('X');
ylabel('Y');
zlabel('Z');

% Set axis limits according to satellite positions
xlim([-8000, 8000])
ylim([-8000, 8000])
zlim([-8000, 8000])
grid on;
view(45, 10);
rotate3d on;

% drawing the earth sphere
earth_sphere('km')



%% Plots
% Initialize plot objects
MATS_plot = plot3(MATS_coords(1,1), MATS_coords(1,2), MATS_coords(1,3), 'o', 'MarkerSize', 5, 'MarkerFaceColor', 'red', 'MarkerEdgeColor', 'red'); % Plot MATS satellite
Starlink_plot = plot3(Starlink_coords(1,1), Starlink_coords(1,2), Starlink_coords(1,3), 'o', 'MarkerSize', 5, 'MarkerFaceColor', 'magenta', 'MarkerEdgeColor', 'magenta'); % Plot Starlink satellite
LineOfSight = plot3([LOS_MATS_coords(1,1), LOS_Starlink_coords(1,1)],...
                    [LOS_MATS_coords(1,2), LOS_Starlink_coords(1,2)],...
                    [LOS_MATS_coords(1,3), LOS_Starlink_coords(1,3)],'Color', 'y', 'LineWidth', 1);% Plot the initial line of sight

% Animate the motion of the satellites
for i = 2:size(MATS_coords, 1)
    % Update satellite positions
    set(MATS_plot, 'XData', MATS_coords(i,1), 'YData', MATS_coords(i,2), 'ZData', MATS_coords(i,3));
    set(Starlink_plot, 'XData', Starlink_coords(i,1), 'YData', Starlink_coords(i,2), 'ZData', Starlink_coords(i,3));

     set(LineOfSight, 'XData', [LOS_MATS_coords(i,1), LOS_Starlink_coords(i,1)],...
                      'YData', [LOS_MATS_coords(i,2), LOS_Starlink_coords(i,2)],...
                      'ZData', [LOS_MATS_coords(i,3), LOS_Starlink_coords(i,3)]);

    drawnow; % Update the plot
    pause(0.05); % Pause to control animation speed
end