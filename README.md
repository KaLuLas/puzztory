# ProjectPuzztoryNext

**Usertable**

| 属性名     |      | 注释                    |
| ---------- | ---- | ----------------------- |
| useremail  |      | 用户邮箱，max_length=50 |
| username   |      | 用户昵称，max_length=50 |
| level      |      | 等级，default=1         |
| experience |      | 经验值，default=0       |

**Storytable**

| 属性名             |      | 注释                                                        |
| ------------------ | ---- | ----------------------------------------------------------- |
| username           |      | 创建人昵称，max_length=50                                   |
| useremail          |      | 创建人邮箱，max_length=50                                   |
| title              |      | 标题，max_length=50                                         |
| likescount         |      | 获得的赞数，default=0                                       |
| fragmentcapacity   |      | 最多允许片段数（由作者决定，default=50                      |
| fragmentscount     |      | 当前片段个数，default=0                                     |
| branch             |      | 是否允许分支，default='0'                                   |
| wordslimit         |      | 是否限制片段字数，default='0'                               |
| finished           |      | 是否完结，default='0'                                       |
| modified           |      | 是否允许修改（作者和游客一起用，作者身份优先），default='1' |
| ineditable         |      | 修改的锁，default='0'                                       |
| createtime         |      | 故事创建日期                                                |
| beginning          |      | 故事开头片段id                                              |
| storyid            |      | 故事id                                                      |
| fragmentwordslimit |      | 片段的具体限制字数，default=0                               |

**Fragmenttable**

| 属性名        |      | 注释                      |
| ------------- | ---- | ------------------------- |
| username      |      | 创建人昵称，max_length=50 |
| useremail     |      | 创建人邮箱，max_length=50 |
| content       |      | 片段文本                  |
| createtime    |      | 创建时间                  |
| commentscount |      | 评论数，default=0         |
| likescount    |      | 获得的赞数，default=0     |
| storyid       |      | 故事ID                    |
| branchid      |      | 所处分支ID                |
| branchleft    |      | 左分支ID                  |
| branchright   |      | 右分支ID                  |

**Commenttable**

| 属性名     |      | 注释                    |
| ---------- | ---- | ----------------------- |
| commentid  |      | 评论ID                  |
| storyid    |      | 故事ID                  |
| fragmentid |      | 片段ID                  |
| content    |      | 评论文本                |
| username   |      | 用户昵称，max_length=50 |
| useremail  |      | 用户邮箱，max_length=50 |
| createtime |      | 创建时间                |
| likescount |      | 点赞数，default=0       |



**2019.05.12:**

- [x] 新增pythonUser信息中的用户昵称，并且更改欢迎页及用户空间
- [x] 增加已有用户的lastname
- [x] 【新建故事提交UI】新建故事输入框限制
- [x] 主页上面加点margin，
- [x] 【新建故事提交UI】自定义关键词 / 自定义规则 （行数可变的输入）
- [x] 【新建故事提交UI】字数限制，输入类型限制
- [ ] 测试数据库是否修改成功



**TODO:**

- [x] 数据库内容检索
- [x] 登陆错误信息弹窗
- [x] 输入为空时的对应处理
- [x] 登陆/注册界面UI完善

- [ ] 故事发布页UI / 逻辑 【 KAL

- [ ] 主界面列表图标 & 故事框图片添加 【 KAL
- [x] （故事发布完成）主界面故事展示 & 排行榜 【 ALEX
- [ ] 故事展示页UI / 逻辑 & 添加片段功能 【 ALEX



**2019/05/08**

- [x] 数据库models修改【ALEX
- [x] 用户登录状态保存 



**2019/05/04**

- [x] 主界面UI粗略版本完成 【 KAL



**2019/05/03** 

- [x] 登陆界面UI完善 / 功能完善 / 
- [x] 主界面UI完善  LOGO 调整/  【 KAL



**2019/05/02** 主界面导航条， login.html



**APPEND：**

- [x] bootstrap3到bootstrap4过渡
- [x] 数据库表单更新



