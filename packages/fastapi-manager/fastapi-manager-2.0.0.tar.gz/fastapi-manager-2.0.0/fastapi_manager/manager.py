from typing import Any, Optional
from importlib import import_module

from fastapi import FastAPI, Depends

# 全局配置
# 需要注意的是全局配置在 Manager 类初始化之前是拿不到的
settings: Any = None
app: Optional[FastAPI] = None


class Manager:

    def __init__(
            self,
            fa: FastAPI,
            setting_obj: Any = None,
            setting_py: str = None,
            url_router_setting_key: str = 'URL_ROUTERS',
            url_func_setting_key: str = 'URL_FUNCTIONS',
            middle_setting_key: str = 'MIDDLEWARE',
            depend_setting_key: str = 'DEPENDENCIES',
            custom_setting_key: str = 'CUSTOM_FUNCTIONS'
    ) -> None:
        self._fa = fa
        self._set_global_app()
        self._setting_obj = setting_obj
        self._setting_py = setting_py
        self._url_router_setting_key = url_router_setting_key
        self._url_func_setting_key = url_func_setting_key
        self._middle_setting_key = middle_setting_key
        self._depend_setting_key = depend_setting_key
        self._custom_setting_key = custom_setting_key

        # 配置初始化，
        self._setting: Any = None
        self._init()

    def _init(self):
        self._init_setting()
        self._init_api_core()

    # 根据不同的方法导入配置的对象
    # 如果直接指定 __init__ 方法中的 setting_obj 参数，则会根据传入
    # 数据的类型生成配置对象，规则如下：
    # - 当数据类型为 str 时: 直接当作动态导入的对象处理，这里不会去识
    #   别他是不是什么后缀文件，且动态导入的对象会去切割其最后一个 `.`
    #   符号，将其第一部分作为动态导入的对象，第二部分作为 getattr 反
    #   射获取的配置对象。
    #
    #       E.G.:
    #           app = FastAPI()
    #           Manager(app, 'settings.dev.dev_settings_obj')
    #
    #           - settings
    #                |
    #                —— dev.py  # dev.py文件中包含 dev_settings_obj 的一个对象
    #
    # - 当是其他类型的数据时，直接附加上去，只要此对象支持 getattr 反
    #   射获取对应的属性即可。
    #
    #       E.G.:
    #           app = FastAPI()
    #           setting = {"ROUTERS": [], ...}
    #           Manager(app, setting)
    #
    def _init_setting(self):
        # 对象
        if self._setting_obj and isinstance(self._setting_obj, str):
            m, s = self._setting_obj.rsplit('.', 1)
            module = import_module(m)
            setting = getattr(module, s)
        else:
            setting = self._setting_obj

        # py文件对象
        # 如果两个都指定，则后面的 py 文件配置会覆盖掉对象配置
        if self._setting_py and isinstance(self._setting_py, str):
            setting = import_module(self._setting_py)

        # 将解析好的配置文件对象重新挂载到一个新的属性上面
        # 当没有指定任何配置时，默认是一个空字典作为配置，
        # 防止后续代码执行报错。
        self._setting = setting or {}

        # 替换全局配置
        self._set_global_setting()

    # 将加载的配置替换到全局中
    def _set_global_setting(self):
        global settings
        settings = self._setting

    def _set_global_app(self):
        global app
        app = self._fa

    # 初始化 FastAPI 必要的的通用设置
    # _init_url_router: 初始化 FastAPI APIRouter 路由
    # _init_url_func: 初始化 FastAPI 函数路由
    # _init_depend: 初始化 FastAPI 依赖项
    # _init_middle: 初始化 FastAPI 中间件
    # _init_custom: 初始化 FastAPI 为主的一些函数，这些
    #   函数都已 FastAPI 对象为入参，且没有返回值
    def _init_url_router(self):
        routers = getattr(self._setting, self._url_router_setting_key, [])

        if not isinstance(routers, list):
            raise TypeError(
                f'{self._url_router_setting_key} is not a list type'
            )

        for router in routers:
            m, rt = router.rsplit('.', 1)
            self._fa.include_router(getattr(import_module(m), rt))

    def _init_url_func(self):
        funcs = getattr(self._setting, self._url_func_setting_key, [])

        if not isinstance(funcs, list):
            raise TypeError(f'{self._url_func_setting_key} is not a list type')

        for func in funcs:
            import_module(func)

    def _init_depend(self):
        dependencies = getattr(self._setting, self._depend_setting_key, [])

        if not isinstance(dependencies, list):
            raise TypeError(f'{self._depend_setting_key} is not a list type')

        for depend in dependencies:
            m, dep = depend.rsplit('.', 1)
            self._fa.router.dependencies.append(Depends(getattr(import_module(m), dep)))

    def _init_middle(self):
        middlewares = getattr(self._setting, self._middle_setting_key, {})

        if not isinstance(middlewares, dict):
            raise TypeError(f'{self._middle_setting_key} is not a dict type')

        for middleware, params in middlewares.items():
            m, md = middleware.rsplit('.', 1)
            params = params or {}
            app.add_middleware(getattr(import_module(m), md), **params)

    def _init_custom(self):
        custom_functions = getattr(self._setting, self._custom_setting_key, [])

        if not isinstance(custom_functions, list):
            raise TypeError(f'{self._custom_setting_key} is not a list type')

        for func in custom_functions:
            m, cf = func.rsplit('.', 1)
            getattr(import_module(m), cf)(self._fa)

    def _init_api_core(self):
        self._init_depend()
        self._init_middle()
        self._init_custom()
        self._init_url_router()
        self._init_url_func()
