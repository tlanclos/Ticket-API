import base64
import argparse
import pyperclip


if __name__ == '__main__':
    # Create our argument parser
    parser = argparse.ArgumentParser(
        description='Simple encoder script to base64 encode a file and either save it to a file or print to stdout',
        epilog='And that\'s how you do it'
    )

    # Add our arguments to the CLI
    parser.add_argument(
        'filename',
        help='filename to encode in base64'
    )
    parser.add_argument(
        '--copy', '-c',
        action='store_true',
        help='if specified, this will copy the base64 string to the clipboard'
    )
    parser.add_argument(
        '--no-stdout', '-P',
        dest='no_stdout',
        action='store_true',
        help='do not print the string to stdout'
    ),
    parser.add_argument(
        '--save', '-s',
        metavar='filename.b64',
        help='save the file to the provided filepath, this will disable print to stdout'
    )

    args = parser.parse_args()

    try:
        # Read the file's data
        with open(args.filename, 'rb') as f:
            data = f.read()
    except Exception as e:
        # either the file doesn't exist or permission denied, but something went wrong
        print('Unable to read the file: {filename}'.format(filename=args.filename))
        print(e)
    else:
        # encode the string into base64
        encoded = base64.standard_b64encode(data).decode('ascii')

        # copy to the users clipboard if specified
        if args.copy:
            pyperclip.copy(encoded)

        # if a filename is given, then attempt to save to that file
        if args.save:
            args.no_stdout = True
            try:
                # we only need to write ascii because its base64
                with open(args.save, 'w') as s:
                    s.write(encoded)
            except Exception as e:
                # we wer unable to save the data, probably permission denied
                print('Unable to save file: {filename}'.format(filename=args.save))
                print(e)

        # don't print to stdout if specified
        if not args.no_stdout:
            print(encoded)
