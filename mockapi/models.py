# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Model, CharField, TextField, IntegerField

class MockAnswer(Model):
    url = CharField(max_length=400)
    req_method = CharField(max_length=20, default="GET")
    use_up = IntegerField(null=True, blank=True)
    query_params = TextField(default="")
    req_body = TextField(default="")
    ans_status = IntegerField(default=200)
    ans_body = TextField(default="")
    
    __str__ = lambda self: "{} /{}".format(self.req_method, self.url)
    
