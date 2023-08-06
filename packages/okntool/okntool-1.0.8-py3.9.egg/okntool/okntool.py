import sys
import argparse
import json
import csv
import numpy as np
import os
import subprocess
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


# This function is to get header position from the given array
def get_index(search_input, array_in):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(array_in):
        if val == search_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_input} can not be found!")

    return return_idx


# This function is to get file name from the given directory
def get_file_name(dir_input):
    output_file_name = None
    dir_input = str(dir_input).replace("\\\\", "\\")
    string_array = str(dir_input).split("\\")
    if len(string_array) > 0:
        output_file_name = string_array[-1]

    return output_file_name


# This function is to translate disk condition string to logmar value
def disk_to_logmar(disk_string_input):
    disk_logmar_equivalent = {"disk-condition-1-1": 1.0, "disk-condition-1-2": 1.0, "disk-condition-2-1": 0.9,
                              "disk-condition-2-2": 0.9, "disk-condition-3-1": 0.8, "disk-condition-3-2": 0.8,
                              "disk-condition-4-1": 0.7, "disk-condition-4-2": 0.7, "disk-condition-5-1": 0.6,
                              "disk-condition-5-2": 0.6, "disk-condition-6-1": 0.5, "disk-condition-6-2": 0.5,
                              "disk-condition-7-1": 0.4, "disk-condition-7-2": 0.4, "disk-condition-8-1": 0.3,
                              "disk-condition-8-2": 0.3, "disk-condition-9-1": 0.2, "disk-condition-9-2": 0.2,
                              "disk-condition-10-1": 0.1, "disk-condition-10-2": 0.1, "disk-condition-11-1": 0.0,
                              "disk-condition-11-2": 0.0, "disk-condition-12-1": -0.1, "disk-condition-12-2": -0.1,
                              "disk-condition-13-1": -0.2, "disk-condition-13-2": -0.2, "no-disk-condition": "no logMAR"}

    return disk_logmar_equivalent[disk_string_input]


# This function is to draw a graph with slow phase and quick phase overlay from the given config info
def draw_graph_with_overlay(input_dir, x_header, y_header, title, x_label_input, y_label_input,
                            sp_data_header_name_input, qp_data_header_name_input,
                            graph_line_color_input, graph_line_thickness_input,
                            sp_line_color_input, sp_line_thickness_input,
                            qp_line_color_input, qp_line_thickness_input,
                            output_image_name_input, signal_dir_input):
    file_to_open = open(input_dir)
    csv_reader = csv.reader(file_to_open)
    header_array = []
    rows = []
    count_one = 0

    for row in csv_reader:
        if count_one <= 0:
            header_array = row
            count_one += 1
        else:
            rows.append(row)

    x_header_position = get_index(x_header, header_array)
    y_header_position = get_index(y_header, header_array)

    x_array = []
    y_array = []
    first_value_recorded = False
    first_value = 0

    for row in rows:
        raw_value = float(row[x_header_position])
        if not first_value_recorded:
            first_value = raw_value
            first_value_recorded = True
        value_input = raw_value - first_value
        x_array.append(value_input)

        y_array.append(float(row[y_header_position]))

    file_to_open = open(signal_dir_input)
    csv_reader2 = csv.reader(file_to_open)
    header_array2 = []
    rows2 = []
    count_one2 = 0

    for row in csv_reader2:
        if count_one2 <= 0:
            header_array2 = row
            count_one2 += 1
        else:
            rows2.append(row)

    # print(header_array2)
    slow_phase_position = get_index(sp_data_header_name_input, header_array2)
    quick_phase_position = get_index(qp_data_header_name_input, header_array2)

    sp_array = []
    qp_array = []

    for row in rows2:
        sp_value = row[slow_phase_position]
        qp_value = row[quick_phase_position]
        sp_array.append(str(sp_value).lower())
        qp_array.append(str(qp_value).lower())

    # for ind in range(len(sp_array)):
    #     print(sp_array[ind], qp_array[ind])
    #     if sp_array[ind] == "false" and qp_array[ind] == "false":
    #         print("both false")

    for ind in range(len(sp_array)):
        if sp_array[ind] == "true":
            sp_array[ind] = y_array[ind]
        else:
            sp_array[ind] = np.nan

    for ind in range(len(qp_array)):
        if qp_array[ind] == "true":
            qp_array[ind] = y_array[ind]
            previous_ind = ind - 1
            if previous_ind >= 0:
                qp_array[ind - 1] = y_array[ind - 1]

        else:
            qp_array[ind] = np.nan

    plt.plot(x_array, y_array, color=graph_line_color_input, linewidth=graph_line_thickness_input)
    plt.plot(x_array, sp_array, color=sp_line_color_input, linewidth=sp_line_thickness_input)
    plt.plot(x_array, qp_array, color=qp_line_color_input, linewidth=qp_line_thickness_input)
    plt.title(title)
    plt.xlabel(x_label_input)
    plt.ylabel(y_label_input)
    csv_name = get_file_name(input_dir)
    output_dir = input_dir.replace(csv_name, "")
    os.chdir(output_dir)
    plt.savefig(output_image_name_input)
    plt.close()

    print(f"{output_image_name_input} is created in the directory:{output_dir}.")


# This function is to produce a plan as an array from the given folder to be used in drawing combined summary plot
def get_plot_info(data_dir, x_data_header, y_data_header,
                  x_axis_limit_input, y_axis_limit_input, mean_offset_input,
                  axis_adjustment_types_input, axis_adjustment_type_number_input,
                  x_label_input, y_label_input, signal_csv_folder_name_input,
                  signal_csv_name_input, sp_column_name_input,
                  sp_line_color_input, sp_line_thickness_input,
                  qp_column_name_input, qp_line_color_input,
                  qp_line_thickness_input, summary_csv_name_input):
    # folder_array = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]
    # for name in os.listdir(data_dir):
    #     print(name)
    folder_array = get_folder_name_from_dir(data_dir, "trial_id", "disk_condition", summary_csv_name_input)

    adjustment_type = axis_adjustment_types_input[str(axis_adjustment_type_number_input)]
    if adjustment_type == "mean_offset":
        plot_info_array = []
        x_adjust_limit, y_adjust_limit = get_adjust_limit(data_dir, x_data_header, y_data_header, folder_array,
                                                          x_axis_limit_input, y_axis_limit_input, mean_offset_input,
                                                          axis_adjustment_types_input,
                                                          axis_adjustment_type_number_input)
        adjust_limit_dict = {"x_adjust_limit": x_adjust_limit, "y_adjust_limit": y_adjust_limit}
        for folder_name in folder_array:
            trial_id, disk_condition = str(folder_name).split("_")
            # print(trial_id)
            # print(disk_condition)
            data_dir_to_be_used = os.path.join(data_dir, folder_name, f"updated_{folder_name}.csv")
            x_array = get_data_array(data_dir_to_be_used, x_data_header)
            y_array = get_data_array(data_dir_to_be_used, y_data_header)
            y_mean = np.mean(y_array)
            y_array = [value - y_mean for value in y_array]
            signal_csv_dir = os.path.join(data_dir, folder_name, signal_csv_folder_name_input, signal_csv_name_input)
            sp_array, qp_array = get_sp_and_qp_array(signal_csv_dir, sp_column_name_input, qp_column_name_input,
                                                     y_array)
            plot_info = {"trial_id": trial_id, "disk_condition": disk_condition,
                         "x_label": x_label_input, "y_label": y_label_input,
                         "x_array": x_array, "y_array": y_array,
                         "sp_array": sp_array, "qp_array": qp_array,
                         "sp_line_color": sp_line_color_input, "sp_line_thickness": sp_line_thickness_input,
                         "qp_line_color": qp_line_color_input, "qp_line_thickness": qp_line_thickness_input,
                         "logmar": disk_to_logmar(disk_condition)}
            plot_info_array.append(plot_info)
    else:
        plot_info_array = []
        x_adjust_limit, y_adjust_limit = get_adjust_limit(data_dir, x_data_header, y_data_header, folder_array,
                                                          x_axis_limit_input, y_axis_limit_input, mean_offset_input,
                                                          axis_adjustment_types_input,
                                                          axis_adjustment_type_number_input)
        adjust_limit_dict = {"x_adjust_limit": x_adjust_limit, "y_adjust_limit": y_adjust_limit}
        for folder_name in folder_array:
            trial_id, disk_condition = str(folder_name).split("_")
            # print(trial_id)
            # print(disk_condition)
            data_dir_to_be_used = os.path.join(data_dir, folder_name, f"updated_{folder_name}.csv")
            x_array = get_data_array(data_dir_to_be_used, x_data_header)
            y_array = get_data_array(data_dir_to_be_used, y_data_header)
            signal_csv_dir = os.path.join(data_dir, folder_name, signal_csv_folder_name_input, signal_csv_name_input)
            sp_array, qp_array = get_sp_and_qp_array(signal_csv_dir, sp_column_name_input, qp_column_name_input,
                                                     y_array)
            plot_info = {"trial_id": trial_id, "disk_condition": disk_condition,
                         "x_label": x_label_input, "y_label": y_label_input,
                         "x_array": x_array, "y_array": y_array,
                         "sp_array": sp_array, "qp_array": qp_array,
                         "sp_line_color": sp_line_color_input, "sp_line_thickness": sp_line_thickness_input,
                         "qp_line_color": qp_line_color_input, "qp_line_thickness": qp_line_thickness_input,
                         "logmar": disk_to_logmar(disk_condition)}
            plot_info_array.append(plot_info)

    return plot_info_array, adjust_limit_dict


# This function is to retrieve folder names from the given csv
def get_folder_name_from_dir(dir_input, trial_id_header_input, disk_condition_header_input,
                             summary_csv_name_input):
    csv_dir = os.path.join(dir_input, summary_csv_name_input)

    file_to_open = open(csv_dir)
    csv_reader = csv.reader(file_to_open)
    header_array = []
    rows = []
    count_one = 0
    output_array = []

    for row in csv_reader:
        if count_one <= 0:
            header_array = row
            count_one += 1
        else:
            rows.append(row)

    trial_id_header_position = get_index(trial_id_header_input, header_array)
    disk_condition_header_position = get_index(disk_condition_header_input, header_array)

    for row in rows:
        trial_string_raw = row[trial_id_header_position]
        disk_string_raw = row[disk_condition_header_position]
        folder_name_input = f"{trial_string_raw}_{disk_string_raw}"
        output_array.append(folder_name_input)

    return output_array


# This function is to retrieve the data array from the given csv and header name
def get_data_array(data_dir, header_name_input):
    file_to_open = open(data_dir)
    csv_reader = csv.reader(file_to_open)
    header_array = []
    rows = []
    count_one = 0

    for row in csv_reader:
        if count_one <= 0:
            header_array = row
            count_one += 1
        else:
            rows.append(row)

    header_position = get_index(header_name_input, header_array)

    output_array = []
    first_value_recorded = False
    first_value = 0

    if "timestamp" in str(header_name_input):
        for row in rows:
            raw_value = float(row[header_position])
            if not first_value_recorded:
                first_value = raw_value
                first_value_recorded = True
            value_input = raw_value - first_value
            output_array.append(value_input)
    else:
        for row in rows:
            output_array.append(float(row[header_position]))

    return output_array


# This function is to retrieve the slow phase and quick phase data arrays from the given signal csv
def get_sp_and_qp_array(signal_dir_input, sp_column_name_input, qp_column_name_input, y_data_array_input):
    sp_array = []
    qp_array = []
    file_to_open = open(signal_dir_input)
    csv_reader = csv.reader(file_to_open)
    header_array = []
    rows = []
    count = 0

    for row in csv_reader:
        if count <= 0:
            header_array = row
            count += 1
        else:
            rows.append(row)

    slow_phase_position = get_index(sp_column_name_input, header_array)
    quick_phase_position = get_index(qp_column_name_input, header_array)

    for row in rows:
        sp_value = row[slow_phase_position]
        qp_value = row[quick_phase_position]
        sp_array.append(str(sp_value).lower())
        qp_array.append(str(qp_value).lower())

    for ind in range(len(sp_array)):
        if sp_array[ind] == "true":
            sp_array[ind] = y_data_array_input[ind]
        else:
            sp_array[ind] = np.nan

    for ind in range(len(qp_array)):
        if qp_array[ind] == "true":
            qp_array[ind] = y_data_array_input[ind]
            previous_ind = ind - 1
            if previous_ind >= 0:
                qp_array[ind - 1] = y_data_array_input[ind - 1]
        else:
            qp_array[ind] = np.nan

    return sp_array, qp_array


# The main function to plot the combined graph with plan array/plot info
# If max graph in a row is "none", there is no limitation of graph number in a row
def plot_combined_graph(plot_info_input, max_graph_in_a_row_input, output_dir,
                        adjust_limit_info_input, line_color, line_thickness,
                        image_scale_input, output_image_name_input):
    x_adjust_limit = adjust_limit_info_input["x_adjust_limit"]
    x_lower_limit = x_adjust_limit["lower_limit"]
    x_upper_limit = x_adjust_limit["upper_limit"]
    y_adjust_limit = adjust_limit_info_input["y_adjust_limit"]
    y_lower_limit = y_adjust_limit["lower_limit"]
    y_upper_limit = y_adjust_limit["upper_limit"]

    if type(max_graph_in_a_row_input) == str and str(max_graph_in_a_row_input).lower() == "none":
        final_plot_array = []
        logmar_level_array = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1, -0.2, "no logMAR"]
        for logmar_level in logmar_level_array:
            temp_logmar_info_array = []

            for info in plot_info_input:
                if info["logmar"] == logmar_level:
                    temp_logmar_info_array.append(info)

            if len(temp_logmar_info_array) > 0:
                temp_dict = {"logmar_level": logmar_level, "info_array": temp_logmar_info_array}
                final_plot_array.append(temp_dict)

        if len(final_plot_array) > 0:
            final_row_length = len(final_plot_array)
            final_column_length = 0
            for plot_info in final_plot_array:
                info_array = plot_info["info_array"]
                if len(info_array) > final_column_length:
                    final_column_length = len(info_array)

            # print(final_row_length)
            # print(final_column_length)
            if final_row_length <= 1:
                plot_info_len = len(final_plot_array)
                print("len", plot_info_len)
                if plot_info_len <= 1:
                    plot_info = final_plot_array[0]
                    logmar_level = plot_info["logmar_level"]
                    info_array = plot_info["info_array"]
                    info = info_array[0]
                    x_array = info["x_array"]
                    y_array = info["y_array"]
                    x_label = info["x_label"]
                    y_label = info["y_label"]
                    sp_array = info["sp_array"]
                    sp_line_color = info["sp_line_color"]
                    sp_line_thickness = info["sp_line_thickness"]
                    qp_array = info["qp_array"]
                    qp_line_color = info["qp_line_color"]
                    qp_line_thickness = info["qp_line_thickness"]
                    trial_id = info["trial_id"]
                    axs_title = f"{trial_id}(logMAR {logmar_level})"
                    plt.plot(x_array, y_array, color=line_color, linewidth=line_thickness)
                    plt.plot(x_array, sp_array, color=sp_line_color, linewidth=sp_line_thickness)
                    plt.plot(x_array, qp_array, color=qp_line_color, linewidth=qp_line_thickness)
                    plt.title(axs_title)
                    plt.xlabel(x_label)
                    plt.ylabel(y_label)
                    os.chdir(output_dir)
                    plt.savefig(output_image_name_input)
                    plt.close()
                else:
                    fig, axs = plt.subplots(final_row_length, final_column_length,
                                            figsize=(final_column_length * image_scale_input,
                                                     final_row_length * image_scale_input))
                    for row_index, plot_info in enumerate(final_plot_array):
                        # print(row_index)
                        logmar_level = plot_info["logmar_level"]
                        info_array = plot_info["info_array"]
                        info_array_length = len(info_array)
                        num_plot_to_be_deleted = 0
                        if info_array_length < int(final_column_length):
                            num_plot_to_be_deleted = final_column_length - info_array_length
                        for column_index, info in enumerate(info_array):
                            # print(column_index)
                            x_array = info["x_array"]
                            y_array = info["y_array"]
                            x_label = info["x_label"]
                            y_label = info["y_label"]
                            sp_array = info["sp_array"]
                            sp_line_color = info["sp_line_color"]
                            sp_line_thickness = info["sp_line_thickness"]
                            qp_array = info["qp_array"]
                            qp_line_color = info["qp_line_color"]
                            qp_line_thickness = info["qp_line_thickness"]
                            trial_id = info["trial_id"]
                            axs_title = f"{trial_id}(logMAR {logmar_level})"
                            axs[column_index].plot(x_array, y_array, color=line_color, linewidth=line_thickness)
                            axs[column_index].plot(x_array, sp_array, color=sp_line_color, linewidth=sp_line_thickness)
                            axs[column_index].plot(x_array, qp_array, color=qp_line_color, linewidth=qp_line_thickness)
                            axs[column_index].set_title(axs_title)
                            axs[column_index].set_xlim([x_lower_limit, x_upper_limit])
                            axs[column_index].set_ylim([y_lower_limit, y_upper_limit])
                            for ax in axs.flat:
                                ax.set(xlabel=x_label, ylabel=y_label)

                        if num_plot_to_be_deleted > 0:
                            for index in range(num_plot_to_be_deleted):
                                # print(int(final_column_length) - index)
                                column_index_to_be_deleted = int(final_column_length) - (index + 1)
                                axs[row_index, column_index_to_be_deleted].set_axis_off()

                        # Hide x labels and tick labels for top plots and y ticks for right plots.
                        for ax in axs.flat:
                            ax.label_outer()

                    plt.tight_layout()
                    os.chdir(output_dir)
                    fig.savefig(output_image_name_input)
                    plt.close()
            else:
                fig, axs = plt.subplots(final_row_length, final_column_length,
                                        figsize=(final_column_length * image_scale_input,
                                                 final_row_length * image_scale_input))

                for row_index, plot_info in enumerate(final_plot_array):
                    logmar_level = plot_info["logmar_level"]
                    info_array = plot_info["info_array"]
                    info_array_length = len(info_array)
                    num_plot_to_be_deleted = 0
                    if info_array_length < int(final_column_length):
                        num_plot_to_be_deleted = final_column_length - info_array_length
                    for column_index, info in enumerate(info_array):
                        x_array = info["x_array"]
                        y_array = info["y_array"]
                        x_label = info["x_label"]
                        y_label = info["y_label"]
                        sp_array = info["sp_array"]
                        sp_line_color = info["sp_line_color"]
                        sp_line_thickness = info["sp_line_thickness"]
                        qp_array = info["qp_array"]
                        qp_line_color = info["qp_line_color"]
                        qp_line_thickness = info["qp_line_thickness"]
                        trial_id = info["trial_id"]
                        axs_title = f"{trial_id}(logMAR {logmar_level})"
                        axs[row_index, column_index].plot(x_array, y_array, color=line_color, linewidth=line_thickness)
                        axs[row_index, column_index].plot(x_array, sp_array, color=sp_line_color,
                                                          linewidth=sp_line_thickness)
                        axs[row_index, column_index].plot(x_array, qp_array, color=qp_line_color,
                                                          linewidth=qp_line_thickness)
                        axs[row_index, column_index].set_title(axs_title)
                        axs[row_index, column_index].set_xlim([x_lower_limit, x_upper_limit])
                        axs[row_index, column_index].set_ylim([y_lower_limit, y_upper_limit])

                        for ax in axs.flat:
                            ax.set(xlabel=x_label, ylabel=y_label)

                    if num_plot_to_be_deleted > 0:
                        for index in range(num_plot_to_be_deleted):
                            # print(int(final_column_length) - index)
                            column_index_to_be_deleted = int(final_column_length) - (index + 1)
                            axs[row_index, column_index_to_be_deleted].set_axis_off()

                    # Hide x labels and tick labels for top plots and y ticks for right plots.
                    for ax in axs.flat:
                        ax.label_outer()

                plt.tight_layout()
                os.chdir(output_dir)
                fig.savefig(output_image_name_input)
                plt.close()
        else:
            print("There is nothing to plot")
    else:
        if int(max_graph_in_a_row_input) <= 0:
            print(f"Max graph in a row must be greater than zero but the input is {int(max_graph_in_a_row_input)}")
        else:
            final_plot_array = []
            logmar_level_array = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1, -0.2, "no logMAR"]
            for logmar_level in logmar_level_array:
                temp_logmar_info_array = []

                for info in plot_info_input:
                    if info["logmar"] == logmar_level:
                        if len(temp_logmar_info_array) >= max_graph_in_a_row_input:
                            temp_dict = {"logmar_level": logmar_level, "info_array": temp_logmar_info_array}
                            final_plot_array.append(temp_dict)
                            temp_logmar_info_array = [info]
                        else:
                            temp_logmar_info_array.append(info)

                if len(temp_logmar_info_array) > 0:
                    temp_dict = {"logmar_level": logmar_level, "info_array": temp_logmar_info_array}
                    final_plot_array.append(temp_dict)

            if len(final_plot_array) > 0:
                final_row_length = len(final_plot_array)
                final_column_length = 0
                for plot_info in final_plot_array:
                    info_array = plot_info["info_array"]
                    if len(info_array) > final_column_length:
                        final_column_length = len(info_array)

                # print(final_row_length)
                # print(final_column_length)
                fig, axs = plt.subplots(final_row_length, final_column_length,
                                        figsize=(10 * final_row_length, final_column_length))

                for row_index, plot_info in enumerate(final_plot_array):
                    logmar_level = plot_info["logmar_level"]
                    info_array = plot_info["info_array"]
                    info_array_length = len(info_array)
                    num_plot_to_be_deleted = 0
                    if info_array_length < int(max_graph_in_a_row_input):
                        num_plot_to_be_deleted = max_graph_in_a_row_input - info_array_length
                    for column_index, info in enumerate(info_array):
                        x_array = info["x_array"]
                        y_array = info["y_array"]
                        x_label = info["x_label"]
                        y_label = info["y_label"]
                        trial_id = info["trial_id"]
                        axs_title = f"{trial_id}(logMAR {logmar_level})"
                        axs[row_index, column_index].plot(x_array, y_array, color="black", linewidth=1)
                        axs[row_index, column_index].set_title(axs_title)
                        axs[row_index, column_index].set_ylim([0.4, 0.5])
                        for ax in axs.flat:
                            ax.set(xlabel=x_label, ylabel=y_label)

                    if num_plot_to_be_deleted > 0:
                        for index in range(num_plot_to_be_deleted):
                            # print(int(max_graph_in_a_row_input) - index)
                            column_index_to_be_deleted = int(max_graph_in_a_row_input) - (index + 1)
                            axs[row_index, column_index_to_be_deleted].set_axis_off()

                    # Hide x labels and tick labels for top plots and y ticks for right plots.
                    for ax in axs.flat:
                        ax.label_outer()

                plt.tight_layout()
                os.chdir(output_dir)
                fig.savefig(f"okn_detector_summary.png")
                plt.close()
            else:
                print("There is nothing to plot")


# This function is to draw va testing progress graph from the given config info
def draw_progress_graph(folder_dir_input, summary_csv_name_input, x_label_input, y_label_input, trial_id_header_input,
                        logmar_level_header_input, okn_matlab_header_input, line_color_input, line_thickness_input,
                        graph_line_style_input, image_name_input, marker_type_equivalent_input,
                        marker_type_input, marker_size_input, okn_marker_color_input, okn_marker_edge_color_input,
                        okn_legend_label_input, non_okn_marker_color_input, non_okn_marker_edge_color_input,
                        non_okn_legend_label_input, final_va_line_color_input, final_va_line_thickness_input,
                        final_va_line_style_input, final_va_line_legend_label_input, legend_background_color_input,
                        legend_edge_color_input, legend_location_input, legend_font_size_input,
                        legend_icon_size_input, line_style_equivalent_input):
    summary_csv_dir = os.path.join(folder_dir_input, summary_csv_name_input)
    # csv_name = get_file_name(summary_csv_dir)
    out_image_dir = os.path.join(folder_dir_input, image_name_input)
    # out_image = str(summary_csv_dir).replace(csv_name, image_name_input)

    file_to_open = open(summary_csv_dir)
    csv_reader = csv.reader(file_to_open)
    header_array = []
    rows = []
    count_one = 0

    for row in csv_reader:
        if count_one <= 0:
            header_array = row
            count_one += 1
        else:
            rows.append(row)

    x_header_position = get_index(trial_id_header_input, header_array)
    y_header_position = get_index(logmar_level_header_input, header_array)
    okn_header_position = get_index(okn_matlab_header_input, header_array)
    # print(x_header_position)
    # print(y_header_position)
    x_array = []
    y_array = []
    okn_array = []
    x_index_array = []

    for row in rows:
        x_array.append(row[x_header_position])
        y_array.append(float(row[y_header_position]))
        okn_array.append(int(float(row[okn_header_position])))

    for ind in range(len(x_array)):
        x_index_array.append(str(ind + 1))

    # print(x_array)
    # print(y_array)
    # print(okn_array)
    overlay_x_array = []
    overlay_y_array = []
    final_va_line_level = y_array[-1]

    for ind, value in enumerate(okn_array):
        if value >= 1:
            overlay_x_array.append(x_index_array[ind])
            overlay_y_array.append(y_array[ind])

    bot_limit = min(y_array) - 0.2
    top_limit = max(y_array) + 0.1

    plt.plot(x_index_array, y_array, line_style_equivalent_input[graph_line_style_input],
             marker=marker_type_equivalent_input[marker_type_input], markersize=marker_size_input, fillstyle='full',
             color=line_color_input, linewidth=line_thickness_input,
             markerfacecolor=non_okn_marker_color_input, markeredgecolor=non_okn_marker_edge_color_input)
    plt.plot(overlay_x_array, overlay_y_array, ' ', marker=marker_type_equivalent_input[marker_type_input],
             markersize=marker_size_input, fillstyle='full', color=line_color_input,
             linewidth=line_thickness_input, markerfacecolor=okn_marker_color_input,
             markeredgecolor=okn_marker_edge_color_input)
    plt.axhline(y=final_va_line_level, color=final_va_line_color_input,
                linestyle=line_style_equivalent_input[final_va_line_style_input],
                linewidth=final_va_line_thickness_input)
    plt.ylim(bot_limit, top_limit)
    plt.xlabel(x_label_input)
    plt.ylabel(y_label_input)
    # plt.xticks(rotation=90)
    y_axis_array = np.arange(start=top_limit, stop=bot_limit, step=-0.1)
    plt.yticks(y_axis_array)
    plt.tight_layout()
    okn_marker = Line2D([0], [0], marker=marker_type_equivalent_input[marker_type_input],
                        color=legend_background_color_input, label=okn_legend_label_input,
                        markerfacecolor=okn_marker_color_input, markeredgecolor=okn_marker_edge_color_input,
                        markersize=legend_icon_size_input)
    non_okn_marker = Line2D([0], [0], marker=marker_type_equivalent_input[marker_type_input],
                            color=legend_background_color_input, label=non_okn_legend_label_input,
                            markerfacecolor=non_okn_marker_color_input, markeredgecolor=non_okn_marker_edge_color_input,
                            markersize=legend_icon_size_input)
    final_va_line = Line2D([0], [0], linestyle=line_style_equivalent_input[final_va_line_style_input],
                           color=final_va_line_color_input, label=final_va_line_legend_label_input,
                           linewidth=final_va_line_thickness_input)
    legend_array = [okn_marker, non_okn_marker, final_va_line]
    legend = plt.legend(handles=legend_array, loc=legend_location_input, fontsize=legend_font_size_input, fancybox=True)
    frame = legend.get_frame()
    frame.set_facecolor(legend_background_color_input)
    frame.set_edgecolor(legend_edge_color_input)
    frame.set_alpha(1)
    os.chdir(folder_dir_input)
    plt.savefig(out_image_dir)
    print(f"{image_name_input} is created in {folder_dir_input}.")
    # plt.show()
    plt.close()


# This function is to produce x and y adjustment limits according the type of adjustment
# Type comes into the function as int number and is converted into string to be used
# to retrieve the string type from adjustment dictionary
def get_adjust_limit(data_dir_input, x_header_input, y_header_input, folder_array_input,
                     x_axis_limit_input, y_axis_limit_input, mean_offset_input,
                     axis_adjustment_types_input, axis_adjustment_type_number_input):
    adjustment_type = axis_adjustment_types_input[str(axis_adjustment_type_number_input)]
    print(f"axis_adjustment_type:{adjustment_type}")
    if adjustment_type == "manual":
        x_adjust_limit = {"lower_limit": x_axis_limit_input[0], "upper_limit": x_axis_limit_input[1]}
        y_adjust_limit = {"lower_limit": y_axis_limit_input[0], "upper_limit": y_axis_limit_input[1]}
        print(f"x_adjust_limit:{x_adjust_limit}")
        print(f"y_adjust_limit:{y_adjust_limit}")

    elif adjustment_type == "min_max_mean":
        x_lower_limit_array = []
        x_upper_limit_array = []
        y_lower_limit_array = []
        y_upper_limit_array = []
        for folder in folder_array_input:
            data_dir_to_be_used = os.path.join(data_dir_input, folder, f"updated_{folder}.csv")
            x_array = get_data_array(data_dir_to_be_used, x_header_input)
            x_lower_limit_array.append(min(x_array))
            x_upper_limit_array.append(max(x_array))
            y_array = get_data_array(data_dir_to_be_used, y_header_input)
            y_lower_limit_array.append(min(y_array))
            y_upper_limit_array.append(max(y_array))

        x_adjust_limit = {"lower_limit": int(min(x_lower_limit_array)),
                          "upper_limit": int(max(x_upper_limit_array))}
        y_adjust_limit = {"lower_limit": round(np.mean(y_lower_limit_array), 2),
                          "upper_limit": round(np.mean(y_upper_limit_array), 2)}
        print(f"x_adjust_limit:{x_adjust_limit}")
        print(f"y_adjust_limit:{y_adjust_limit}")

    elif adjustment_type == "mean_offset":
        x_lower_limit_array = []
        x_upper_limit_array = []
        for folder in folder_array_input:
            data_dir_to_be_used = os.path.join(data_dir_input, folder, f"updated_{folder}.csv")
            x_array = get_data_array(data_dir_to_be_used, x_header_input)
            x_lower_limit_array.append(min(x_array))
            x_upper_limit_array.append(max(x_array))
            y_array = get_data_array(data_dir_to_be_used, y_header_input)

        x_adjust_limit = {"lower_limit": int(min(x_lower_limit_array)),
                          "upper_limit": int(max(x_upper_limit_array))}
        y_adjust_limit = {"lower_limit": round(float(- mean_offset_input), 2),
                          "upper_limit": round(float(mean_offset_input), 2)}
        print(f"x_adjust_limit:{x_adjust_limit}")
        print(f"y_adjust_limit:{y_adjust_limit}")

    else:
        x_lower_limit_array = []
        x_upper_limit_array = []
        y_lower_limit_array = []
        y_upper_limit_array = []
        for folder in folder_array_input:
            data_dir_to_be_used = os.path.join(data_dir_input, folder, f"updated_{folder}.csv")
            x_array = get_data_array(data_dir_to_be_used, x_header_input)
            x_lower_limit_array.append(min(x_array))
            x_upper_limit_array.append(max(x_array))
            y_array = get_data_array(data_dir_to_be_used, y_header_input)
            y_lower_limit_array.append(min(y_array))
            y_upper_limit_array.append(max(y_array))

        x_adjust_limit = {"lower_limit": int(min(x_lower_limit_array)),
                          "upper_limit": int(max(x_upper_limit_array))}
        y_adjust_limit = {"lower_limit": round(min(y_lower_limit_array), 2),
                          "upper_limit": round(max(y_upper_limit_array), 2)}
        print(f"x_adjust_limit:{x_adjust_limit}")
        print(f"y_adjust_limit:{y_adjust_limit}")

    return x_adjust_limit, y_adjust_limit


def main():
    parser = argparse.ArgumentParser(prog='okntool',
                                     description='okn related graphs plotting program.')
    parser.add_argument('--version', action='version', version='1.0.8'),
    parser.add_argument("-t", dest="plot_type", required=True, default=sys.stdin,
                        help="trial, summary or staircase", metavar="plot type")
    parser.add_argument("-d", dest="directory_input", required=True, default=sys.stdin,
                        help="directory folder to be processed", metavar="directory")
    parser.add_argument("-c", dest="config_dir", required=False, default=sys.stdin,
                        help="config file to be used", metavar="config location")

    args = parser.parse_args()
    directory_input = str(args.directory_input)
    type_input = str(args.plot_type)
    config_file_location = str(args.config_dir)
    config_location = None

    # print(config_file_location)
    if "_io.TextIOWrapper" in config_file_location:
        print(f"There is no config input.")
        tool_info = subprocess.check_output("pip show okntool")
        data = tool_info.decode("utf-8")
        data_array = str(data).split("\r\n")
        data_dict = {}
        for info in data_array:
            try:
                key, value = str(info).split(": ", 1)
                data_dict[key] = value
            except ValueError:
                pass

        config_location_in_dict = data_dict["Location"]

        if "okntool" in config_location_in_dict:
            config_location = os.path.join(config_location_in_dict, "oknserver_graph_plot_config.json")
        else:
            config_location = os.path.join(config_location_in_dict, "okntool", "oknserver_graph_plot_config.json")
        print(f"Therefore, okntool is using build-in config: {config_location}.")
        config_build_in_exist = os.path.isfile(config_location)
        if not config_build_in_exist:
            print(f"Error in retrieving config:{config_location}.")
            return
    else:
        config_dir_exist = os.path.isfile(config_file_location)
        if not config_dir_exist:
            print(f"Config location input:{config_file_location} does not exist.")
        else:
            config_location = config_file_location
            print(f"Config location input:{directory_input} is valid.")

    print("------------------")
    print(f"OKN TOOL PLOT INFO")
    print(f"Input directory:{directory_input}")
    print(f"Plot type:{type_input}")
    print(f"Config: {config_location}")

    # check whether input directory exists or not
    dir_exist = os.path.isdir(directory_input)
    if not dir_exist:
        f"Directory input:{directory_input} does not exist"
        return
    else:
        f"Directory input:{directory_input} is valid"

    # Opening oknserver graph plot config
    with open(config_location) as f:
        plot_config_info = json.load(f)
        if plot_config_info is not None:
            print("oknserver_graph_plot_config.json is found.")
        else:
            print("Essential config file oknserver_graph_plot_config.json is missing.")

        # Retrieve summary plot info from config
        summary_plot_info = plot_config_info["summary_plot"]
        x_label = summary_plot_info["x_label"]
        y_label = summary_plot_info["y_label"]
        x_data_column_name = summary_plot_info["x_data_column_name"]
        y_data_column_name = summary_plot_info["y_data_column_name"]
        x_axis_limit = summary_plot_info["x_axis_limit"]
        x_axis_lower_limit = x_axis_limit[0]
        x_axis_upper_limit = x_axis_limit[1]
        y_axis_limit = summary_plot_info["y_axis_limit"]
        y_axis_lower_limit = y_axis_limit[0]
        y_axis_upper_limit = y_axis_limit[1]
        mean_offset = summary_plot_info["mean_offset"]
        axis_adjustment_types = summary_plot_info["axis_adjustment_types"]
        axis_adjustment_type_number = summary_plot_info["axis_adjustment_type_number"]
        graph_line_color = summary_plot_info["graph_line_color"]
        graph_line_thickness = summary_plot_info["graph_line_thickness"]
        max_graph_in_a_row = summary_plot_info["max_graph_in_a_row"]
        image_scale = summary_plot_info["image_scale"]
        signal_csv_folder_name = summary_plot_info["signal_csv_folder_name"]
        signal_csv_name = summary_plot_info["signal_csv_name"]
        sp_column_name = summary_plot_info["sp_column_name"]
        qp_column_name = summary_plot_info["qp_column_name"]
        sp_line_color = summary_plot_info["sp_line_color"]
        sp_line_thickness = summary_plot_info["sp_line_thickness"]
        qp_line_color = summary_plot_info["qp_line_color"]
        qp_line_thickness = summary_plot_info["qp_line_thickness"]
        summary_csv_name = summary_plot_info["summary_csv_name"]
        output_image_name = summary_plot_info["output_image_name"]

        # Retrieve trial plot info from config
        trial_plot_info = plot_config_info["trial_plot"]
        trial_title = trial_plot_info["title"]
        trial_x_label = trial_plot_info["x_label"]
        trial_y_label = trial_plot_info["y_label"]
        trial_x_data_column_name = trial_plot_info["x_data_column_name"]
        trial_y_data_column_name = trial_plot_info["y_data_column_name"]
        trial_graph_line_color = trial_plot_info["graph_line_color"]
        trial_graph_line_thickness = trial_plot_info["graph_line_thickness"]
        trial_image_scale = trial_plot_info["image_scale"]
        trial_signal_csv_folder_name = trial_plot_info["signal_csv_folder_name"]
        trial_signal_csv_name = trial_plot_info["signal_csv_name"]
        trial_sp_column_name = trial_plot_info["sp_column_name"]
        trial_qp_column_name = trial_plot_info["qp_column_name"]
        trial_sp_line_color = trial_plot_info["sp_line_color"]
        trial_sp_line_thickness = trial_plot_info["sp_line_thickness"]
        trial_qp_line_color = trial_plot_info["qp_line_color"]
        trial_qp_line_thickness = trial_plot_info["qp_line_thickness"]
        trial_output_image_name = trial_plot_info["output_image_name"]

        # Retrieve progress plot info from config
        progress_plot_info = plot_config_info["progress_plot"]
        progress_plot_x_label = progress_plot_info["x_label"]
        progress_plot_y_label = progress_plot_info["y_label"]
        progress_plot_x_data_column_name = progress_plot_info["x_data_column_name"]
        progress_plot_y_data_column_name = progress_plot_info["y_data_column_name"]
        progress_plot_okn_matlab_column_name = progress_plot_info["okn_matlab_column_name"]
        progress_plot_graph_line_color = progress_plot_info["graph_line_color"]
        progress_plot_graph_line_thickness = progress_plot_info["graph_line_thickness"]
        progress_plot_graph_line_style = progress_plot_info["graph_line_style"]
        progress_plot_summary_csv_name = progress_plot_info["summary_csv_name"]
        progress_plot_output_image_name = progress_plot_info["output_image_name"]
        pp_marker_type_equivalent = progress_plot_info["marker_type_equivalent"]
        pp_marker_type = progress_plot_info["marker_type"]
        pp_marker_size = progress_plot_info["marker_size"]
        pp_okn_marker_color = progress_plot_info["okn_marker_color"]
        pp_okn_marker_edge_color = progress_plot_info["okn_marker_edge_color"]
        pp_okn_legend_label = progress_plot_info["okn_legend_label"]
        pp_non_okn_marker_color = progress_plot_info["non_okn_marker_color"]
        pp_non_okn_marker_edge_color = progress_plot_info["non_okn_marker_edge_color"]
        pp_non_okn_legend_label = progress_plot_info["non_okn_legend_label"]
        pp_final_va_line_color = progress_plot_info["final_va_line_color"]
        pp_final_va_line_thickness = progress_plot_info["final_va_line_thickness"]
        pp_final_va_line_style = progress_plot_info["final_va_line_style"]
        pp_final_va_line_legend_label = progress_plot_info["final_va_line_legend_label"]
        pp_legend_background_color = progress_plot_info["legend_background_color"]
        pp_legend_edge_color = progress_plot_info["legend_edge_color"]
        pp_legend_location = progress_plot_info["legend_location"]
        pp_legend_font_size = progress_plot_info["legend_font_size"]
        pp_legend_icon_size = progress_plot_info["legend_icon_size"]
        pp_line_style_equivalent = progress_plot_info["line_style_equivalent"]

        if plot_config_info is not None and dir_exist:
            if type_input == "trial":
                csv_name = f"updated_{os.path.basename(directory_input)}.csv"
                updated_csv_dir = os.path.join(directory_input, csv_name)
                signal_csv_dir = os.path.join(directory_input, trial_signal_csv_folder_name, trial_signal_csv_name)
                draw_graph_with_overlay(updated_csv_dir, trial_x_data_column_name, trial_y_data_column_name,
                                        trial_title, trial_x_label, trial_y_label,
                                        trial_sp_column_name, trial_qp_column_name,
                                        trial_graph_line_color, trial_graph_line_thickness,
                                        trial_sp_line_color, trial_sp_line_thickness,
                                        trial_qp_line_color, trial_qp_line_thickness,
                                        trial_output_image_name, signal_csv_dir)
            elif type_input == "summary":
                plot_data_array, auto_adjust_info = get_plot_info(directory_input, x_data_column_name,
                                                                  y_data_column_name,
                                                                  x_axis_limit, y_axis_limit, mean_offset,
                                                                  axis_adjustment_types, axis_adjustment_type_number,
                                                                  x_label, y_label, signal_csv_folder_name,
                                                                  signal_csv_name, sp_column_name, sp_line_color,
                                                                  sp_line_thickness, qp_column_name, qp_line_color,
                                                                  qp_line_thickness, summary_csv_name)
                plot_combined_graph(plot_data_array, max_graph_in_a_row, directory_input,
                                    auto_adjust_info, graph_line_color, graph_line_thickness,
                                    image_scale, output_image_name)
            elif type_input == "staircase":
                draw_progress_graph(directory_input, progress_plot_summary_csv_name, progress_plot_x_label,
                                    progress_plot_y_label, progress_plot_x_data_column_name,
                                    progress_plot_y_data_column_name, progress_plot_okn_matlab_column_name,
                                    progress_plot_graph_line_color, progress_plot_graph_line_thickness,
                                    progress_plot_graph_line_style, progress_plot_output_image_name,
                                    pp_marker_type_equivalent, pp_marker_type,
                                    pp_marker_size, pp_okn_marker_color, pp_okn_marker_edge_color, pp_okn_legend_label,
                                    pp_non_okn_marker_color, pp_non_okn_marker_edge_color, pp_non_okn_legend_label,
                                    pp_final_va_line_color, pp_final_va_line_thickness, pp_final_va_line_style,
                                    pp_final_va_line_legend_label, pp_legend_background_color, pp_legend_edge_color,
                                    pp_legend_location, pp_legend_font_size, pp_legend_icon_size,
                                    pp_line_style_equivalent)
            else:
                print("wrong plot type or invalid plot type.")
