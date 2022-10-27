import click


class BaseGroup(click.Group):
    def load_dynamic_commands(self):
        raise NotImplementedError()

    def list_commands(self, context):
        names = super().list_commands(context)
        names += [name for name, command in self.load_dynamic_commands()]
        return sorted(names)

    def get_command(self, context, name):
        command = super().get_command(context, name)
        if command:
            return command
        return dict(self.load_dynamic_commands())[name]
