# Generated by Django 4.0.3 on 2022-04-21 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='小说名')),
                ('image_url', models.CharField(max_length=500, verbose_name='封面图片链接')),
                ('book_url', models.CharField(max_length=500, verbose_name='小说主页链接')),
                ('new_chapter_name', models.CharField(max_length=100, verbose_name='最新章节名')),
                ('new_chapter_url', models.CharField(max_length=500, verbose_name='最新章节链接')),
                ('update_time', models.DateTimeField(verbose_name='最近更新时间')),
                ('status', models.CharField(max_length=20, verbose_name='连载状态')),
                ('detail', models.CharField(max_length=1000, verbose_name='简介')),
            ],
            options={
                'db_table': 'book_info',
            },
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='作者名')),
            ],
            options={
                'db_table': 'book_author',
            },
        ),
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='漫画名')),
                ('image_url', models.CharField(max_length=500, verbose_name='最后阅读章节的链接')),
                ('manga_url', models.CharField(max_length=500, verbose_name='漫画主页链接')),
                ('status', models.CharField(max_length=20, verbose_name='状态')),
                ('detail', models.CharField(max_length=1000, verbose_name='简介')),
            ],
            options={
                'db_table': 'manga_info',
            },
        ),
        migrations.CreateModel(
            name='MangaAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='作者名')),
                ('url', models.CharField(max_length=500, verbose_name='作者主页链接')),
            ],
            options={
                'db_table': 'manga_author',
            },
        ),
        migrations.CreateModel(
            name='MangaCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='类别名')),
                ('url', models.CharField(max_length=500, verbose_name='类别链接')),
            ],
            options={
                'db_table': 'manga_category',
            },
        ),
        migrations.CreateModel(
            name='MangaHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_read_chapter', models.CharField(max_length=100, null=True, verbose_name='最后阅读章节')),
                ('last_read_time', models.DateTimeField(auto_now=True, verbose_name='最后阅读时间')),
                ('last_read_url', models.CharField(max_length=500, null=True, verbose_name='最后阅读章节的链接')),
                ('is_read', models.SmallIntegerField(default=0, verbose_name='是否浏览')),
                ('collect', models.SmallIntegerField(choices=[(0, '未加入书架'), (1, '已加入书架')], default=0, verbose_name='是否收藏')),
            ],
            options={
                'db_table': 'manga_history',
            },
        ),
        migrations.CreateModel(
            name='MangaInfoTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'manga_info_tag',
            },
        ),
        migrations.CreateModel(
            name='MangaTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='标签名')),
                ('url', models.CharField(max_length=500, verbose_name='标签链接')),
            ],
            options={
                'db_table': 'manga_tag',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('nickname', models.CharField(max_length=100, verbose_name='昵称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('phone_number', models.CharField(max_length=15, null=True, verbose_name='手机号')),
                ('email', models.CharField(max_length=50, verbose_name='邮箱')),
                ('active_status', models.SmallIntegerField(choices=[(0, '未激活用户'), (1, '已激活用户')], default=0, verbose_name='账号激活状态')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('active_status', 0), ('active_status', 1), _connector='OR'), name='action_check'),
        ),
        migrations.AddField(
            model_name='mangainfotag',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.manga', verbose_name='漫画id'),
        ),
        migrations.AddField(
            model_name='mangainfotag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.mangatag', verbose_name='标签id'),
        ),
        migrations.AddField(
            model_name='mangahistory',
            name='manga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.manga', verbose_name='漫画id'),
        ),
        migrations.AddField(
            model_name='mangahistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user', verbose_name='用户id'),
        ),
        migrations.AddField(
            model_name='manga',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.mangaauthor', verbose_name='作者id'),
        ),
        migrations.AddField(
            model_name='manga',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.mangacategory', verbose_name='类别id'),
        ),
        migrations.AddField(
            model_name='manga',
            name='tags',
            field=models.ManyToManyField(through='app.MangaInfoTag', to='app.mangatag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.bookauthor', verbose_name='作者id'),
        ),
    ]