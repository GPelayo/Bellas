from gallery.logger import BellLogger
from io import BytesIO
import imghdr
import struct

DEFAULT_IMG_WIDTH = 1852
DEFAULT_IMG_HEIGHT = 442

imgerr_log = BellLogger("image_sizer", default_level="INFO")


def calc_image_size(image_buffer, filename="No Name"):
    image_buffer.seek(0)
    head = image_buffer.read(24)
    if len(head) != 24:
        imgerr_log.log("Error Short head < 24: {}".format(filename))
        return DEFAULT_IMG_WIDTH, DEFAULT_IMG_HEIGHT
    if imghdr.what(image_buffer) == 'png':
        check = struct.unpack('>i', head[4:8])[0]
        if check != 0x0d0a1a0a:
            imgerr_log.log("Error PNG 0x0d0a1a0a: {}".format(filename))
            return DEFAULT_IMG_WIDTH, DEFAULT_IMG_HEIGHT
        width, height = struct.unpack('>ii', head[16:24])
    else:
        image_buffer.seek(0)
        if imghdr.what(image_buffer) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        else:
            try:
                image_buffer.seek(0)  # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    image_buffer.seek(size, 1)
                    byte = image_buffer.read(1)
                    while ord(byte) == 0xff:
                        byte = image_buffer.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', image_buffer.read(2))[0] - 2
                # We are at a SOFn block
                image_buffer.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', image_buffer.read(4))
            except Exception as e:
                imgerr_log.log("Error W0703: {}, {}".format(filename, str(e)))
                return DEFAULT_IMG_WIDTH, DEFAULT_IMG_HEIGHT
    imgerr_log.log("{}: {}x{}".format(filename, width, height))

    width = width if width > 20 else DEFAULT_IMG_WIDTH
    height = height if height > 20 else DEFAULT_IMG_HEIGHT
    return width, height
