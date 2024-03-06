from tortoise import Model, fields


class User(Model):
    telegram_id = fields.IntField(pk=True)
    generations = fields.IntField(default=0)

    settings: fields.ReverseRelation['Settings']


class Settings(Model):
    complexity = fields.IntField(default=4)
    length = fields.IntField(default=16)
    separator = fields.TextField(null=True)
    use_number = fields.BooleanField(default=True)
    use_upper = fields.BooleanField(default=True)
    use_lower = fields.BooleanField(default=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name='models.User',
        related_name='settings'
    )
