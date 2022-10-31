from peewee import CharField, IntegerField, ForeignKeyField, OperationalError

from juniorguru.models.base import BaseModel


class Sync(BaseModel):
    id = CharField(primary_key=True)

    @classmethod
    def _restart(cls):
        for model in [cls, SyncCommand]:
            model.drop_table()
            model.create_table()

    @classmethod
    def start(cls, id):
        try:
            return cls.get(id=id)
        except cls.DoesNotExist:
            cls._restart()
            return cls.create(id=id)
        except OperationalError:
            cls._restart()
            return cls.start(id)

    def command_start(self, name, time):
        return SyncCommand.create(name=name, sync=self, time_start=time)

    def command_end(self, name, time):
        command = self.list_commands \
            .where(SyncCommand.name == name) \
            .get()
        command.time_diff = time - command.time_start
        command.save()
        return command

    def is_command_seen(self, name):
        return self.list_commands \
            .where(SyncCommand.name == name) \
            .exists()

    def is_command_unseen(self, name):
        return not self.is_command_seen(name)

    def times_min(self):
        return {command.name: command.time_diff_min
                for command
                in self.list_commands.order_by(SyncCommand.time_diff.desc())}


class SyncCommand(BaseModel):
    name = CharField(primary_key=True)
    sync = ForeignKeyField(Sync, backref='list_commands')
    time_start = IntegerField()
    time_diff = IntegerField(null=True)

    @property
    def time_diff_min(self):
        return self.time_diff / 60000000000
