import asyncio
import traceback
import Utils_DP
import time
from concurrent.futures import ThreadPoolExecutor
import threading
from logger import log_info, log_debug, log_warning, log_error  # 新增logger导入
from config import AppConfig

def fill_form(task_id):
    # 启动一个新的浏览器实例
    # print("=" * 30)
    # print(f"当前任务ID:{task_id}")
    log_info(f"当前任务ID:{task_id}")  # 使用log_info代替print
    try:
        yun = Utils_DP.browerUtils(log=True, rate=0.08)
        log_debug("创建对象完毕")  # 使用log_debug代替print
        # 打开页面失败
        if not yun.ws:
            # print("获取ws连接失败")
            log_error("获取ws连接失败")
            return
        # if not yun.connect(task_id,"https://c.adsco.re/r#apikey=QsVLAwAAAAAAcjHL6IB2vdj15VOkOsvpReSVVxc&sub_id=123456&type=3&data=AAJhtSfT_D4xoIIyyzKJaAfGL7kYhdEWnt1FrhGS7hW_MyijFepp55oHUgVZ66sXCIvFvgbQUkAGxK8KeBMlt0x19U-GfAN3nMf_g1ZjYCytQA"):
        #     return
        if not yun.connect(task_id, all_config["OpenUrl"]["url"]):  # 填写你的URL
            return
    except Exception as e:
        log_error(f"初始化失败: {e}")  # 使用log_error代替print
        traceback.print_exc()
        if yun and yun.browser:
            yun.browser.quit()
        yun.deleteBrower()
        return
    time.sleep(20)

    current_url = yun.page.url  # 获取当前标签页的 URL
    log_info(f"task_id:{task_id} 跳转到页面URL: {current_url}")

    page_title = yun.page.title  # 获取当前页面的标题
    log_info(f"task_id:{task_id} 跳转后的页面标题: {page_title}")
    
    if all_config["Operation"]["isdelete"]:
        yun.deleteBrower()  

    if all_config["Operation"]["isquit"]:
        yun.browser.quit()
    return
  

def task(worker_id):
    """每个任务的具体逻辑"""
    log_info(f"Worker-{worker_id} 执行任务")  # 使用log_info代替print
    start_time = time.time()
    try:
        fill_form(worker_id)
    except Exception as e:
        log_error(f"线程报错: {e}")  # 使用log_error代替print
    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time  # 总耗时（秒）
    log_info(f"任务耗时：{elapsed_time} 秒")  # 使用log_info代替print
    time.sleep(1)  # 模拟耗时
    return worker_id

def resubmit_task(executor, task_id):
    """任务完成后重新提交新任务"""
    future = executor.submit(task, task_id)
    future.add_done_callback(lambda _: resubmit_task(executor, task_id + 1))
def run_forever(num_workers=3):
    """启动无限运行的线程池"""
    # 创建线程池（3个线程）
    log_info("创建线程池")
    log_info(f"当前线程数：{num_workers}")
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # 初始提交3个任务（每个任务完成后会触发新任务）
        for i in range(3):
            resubmit_task(executor, i)

        # 防止主线程退出
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            # print("程序终止")
            log_info("程序终止")

if __name__ == '__main__':
    # 使用示例（可自由修改线程数）

    # 初始化配置读取类
    config = AppConfig('config.ini')  # 替换为实际文件路径
    
    # 如果配置文件不存在，加载默认配置
    if not config.config.read('config.ini'):
        config.load_default_config()

    # 获取所有配置并打印
    all_config = config.get_all_config()

    run_forever(num_workers=1)  # 单线程运行
    # print("线程结束")
    log_info("线程结束")  # 使用log_info代替print
    # run_infinite_tasks(num_workers=5)  # 5线程运行









