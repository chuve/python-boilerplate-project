from tortoise import fields, models


class BlogPost(models.Model):
    """
    The BlogPost model
    """

    id = fields.UUIDField(primary_key=True)
    title = fields.CharField(max_length=50, null=True)
    summary = fields.TextField(max_length=256, null=True)
    body = fields.TextField(max_length=256, null=True)
