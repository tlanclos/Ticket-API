import os
import argparse
from os.path import basename
from ticketapi.datalayer import *
from ticketapi.data.logger import logger
from ticketapi.data import LOG_FILE
from ticketapi.data import TICKET_API_ROOT
from io import BytesIO
from PIL import Image


# This is where we will store all photos called with --save
PHOTO_LOCATION = os.path.join(TICKET_API_ROOT, 'saved_photos')


def get_image(data):
    """
    Convert byte string data to a PIL image

    :param data: bytestring data to convert
    :return: a PIL image
    """
    # get a byte stream of data (file descriptor to data)
    stream = BytesIO(data)
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
            '{location}. If the directory does not exist, it will be created.'.format(location=PHOTO_LOCATION)
        ])
    )
    parser.add_argument(
        '--display', '-d',
        action='store_true',
        help='Display the photo via ImageMagick, requires a display of some sort whether it be SSH X forwarding, etc.'
    )

    # Parse the current command line arguments
    args = parser.parse_args()

    try:
        with DB() as s:
            # Open a query for the selected ticket
            ticket = s.query(Ticket).filter(Ticket.ticketID == args.ticket_id).first()
            if ticket is not None:
                # Here we take in the photo and get the PIL image associated with it
                img_data = ticket.photo
                img = get_image(img_data)

                if args.save:
                    if not os.path.exists(PHOTO_LOCATION):
                        # Create the directory if it does not exist
                        os.mkdir(PHOTO_LOCATION)
                        
                    # Since we're saving in an explicit directory we definitely have access to,
                    # we get the basename of the passed in save location here and join it with the photo path
                    path = os.path.join(PHOTO_LOCATION, basename(args.save))
                    img.save(path)
                    print('image saved to: {path}'.format(path=path))

                if args.display:
                    try:
                        # if we want to display the image then attempt to display it
                        img.show()
                    except Exception as e:
                        logger.exception(e)
                        print('Something went wrong, probably unable to open display, check logs: {logfile}'.format(
                            logfile=LOG_FILE
                        ))
            else:
                print('Ticket ID not found, please check parameters')
                exit(2)
    except Exception as e:
        logger.exception(e)
        print('Something went wrong processing request, check logs: {logfile}'.format(logfile=LOG_FILE))


