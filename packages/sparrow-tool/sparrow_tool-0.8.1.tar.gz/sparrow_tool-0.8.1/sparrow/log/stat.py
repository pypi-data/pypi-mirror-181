import pynvml
import time


class GpuStat:
    def __init__(self):
        pynvml.nvmlInit()

    def stop(self):
        pynvml.nvmlShutdown()

    def start_stat(self, interval=1, log=None):
        # 在线程中执行
        while True:
            time.sleep(interval)
            if log:
                log.debug(self.gpu_stat())
            else:
                print(self.gpu_stat())

    def gpu_stat(self):
        # https://pypi.org/project/nvidia-ml-py/
        gpu_num = pynvml.nvmlDeviceGetCount()
        gpu_version = pynvml.nvmlSystemGetDriverVersion()
        result = {}
        for i in range(gpu_num):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            total_memory = info.total / 1024 ** 2
            used_memory = info.used / 1024 ** 2
            free_memory = total_memory - used_memory
            # print(f"Device {i} : {pynvml.nvmlDeviceGetName(handle)}")
            # print(f"gpu num: {i}, total: {total_memory}Mb, used: {used_memory}mb free: {free_memory}Mb \n")
            # 获取显卡的工作模式，0 为 WDDM 模式、1 为 TCC 模式
            # WDDM 模式：GPU 负责计算以及图像显示，打游戏显然是 WDDM 模式
            # TCC 模式：GPU 只负责计算，不负责图像显示，机器学习的时候一般是 TCC 模式
            # print(pynvml.nvmlDeviceGetDriverModel(handle))  # [0, 0]
            """
            # 可以设置显卡工作模式，如果报如下错误
            # pynvml.NVMLError_NoPermission: Insufficient Permissions
            # 那么以管理员的身份打开命令行，然后执行
            pynvml.nvmlDeviceSetDriverModel(handle, 1)
            # 当然，如果显卡不是 Tesla 和 Quadro，那么不支持设置工作模式，此时会抛出如下错误：
            # pynvml.NVMLError_NotSupported: Not Supported
            """
            # fans = pynvml.nvmlDeviceGetFanSpeed(handle)
            temperature = pynvml.nvmlDeviceGetTemperature(handle, i)
            powerstate = pynvml.nvmlDeviceGetPowerState(handle)
            # gpu计算核心使用率
            gpu_rate = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            # gpu内存使用率
            memory_rate = pynvml.nvmlDeviceGetUtilizationRates(handle).memory

            pid_info_list = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
            # print(temperature, powerstate, gpu_rate, memory_rate)
            for pid_info in pid_info_list:
                # pid_info.pid: 此进程的pid，再基于 psutil.Process 可以得到更详细的信息
                # pid_info.usedGpuMemory: 此进程使用的显存大小
                ...

            info = {"gpu_rate": gpu_rate,
                    "temperature": temperature,
                    "used_memory": used_memory,
                    "free_memory": free_memory,
                    "total_memory": total_memory,
                    }
            result[i] = info
        return result


if __name__ == "__main__":
    gst = GpuStat()
    print(gst.gpu_stat())
    gst.stop()
    # method 2 使用gpustat库
    # from sparrow.cli.core import command, commandexists
    # print(command(["gpustat", "--no-color"]))
