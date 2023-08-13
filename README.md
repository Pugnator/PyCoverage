# Gcov Wrapper for MinGW

This is a Python-based wrapper for using gcov with MinGW. It helps you generate code coverage reports for your C/C++ source files and creates HTML reports for function coverage percentages.

## Prerequisites

1. Python 3.x
2. MinGW (for gcov)

## Usage

### Install Prerequisites

Before using this script, make sure you have Python 3.x installed on your system. Additionally, ensure that MinGW is properly set up and available in your system's PATH, as the script uses gcov for code coverage analysis.

### Running the Script

To generate code coverage reports and HTML reports for function coverage, you can use the following command-line arguments:

```sh
python gcov_wrapper.py -s <source_file> [-b <build_folder>]
python gcov_wrapper.py -f <source_folder> [-b <build_folder>]
                       
-s, --source_file: The path to the source file for which you want to generate a coverage report.
-f, --source_folder: The path to the source folder containing multiple source files. The script will process all source files in this folder and generate a combined HTML report.
-b, --build_folder: The optional path to the build folder (if your project's build artifacts are located there).
```

## Output

The script generates two types of output:

Coverage Reports: Temporary .gcov files are created during the coverage analysis process. These files will be automatically removed after processing.
HTML Reports: HTML reports are generated with coverage information. You will find a separate HTML file for each source file when using the -f flag. 
When using the -s flag, a combined HTML report will be generated that includes all processed source files.

## License

This project is licensed under the MIT License. Feel free to use and modify it according to your needs.

If you encounter any issues or have questions, feel free to contact me.

