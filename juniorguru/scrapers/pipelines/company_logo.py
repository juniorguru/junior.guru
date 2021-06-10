import hashlib
from io import BytesIO

from PIL import Image, ImageChops, ImageOps, UnidentifiedImageError

from scrapy.pipelines.images import ImagesPipeline, ImageException
from scrapy.utils.python import to_bytes
from scrapy.utils.misc import md5sum


class Pipeline(ImagesPipeline):
    DEFAULT_IMAGES_URLS_FIELD = 'company_logo_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'company_logos'

    size_px = 100
    allowed_square_deviation_px = 2

    def __init__(self, store_uri, *args, **kwargs):
        self.images_dir = store_uri
        super().__init__(store_uri, *args, **kwargs)

    def image_downloaded(self, response, request, info, item=None):
        path = self.file_path(request, response=response, info=info)

        try:
            orig_image = Image.open(BytesIO(response.body))
        except UnidentifiedImageError:
            raise ImageException(f'Image cannot be identified ({request.url})')

        width, height = orig_image.size
        if abs(width - height) > self.allowed_square_deviation_px:
            raise ImageException(f'Image is not square ({width}x{height})')

        image, buffer = self.convert_image(orig_image)
        buffer.seek(0)
        checksum = md5sum(buffer)

        width, height = image.size
        self.store.persist_file(path, buffer, info,
                                meta={'width': width, 'height': height},
                                headers={'Content-Type': 'image/png'})
        return checksum

    def convert_image(self, image, size=None):
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

        buffer = BytesIO()
        image.save(buffer, 'PNG')
        return image, buffer

    def file_path(self, request, response=None, info=None, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'company-logos/{image_guid}.png'
