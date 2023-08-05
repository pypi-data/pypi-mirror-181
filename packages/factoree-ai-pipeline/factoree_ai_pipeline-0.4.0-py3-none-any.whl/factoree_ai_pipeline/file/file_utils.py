from datetime import datetime
from factoree_ai_pipeline.system_params import SEPARATOR_CHAR, PATH_SEPARATOR_CHAR


def get_silver_file_name(
        data_type: str,
        facility: str,
        sensor_type: str,
        first_sample: datetime,
        last_sample: datetime,
        is_test: bool = False,
        tag: str | None = None
) -> str:
    first_sample_display = first_sample.strftime("%Y_%m_%dT%H_%M_%S%z").replace("+", "_")
    last_sample_display = last_sample.strftime("%Y_%m_%dT%H_%M_%S%z").replace("+", "_")
    folder = 'tests' if is_test else 'input'

    if tag:
        file_base_name = SEPARATOR_CHAR.join([
            facility,
            sensor_type,
            tag,
            first_sample_display,
            last_sample_display
        ])
    else:
        file_base_name = SEPARATOR_CHAR.join([
            facility,
            sensor_type,
            first_sample_display,
            last_sample_display
        ])
    file_name = f'{file_base_name}.json'

    return PATH_SEPARATOR_CHAR.join([
        folder,
        data_type,
        file_name
    ])


def read_csv_file(file_name) -> list[str]:
    input_file = open(file_name, "rt")
    result = input_file.readlines()
    input_file.close()
    return result


def write_json_file(tag_name, data, dst_folder) -> None:
    file_name = dst_folder + tag_name.replace('/', ":") + '.json'
    try:
        with open(file_name, "wt") as output_file:
            output_file.write("{ data: [\n")
            for record in data:
                output_file.write(str(record) + ",\n")
            output_file.write("] }\n")
    except FileNotFoundError or PermissionError:
        print("Error occurred: No such file or directory or permission denied.")


def write_json_files(tag_to_data, dst_folder) -> None:
    for tag_name, data in tag_to_data.items():
        write_json_file(tag_name, tag_to_data[tag_name], dst_folder)


def grid_to_csv(data: list[list]) -> str:
    comma_separated_rows = []
    for row_idx in range(len(data)):
        new_row = []
        for value in data[row_idx]:
            new_row.append(str(value))
        comma_separated_rows.append(",".join(new_row))
    return "\n".join(comma_separated_rows)
