#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pyosys import libyosys as ys
from pathlib import Path
from argparse import ArgumentParser

def make_training_case(verilog_file: Path, case_id: str = ""):
    """
    Synthesize a Verilog file using Yosys, then create a training case out of presinthesized / postsynthesized pair.

    Args:
        verilog_file (Path): Path to the input Verilog file.
    """

    if not case_id:
        case_id = verilog_file.stem
    # Create a new Yosys design
    design = ys.Design()

    # Read the input Verilog file
    ys.run_pass(f"read_verilog {verilog_file}", design)

    # Perform synthesis
    ys.run_pass("synth", design)

    # Write the synthesized netlist to a file
    output_file = Path("synthesized", verilog_file.stem).with_suffix(".synth.v")
    ys.run_pass(f"write_verilog {output_file}", design)

    print(f"Synthesis complete. Output written to {output_file}")

    training_case = {"question": ouput_file.read_text(), "answer": verilog_file.read_text()}

    training_file = Path("training", f"{case_id}_{verilog_file.stem}").with_suffix(".json")


def make_training_cases(input_dir: Path, case_id: str = ""):
    """
    Try to create training cases for all Verilog files in the input directory.

    Args:
        input_dir (Path): Path to the input directory containing Verilog files.
    """
    if not case_id:
        case_id = input_dir.stem
    # Create the output directory if it doesn't exist
    output_dir = Path("training")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iterate over all Verilog files in the input directory
    for verilog_file in input_dir.glob("*.v"):
        try:
            make_training_case(verilog_file, case_id)
        except Exception as e:
            print(f"Error processing {verilog_file}: {e}")
            continue

if __name__ == "__main__":
    parser = ArgumentParser(description="Synthesize Verilog files and create training cases.")
    parser.add_argument("input_dir", type=Path, help="Path to the input directory containing Verilog files.")
    parser.add_argument("-i","--case-id", type=str, help="Case ID for the training cases.")
    args = parser.parse_args()
    make_training_cases(args.input_dir, args.case_id) if args.case_id else make_training_cases(args.input_dir)
    print(f"Training cases created in {Path('training').absolute()}")

