#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import time
import sys

# Variables
V_X = 0
V_Y = 1
V_Z = 2
V_YAW = 5

# List if indices
## 0    time_stamps

## 1    ground_truth

## 7    est_ellipse
## 13	est_arrow
## 19	est_corners
## 25	est_dead_reckoning

## 31	est_error_ellipse
## 37	est_error_arrow
## 43	est_error_corners
## 49	est_error_dead_reckoning

## 55   filtered_estimate

def plot_data(stored_array, methods_to_plot, variables_to_plot, plot_error=False, plot_z_to_the_right=False, z_right_color='g'):
    t_id = 0            # Time index
    g_id = 1            # Ground truth index
    e_id = g_id + 6     # Ellipse index
    a_id = e_id + 6     # Arrow index
    c_id = a_id + 6     # Corner index
    d_id = c_id + 6     # Dead reckoning index

    error_e_id = d_id + 6     # Ellipse error index
    error_a_id = error_e_id + 6     # Arrow error index
    error_c_id = error_a_id + 6     # Corner error index
    error_d_id = error_c_id + 6     # Dead reckoning error index

    time_stamps = stored_array[:, t_id]

    titles_variables = [
        "x-Position", "y-Position", "z-Position", "None", "None", "yaw-Rotation"
    ]
    titles_error_variables = [
        "x-Position Error", "y-Position Error", "z-Position Error",
        "none", "none", "yaw-Rotation Error"
    ]

    lables_variables = [
        "x-Position [m]", "y-Position [m]", "z-Position [m]", "none", "none", "yaw-Rotation [deg]",
    ]
    lables_error_variables = [
        "x-Position Error [m]", "y-Position Error [m]", "z-Position Error [m]", "none", "none", "yaw-Rotation Error [deg]",
    ]
    titles_methods = [
        "Ground truth",
        "Ellipse",
        "Arrow",
        "Corners",
        "Dead reckogning",
        "Ellipse error",
        "Arrow error",
        "Corners error",
        "Dead reckogning error",
    ]
    indices_methods = [g_id, e_id, a_id, c_id, d_id,
        error_e_id, error_a_id, error_c_id, error_d_id
    ]
    colors_methods = [
        "g",        # green:    "Ground truth"
        "b",        # blue:     "Ellipse"
        "r",        # red:      "Arrow"
        "orange",   # orange:   "Corners"
        "k",        # black:    "Dead reckogning"
        "b",        # blue:     "Ellipse error"
        "r",        # red:      "Arrow error"
        "orange",   # orange:   "Corners error"
        "k"         # black:    "Dead reckogning error"
    ]
    y_ticks_error_pos = np.arange(-0.10, 0.11, 0.025)
    y_ticks_error_rot = np.arange(-10, 11, 2)
    y_ticks_error = np.array([
        [y_ticks_error_pos]*3, [y_ticks_error_rot]*3
    ])

    for variable in variables_to_plot:

        if plot_error:
            title = titles_error_variables[variable]
            y_label = lables_error_variables[variable]
        else:
            title = titles_variables[variable]
            y_label = lables_variables[variable]

        fig, ax = plt.subplots(figsize=(10,8))
        # fig, ax = plt.subplots(figsize=(20,15))

        if plot_error:
            ax.axhline(y=0, color='grey', linestyle='--') # Plot the zero-line


        for method in methods_to_plot:
            legend_text = titles_methods[method]
            line_color = colors_methods[method]
            index = indices_methods[method]

            data = stored_array[:, index:index+6][:,variable]
            time_stamps_local = time_stamps.copy()
            time_stamps_local[np.isnan(data)] = np.nan
      
            line, = ax.plot(time_stamps_local, data)
            line.set_color(line_color)
            line.set_label(legend_text)

            ax.set_title(title)
            ax.set_xlabel('Time [s]')
            ax.set_ylabel(y_label)
            ax.legend(loc='upper left', facecolor='white', framealpha=1)

            # if plot_error:
            #     ax.set_yticks(y_ticks_error[variable])

            # ax.xaxis.grid()
            # ax.yaxis.grid()
            # ax.grid()
        
        if plot_z_to_the_right:
            # Plot the z ground truth
            gt_method = 0
            z_variable = 2

            index = indices_methods[gt_method]
            data = stored_array[:, index:index+6][:, z_variable]
            time_stamps_local = time_stamps.copy()
            time_stamps_local[np.isnan(data)] = np.nan

            ax2 = ax.twinx()
            line, = ax2.plot(time_stamps_local, data)
            line.set_color(z_right_color)
            line.set_label("Ground truth z-Position")

            ax2.legend(loc='upper right', facecolor='white', framealpha=1)

            ax2.set_ylabel('z-Position [m]', color=z_right_color)
            ax2.set_yticks(np.arange(7))
            ax2.tick_params(axis='y', labelcolor=z_right_color)
            ax2.grid(None)

        plt.xlim(time_stamps[0], time_stamps[-1])
        plt.grid()

        fig.tight_layout()
        
        folder = './plots/'
        plt.savefig(folder+title+'.svg')


        fig.draw
        plt.waitforbuttonpress(0)
        plt.close()

        # plt.show()

def plot_data_manually(stored_array):
    index_values = [1, 7, 13, 19]
    color_values = ['green', 'blue', 'red', 'orange']
    legend_values = ['ground truth', 'ellipse', 'arrow', 'corners']
    legend_lines = []

    index_errors = [31, 37, 43]
    color_errors = ['blue', 'red', 'orange']

    time_stamps = stored_array[:, 0]
    ground_truth = stored_array[:, 1:1+6]

    fig = plt.figure(figsize=(10,12))

    for i in range(1,9):
        ax = plt.subplot(4,2,i)
        plt.grid()
        plt.xlim(time_stamps[0], time_stamps[-1])

        # Plot the ground truth value for z
        right_ax = ax.twinx()

        legend_text = 'ground truth z-position'
        z_right_color = 'lightgrey'

        data = ground_truth[:,V_Z]
        time_stamps_local = time_stamps.copy()
        time_stamps_local[np.isnan(data)] = np.nan

        line, = right_ax.plot(time_stamps_local, data)
        line.set_color(z_right_color)

        right_ax.set_ylabel('z-position [m]', color='grey')
        right_ax.tick_params(axis='y', labelcolor='grey')
        right_ax.set_ylim(-0.07, 5.84)

        if i == 1:
            variable = V_X
            y_label = "x-position [m]"
            y_tics = np.linspace(-0.25, 0.05, num=7)
        elif i == 2:
            variable = V_X
            y_label = "x-position error [m]"
            y_tics = np.linspace(-0.10, 0.10, num=5)
        elif i == 3:
            variable = V_Y
            y_label = "y-position [m]"
            y_tics = np.linspace(-0.15, 0.15, num=7)
        elif i == 4:
            variable = V_Y
            y_label = "y-position error[m]"
            y_tics = np.linspace(-0.10, 0.10, num=5)
        elif i == 5:
            variable = V_Z
            y_label = "z-position [m]"
            y_tics = np.linspace(0, 5, num=6)
        elif i == 6:
            variable = V_Z
            y_label = "z-position error[m]"
            y_tics = np.linspace(0.0, 0.8, num=5)
        elif i == 7:
            variable = V_YAW
            y_label = "yaw-rotation [deg]"
            y_tics = np.linspace(0, 80, num=5)
        elif i == 8:
            variable = V_YAW
            y_label = "yaw-rotation error [deg]"
            y_tics = np.linspace(0, 80, num=5)

        # Label x-axis
        if i==7 or i==8:
            ax.set_xlabel('Time [s]')

        # Plot the estimate values
        if i % 2 == 1:
            for j in range(4):
                if (i==7 and j==1): # Skip the ellipse yaw estimate
                   continue 

                index = index_values[j]
                color = color_values[j]
                legend_text = legend_values[j]
            
                data = stored_array[:, index:index+6][:,variable]
            
                time_stamps_local = time_stamps.copy()
                time_stamps_local[np.isnan(data)] = np.nan
        
                line, = ax.plot(time_stamps_local, data)
                line.set_color(color)

                if i == 1:
                    legend_lines.append(line)
            
        # Plot the estimate errors
        if i % 2 == 0:
            ax.axhline(y=0, color='grey', linestyle='--') # Plot the zero-line

            for j in range(3):
                if (i==8 and j==0): # Skip the ellipse yaw estimate
                    continue
                index = index_errors[j]
                color = color_errors[j]            

                data = stored_array[:, index:index+6][:,variable]
            
                time_stamps_local = time_stamps.copy()
                time_stamps_local[np.isnan(data)] = np.nan
        
                line, = ax.plot(time_stamps_local, data)
                line.set_color(color)
            
        ax.set_ylabel(y_label)
        ax.set_yticks(y_tics)


    fig.legend(legend_lines, legend_values, bbox_to_anchor=(0.3, 0.6, 0.4, 0.77), loc='center', ncol=4)

    fig.tight_layout(w_pad=1.5, rect=[0, 0, 1, 0.98])

    folder = './plots/'
    title = 'Up_down_5m'
    plt.savefig(folder+title+'.svg')

    # fig.draw
    # plt.waitforbuttonpress(0)
    # plt.close()

    # plt.show()

    
def plot_hover_compare(hover_0_5m, hover_1m, hover_2m, hover_3m, hover_5m, hover_10m):
    file_titles = ['Hover_x', 'Hover_y', 'Hover_z', 'None', 'None', 'Hover_yaw']
    titles = ['z=0.5m','z=1m','z=1.8m','z=3m','z=5m','z=10m']
    all_hover_data = np.array([hover_0_5m, hover_1m, hover_2m, hover_3m, hover_5m, hover_10m])

    index_values = [1, 7, 13, 19]
    color_values = ['green', 'blue', 'red', 'orange']
    legend_values = ['ground truth', 'ellipse', 'arrow', 'corners']
    y_labels = ['x-position [m]', 'y-position [m]', 'z-position [m]', 'none', 'none', 'yaw-rotation [m]']

    x_ytics = [np.linspace(-0.10, 0.20, num=7)]*6
    y_ytics = [np.linspace(-0.15, 0.15, num=7)]*6
    z_ytics = [np.linspace(0.30, 0.70, num=5), np.linspace(0.80, 1.20, num=5), np.linspace(1.70, 2.10, num=5),
        np.linspace(2.80, 3.20, num=5), np.linspace(4.80, 5.80, num=6), np.linspace(9.80, 10.20, num=5)]
    yaw_ytics = [np.linspace(-8, 8, num=9), np.linspace(-8, 8, num=9), np.linspace(-8, 8, num=9),
        np.linspace(-8, 8, num=9), np.linspace(0, 140, num=8), np.linspace(-8, 8, num=9)]

    for variable in [V_X, V_Y, V_Z, V_YAW]:
        file_title = file_titles[variable]
        y_label = y_labels[variable]
        fig = plt.figure(figsize=(10,12))

        for i in range(6):
            ax = plt.subplot(3,2,i+1)
            if i==4 or i==5:
                ax.set_xlabel('Time [s]')

            title = titles[i]
            hover_data = all_hover_data[i]
            time_stamps = hover_data[:, 0]

            plt.title(title)
            plt.grid()
            plt.xlim(time_stamps[0], time_stamps[-1])

            for j in range(4):
                if variable==V_YAW and j==1: # Skip the ellipse yaw estimate
                    continue
                index = index_values[j]
                color = color_values[j]
                legend_text = legend_values[j]
            
                data = hover_data[:, index:index+6][:,variable]
            
                time_stamps_local = time_stamps.copy()
                time_stamps_local[np.isnan(data)] = np.nan
        
                line, = ax.plot(time_stamps_local, data)
                line.set_color(color)
                line.set_label(legend_text if i==1 else "_nolegend_")
            
            ax.set_ylabel(y_label)

            if variable == V_X:
                ax.set_yticks(x_ytics[i])
            elif variable == V_Y:
                ax.set_yticks(y_ytics[i])
            elif variable == V_Z:
                ax.set_yticks(z_ytics[i]) 
            elif variable == V_YAW:
                ax.set_yticks(yaw_ytics[i])

            # Plot legend on top
            if i==1:
                plt.legend(bbox_to_anchor=(-0.7, 1.2, 1.2, 0.0), loc='upper right', ncol=5, mode='expand')

        fig.tight_layout()

        folder = './plots/'
        plt.savefig(folder+file_title+'.svg')


def plot_hover_error_compare(hover_0_5m, hover_1m, hover_2m, hover_3m, hover_5m, hover_10m):
    file_titles = ['Hover_error_x', 'Hover_error_y', 'Hover_error_z', 'None', 'None', 'Hover_error_yaw']
    titles = ['z=0.5m','z=1m','z=1.8m','z=3m','z=5m','z=10m']
    all_hover_data = np.array([hover_0_5m, hover_1m, hover_2m, hover_3m, hover_5m, hover_10m])
    
    index_values = [31, 37, 43]
    color_values = ['blue', 'red', 'orange']
    legend_values = ['ellipse', 'arrow', 'corners']
    y_labels = ['x-position error[m]', 'y-position error[m]', 'z-position error[m]', 'none', 'none', 'yaw-rotation error[m]']

    x_ytics = [np.linspace(-0.10, 0.10, num=5)]*6
    x_ytics[5] = np.linspace(-0.15, 0.15, num=7)
    y_ytics = x_ytics

    z_ytics = [np.linspace(-0.20, 0.20, num=9)]*6
    z_ytics[4] = np.linspace(0, 1.0, num=6)

    yaw_ytics = [np.linspace(-6, 6, num=7)]*6
    yaw_ytics[4] = np.linspace(-140, 140, num=15)

    for variable in [V_X, V_Y, V_Z, V_YAW]:
        file_title = file_titles[variable]
        y_label = y_labels[variable]
        fig = plt.figure(figsize=(10,12))

        for i in range(6):
            ax = plt.subplot(3,2,i+1)
            ax.axhline(y=0, color='grey', linestyle='--') # Plot the zero-line
            if i==4 or i==5:
                ax.set_xlabel('Time [s]')

            title = titles[i]
            hover_data = all_hover_data[i]
            time_stamps = hover_data[:, 0]

            plt.title(title)
            plt.grid()
            plt.xlim(time_stamps[0], time_stamps[-1])

            for j in range(3):
                if variable==V_YAW and j==0: # Skip the ellipse yaw estimate
                    continue
                index = index_values[j]
                color = color_values[j]
                legend_text = legend_values[j]
            
                data = hover_data[:, index:index+6][:,variable]
            
                time_stamps_local = time_stamps.copy()
                time_stamps_local[np.isnan(data)] = np.nan
        
                line, = ax.plot(time_stamps_local, data)
                line.set_color(color)
                line.set_label(legend_text if i==1 else "_nolegend_")
            
            ax.set_ylabel(y_label)

            if variable == V_X:
                ax.set_yticks(x_ytics[i])
            elif variable == V_Y:
                ax.set_yticks(y_ytics[i])
            elif variable == V_Z:
                ax.set_yticks(z_ytics[i]) 
            elif variable == V_YAW:
                ax.set_yticks(yaw_ytics[i])

            # Plot legend on top
            if i==1:
                plt.legend(bbox_to_anchor=(-0.7, 1.2, 1.2, 0.0), loc='upper right', ncol=5, mode='expand')

        fig.tight_layout()

        folder = './plots/'
        plt.savefig(folder+file_title+'.svg')



def plot_step_z(data_step_z):
    file_title = "Step_z"

    variable = V_Y
    index_values = [1, 7, 13, 19, 25, 55]
    color_values = ['green', 'blue', 'red', 'orange', 'grey', 'black']
    legend_values = ['ground truth', 'ellipse', 'arrow', 'corners', 'filter_estimate', 'dead_reckoning']


    time_stamps = data_step_z[:, 0]

    fig = plt.figure(figsize=(7,5))
    ax = plt.subplot()
    plt.grid()
    plt.xlim(time_stamps[0], time_stamps[-1])

    for i in range(len(index_values)):
        if i==0:
            ax.set_xlabel('Time [s]')
            ax.set_ylabel('z-position [m]')

        index = index_values[i]
        color = color_values[i]
        legend_text = legend_values[i]
    
        data = data_step_z[:, index:index+6][:,variable]
    
        time_stamps_local = time_stamps.copy()
        time_stamps_local[np.isnan(data)] = np.nan

        line, = ax.plot(time_stamps_local, data)
        line.set_color(color)
        line.set_label(legend_text)

    plt.legend()
    
    fig.tight_layout()

    folder = './plots/'
    plt.savefig(folder+file_title+'.svg')


if __name__ == '__main__':
    # Load the data
    # folder = './catkin_ws/src/uav_vision/data_storage/experiment_data/'
    folder = './catkin_ws/src/uav_vision/data_storage/'
    
    # Up and down test
    test_number = 1
    filename = 'test_'+str(test_number)+'.npy'
    path = folder + filename
    up_and_down_5m = np.load(path, allow_pickle=True)

    # Hover tests
    test_number = 2
    filename = 'test_'+str(test_number)+'.npy'
    path = folder + filename
    hover_0_5m = np.load(path, allow_pickle=True)

    test_number = 3
    filename = 'test_'+str(test_number)+'.npy'
    path = folder + filename
    hover_1m = np.load(path, allow_pickle=True)

    test_number = 4
    filename = 'test_'+str(test_number)+'.npy'
    path = folder + filename
    hover_2m = np.load(path, allow_pickle=True)

    test_number = 5
    filename = 'test_'+str(test_number)+'.npy'
    path = folder + filename
    hover_3m = np.load(path, allow_pickle=True)

    test_number = 6
    filename = 'test_'+str(test_number)+'.npy'
    path = folder + filename
    hover_5m = np.load(path, allow_pickle=True)

    test_number = 7
    filename = 'test_'+str(test_number)+'.npy'
    path = folder + filename
    hover_10m = np.load(path, allow_pickle=True)

    # Step test
    test_number = 8
    filename = 'test_'+str(test_number)+'.npy'
    path = folder + filename
    data_step_z = np.load(path, allow_pickle=True)
    



    #################
    # Plot the data #
    #################
    # plot_data_manually(up_and_down_5m)

    # plot_hover_compare(hover_0_5m, hover_1m, hover_2m, hover_3m, hover_5m, hover_10m)
    
    # plot_hover_error_compare(hover_0_5m, hover_1m, hover_2m, hover_3m, hover_5m, hover_10m)

    plot_step_z(data_step_z)