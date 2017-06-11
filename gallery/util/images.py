from gallery.logger import BellLogger
from urllib import request, parse
from io import BytesIO
import imghdr
import struct
import shutil

DEFAULT_IMG_WIDTH = 800
DEFAULT_IMG_HEIGHT = 1200

imgerr_log = BellLogger("image_sizer", default_level="INFO")


def calc_image_size(url, filename):
    full_url = parse.urljoin(url, filename)
    with request.urlopen(full_url) as fhandle:
        file_strm = BytesIO()
        shutil.copyfileobj(fhandle, file_strm)
        file_strm.seek(0)
        head = file_strm.read(24)
        if len(head) != 24:
            imgerr_log.log("Error Short head < 24: {}".format(filename))
            return
        if imghdr.what(file_strm) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                imgerr_log.log("Error PNG 0x0d0a1a0a: {}".format(filename))
                return
            width, height = struct.unpack('>ii', head[16:24])
        else:
            file_strm.seek(0)
            if imghdr.what(file_strm) == 'gif':
                width, height = struct.unpack('<HH', head[6:10])
            else:
                try:
                    file_strm.seek(0)  # Read 0xff next
                    size = 2
                    ftype = 0
                    while not 0xc0 <= ftype <= 0xcf:
                        file_strm.seek(size, 1)
                        byte = file_strm.read(1)
                        while ord(byte) == 0xff:
                            byte = file_strm.read(1)
                        ftype = ord(byte)
                        size = struct.unpack('>H', file_strm.read(2))[0] - 2
                    # We are at a SOFn block
                    file_strm.seek(1, 1)  # Skip `precision' byte.
                    height, width = struct.unpack('>HH', file_strm.read(4))
                except Exception as e:
                    imgerr_log.log("Error W0703: {}, {}".format(filename, str(e)))
                    return
        imgerr_log.log("{}: {}x{}".format(filename, width, height))

        width = width if width > 20 else DEFAULT_IMG_WIDTH
        height = height if height > 20 else DEFAULT_IMG_HEIGHT
    return width, height
