import json

import pathlib as pl
from typing import Dict

import graph_jsp_utils.jsp_instance_parser as parser
import graph_jsp_utils.jsp_or_tools_solver as or_tools_solver

from graph_jsp_utils.disjunctive_graph_logger import log


def update_custom_instance_details(
        custom_instance_details_file_path: pl.Path,
        custom_instances_folder: pl.Path
) -> None:
    # check if custom instance details file exists
    if not custom_instance_details_file_path.is_file():
        log.info("there is no custom instance details file jet. creating one..")
        custom_instance_details_file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(custom_instance_details_file_path, 'w') as fp:
            json.dump({}, fp, indent=4)

    with open(custom_instance_details_file_path) as f:
        details_dict = json.load(f)

    # all instance files
    custom_instances_generator = custom_instances_folder.glob('**/*.txt')

    details_keys = details_dict.keys()
    for custom_instance in custom_instances_generator:
        name = custom_instance.stem
        if name in details_keys:
            continue

        log.info("")
        log.info(f"handling custom instance '{name}'")

        jsp, _ = parser.parse_jps_taillard_specification(instance_path=custom_instance)
        _, n_jobs, n_machines = jsp.shape

        makespan, status, df, info = or_tools_solver.solve_jsp(jsp_instance=jsp, plot_results=False)

        details_dict[name] = {
            "lower_bound": makespan,
            "upper_bound": makespan,
            "jobs": n_jobs,
            "machines": n_machines,
            "n_solutions": 1,
            "lb_optimal": status == "OPTIMAL",
            "path": str(custom_instance),
            "gantt_df": df.to_dict(),
        }

    log.info(f"saving details to .json file ('{custom_instance_details_file_path}')")
    with open(custom_instance_details_file_path, 'w') as fp:
        json.dump(details_dict, fp, indent=4)


def get_custom_instance_details(custom_instance_details_file_path: pl.Path, name: str) -> dict:
    all_details = parse_custom_instance_details(
        custom_instance_details_file_path=custom_instance_details_file_path
    )

    if name not in all_details.keys():
        raise ValueError(f"there are no details for the custom instance '{name}' in the specified details file "
                 f"('{custom_instance_details_file_path}'). You may need to update the custom details using the "
                         f"'update_custom_instance_details' function.")
    return all_details[name]


def parse_custom_instance_details(custom_instance_details_file_path: pl.Path) -> Dict:
    """
    reads 'jps_instance_details/custom_instance_details.json' file and returns it as a dictionary.

    make sure to download the instance details beforehand (run 'download_benchmark_instances_details' once)

    :return: the 'jps_instance_details/custom_instance_details.json'-file as a python dictionary
    """
    with open(custom_instance_details_file_path) as f:
        details_dict = json.load(f)
    return details_dict


if __name__ == '__main__':
    import os
    details_file_path = pl.Path(os.path.abspath(__file__)).parent.parent.parent\
        .joinpath("resources")\
        .joinpath("jps_instance_details")\
        .joinpath("custom_instance_details.json")

    instances_folder = pl.Path(os.path.abspath(__file__)).parent.parent.parent \
        .joinpath("resources") \
        .joinpath("jsp_instances") \
        .joinpath("custom")

    update_custom_instance_details(
        custom_instance_details_file_path=details_file_path,
        custom_instances_folder=instances_folder
    )
    # details = get_custom_instance_details(
    #    custom_instance_details_file_path=details_file_path,
    #    name="Vantablack_Strawberry_57_82f7d5fd" # specify the name of a generated instance
    # )
    # print(details)