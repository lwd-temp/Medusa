medusa_web_user=""
medusa_web_passwd=""
#没有的可以去ceye中申请，http://ceye.io/
#如果没有改为你的Key会导致有些远程命令执行无法检测
dns_log_url="XXXXX.ceye.io"
dns_log_key="XXXXXXXXXXXXXXXXXXXXXXXX"
debug_mode=False
whitelist_group_status=False#白名单是否开启
whitelist_group_list=[]#白名单群ID列表
super_administrator="" #超级管理员,只能一个
managed_group=[""]#你管理的群列表
FaceCascadePath="haarcascade_frontalface_default.xml" #人脸识别训练数据