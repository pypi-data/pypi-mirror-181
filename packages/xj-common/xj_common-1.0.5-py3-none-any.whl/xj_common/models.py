from django.db import models

# from apps.user.models import User

SHARD_TABLE_NUM = 3


class Region(models.Model):
    id = models.AutoField("ID", primary_key=True)
    code = models.IntegerField('行政编码', null=False, default=0)
    p_code = models.IntegerField('上级行政编码', null=False, default=0)
    name = models.CharField('地区名称', null=False, default="", max_length=50)
    level = models.IntegerField('行政划分等级', null=False, default="0")
    is_delete = models.IntegerField('是否删除', null=False, default=0)
    spell = models.CharField('拼音', max_length=50, null=False, default="")

    class Meta:
        managed = False
        db_table = "append_public_region"
        verbose_name = "行政区编码表"
        verbose_name_plural = verbose_name
