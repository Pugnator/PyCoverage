import argparse
import gzip
import json
import os
import re
import subprocess

DESCRIPTION = """Python based gcov wrapper for MinGW        
        """

extensions = ['.cpp', '.c', '.cc']


def generateCombinedHTML(results, htmlName=None):
    content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Combined Function Coverage Report</title>
    </head>
    <body>
        <h1>Combined Function Coverage Report</h1>
    '''

    for source_file, function_coverages in results.items():
        if not function_coverages:
            content += f'''
                    Function {source_file} is not used<br>
            '''
            continue

        content += f'''
        <h2>Function Coverage Report for {source_file}</h2>
        <table>
            <tr>
                <th>Function Name</th>
                <th>Coverage Percentage</th>
            </tr>
        '''

        for coverage in function_coverages:
            content += f'''
            <tr>
                <td>{coverage["function_name"]}</td>
                <td>{coverage["coverage_percent"]:.2f}%</td>
            </tr>
            '''
        content += '''
        </table>
        '''

    content += '''
    </body>
    </html>
    '''

    html_file_path = htmlName or 'report.html'
    with open(html_file_path, 'w') as html_file:
        html_file.write(content)


def parseGzJSON(fileName):
    with gzip.open(fileName, 'rt') as f:
        data = f.read()
        return json.loads(data)


def calculateFunctionCoverage(function):
    blocks = function["blocks"]
    blocksExecuted = function["blocks_executed"]
    if blocks > 0:
        return float(blocksExecuted / blocks) * 100
    else:
        return 0.0


def reportFileCoverage(sourceFile, buildFolder=None):
    gcovOptions = "-m -f -j"
    if buildFolder:
        gcovOptions += f' -o {buildFolder}'

    cmd = f"gcov {sourceFile} {gcovOptions}"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    output = result.stdout

    gcovJsonPattern = r"Creating '([^']+)'"
    linesExecutedPattern = r"Lines executed:([\d.]+)%"
    linesExecutedMatches = re.findall(linesExecutedPattern, output)
    creating_gcov_match = re.search(gcovJsonPattern, output)

    if creating_gcov_match:
        jsonFile = creating_gcov_match.group(1)
        print(f"Gcov report file: {jsonFile}")

    if not linesExecutedMatches:
        os.remove(jsonFile)
        return

    coverageReport = parseGzJSON(jsonFile)
    fileInfo = coverageReport["files"][0]
    fileName = fileInfo["file"]
    print(f"Processing {fileName}")

    function_coverages = []
    for function in fileInfo["functions"]:
        functionName = function["demangled_name"]
        functionCoverage = calculateFunctionCoverage(function)
        function_coverages.append({
            "function_name": functionName,
            "coverage_percent": functionCoverage
        })

    os.remove(jsonFile)
    return function_coverages


def filteredFileList(folder_path, extensions):
    file_paths = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext.lower()) for ext in extensions):
                file_paths.append(os.path.abspath(os.path.join(root, file)))

    return file_paths


def processSourceFolder(folder, buildFolder, outputFile):
    sourceFiles = filteredFileList(folder, extensions)

    results = {}
    for file in sourceFiles:
        result = reportFileCoverage(file, buildFolder)
        results[file] = result

    generateCombinedHTML(results, outputFile)


def args_processing():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=DESCRIPTION)
    parser.add_argument('-f', '--source_folder', required=False, help='The path to the source folder containing multiple source files. The script will process all source files in this folder and generate a combined HTML report')
    parser.add_argument('-s', '--source_file', required=False, help='The path to the source file for which you want to generate a coverage report.')
    parser.add_argument('-b', '--build_folder', help='The optional path to the build folder (if your project''s build artifacts are located there).')
    parser.add_argument('-o', '--output_file', help='Output file name.')
    processed_args = parser.parse_args()
    return processed_args


def main():
    args = args_processing()
    if args.source_folder:
        processSourceFolder(args.source_folder, args.build_folder, args.output_file)
        return

    if not args.source_file:
        print('Please specify a folder or a file to parse')
        return

    result = reportFileCoverage(args.source_file, args.build_folder)
    generateCombinedHTML({["args.source_file"]: result}, args.output_file)


if __name__ == '__main__':
    main()
