#coding:utf8
import commands
import socket
#这是颜色的函数
def inBlack(s):
    return highlight('') + "%s[30;2m%s%s[0m"%(chr(27), s, chr(27))
def inRed(s):
    return highlight('') + "%s[31;2m%s%s[0m"%(chr(27), s, chr(27))
def inGreen(s):
    return highlight('') + "%s[32;2m%s%s[0m"%(chr(27), s, chr(27))
def inYellow(s):
    return highlight('') + "%s[33;2m%s%s[0m"%(chr(27), s, chr(27))
def inBlue(s):
    return highlight('') + "%s[34;2m%s%s[0m"%(chr(27), s, chr(27))
def inPurple(s):
    return highlight('') + "%s[35;2m%s%s[0m"%(chr(27), s, chr(27))
def inWhite(s):
    return highlight('') + "%s[37;2m%s%s[0m"%(chr(27), s, chr(27))
def highlight(s):
    return "%s[30;2m%s%s[1m"%(chr(27), s, chr(27))
#########################功能函数###################################
import paramiko,cmd
from sys import argv
import os
#def login():#user登陆注册
def groupname(name):#name=group 返回组名 name=file返回文件名
    for i in os.walk('./conf'):
        if i[0]=='./conf':#只显示根目录是./conf的文件
            a=i
    li_fn=a[2]
    g_li=[]
    if name=='group':
        for i in li_fn:
            if i.endswith('.config'):
                 g_li.append(i[:-7])#分组添加
        return g_li
    elif name=='file':
        for i in li_fn:
            if i.endswith('.config'):
                 g_li.append(i)#分组添加
        return g_li
def addgroup():#修改查看组信息
  while 1:
    g_info=['删除分组','查看分组','添加分组','修改分组','增加主机']
    print ''
    for k,v in enumerate(g_info):
        print k+1,'- ',inRed(v) 
        print ''
    g_what=raw_input(inGreen('Hi,请输入您的选项:'))
    if g_what=='1':
        g_del=raw_input(inGreen('input del name:'))
        c_statu=commands.getstatusoutput('mv ./conf/%s.config ./conf/%s.config.back'%(g_del,g_del))
        if c_statu[0]==0:
            print inRed('Ok,删出成功,conf目录中.back文件可恢复组配置文件')
            print inRed('exit可以返回上级菜单')        
            break
        else:
            print inRed('False,删除失败,请检查用户权限.或者文件是否存在.')
            print inRed('exit可以返回上级菜单')        
            continue
    elif g_what=='2':
        a=groupname('group')#返回组名
        b=groupname('file')
        for i,v in enumerate(a):
            f=''
            ip_list=[]#ip列表
            with open('./conf/%s'%b[i]) as f:
                for fl in f.readlines():
                    if fl:
                        ip_list.append(fl.strip().split()[0])
            s='-'*30
            gg=len(v)/2
            ag= str(i+1)+' '+'-'*(25-gg)+inRed(v)+(len(s)-len(a)+gg)*'-'
            print '\n',ag[:75],'\n'
            for t,ip in enumerate(ip_list):
                print ''.ljust(17),inGreen(t+1),'-',inGreen(ip)
        print ''        
        print inRed('exit可以返回上级菜单')        
        continue        
    elif g_what=='3':
      while 1:
        a_g=raw_input(inGreen('Please enter the name of a group to add:'))
        if len(a_g)==0:continue
        a_statu=commands.getstatusoutput('touch ./conf/%s.config'%a_g)
        if a_statu[0]==0:
            print inGreen('ok 服务组添加成功.')
            print inRed('exit可以返回上级菜单')        
            a=raw_input("\033[5;35;10m请按Enter键继续添加主机,exit返回上一级.\033[0m")
            if a=='exit':
                return
            else:
                add_host('./conf/%s.config'%a_g)
                print inRed('exit可以返回上级菜单')        
                
                break
        else:
            print inRed('False 服务组添加失败,请检查用户权限是否足够.')
            continue
    elif g_what=='4':
        a=groupname('group')
        while 1:
            gw=raw_input(inGreen('Input to modify the group name:'))
            if gw=='exit':break
            if gw not in a:
                print '\n',inRed('sorry,没有这个组名,请重新输入exit可返回上级.'),'\n'
                continue
            gl=['删除主机','修改组名','修改组员信息']
            print ''
            for k,v in enumerate(gl):
                print inRed(k+1),'-',inRed(v),'\n'
            print '\n',inRed('exit 可以返回上级'),'\n'
            gww=raw_input(inGreen('Choose Modify the options:'))
            if gww=='exit':break
            elif gww=='1':
                while 1:
                  try: 
                    g_ip=raw_input(inGreen('Hi,请输入要删除的ip地址:'))
                    ip_li=[]
                    file_c=[]#修改后的列表
                    with open('./conf/%s.config'%gw) as f:
                        for fl in f.readlines():
                            if fl:
                                ip_li.append(fl.strip().split()[0])
                    if g_ip not in ip_li:
                        print inRed('sorry,没有这个IP地址:%s请重新输入'%g_ip)
                        break
                    ip_in=ip_li.index(g_ip)#取得ip的索引值
                    with open('./conf/%s.config'%gw) as f:    
                        file_c=f.readlines()
                        file_c.remove(file_c[ip_in])
                    with open ('./conf/%s.config'%gw,'wb+') as f:
                        f.writelines(file_c)
                        print inRed('success,修改成功,')
                        return 'ok'
                  except ValueError:
                    print 'ip地址不存在,请重新输入'
                    continue
            elif gww=='2':
              while 1:
                g_m=raw_input(inGreen('Hi,您要修改为:'))
                g_statu=commands.getstatusoutput('mv ./conf/%s.config ./conf/%s.config'%(gw,g_m))
                if g_statu[0]==0:
                    print '\n',inRed('Modify the success'),'\n'
                    break
                else:
                    print inRed('False,请检查用户权限,')
                    continue
            elif gww=='3':
              while 1:  
                g_ip=raw_input(inGreen('Hi,请输入要修改的ip地址:'))
                ip_li=[]
                file_c=[]#修改后的列表
                with open('./conf/%s.config'%gw) as f:
                    for fl in f.readlines():
                        if fl:
                            ip_li.append(fl.strip().split()[0])
                if g_ip not in ip_li:
                    print inRed('sorry,没有这个IP地址:%s请重新输入'%g_ip)
                    break
                ip_in=ip_li.index(g_ip)#取得ip的索引值
                with open('./conf/%s.config'%gw) as f:    
                    file_c=f.readlines()
                    file_c.remove(file_c[ip_in])
                with open ('./conf/%s.config'%gw,'wb+') as f:
                    f.writelines(file_c)
                add_host('./conf/%s.config'%gw)    
                break
            else:
                print inRed('sorry,您只能输入1-3的数字.')
                continue
    elif g_what=='exit':
        break
    elif g_what=='5':
     a=groupname('group')
     while 1:
         print '\n',inRed('exit可以返回上级菜单.'),'\n' 
         gw=raw_input(inGreen('Input to modify the group name:'))
         if gw=='exit':
            break
         elif gw not in a:
            print inRed('sorry,没有这个组名,请重新输入.')
            continue
         add_host('./conf/%s.config'%gw)
        
    else:

        print inRed('sorry,您只能输入1-5的数字.')
        
        print '\n',inRed('exit可以返回上级菜单'),'\n'        

def add_host(config):#添加主机参数是主机配置文件
    i=0#标记
    while 1:
        #判断IP地址是否合法        
      if i!=1:
        try:
            print '\n',inRed('Notice:exit可以返回上级菜单.'),'\n'
            ip = raw_input(inGreen("Enter IP Address: "))    
            if ip=='exit':break
            a=ip.split('.')[0]          #判断第一个是否为0 
            if (0 < int(a)):            #判断第一个是否为0
                if ( 0 < ip[0] ):
                    if len([i for i in ip.split('.') if ( 0 <= int(i) <= 255 ) and ( type(i) is str )])==4:
                        print ip
                        i=1  
                    else:
                        print inRed("number <= 255")
                        continue
            else:
                print inRed("not 0.x.x.x")
                continue
        except ValueError,e:
            print inRed("please enter the number") 
            continue
            
      user=raw_input(inPurple('user>>')).strip()
      if user.isdigit() or len(user)==0:
          print inRed('Sorry,用户名不能为空.或者是全数字,请重新输入用户名')
          continue
      passwd=raw_input(inPurple('passwd>>')).strip()

      port=raw_input(inPurple('port>>')).strip()
      if not port.isdigit():
          print inRed('sorry,port类型只能是数字')
          continue
      info='''
        ip:%s
        user:%s
        passwd:%s
        port:%s
            '''%(ip,user,passwd,port)
            
      print inRed(info)
      while 1:
          confirm=raw_input(inPurple('hi,请确认以上信息是否正确(y/n):'))
          if confirm=='Y' or confirm=='y':
              with open(config,'ab+') as f:
                 h_li=[]
                 for i in f.readlines():
                    h_li.append(i.strip().split()[0])
                 if ip not in h_li:
                    f.writelines('%s\t%s\t%s\t%s\n'%(ip,user,passwd,port))   
                    print '\n',inRed('add host successful'),'\n'
                    ex=raw_input(inGreen('hello,你是否要继续添加主机服务器(任意键继续,n返回上级):'))
                    if ex=='n' or 'N':
                        return True
                    else:   
                        add_host(config)
                 else:
                     print '\n',inRed('Error,主机%s已经存在,请重新输入,exit可以返回上一级.'%ip),'\n'   
                     break
          elif confirm=='N' or confirm=='n':
              print inRed('Ok,请重新输入主机信息,exit可以返回上级菜单')
              add_host(config)  
          else:
             print inRed('Sorry,没有这个选项.')
             continue
        
