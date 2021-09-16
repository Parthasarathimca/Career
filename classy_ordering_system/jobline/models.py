# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Joblineimport(models.Model):
    entrynum = models.DecimalField(db_column='EntryNum', primary_key=True, max_digits=20, decimal_places=2)  # Field name made lowercase.
    jobimportnum = models.DecimalField(db_column='JobImportNum', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    jobnum = models.DecimalField(db_column='JobNum', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ccphasecode = models.CharField(db_column='CCPhaseCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type1 = models.CharField(db_column='Type1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    num = models.CharField(db_column='Num', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description2 = models.CharField(db_column='Description2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    quantity = models.DecimalField(db_column='Quantity', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    materialtypecode = models.CharField(db_column='MaterialTypeCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    boardcolorcode = models.CharField(db_column='BoardColorCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    heightinches = models.DecimalField(db_column='HeightInches', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    widthinches = models.DecimalField(db_column='WidthInches', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    depthinches = models.DecimalField(db_column='DepthInches', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    drillpatternleft = models.CharField(db_column='DrillPatternLeft', max_length=255, blank=True, null=True)  # Field name made lowercase.
    drillpatternright = models.CharField(db_column='DrillPatternRight', max_length=255, blank=True, null=True)  # Field name made lowercase.
    l1ep = models.CharField(db_column='L1EP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    l1et = models.CharField(db_column='L1ET', max_length=255, blank=True, null=True)  # Field name made lowercase.
    l1ec = models.CharField(db_column='L1EC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    l2ep = models.CharField(db_column='L2EP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    l2et = models.CharField(db_column='L2ET', max_length=255, blank=True, null=True)  # Field name made lowercase.
    l2ec = models.CharField(db_column='L2EC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    s1ep = models.CharField(db_column='S1EP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    s1et = models.CharField(db_column='S1ET', max_length=255, blank=True, null=True)  # Field name made lowercase.
    s1ec = models.CharField(db_column='S1EC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    s2ep = models.CharField(db_column='S2EP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    s2et = models.CharField(db_column='S2ET', max_length=255, blank=True, null=True)  # Field name made lowercase.
    s2ec = models.CharField(db_column='S2EC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    staincode = models.CharField(db_column='StainCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    itemnum = models.CharField(db_column='ItemNum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vendornum = models.CharField(db_column='VendorNum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nonstockunitcost = models.DecimalField(db_column='NonStockUnitCost', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    nonstockunitprice = models.DecimalField(db_column='NonStockUnitPrice', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    note2 = models.CharField(db_column='Note2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    note3 = models.CharField(db_column='Note3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    prodcenter = models.CharField(db_column='ProdCenter', max_length=255, blank=True, null=True)  # Field name made lowercase.
    partsubcategory = models.CharField(db_column='PartSubCategory', max_length=255, blank=True, null=True)  # Field name made lowercase.
    custom = models.CharField(db_column='Custom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    spnum = models.CharField(db_column='SPNum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    roomid = models.CharField(max_length=255, db_column='RoomID', blank=True, null=True)  # Field name made lowercase.
    roomname = models.CharField(db_column='RoomName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    send = models.CharField(db_column='Send', max_length=255, blank=True, null=True)  # Field name made lowercase.
    partcost = models.DecimalField(db_column='PartCost', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    sqfttotal = models.DecimalField(db_column='SQFtTotal', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    bdcost = models.DecimalField(db_column='BDCost', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    edgecost = models.DecimalField(db_column='EdgeCost', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    staincost = models.DecimalField(db_column='StainCost', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    drillcost = models.DecimalField(db_column='DrillCost', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    stainlf = models.DecimalField(db_column='StainLF', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    stainopt = models.DecimalField(db_column='StainOpt', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    glaze = models.IntegerField(db_column='Glaze', blank=True, null=True)  # Field name made lowercase.
    loccode = models.CharField(db_column='LocCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    send_date_time = models.DateTimeField(blank=True, null=True)



    class Meta:
        managed = False
        db_table = 'JobLineImport'
