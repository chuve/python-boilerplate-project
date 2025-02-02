from tortoise import fields, models


class BlogPost(models.Model):
    """
    The BlogPost model
    """

    id = fields.UUIDField(primary_key=True)
    title = fields.CharField(max_length=50, null=True)
    summary = fields.TextField(max_length=256, null=True)
    body = fields.TextField(max_length=256, null=True)


# class Users(models.Model):
#     """
#     The User model
#     """

#     id = fields.IntField(primary_key=True)
#     #: This is a username
#     username = fields.CharField(max_length=20, unique=True)
#     name = fields.CharField(max_length=50, null=True)
#     family_name = fields.CharField(max_length=50, null=True)
#     category = fields.CharField(max_length=30, default="misc")
#     password_hash = fields.CharField(max_length=128, null=True)
#     created_at = fields.DatetimeField(auto_now_add=True)
#     modified_at = fields.DatetimeField(auto_now=True)

#     def full_name(self) -> str:
#         """
#         Returns the best name
#         """
#         if self.name or self.family_name:
#             return f"{self.name or ''} {self.family_name or ''}".strip()
#         return self.username

#     class PydanticMeta:
#         computed = ["full_name"]
#         exclude = ["password_hash"]
