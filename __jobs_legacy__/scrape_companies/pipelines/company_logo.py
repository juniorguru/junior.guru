import hashlib
from io import BytesIO
from pathlib import Path

import piexif
from PIL import Image, ImageChops, ImageOps, UnidentifiedImageError

from scrapy.pipelines.images import ImagesPipeline, ImageException
from scrapy.utils.python import to_bytes
from scrapy.utils.misc import md5sum


class Pipeline(ImagesPipeline):
    DEFAULT_IMAGES_URLS_FIELD = 'company_logo_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'company_logos'

    max_size_px = 1000
    size_px = 100

    def __init__(self, store_uri, *args, **kwargs):
        self.images_dir = store_uri
        super().__init__(store_uri, *args, **kwargs)

    def item_completed(self, results, item, info):
        item = super().item_completed(results, item, info)

        # Loading information about original width and height for each of the images
        # from their EXIF meta data, then selecting the best suited.
        #
        # Why is this saved in EXIF? Because the ImagesPipeline caches images. If it
        # figures out that the image for given URL is already on disk, it won't run
        # most of the things here. Also, the data in the database are flushed
        # with every sync. And so on. Been there. Done that. Saving it to EXIF
        # is the best method, which survives all the pitfalls, trust me!
        company_logos = item.get(self.DEFAULT_IMAGES_RESULT_FIELD, [])
        orig_sizes = [load_orig_size(Path(self.images_dir) / company_logo['path'])
                      for company_logo in company_logos]
        company_logo = select_company_logo(company_logos, orig_sizes, self.size_px)
        if company_logo:
            item['company_logo_path'] = f"images/{company_logo['path']}"
        return item

    def image_downloaded(self, response, request, info, item=None):
        path = self.file_path(request, response=response, info=info)

        try:
            orig_image = Image.open(BytesIO(response.body))
        except UnidentifiedImageError:
            raise ImageException(f'Image cannot be identified ({request.url})')

        width, height = orig_image.size
        if width > self.max_size_px or height > self.max_size_px:
            raise ImageException(f'Image too large ({width}x{height} < {self.max_size_px}x{self.max_size_px})')

        image, buffer = self.convert_image(orig_image)
        buffer.seek(0)
        checksum = md5sum(buffer)

        width, height = image.size
        self.store.persist_file(path, buffer, info,
                                meta={'width': width, 'height': height},
                                headers={'Content-Type': 'image/png'})
        return checksum

    def convert_image(self, image):
        orig_width, orig_height = image.size

        # transparent to white
        image = image.convert('RGBA')
        background = Image.new('RGBA', image.size, (255, 255, 255))
        background.paste(image, (0, 0), image)
        image = background.convert('RGB')

        # trim white
        background = Image.new('RGB', image.size, (255, 255, 255))
        diff = ImageChops.difference(image, background)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        image = image.crop(diff.getbbox())

        # make it a square
        side_size = max(image.width, image.height)
        image = ImageOps.pad(image, (side_size, side_size), color=(255, 255, 255))

        # resize
        image = image.resize((self.size_px, self.size_px))

        # save, put information about the original width and height to EXIF
        buffer = BytesIO()
        image.save(buffer, 'PNG', exif=create_orig_size_exif(orig_width, orig_height))
        return image, buffer

    def file_path(self, request, response=None, info=None, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'logos-jobs/{image_guid}.png'


def create_orig_size_exif(width, height):
    return piexif.dump({
        '0th': {
            piexif.ImageIFD.Make: 'junior.guru',
            piexif.ImageIFD.XResolution: (width, 1),
            piexif.ImageIFD.YResolution: (height, 1),
        }
    })


def load_orig_size(path):
    image = Image.open(path)
    exif = piexif.load(image.info['exif'])
    try:
        width = exif['0th'][piexif.ImageIFD.XResolution][0]
        height = exif['0th'][piexif.ImageIFD.YResolution][0]
        return width, height
    except (IndexError, KeyError):
        return 0, 0


def select_company_logo(company_logos, orig_sizes, size_px):
    def sort_key(company_logo__orig_size):
        # Deconstruct given tuple to the original width and height of the image.
        width, height = company_logo__orig_size[1]

        # Multiplied by -1 to ensure descending sort, i.e. larger is better.
        area = -1 * width * height

        # For small images, the shape doesn't matter. All will be compared
        # as if they were perfect squares.
        if width < size_px or height < size_px:
            similarity_to_square = 0
        else:
            similarity_to_square = abs(width - height)  # closer to zero, more like square

        return (similarity_to_square, area)

    zipped_sorted_list = sorted(zip(company_logos, orig_sizes), key=sort_key)
    try:
        company_logo__orig_size = zipped_sorted_list[0]
    except IndexError:
        return None
    return company_logo__orig_size[0]
