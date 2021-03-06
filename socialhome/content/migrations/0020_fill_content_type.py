# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-18 20:10
from __future__ import unicode_literals

from django.db import migrations
from django.db.migrations import RunPython
from django.db.models import Q

from socialhome.content.enums import ContentType


def forward(apps, schema_editor):
    Content = apps.get_model("content", "Content")
    for content in Content.objects.filter(Q(parent__isnull=False) | Q(share_of__isnull=False)):
        if content.parent:
            Content.objects.filter(id=content.id).update(content_type=ContentType.REPLY)
        elif content.share_of:
            Content.objects.filter(id=content.id).update(content_type=ContentType.SHARE)
        # No need to do ContentType.CONTENT - it's the default


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0019_content_content_type'),
    ]

    operations = [
        RunPython(forward, RunPython.noop),
    ]
