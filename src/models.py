from tortoise import Model, fields


class User(Model):
    telegram_id = fields.IntField(pk=True)

    settings: fields.ReverseRelation['Settings']


class Settings(Model):
    complexity = fields.IntField(default=4)
    separator = fields.TextField(null=True)
    use_number = fields.BooleanField(default=True)

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name='models.User',
        related_name='settings'
    )


class Statistics(Model):
    user_id = fields.IntField(pk=True)
    generation_human = fields.IntField(default=0)
    generation_non_human = fields.IntField(default=0)
    # generation_numbers_only = fields.IntField(default=0)
