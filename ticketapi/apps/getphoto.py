import argparse
import sys
from ticketapi.datalayer import *
from ticketapi.data.logger import logger
from ticketapi.data import LOG_FILE
from io import StringIO
from PIL import Image


def get_image(data):
    stream = StringIO(data)
    return Image.open(stream)


if __name__ == '__main__':
    # Create our arguement parser
    parser = argparse.ArgumentParser(
        description=' '.join([
            'This CLI utility allows one to pull a photo out of the database and either view or save it.',
            'This is an internal tool used to pull images from the database temporarily and may be used as',
            'a reference on how data can be pulled from the database. This may be used by anyone given they',
            'know how to get a ticket id'
        ]),
        epilog='And that\'s how you do it'
    )

    # Setup our arguments
    parser.add_argument(
        'ticket_id',
        metavar='888',
        type=int,
        help='id of the ticket to pull from the database, this may require examining the database itself.'
    )
    parser.add_argument(
        '--save', '-s',
        metavar='filename.png',
        help=' '.join([
            'Save an image with a filename. This must be a filename and not filepath, the photo will be stored in',
            'the ticketapi directory under saved_photos. If the directory does not exist, it will be created.'
        ])
    )
    parser.add_argument(
        '--display', '-d',
        action='store_true',
        help='Display the photo via ImageMagick, requires a display of some sort whether it be SSH X forwarding, etc.'
    )

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    try:
        with DB() as s:
            ticket = s.query(Ticket).filter(Ticket.ticketID == args.ticket_id).first()
            if ticket is not None:
                img_data = ticket.photo
                img = get_image(img_data)

                if args.save:
                    img.save(args.save)

                if args.display:
                    try:
                        img.show()
                    except Exception as e:
                        logger.exception(e)
                        print('Something went wrong, probably unable to open display, check logs: {logfile}'.format(
                            logfile=LOG_FILE
                        ))
    except Exception as e:
        logger.exception(e)
        print('Something went wrong processing request, check logs: {logfile}'.format(logfile=LOG_FILE))


