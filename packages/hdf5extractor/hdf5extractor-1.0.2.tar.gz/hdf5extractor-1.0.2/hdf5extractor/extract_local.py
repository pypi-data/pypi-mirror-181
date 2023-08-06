import argparse
import os
import re
import zipfile
from io import BytesIO

from hdf5extractor.h5handler import (
    write_h5,
    find_data_ref_in_xml,
    write_h5_memory_in_local,
    find_data_ref_in_energyml_files,
)
from hdf5extractor.common import FILE_NAME_REGEX


def process_files_old(
    file_path: str, input_h5: str, output_folder: str, overwrite=False
):
    print(FILE_NAME_REGEX)
    to_process_files = []
    if file_path.endswith(".xml"):
        file_name = file_path
        if "/" in file_name:
            file_name = file_name[file_name.rindex("/") + 1 :]
        if "\\" in file_name:
            file_name = file_name[file_name.rindex("\\") + 1 :]

        xml_content = open(file_path, "rb").read()
        to_process_files.append((xml_content, file_name))
    elif file_path.endswith(".epc"):
        with zipfile.ZipFile(file_path) as epc_as_zip:
            for f_name in epc_as_zip.namelist():
                if not f_name.startswith("_rels/") and re.match(
                    FILE_NAME_REGEX, f_name
                ):
                    with epc_as_zip.open(f_name) as myfile:
                        to_process_files.append((myfile.read(), f_name))

    for f_content, f_name in to_process_files:
        write_h5(
            input_h5,
            output_folder + "/" + f_name[: f_name.rindex(".")] + ".h5",
            find_data_ref_in_xml(f_content),
            overwrite,
        )

def process_files_memory(file_path: str, input_h5: str):
    to_process_files = []
    if file_path.endswith(".xml"):
        file_name = file_path
        if "/" in file_name:
            file_name = file_name[file_name.rindex("/") + 1 :]
        if "\\" in file_name:
            file_name = file_name[file_name.rindex("\\") + 1 :]

        xml_content = open(file_path, "rb").read()
        to_process_files.append((xml_content, file_name))
    elif file_path.endswith(".epc"):
        with zipfile.ZipFile(file_path) as epc_as_zip:
            for f_name in epc_as_zip.namelist():
                if not f_name.startswith("_rels/") and re.match(
                    FILE_NAME_REGEX, f_name
                ):
                    with epc_as_zip.open(f_name) as myfile:
                        to_process_files.append((myfile.read(), f_name))

    mapper = {}
    for f_content, f_name in to_process_files:
        data_refs = find_data_ref_in_xml(f_content)
        if data_refs is not None:
            mapper[f_name] = write_h5_memory_in_local(
                input_h5,
                list(data_refs.values())[0],
            )
    # filter None
    mapper = {k: v for k, v in mapper.items() if v is not None}

    # print(mapper)
    return mapper


def process_files(
    file_path: str, input_h5: str, output_folder: str, overwrite=False
):
    mini_h5_map = process_files_memory(file_path, input_h5)
    for f_name in mini_h5_map:
        print(f"{f_name} : {mini_h5_map[f_name]}")
        with open(
            output_folder + "/" + f_name[: f_name.rindex(".")] + ".h5", "wb"
        ) as file:
            file.write(mini_h5_map[f_name].getbuffer())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=str,
        help="[Required] Input file (xml of epc) from which the\
        referenced data path are taken",
    )
    parser.add_argument(
        "--h5",
        required=True,
        type=str,
        help="[Required] Input h5 file or folder that contains h5 files",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="extracted",
        type=str,
        help="H5 output folder",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force the overwrite the output files if allready exists",
    )
    args = parser.parse_args()

    try:
        os.makedirs(args.output)
    except OSError:
        pass

    print("reading", args.input)
    process_files(
        file_path=args.input,
        input_h5=args.h5,
        output_folder=args.output,
        overwrite=args.force,
    )
