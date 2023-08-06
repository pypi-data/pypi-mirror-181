import os
import subprocess
import time


def execute_command_with_no_out(cmd, timeout):
    """
    执行shell命令
    :param cmd: shell命令
    :return: 执行结果和错误消息
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    # 使用wait，设置超时时间，超时后触发TimeoutExpired异常
    try:
        p.wait(timeout=timeout)
        if p.poll:
            # 执行结果，communicate返回一个元组，如果执行成功，errs为空
            outs, errs = p.communicate()
            print(errs)
            print(outs)
    except subprocess.TimeoutExpired as e:
        print('执行超时')
        p.kill()


#程序执行终止时间为当前时刻延迟15秒
stoptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+1))
def run_adbshell():
    p = subprocess.Popen('ls', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while True:
        line=p.stdout.readline().strip()
        print(line)
        #当前时间
        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if curtime>=stoptime:
            #终止子进程
            p.terminate()
            #等待子进程终止后跳出while循环
            if subprocess.Popen.poll(p) is not None:
                break
            else:
                print(u'等待subprocess子进程终止。')
    print(u'完成')

if __name__ == '__main__':
    # execute_command_with_no_out(['cd D:', 'cd ..'], 5)
    # run_adbshell()
    # status, output = subprocess.getstatusoutput("cd ..")
    # print(status)
    # print(output)
    # status, output = subprocess.getstatusoutput("ls")
    # print(status)
    # print(output)
    def get_my_key(obj):
        return obj['name']


    my_list = [{'name': "foo", 'size': 5}, {'name': "bar", 'size': 3}, {'name': "baz", 'size': 7}]
    my_list.sort(key=get_my_key, reverse=False)
    print(my_list)
