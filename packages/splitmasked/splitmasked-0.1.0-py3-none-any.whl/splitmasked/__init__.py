import sys
import argparse
import logging

from splitmasked.split import split_masked

logger = logging.getLogger(__name__)

__version__ = "0.1.0"


def parse_args():
    parser = argparse.ArgumentParser(
        description = "Split sequences based on masking.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--maskchar",
        required = True,
        type = str,
        help = "Character specifying masking in a sequence, eg. `N` or `n`. "
               "Case sensitive!"
               "Can also be `lowercase` to consider all lowercase character as masked."
    )
    parser.add_argument(
        "--minlength_masked",
        default = 0,
        type = int,
        help = "Minimum length of a masked sequence part (after splitting) to be output. 0 to disable."
    )
    parser.add_argument(
        "--minlength_unmasked",
        default = 0,
        type = int,
        help = "Minimum length of an unmasked sequence part (after splitting) to be output. 0 to disable."
    )
    parser.add_argument(
        "--outfile_masked",
        help = "File to write masked parts to. Masked parts are discard if this is not specified."
    )
    parser.add_argument(
        "--outfile_unmasked",
        help = "File to write unmasked parts to. Defaults to stdout if not specified."
    )
    parser.add_argument(
        "--revert_lowercase",
        action = "store_true",
        help = "Revert lowercase masking after splitting. Only works with `--maskchar lowercase`."
    )
    parser.add_argument(
        "input",
        nargs = "?",
        default = sys.stdin,
        help = "Input FAST(A/Q) file. Can be gzip compressed. If not given, read from stdin.")

    args = parser.parse_args()
    if args.input is sys.stdin and sys.stdin.isatty():
        logger.error("No input file specified. Tried reading from stdin, but stdin is not a stream!")
        sys.exit(1)

    if args.outfile_unmasked is None:
        args.outfile_unmasked = sys.stdout

    if args.outfile_masked == args.outfile_unmasked:
        logger.error("Masked and unmasked parts cannot be written to the same file.")
        sys.exit(1)

    if args.revert_lowercase and not args.maskchar == "lowercase":
        logger.error("--revert_lowercase is only valid with --maskchar lowercase")
        sys.exit(1)

    return args


def main():
    """
    Entry point for command line use.
    """
    logging.basicConfig(level = logging.INFO)
    args = parse_args()
    # Set up output file handles
    if args.outfile_unmasked:
        if args.outfile_unmasked is not sys.stdout:
            fh_unmasked = open(args.outfile_unmasked, "w")
        else:
            fh_unmasked = sys.stdout
    if args.outfile_masked:
        if args.outfile_masked is not sys.stdout:
            fh_masked = open(args.outfile_masked, "w")
        else:
            fh_masked = None

    try:
        split_masked(
            args.input,
            fh_unmasked,
            fh_masked,
            args.maskchar,
            args.minlength_masked,
            args.minlength_unmasked,
            args.revert_lowercase
        )
    finally:
        fh_unmasked.close()
        fh_masked.close()


if __name__ == "__main__":
    main()
