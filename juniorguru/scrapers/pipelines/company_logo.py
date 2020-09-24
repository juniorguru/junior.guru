import hashlib
from io import BytesIO
from pathlib import Path

from PIL.PngImagePlugin import PngInfo
from PIL import Image, ImageChops, ImageOps

from scrapy.pipelines.images import ImagesPipeline, ImageException
from scrapy.utils.python import to_bytes
from scrapy.utils.misc import md5sum


class Pipeline(ImagesPipeline):
    MAX_SIZE_PX = 1000
    SIZE_PX = 100
    PADDING_PX = 5

    DEFAULT_IMAGES_URLS_FIELD = 'company_logo_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'company_logos'

    def __init__(self, store_uri, *args, **kwargs):
        self.images_dir = store_uri
        super().__init__(store_uri, *args, **kwargs)

    def image_downloaded(self, response, request, info):
        path = self.file_path(request, response=response, info=info)

        orig_image = Image.open(BytesIO(response.body))
        width, height = orig_image.size
        if width > self.MAX_SIZE_PX or height > self.MAX_SIZE_PX:
            raise ImageException(f'Image too large ({width}x{height} < {self.MAX_SIZE_PX}x{self.MAX_SIZE_PX})')

        image, buffer = self.convert_image(orig_image)
        buffer.seek(0)
        checksum = md5sum(buffer)

        width, height = image.size
        self.store.persist_file(path, buffer, info,
                                meta={'width': width, 'height': height},
                                headers={'Content-Type': 'image/png'})
        return checksum

    def convert_image(self, image, size=None):
        pnginfo = PngInfo()
        pnginfo.add_text('original_width', str(image.width))
        pnginfo.add_text('original_height', str(image.height))

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
        side_size = self.SIZE_PX - (2 * self.PADDING_PX)
        image = image.resize((side_size, side_size))

        # add padding
        image = ImageOps.expand(image, border=self.PADDING_PX, fill=(255, 255, 255))

        buffer = BytesIO()
        image.save(buffer, 'PNG', pnginfo=pnginfo)
        return image, buffer

    def file_path(self, request, **kwargs):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'company-logos/{image_guid}.png'

    def item_completed(self, results, item, info):
        if results:
            results = sorted(results, key=self.image_original_size, reverse=True)
            results = [results[0]]
        return super().item_completed(results, item, info)

    def image_original_size(self, result):
        ok, result = result
        if ok:
            image = Image.open(Path(self.images_dir) / result['path'])
            width = int(image.text['original_width'])
            height = int(image.text['original_height'])
            return width * height
        return 0
