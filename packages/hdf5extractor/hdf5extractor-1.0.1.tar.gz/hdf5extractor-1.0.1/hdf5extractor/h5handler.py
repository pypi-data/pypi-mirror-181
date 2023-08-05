from lxml import etree
import os
import h5py
from io import BytesIO


def write_h5(
    input_h5: str, output_h5: str, h5_datasets: list, overwrite=False
):
    if len(h5_datasets) > 0:

        if not overwrite and os.path.exists(output_h5):
            print(f"The output file '{output_h5}'allready exists")
            return

        print(f"writing: {output_h5}: Found datasets: {h5_datasets}")

        with h5py.File(output_h5, "w") as f_dest:
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    f_dest.create_dataset(dataset, data=f_src[dataset])


def write_h5_memory(input_h5: BytesIO, h5_datasets: list):
    result = None
    print(h5_datasets)
    if len(h5_datasets) > 0:
        result = BytesIO()
        with h5py.File(result) as f_dest:
            input_h5.seek(0)
            with h5py.File(input_h5) as f_src:
                for dataset in h5_datasets:
                    f_dest.create_dataset(dataset, data=f_src[dataset])
        result.seek(0)
    return result


def write_h5_memory_in_local(input_h5: str, h5_datasets: list):
    result = None
    if len(h5_datasets) > 0:
        result = BytesIO()
        with h5py.File(result, "w") as f_dest:
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    f_dest.create_dataset(dataset, data=f_src[dataset])
        result.seek(0)
    return result


def find_data_ref_in_xml(xml_content: bytes):
    tree = etree.ElementTree(etree.fromstring(xml_content))
    root = tree.getroot()
    return [
        x.text for x in root.xpath("//*[local-name() = 'PathInHdfFile']")
    ] + [
        x.text for x in root.xpath("//*[local-name() = 'PathInExternalFile']")
    ]
