import argparse
from optparse import OptionParser, OptionGroup


def get_option_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--nopsyco", help="Do not import psyco", dest="nopsyco", default=True,
                             action="store_true")

    parser.add_argument("--benchmark", help="Run a benchmark-test", dest="benchmark", default=None,
                             action="store_true")

    parser.add_argument("--benchmark-settings",
                             help="Format: 'x,y,z' x=Number of words on each crossword, y=Number of crosswords to generate, z=Each crossword should be the best of ...?",
                             dest="bsettings", default="100,100,3", action="store")

    parser.add_argument("--stats", help="Print stats", dest="stats", default=None, action="store_true")



    parser.add_argument("-c", "--cols", help="Number of columns to use (Default: auto)", dest="columns",
                               default="auto", action="store")
    parser.add_argument("-r", "--rows", help="Number of rows to use (Default: auto)", dest="rows",
                               default="auto", action="store")
    parser.add_argument("-s", "--solution",
                               help="The crossword's solution (some colored fields which letters can be used to build a word).\nNote: This will overwrite any solution defined in the input file(s)!! ",
                               action="store", dest="solution", default=None)
    parser.add_argument("--solved", help="Create a solved crossword", action="store_true", dest="solved",
                               default=False)


    parser.add_argument("--print-clues", help="Print crossword clues to stdout", action="store_true",
                            dest="print_clues", default=False)
    parser.add_argument("--print-crossword", help="Print crossword to stdout", action="store_true",
                            dest="print_crossword", default=False)
    parser.add_argument("--create-image", help="Create a crossword image", action="store_true", dest="create_image",
                            default=False)
    parser.add_argument("-o", "--output",
                            help="Specify filename (only for --create-image). If no filename is give, the name will be generated from the input file. If you specify multiple input files and an output file, numbers will be appended to the given output-filename",
                            action="store", dest="output", default=None)
    parser.add_argument("-p", "--pixels", help="Number of pixels per block for the corssword image", action="store", dest="ppb",
                default=32)
    parser.add_argument("-b", "--bestof", help="Create n crosswords and keep the best", action="store",
                               dest="bestof", default=3)

    (opt, _) = parser.parse_known_args()
    return (opt, _)