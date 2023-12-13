import random
import argparse

def shuffle_txt(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    random.shuffle(lines)

    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = 'please enter embed parameter ...'
    parser.add_argument("-i", "--input_file_path")
    parser.add_argument("-o", "--output_file_path")
    args = parser.parse_args()
    
    shuffle_txt(args.input_file_path, args.output_file_path)