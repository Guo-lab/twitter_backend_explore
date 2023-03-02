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

# S
