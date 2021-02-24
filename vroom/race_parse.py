import argparse
import miff_parse as miff

def open_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()




def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest="input_file", help="the .scn race file to open", metavar="FILE.scn",
                        required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    options = parse_command_line()
    input_file = options.input_file
    raw_data = open_file(input_file)
    parsed_data = miff.parse_scenario(raw_data)
    for k, v in parsed_data.items():
        print(f"{k}: ", end='')
        if isinstance(v, list):
            print()
            for x in v:
                print(f"\t{x}, len: {len(x)}")
        else:
            print(v)