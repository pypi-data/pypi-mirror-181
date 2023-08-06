# -*- coding: utf-8 -*-
"""
This module is used to provide the console program.
"""
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from os import path

from .excel_operation import process_excel_file

__all__ = ["sort_excel_file"]


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="Jira tool: Used to sort stories",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("input_file", type=str, help="Source file path.")
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        required=False,
        help="Target file name.",
    )
    parser.add_argument(
        "--excel_definition_config",
        type=str,
        required=False,
        help="Excel definition JSON file.",
    )
    parser.add_argument(
        "--sprint_schedule_config",
        type=str,
        required=False,
        help="Milestone priority JSON file.",
    )
    parser.add_argument(
        "--over_write",
        type=bool,
        required=False,
        help="Whether or not to over write existing file.",
    )

    args = parser.parse_args()

    return args


def sort_excel_file():
    try:
        args = get_args()

        input_file_name = path.splitext(args.input_file)[0]

        output_file = f"{input_file_name}_sorted.xlsx"
        if args.output_file is not None:
            output_file = args.output_file

        over_write = True
        if args.over_write is not None:
            over_write = args.over_write

        process_excel_file(
            args.input_file,
            output_file,
            args.excel_definition_config,
            args.sprint_schedule_config,
            over_write,
        )
    except Exception as e:
        print(e)
