import sdformat13 as sdf
import sys

def main():
    input_file = './safmc.world'
    root = sdf.Root()
    try:
        root.load(input_file)
    except sdf.SDFErrorsException as e:
        print(e, file=sys.stderr)

if __name__ == "__main__":
    main()
