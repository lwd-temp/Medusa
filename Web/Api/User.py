from Web.WebClassCongregation import UserInfo
from django.http import JsonResponse
from ClassCongregation import ErrorLog,randoms,Md5Encryption
import json
from Web.Workbench.LogRelated import UserOperationLogRecord,RequestLogRecord
"""login
{
	"username": "ascotbe",
	"passwd": "1"
}
"""
def Login(request):#用户登录，每次登录成功都会刷新一次Token
    RequestLogRecord(request, request_api="login")
    if request.method == "POST":
        try:
            Username=json.loads(request.body)["username"]
            Passwd=json.loads(request.body)["passwd"]
            Md5Passwd=Md5Encryption().Md5Result(Passwd)#对密码加密
            UserLogin=UserInfo().UserLogin(Username,Md5Passwd)
            if UserLogin is None:
                return JsonResponse({'message': '账号或密码错误', 'code': 604, })

            else:
                while True:#如果查询确实冲突了
                    Token = randoms().result(250)
                    QueryTokenValidity = UserInfo().QueryTokenValidity(Token)#用来查询Token是否冲突了
                    if not QueryTokenValidity:#如果不冲突的话跳出循环
                        break
                UpdateToken=UserInfo().UpdateToken(name=Username, token=Token)#接着更新Token
                if UpdateToken:#如果更新成功了
                    Uid = UserInfo().QueryUidWithToken(Token)  # 查询UID
                    UserOperationLogRecord(request, request_api="login", uid=Uid)
                    return JsonResponse({'message': Token, 'code': 200, })
        except Exception as e:
            ErrorLog().Write("Web_Api_User_LogIn(def)", e)
    else:
        return JsonResponse({'message': '请使用Post请求', 'code': 500, })


"""update_password
{
	"username": "ascotbe",
	"old_passwd": "1",
	"new_passwd": "1111"
}
"""
def UpdatePassword(request):#更新密码
    RequestLogRecord(request, request_api="update_password")
    if request.method == "POST":
        try:
            UserName=json.loads(request.body)["username"]
            OldPasswd=json.loads(request.body)["old_passwd"]
            NewPasswd = json.loads(request.body)["new_passwd"]
            Md5NewPasswd = Md5Encryption().Md5Result(NewPasswd)  # 对新密码加密
            Md5OldPasswd = Md5Encryption().Md5Result(OldPasswd)  # 对旧密码加密
            UpdatePassword=UserInfo().UpdatePasswd(name=UserName,old_passwd=Md5OldPasswd,new_passwd=Md5NewPasswd)
            if UpdatePassword:
                UserOperationLogRecord(request, request_api="update_password", uid=UserName)#如果修改成功写入数据库中
                return JsonResponse({'message': '好耶！修改成功~', 'code': 200, })
            else:
                return JsonResponse({'message': "输入信息有误重新输入", 'code': 403, })
        except Exception as e:
            ErrorLog().Write("Web_Api_User_UpdatePassword(def)", e)
    else:
        return JsonResponse({'message': '请使用Post请求', 'code': 500, })

"""update_show_name
{
	"token": "xxxxx",
	"new_show_name": "1"
}
"""
def UpdateShowName(request):#更新显示名字
    RequestLogRecord(request, request_api="update_show_name")
    if request.method == "POST":
        try:
            Token=json.loads(request.body)["token"]
            NewShowName= json.loads(request.body)["new_show_name"]
            Uid = UserInfo().QueryUidWithToken(Token)  # 如果登录成功后就来查询UID
            if Uid != None:  # 查到了UID
                UserOperationLogRecord(request, request_api="update_show_name", uid=Uid)  # 查询到了在计入
                UpdateShowNameResult=UserInfo().UpdateShowName(uid=Uid,show_name=NewShowName)#获取值查看是否成功
                if UpdateShowNameResult:
                    return JsonResponse({'message': '好诶！修改成功~', 'code': 200, })
                else:
                    return JsonResponse({'message': "输入信息有误重新输入", 'code': 403, })
        except Exception as e:
            ErrorLog().Write("Web_Api_User_UpdateShowName(def)", e)
    else:
        return JsonResponse({'message': '请使用Post请求', 'code': 500, })

"""update_key
{
	"token": "xxxxx"
}
"""
def UpdateKey(request):#更新Key
    RequestLogRecord(request, request_api="update_key")
    if request.method == "POST":
        try:
            Token=json.loads(request.body)["token"]
            NewKey= randoms().result(40)#生成随机的key,有可能会重复，这边先暂时不管了，这概论太j8低了
            Uid = UserInfo().QueryUidWithToken(Token)  # 如果登录成功后就来查询UID
            if Uid != None:  # 查到了UID
                UserOperationLogRecord(request, request_api="update_key", uid=Uid)  # 查询到了在计入
                UpdateKeyResult=UserInfo().UpdateKey(uid=Uid,key=NewKey)#获取值查看是否成功
                if UpdateKeyResult:
                    return JsonResponse({'message': '呐呐呐呐！修改成功了呢~', 'code': 200, })
                else:
                    return JsonResponse({'message': "输入信息有误重新输入", 'code': 403, })
        except Exception as e:
            ErrorLog().Write("Web_Api_User_UpdateKey(def)", e)
    else:
        return JsonResponse({'message': '请使用Post请求', 'code': 500, })

#还差更新邮箱和更新头像功能

"""user_info
{
	"token": ""
}
"""
def PersonalInformation(request):#用户个人信息
    RequestLogRecord(request, request_api="personal_information")
    if request.method == "POST":
        try:
            Token=json.loads(request.body)["token"]
            Info=UserInfo().QueryUserInfo(Token)
            Uid = UserInfo().QueryUidWithToken(Token)  # 如果登录成功后就来查询用户名
            if Uid!=None: # 查到了UID
                UserOperationLogRecord(request, request_api="personal_information", uid=Uid)
            if Info is None:
                return JsonResponse({'message': '搁着闹呢？', 'code': 404, })
            elif Info != None:
                JsonValues = {}#对数据进行二次处理
                JsonValues["id"] = Info["id"]
                JsonValues["key"] = Info["key"]
                JsonValues["name"] = Info["name"]
                JsonValues["token"] = Info["token"]
                JsonValues["show_name"] = Info["show_name"]
                JsonValues["email"] = Info["email"]
                JsonValues["img_path"] = Info["img_path"]
                return JsonResponse({'message': JsonValues, 'code': 200, })


        except Exception as e:
            ErrorLog().Write("Web_Api_UserInfo_PersonalInformation(def)", e)
    else:
        return JsonResponse({'message': '请使用Post请求', 'code': 500, })
