#!/usr/bin/env python
# _*_ coding: utf-8 _*_
from OA.Seeyou import Seeyou
from OA.Weaver import Weaver
from OA.Ruvar import Ruvar
def Main(Url,FileName,Values,ProxyIp):
    try:
        Seeyou.Main(Url, FileName, Values, ProxyIp)
        Weaver.Main(Url,FileName,Values,ProxyIp)
        Ruvar.Main(Url,FileName,Values,ProxyIp)
    except:
        pass