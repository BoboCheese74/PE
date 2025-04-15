import json



# 用户相关视图文件，处理用户登录、验证和JWT令牌相关的功能


class LoginView(View):
    """
    用户登录视图类
    处理用户登录请求，验证用户身份，生成JWT令牌，获取用户角色和菜单权限
    """

    def buildTreeMenu(self, sys_menu_list):
        """
        将菜单列表构建成树形结构

        参数:
            sys_menu_list: 菜单列表
        返回:
            构建好的树形菜单列表
        """
        resultMenuList: list[SysMenu] = list()
        for menu in sys_menu_list:
            for e in sys_menu_list:
                if e.parent_id == menu.id:
                    # 如果菜单没有children属性，则添加一个children列表
                    if not hasattr(menu, "children"):
                        menu.children = list()
                    menu.children.append(e)
            # 将顶级菜单(parent_id=0)添加到结果列表中
            if menu.parent_id == 0:
                resultMenuList.append(menu)
        return resultMenuList

    def post(self, request):
        """
        处理POST请求，用于用户登录

        参数:
            request: HTTP请求对象
        返回:
            JsonResponse: 包含登录结果、用户信息和JWT令牌
        """
        try:
            # 解析请求体中的JSON数据
            data = json.loads(request.body.decode("utf-8"))
            username = data["username"]
            password = data["password"]
            print(username, password)

            # 根据用户名和密码查询用户
            user = SysUser.objects.get(username=username, password=password)

            # 获取JWT处理器
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 生成JWT载荷和令牌
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            # 获取用户角色列表
            roleList = SysRole.objects.raw(
                "SELECT id,name FROM sys_role WHERE id IN (SELECT role_id FROM "
                "sys_user_role WHERE user_id = " + str(user.id) + ")"
            )
            print("roleList=", roleList)

            # 获取用户菜单权限
            menuSet: set[SysMenu] = set()
            for row in roleList:
                print(row.id, row.name)
                # 根据角色ID获取关联的菜单
                menuList = SysMenu.objects.raw(
                    "SELECT * FROM sys_menu WHERE id IN (SELECT menu_id FROM sys_role_menu WHERE role_id = "
                    + str(row.id)
                    + ")"
                )
                for row2 in menuList:
                    print(row2.id, row2.name)
                    menuSet.add(row2)

            # 对菜单进行排序和构建树形结构
            menuList: list[SysMenu] = list(menuSet)
            sortedMenuList = sorted(menuList)
            self.buildTreeMenu(sortedMenuList)
            print(sortedMenuList)

            # 返回登录成功的响应，包含用户信息和JWT令牌
            return JsonResponse(
                {
                    "code": 200,
                    "succeed": True,
                    "message": "登录成功",
                    "data": SysUserSerializer(user).data,
                    "token": token,
                }
            )

        except ObjectDoesNotExist as e:
            # 用户名或密码错误
            return JsonResponse({"code": 2001, "message": "用户名或密码错误", "succeed": False})
        except Exception as e:
            # 其他异常处理
            print(e)
            return JsonResponse({"code": 500, "message": e})


class TestView(View):
    """
    测试视图类
    用于测试用户权限验证
    """

    def get(self, request):
        """
        处理GET请求，检查请求中的Authorization头

        参数:
            request: HTTP请求对象
        返回:
            JsonResponse: 根据权限返回用户列表或拒绝访问
        """
        # 获取请求头中的Authorization字段
        token = request.META.get("HTTP_AUTHORIZATION")
        if token is not None and token is not "":
            # 有权限时，返回所有用户信息
            UserList = SysUser.objects.all().values()
            data = list(UserList)
            return JsonResponse({"code": 200, "info": "调试", "message": data})
        else:
            # 无权限时，返回401错误
            return JsonResponse({"code": 401, "info": "没有访问权限"})


class JwtTestView(View):
    """
    JWT测试视图类
    用于测试JWT令牌的生成
    """

    def get(self, request):
        """
        处理GET请求，为特定用户生成JWT令牌

        参数:
            request: HTTP请求对象
        返回:
            JsonResponse: 包含生成的JWT令牌
        """
        # 获取特定用户
        user = SysUser.objects.get(username="BoboCheese", password="74Cheese")

        # 获取JWT处理器
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 生成JWT载荷和令牌
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 返回生成的JWT令牌
        return JsonResponse({"code": 200, "token": token})
