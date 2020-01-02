from pandas import read_csv, DataFrame
from pprint import pprint
import os
import sys

if __name__ == '__main__':
    try:
        classification_file_name = sys.argv[1]
        classification_name = os.path.basename(classification_file_name)
    except:
        print('Error: Expected Classification Filename')
    classification_file_path = os.path.join('classification_csvs', classification_file_name)
    classification_file = read_csv(classification_file_path)
    number_of_frames = classification_file.shape[0]

    # classification_file = classification_file.truncate(after=number_of_frames//2)

    classification_file_attrs = classification_file.describe().iloc[:, :]

    classification_means = classification_file_attrs.iloc[0, :]
    classification_stds = classification_file_attrs.iloc[1, :]
    classification_maxs = classification_file_attrs.iloc[6, :]
    attributes = {}

    max_in_row_count = 'max_in_row_count'
    std = 'std'
    max_value = 'max_value'
    frames_with_max_value = 'frames_with_max_value'
    frames_to_cover = number_of_frames // 4

    for col in classification_file.columns:
        col_value_indexes = []
        col_values = classification_file[col]
        sorted_col_values = col_values.sort_values(ascending=False)
        frames_covered = 0
        for col_val in sorted_col_values:
            col_value_indexes.append(col_values.tolist().index(col_val))
            frames_covered += 1
            if frames_covered >= frames_to_cover:
                break

        attr_def = {max_in_row_count: 0,
                    max_value: classification_maxs[col],
                    std: classification_stds[col],
                    frames_with_max_value: col_value_indexes}

        attributes[col] = attr_def

    for index, row in classification_file.iterrows():
        max_value_field = row.idxmax()
        if row[max_value_field] > 0.75:
            attributes[max_value_field][max_in_row_count] += 1

    metrics_output_dir = 'metrics'
    if not os.path.exists(metrics_output_dir):
        os.makedirs(metrics_output_dir)

    file_name_without_ext = os.path.splitext(classification_file_name)[0]
    metrics_file_name = f'{file_name_without_ext}.csv'
    metrics_file_path = os.path.join(metrics_output_dir, metrics_file_name)

    DataFrame(attributes).to_csv(metrics_file_path)
