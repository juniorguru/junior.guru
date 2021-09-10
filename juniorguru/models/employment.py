from peewee import CharField, DateField, ForeignKeyField, TextField

from juniorguru.models.base import BaseModel


# Experimenting with Czechitas. Calling the model employment is stupid,
# but I needed to find a different name than 'job' so that the old model
# and the new model can co-exist for a while.


class Employment(BaseModel):
    title = CharField()
    company_name = CharField()
    description_html = TextField()


class EmploymentPosting(BaseModel):
    job = ForeignKeyField(Employment, backref='list_postings')
    url = CharField()
    source = CharField()
    seen_at = DateField()
