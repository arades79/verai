# Verilog Reverse Engineering with LLM

This project explores the use of a Large Language Model (LLM) to assist in reverse engineering Verilog code. The goal is to analyze Verilog designs, extract insights, and potentially reconstruct high-level functionality from low-level hardware descriptions.

## Features
- Parsing and analyzing Verilog code.
- Extracting module hierarchies and signal relationships.
- Generating human-readable summaries of Verilog designs.
- Experimenting with LLM capabilities for hardware design understanding.

## Usage
1. Provide a Verilog file to analyze:
    ```bash
    python analyze.py --file path/to/verilog_file.v
    ```
2. Review the generated insights and summaries.

## Limitations
- The LLM may not fully understand complex Verilog constructs.
- Results may require manual verification for accuracy.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
See licences directory to see licenses of training data and tools.

## Acknowledgments
- This readme generated using AI.
- Yosys project for providing an openly licensed synthesis tool
