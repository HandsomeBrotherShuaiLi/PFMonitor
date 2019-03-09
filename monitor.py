import psutil,os,time,datetime
class Monitor(object):
    def __init__(self,api_key,model_path,pid):
        """

        :param api_key: pushbullet.py api key for your cross-platform socket access
        :param model_path:the model folder path
        :param pid: the process id which you wanna monitor
        """
        self.model_path=model_path
        self.api_key=api_key
        self.pid=pid
    def get_model_status(self,model_path,time_now):
        """
        check models under this model_path model
        :param model_path: the model folder which you want to monitor
        :param now_time:
        :return:
        """
        model_list = os.listdir(model_path)
        model = [float(i.strip('.hdf5').split('--')[-1]) for i in model_list]
        min_model_loss = min(model)
        min_index = model.index(min_model_loss)
        return str(time_now) + '\n\n此时一共有{}个训练好的模型:\n'.format(len(model_list)) + \
               '\n\n'.join(model_list) + \
               '\n\n综上，最好是第{}个epoch的模型,val_loss是{}\n\n'.format(min_index + 1, str(min_model_loss))
    def get_process_status(self,pid):
        """
            process id
            this function is to check the python exe is running or not,and returns some key status information
            :param pid: process id, which you can query by 'Ctrl+Alt+del' in windows system
            :return:
            """
        try:
            p = psutil.Process(pid)
        except Exception as e:
            return e
        p_name = p.name()
        p_status = p.status()
        p_cpu = p.cpu_percent()
        p_mem = p.memory_percent()
        p_threads = p.num_threads()
        p_create_times = datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")
        if p_status == 'running':
            try:
                p_cwd = p.cwd()
                p_exe = p.exe()
                return '{}进程,状态是{},进程创建时间是{}\n该进程下的线程个数是{}\n项目path是 {}\npython解释器的path是 {}\n\n汇报完毕!\n\n'.format(
                    p_name, p_status, p_create_times, p_threads, p_cwd, p_exe
                ), 'running'
            except:
                return '{}进程,状态是{},进程创建时间是{},cpu使用率是{}\n内存使用率是{},该进程下的线程个数是{}\n 汇报完毕!'.format(
                    p_name, p_status, p_create_times, p_cpu, p_mem, p_threads
                ), 'running'
        else:
            return '', 'fail'
    def monitor(self):
        current_model_list = os.listdir(self.model_path)
        from pushbullet import PushBullet
        pb = PushBullet(api_key=self.api_key)
        res1 = self.get_model_status(self.model_path, time.ctime())
        res2, status = self.get_process_status(self.pid)
        pb.push_note(title='神经网络进程运行情况监视器 made by 李帅', body=res1 + res2)
        while True:
            now_model_list = os.listdir(self.model_path)
            if now_model_list == current_model_list:
                res2, status = self.get_process_status(self.pid)
                if status == 'fail':
                    pb.push_note(title='神经网络进程运行情况监视器 made by 李帅', body='运行结束或者异常，请检查电脑运行情况!!!!!!!')
                    break
                else:
                    pass
            else:
                res1 = self.get_model_status(self.model_path, time.ctime())
                res2, status = self.get_process_status(self.pid)
                current_model_list = now_model_list
                if status == 'fail':
                    pb.push_note(title='神经网络进程运行情况监视器 made by 李帅', body='运行结束或者异常，请检查电脑运行情况!!!!!!!')
                    break
                else:
                    pb.push_note(title='神经网络进程运行情况监视器 made by 李帅', body=res1 + res2)

if __name__=='__main__':
    monitor=Monitor(
        api_key='***********',
        model_path='***********',
        pid=666# int number not string
    )
    monitor.monitor()



