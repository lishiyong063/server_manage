#coding:utf8
#Author vincent
#CreatBy:2014/7/23
from config import inRed,inGreen,inYellow,inBlue,addgroup,groupname
import sys,os,time
import paramiko,socket
import multiprocessing
def cmd_exec(*cmd):#批量执行命令脚本的函数
    try:
        s=paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(cmd[0],int(cmd[3]),cmd[1],cmd[2])
        stdin,stdout,stderr = s.exec_command(cmd[4]) #执行命令
        cmd_result = stderr.read(),stdout.read()
        for line in cmd_result:
          if line and cmd[4].startswith('ls'):
            re=0  
            print inBlue('############################IP:%s###########################'%cmd[0])
            li=line.split()
            for l in range(len(li)/3+1):
                if  len(li[re:re+3]) == 3 :
                    print li[re].ljust(30),li[re+1].ljust(30),li[re+2].ljust(30)
                elif len(li[re:re+3])==2:
                    print li[re].ljust(30),li[re+1].ljust(30)
                elif len(li[re:re+3])==1:
                    print li[re].ljust(30)
                else:break    
                re=re+3
          else:
              if line:
                  print inBlue('############################IP:%s###########################'%cmd[0])
                  print line 
        s.close()
    except:
        print cmd[0],'timeout'
def file_muliti(*cmd):#文件分发的函数
    try:
        print cmd[0],'transfer............'
        scp=paramiko.Transport((cmd[0],int(cmd[3])))
        scp.connect(username=cmd[1],password=cmd[2])
        sftp = paramiko.SFTPClient.from_transport(scp)
        sftp.put(cmd[4],cmd[5])
        scp.close()
    except IOError:
        print cmd[0],inRed('Error,没有这个文件,请返回上级菜单.批量执行mkdir -p tmp')
    except Exception, e:
        import traceback
        traceback.print_exc()
        print 'erro'
        try:
            scp.close()
        except:
            pass
try:
    ad_pa=sys.argv[1] 
except:
    print '\n',inRed('sorry 请输入正确的格式运行该系统 eg:python main.py password'),'\n'
    sys.exit()
try:    
    wel_info='welcome 欢迎来到批量管理系统...'
    print '\n',inGreen(wel_info),'\n'
    opr_li=['服务组管理','批量执行','文件分发','退出系统']
    while True:
        print ''
        for k,v in enumerate(opr_li):
            print inRed(k+1),'- ',inRed(v),'\n'
        w_opr=raw_input(inGreen('please input your opration:')).strip()
        print ''
        if w_opr=='1':
            addgroup()
        elif w_opr=='2':
            while 1:
                confr=raw_input(inGreen('hi,请输入操作的组名:')).strip()
                if confr=='exit':
                    break
                ga=groupname('group')  #得到存在的组名列表
                if confr not in ga:
                    print '\n',inRed('sorry,没有这个组名,请重新输入exit可返回上级菜单.'),'\n'
                    continue
                conf='./conf/%s.config'%confr
                hosts=[] #存主机信息
                for i in open(conf): ##zhijie dakai
                    i = i.strip()
                    if i:
                        ip,username,password,port = i.split()[:4]
                        hosts.append((ip,username,password,port))#添加元组信息
                while 1:        
                    what=raw_input(inGreen('ssh>>'))
                    if what=='exit':
                        break
                    elif len(what)==0:continue    
                    result = []
                    p = multiprocessing.Pool(processes=20)
                    for i in hosts:
                        h=list(i)
                        h.append(what)
                        result.append(p.apply_async(cmd_exec,(tuple(h))))#异步执行
                    p.close()
                    for res in result:
                       try: 
                          res.get(timeout=30)#需要用到get取值
                       except:
                          print inRed('timeout')  
                    print '\n',inRed('exit可以返回上级操作.'),'\n'      
        elif w_opr=='3':
            while 1:
                confr=raw_input(inGreen('hi,请输入操作的组名:')).strip()
                if confr=='exit':break
                ga=groupname('group')  #得到存在的组名列表
                if confr not in ga:
                    print inRed('sorry,没有这个组名,请重新输入.exit可返回上级菜单.')
                    continue
                conf='./conf/%s.config'%confr
                hosts=[] #存主机信息
                for i in open(conf): ##zhijie dakai
                    i = i.strip()
                    if i:
                        ip,username,password,port = i.split()[:4]
                        hosts.append((ip,username,password,port))#添加元组信息
                while 1:        
                    print '\n',inRed('exit 可以返回到上级目录,ls可以查看可上传的文件.'),'\n'
                    what=raw_input(inGreen('hi,请输入要分发的文件名:'))
                    if os.path.exists(what) and what != 'ls':
                        for i in hosts:
                            h=list(i)
                            h.append(what)
                            h.append('/home/%s/tmp/%s'%(i[1],what))
                            result = []
                            p = multiprocessing.Pool(processes=4)
                            result.append(p.apply_async(file_muliti,(tuple(h))))#异步模式
                        for res in result:
                            res.get()
                    elif what=='ls':
                        os.system('ls')
                        continue
                    elif what=='exit':
                        break
                    else:
                         print '\n',inRed('exit可返回上级菜单.没有这个文件请重新输入:'),'\n'
                         continue
        elif w_opr=='4' or w_opr=='exit':
            sys.exit()
        else:
            print '\n',inRed('ERROR：你只能输入1-3的数字.请重新输入!'),'\n'
            continue
except UnboundLocalError:
    print '\n',inRed('ERROR,请确认conf 目录是否存在.若不存在请运行mkdir conf'),'\n'
