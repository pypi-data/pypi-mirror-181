# fastapi-manager

方便的初始化路由，中间件

## 安装

```shell
pip install fastapi-manager
```

## 使用

```python
# local.setting.py

# APIRouter的路由注册配置
URL_ROUTERS = [
    ...
]

# 使用 app 的路由注册配置
URL_FUNCTIONS = [
    ...
]

# 中间件注册配置
MIDDLEWARE = {
    ...
}

# 依赖项注册配置
DEPENDENCIES = [
    ...
]
```

```python
from fastapi import FastAPI
from fastapi_manager.manager import Manager

app = FastAPI()
Manager(app, setting_py='local.setting')
```

初始化完成后就可以在接口中使用 `local.setting.py` 中的配置

```python
from fastapi import APIRouter
from fastapi_manager.manager import settings

user = APIRouter(prefix='/user', tags=['用户信息'])


@user.post('/login', name='登录')
def login():
    print(settings)
    return {"msg": "登录成功"}
```

关于如何注册函数路由

```python
from fastapi_manager.manager import app


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

像如上方式编写接口代码后，配置里面的`URL_FUNCTIONS`才可以生效，直接导入实例化的 Fastapi 对象时没有效果的