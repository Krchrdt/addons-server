# Generated by Django 2.2.5 on 2019-09-12 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import olympia.amo.fields
import olympia.amo.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviewers', '__first__'),
        ('access', '0001_initial'),
        ('versions', '__first__'),
        ('addons', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('action', models.SmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (12, 12), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (53, 53), (60, 60), (98, 98), (99, 99), (100, 100), (101, 101), (102, 102), (103, 103), (104, 104), (105, 105), (106, 106), (107, 107), (108, 108), (109, 109), (110, 110), (120, 120), (121, 121), (128, 128), (130, 130), (131, 131), (132, 132), (133, 133), (134, 134), (135, 135), (136, 136), (137, 137), (138, 138), (139, 139), (140, 140), (141, 141), (142, 142), (143, 143), (144, 144), (145, 145), (146, 146), (147, 147), (148, 148), (149, 149), (150, 150), (151, 151), (152, 152), (153, 153), (154, 154), (155, 155)])),
                ('_arguments', models.TextField(blank=True, db_column='arguments')),
                ('_details', models.TextField(blank=True, db_column='details')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'log_activity',
                'ordering': ('-created',),
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ActivityLogEmails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('messageid', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'log_activity_emails',
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VersionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('activity_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.ActivityLog')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='versions.Version')),
            ],
            options={
                'db_table': 'log_activity_version',
                'ordering': ('-created',),
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('activity_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.ActivityLog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'log_activity_user',
                'ordering': ('-created',),
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GroupLog',
            fields=[
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', olympia.amo.fields.PositiveAutoField(primary_key=True, serialize=False)),
                ('activity_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.ActivityLog')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='access.Group')),
            ],
            options={
                'db_table': 'log_activity_group',
                'ordering': ('-created',),
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DraftComment',
            fields=[
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', olympia.amo.fields.PositiveAutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(blank=True, max_length=255, null=True)),
                ('lineno', models.PositiveIntegerField(null=True)),
                ('comment', models.TextField(blank=True)),
                ('canned_response', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='reviewers.CannedResponse')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='versions.Version')),
            ],
            options={
                'db_table': 'log_activity_comment_draft',
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CommentLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('comments', models.TextField()),
                ('activity_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.ActivityLog')),
            ],
            options={
                'db_table': 'log_activity_comment',
                'ordering': ('-created',),
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AddonLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('activity_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activity.ActivityLog')),
                ('addon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addons.Addon')),
            ],
            options={
                'db_table': 'log_activity_addon',
                'ordering': ('-created',),
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ActivityLogToken',
            fields=[
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', olympia.amo.fields.PositiveAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('use_count', models.IntegerField(default=0, help_text='Stores the number of times the token has been used')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_log_tokens', to=settings.AUTH_USER_MODEL)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token', to='versions.Version')),
            ],
            options={
                'db_table': 'log_activity_tokens',
            },
            bases=(olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name='activitylogtoken',
            constraint=models.UniqueConstraint(fields=('version', 'user'), name='version_id'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['action'], name='log_activity_1bd4707b'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['created'], name='created_idx'),
        ),
    ]
