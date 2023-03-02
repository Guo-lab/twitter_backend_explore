# twitter-comment-Component 第四个视频差2:26:10

## 简单尝试直接实现 “评论” 模块 一个读写闭环

A. 创建出应用组件 `python manage.py startapp comments`

先 model 后 api, model 创建好之后需要在迁移之前补充 project setting.py 中的组件 INSTALLED_APPS, 然后 `python manage.py makemigrations`

B. admin.py 注册模型

C. migrate 消耗时间，一般情况是 test 通过之后才会 migrate

- `python manage.py test`
- `python manage.py migrate`.
- 注意此时路径 `path('admin/', admin.site.urls),`

（后续自学 custom testcase 建立）

Model + Admin Done

<br>

## 实现 Comment 的相关 API 进行补充增删查改功能

```
POST   /api/comments/    -> create
GET    /api/comments/    -> list
GET    /api/comments/1/  -> retrieve
DELETE /api/comments/1/  -> destroy
PATCH  /api/comments/1/  -> partial update
PUT    /api/comments/1/  -> update
```

url.py 的补充, api/view 的实现(包括views, serializers 每一个不同的object在不同的场景下需要渲染的都“应该”是不同的 serializer)

对于 model 的测试 /comments/test.py 和对于 api 的测试 /comments/api/test.py 需要分别实现

`python manage.py test comments`

<br>

### Create: 保证 APIClient 能够 post 成功

<br>

个人理解:

- Model 创建好之后，migrations 会将其“实例化”，（在实际最终test过程中，会先测试api在测试model）
- 选取具备 actions 的 ViewSet 可以分步创建序列器， 这样更好地进行对数据的检验截取，并且可以达到不同的渲染效果 (针对不同的数据库操作，首先完成 create action)
- <br>
  <br>

### Update / Destroy / List: 使得 APIClient

<br>更新删除帖子，需要自己设计权限

每次 self.get_object() 以实例进行更新

至于 list， 可以安装 django_filters [Filtering - Django REST framework . django-rest-framework.org](https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend) 应用在 ViewSet 中


> 交互  <br>
>
> - 选择1:  `python manage.py shell`.
>
>   ```
>   from comments.model import Comment
>   Comment.objects.all()
>   print(Comment.objects.all().query())
>   ```
> - 选择2: logging [python字符串对齐](https://zhuanlan.zhihu.com/p/51436239) and [Logging raw SQL to the console in Django](https://www.neilwithdata.com/django-sql-logging)
>
>   Logging 在 settings.py 的 local 配置 (try, except)
>   通过看到 logging 可以进行除cache策略以外的数据库层的优化比如
> - - `self.filter_queryset(queryset).prefetch_related('user').order_by('created_at')` or
> - - `self.filter_queryset(queryset).select_related('user').order_by('created_at')` (JOIN) 多数据库存书可能失效
