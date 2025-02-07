import argparse

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('operation', choices=['extract', 'edit'])
cli_parser.add_argument('filename')
cli_parser.add_argument(
    '-v', 
    '--verbose', 
    action='store_true',
    help='toggle verbose mode')
cli_parser.add_argument(
    '-n', 
    '--new', 
    action='store_true',
    help='overwrite or create a file instead of patching an .EMI file')
cli_parser.add_argument(
    '-c', 
    '--copy', 
    action='store_true',
    help='copy the file before applying the patch')
cli_parser.add_argument(
    '-o', 
    '--out', 
    default=None,
    help='set the name of the output file')
cli_parser.add_argument(
    '-m', 
    '--mode',
    choices=['3', '4'],
    help='set the mode (3 or 4)')
cli_parser.add_argument(
    '-t', 
    '--toc',
    default=None,
    help='force extraction from the nth TOC entry')

def main():
    args = cli_parser.parse_args()
    if args.operation.lower() == "edit":
        from .editor import editor
        editor(args.filename, args.verbose, args.new, args.mode, args.copy)
    elif args.operation.lower() == "extract":
        from .extractor import extractor
        extractor(args.filename, args.verbose, args.mode, args.toc, args.out)