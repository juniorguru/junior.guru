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
    min_square_size_px = 100
    size_px = 100

    def __init__(self, store_uri, *args, **kwargs):
        self.images_dir = store_uri
        super().__init__(store_uri, *args, **kwargs)

    def item_completed(self, results, item, info):
        item = super().item_completed(results, item, info)

        def sort_key(key_value):
            orig_width, orig_height = key_value[1]
            orig_area = orig_width * orig_height
            if orig_width < self.min_square_size_px or orig_height < self.min_square_size_px:
                return (0, -1 * orig_area)
            similarity_to_square = abs(orig_width - orig_height)  # 0 means it is square
            return (similarity_to_square, -1 * orig_area)

        paths = [tuple_[0] for tuple_ in sorted([
            (company_logo['path'], self.get_orig_size(company_logo['path']))
            for company_logo
            in item.get(self.DEFAULT_IMAGES_RESULT_FIELD, [])
        ], key=sort_key)]

        if paths:
            item['company_logo_path'] = f"images/{paths[0]}"
        return item

    def get_orig_size(self, path):
        image = Image.open(Path(self.images_dir) / path)
        exif = piexif.load(image.info['exif'])
        try:
            return exif['0th'][piexif.ImageIFD.XResolution][0], exif['0th'][piexif.ImageIFD.YResolution][0]
        except (IndexError, KeyError):
            return 0, 0

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

        # meta data
        exif = piexif.dump({
            '0th': {
                piexif.ImageIFD.Make: 'junior.guru',
                piexif.ImageIFD.XResolution: (orig_width, 1),
                piexif.ImageIFD.YResolution: (orig_height, 1),
            }
        })

        buffer = BytesIO()
        image.save(buffer, 'PNG', exif=exif)
        return image, buffer

    def file_path(self, request, response=None, info=None, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'company-logos/{image_guid}.png'
