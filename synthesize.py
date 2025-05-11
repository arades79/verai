#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pyosys import libyosys as ys
from pathlib import Path
from argparse import ArgumentParser
import json
import multiprocessing


def make_training_case(verilog_file: Path, case_id: str = ""):
    """
    Synthesize a Verilog file using Yosys, then create a training case out of presinthesized / postsynthesized pair.

    Args:
        verilog_file (Path): Path to the input Verilog file.
    """

    if not case_id:
        case_id = verilog_file.parent.stem

    output_file = Path("synthesized", verilog_file.stem).with_suffix(".synth.v")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    design = ys.Design()
    ys.run_pass(f"read_verilog {verilog_file}", design)
    ys.run_pass("synth", design)
    ys.run_pass(f"write_verilog {output_file}", design)
    print(f"Synthesis complete. Output written to {output_file}")

    def escape(s: str) -> str:
        return (
            s
            # .replace("\\", "\\\\")
            # .replace("\n", "\\n")
            # .replace('"', '\\"')
            # .replace("\r", "\\r")
            # .replace("\t", "\\t")
            # .replace("\b", "\\b")
            # .replace("\f", "\\f")
        )

    training_case = {"question": output_file.read_text(), "answer": verilog_file.read_text()}
    training_file = Path("training", f"{case_id}_{verilog_file.stem}").with_suffix(
        ".json"
    )
    training_file.write_text(json.dumps(training_case))


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
    with multiprocessing.Pool(processes=4) as pool:
        try:
            pool.imap_unordered(make_training_case, input_dir.glob("*.v"))
        except BaseException as e:
            print(f"Thing machine broke {e}")
        finally:
            pass
            # pool.apply()
            pool.close()
            pool.join()
        #     pool.close()
        #     pool.join()
        # try:
        #     pool.make_training_case(verilog_file, case_id)
        # except:
        #     print(f"Error processing {verilog_file}. Skipping.")
        # else:
        #     print(f"Training case created for {verilog_file}")


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Synthesize Verilog files and create training cases."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Path to the input directory containing Verilog files.",
    )
    parser.add_argument(
        "-i", "--case-id", type=str, help="Case ID for the training cases."
    )
    args = parser.parse_args()
    make_training_cases(
        args.input_dir, args.case_id
    ) if args.case_id else make_training_cases(args.input_dir)
    print(f"Training cases created in {Path('training').absolute()}")
