from datetime import date, timedelta

from scrapy.exceptions import DropItem


class NotApproved(DropItem):
    pass


class Expired(DropItem):
    pass


class Pipeline():
    IMPLICIT_EXPIRATION_DAYS = 30

    def __init__(self, today=None):
        self.today = today or date.today()

    def process_item(self, item, spider):
        if not item.get('approved_at'):
            raise NotApproved()
        item['posted_at'] = item['approved_at']

        if not item.get('expires_at'):
            item['expires_at'] = item['approved_at'] + timedelta(days=self.IMPLICIT_EXPIRATION_DAYS)
        if item['expires_at'] <= self.today:
            raise Expired(f"Expiration {item['expires_at']:%Y-%m-%d} ≤ today {self.today:%Y-%m-%d}")

        return item
