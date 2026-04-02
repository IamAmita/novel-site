from django.db import models


class MasterClass(models.Model):
    """クラス種別（ID: 10-99）"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'masters_masterclass'

    def __str__(self):
        return self.name


class MasterStatus(models.Model):
    """状態種別（ID: 100-999）"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'masters_masterstatus'

    def __str__(self):
        return self.name


class MasterAction(models.Model):
    """アクション種別（ID: 100-999）"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'masters_masteraction'

    def __str__(self):
        return self.name


class MasterOperation(models.Model):
    """操作種別"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'masters_masteroperation'

    def __str__(self):
        return self.name


class MasterPermission(models.Model):
    """権限種別"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'masters_masterpermission'

    def __str__(self):
        return self.name


class MasterReason(models.Model):
    """理由マスタ"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'masters_masterreason'

    def __str__(self):
        return self.name


class MasterTable(models.Model):
    """テーブル種別（ID: 1000-9999）"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'masters_mastertable'

    def __str__(self):
        return self.name


class MasterTwoFactorMethod(models.Model):
    """2FA 認証方式"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)  # Email/SMS/TOTP
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'masters_mastertwofactormethod'

    def __str__(self):
        return self.name
