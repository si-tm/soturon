import sys
import os

# make dictionary of files in the folder
def get_files(path):
    # read names of the files
    files = os.listdir(path)
    files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
    # make dictionary
    dict_f = {}
    for ff in files_file:
        dict_f[ff[:-22]] = ff
    return dict_f

# reshape to input value
def reshape(folder):
    lst = []
    dic = get_files(folder)
    with open(folder + "/" + dic["seq"], "r") as f:
        for l in f:
            print(l)
    return lst

def main():
    lst = reshape("../oxDNA/test_sample/test_20221102/test_20221102_2")
    print(lst)

if __name__ == "__main__":
    main()
