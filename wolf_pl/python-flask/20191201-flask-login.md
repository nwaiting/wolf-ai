### flask - login
- **概述：**
>       
>       
>    
>       
>    
>       
>    

- **flask-login使用步骤：**
>       1、初始化
>           login_manager = LoginManager()
>           login_manager.init_app(apps)
>       2、添加一个获取登录用户的方法
>           #当需要验证一个用户的时候
>           @login_manager.user_loader      # 这个方法里的login_manager是初始化的那个对象，这个方法的目的就是flask-login会通过这个验证用户是否存在。返回为None的话会抛异常。
>           def load_user(user_id):
>               user = UserMixin()
>               return user
>       3、定义登陆方法，当系统要进行登陆时会跳转到此方法
>           @apps.route('/login', methods=['GET', 'POST'])
>           def login():
>               #验证通过后加入到login_user里面
>               user = UserMixin()
>               user.id = '111111'
>               login_user(user)
>               return flask.render_template('login.html',errormsg = errormsg)
>           
>       
>    
>       
>    
>       
>    
>       

- **待续：**
>       参考：https://my.oschina.net/u/1462124/blog/611471     Flask-Login使用教程
>            https://blog.csdn.net/weixin_41263513/article/details/85013477     【Flask/跟着学习】Flask大型教程项目#04：用户登陆
>            https://www.jb51.net/article/143893.htm    Flask框架通过Flask_login实现用户登录功能示例
>       
>    
>       
>    
>       
>    
>       
>    
>       
>    
>       
>    
>       
>    
