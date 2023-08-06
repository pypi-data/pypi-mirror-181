import os
from twisted.internet import task
from scrapy.exceptions import NotConfigured
from scrapy import signals
import socket
from prometheus_client import Gauge, CollectorRegistry, push_to_gateway


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


class ScrapyPrometheusPush:
    """上传stats数据到Prometheus"""

    def __init__(self, stats, push_gateway_url,metrics_name, job_name, push_timeout):
        self.stats = stats
        self.interval = 15
        self.task = None
        self.conn = None
        self.grouping_key = {"host": extract_ip()}
        self.push_gateway_url = push_gateway_url
        self.job_name = job_name
        self.push_timeout = push_timeout
        self.metrics_name = metrics_name
        self.registry = CollectorRegistry(auto_describe=True)
        self.items_gau = Gauge(self.metrics_name + "_items", "结果数量", ["spider"], registry=self.registry)
        self.pages_gau = Gauge(self.metrics_name+"_pages", "返回页面数",  ["spider"], registry=self.registry)
        self.exception_gau = Gauge(self.metrics_name+"_exception_count", "下载异常数",  ["spider"], registry=self.registry)
        self.retry_gau = Gauge(self.metrics_name+"_retry", "重试次数",  ["spider"], registry=self.registry)
        self.exception_type_gau = Gauge(self.metrics_name + "_exception_type_count", "下载异常类型分别统计",
                               ["spider", 'exception_type'],
                               registry=self.registry)
        self.status_code_gau = Gauge(self.metrics_name + "_status_code", "...", ["spider", 'status_code'],
                                     registry=self.registry)
        self.spider_exception_type_gau = Gauge(self.metrics_name + "_spider_type_count", "爬虫代码逻辑异常统计",
                                               ["spider", 'spider_exceptions'],
                                               registry=self.registry)
    @classmethod
    def from_crawler(cls, crawler):
        push_gateway_url = crawler.settings.get("SCRAPROM_PUSHGATEWAY_URL",'127.0.0.1:10002')
        job_name = crawler.settings.get("SCRAPROM_JOB_NAME", "scrapy_pro")
        push_timeout = crawler.settings.get("SCRAPROM_PUSH_TIMEOUT", 3)
        metrics_name = crawler.settings.get("SCRAPROM_METRICS_BASE", 'scrapy_pro')
        if not push_gateway_url:
            raise NotConfigured
        o = cls(crawler.stats, push_gateway_url,metrics_name, job_name, push_timeout)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self,spider ):
        self.pagesprev = 0
        self.itemsprev = 0
        self.excepprev = 0
        self.retryprev = 0
        self.exception_type_prev = {}
        self.spider_exception_type_prev = {}
        self.status_code_prev = {}
        self.task = task.LoopingCall(self.update_stats, spider)
        self.task.start(self.interval)

    def spider_closed(self):
        if self.task and self.task.running:
            self.task.stop()

    def exception_type_count(self,spider):
        exception_type = {}
        for key, value in self.stats.get_stats().items():
            sort_key = key.split("/")[-1]
            if "downloader/exception_type_count" in key:
                exception_type[sort_key] = value
        for key, value in exception_type.items():
            e_t_rate = value - self.exception_type_prev.get(key, 0)
            self.exception_type_gau.labels(spider=spider.name, exception_type=key).set(e_t_rate)
            self.exception_type_prev[key] = value

    def status_code_count(self,spider):
        status_code = {}
        for key, value in self.stats.get_stats().items():
            sort_key = key.split("/")[-1]
            if "downloader/response_status_count" in key:
                status_code[sort_key] = value
        for key, value in status_code.items():
            s_t_rate = value - self.status_code_prev.get(key, 0)
            self.status_code_gau.labels(spider=spider.name, status_code=key).set(s_t_rate)
            self.status_code_prev[key] = value

    def spider_exception_type(self,spider):
        spider_exception_type = {}
        for key, value in self.stats.get_stats().items():
            sort_key = key.split("/")[-1]
            if "spider_exceptions/" in key:
                spider_exception_type[sort_key] = value
        for key, value in spider_exception_type.items():
            s_e_t_rate = value - self.spider_exception_type_prev.get(key, 0)

            self.spider_exception_type_gau.labels(spider=spider.name, spider_exceptions=key).set(s_e_t_rate)
            self.spider_exception_type_prev[key] = value

    def update_stats(self,spider):

        # item数
        items = self.stats.get_value('item_scraped_count', 0)
        irate = items - self.itemsprev
        self.items_gau.labels(spider=spider.name).set(irate)

        # page数
        pages = self.stats.get_value('response_received_count', 0)
        prate = pages - self.pagesprev
        self.pages_gau.labels(spider=spider.name).set(prate)

        # 下载异常
        exception_count = self.stats.get_value('downloader/exception_count', 0)
        erate = exception_count - self.excepprev
        self.exception_gau.labels(spider=spider.name).set(erate)

        # 重试次数
        retrys = self.stats.get_value("retry/count", 0)
        rrate = retrys - self.retryprev
        self.retry_gau.labels(spider=spider.name).set(rrate)

        # 异常类型
        self.exception_type_count(spider,)
        # 状态码
        self.status_code_count(spider,)
        # 爬虫异常类型
        self.spider_exception_type(spider, )
        push_to_gateway(self.push_gateway_url, job=self.job_name, registry=self.registry, timeout=self.push_timeout,
                        grouping_key=self.grouping_key)

        self.pagesprev, self.itemsprev, self.excepprev, self.retryprev = pages, items, exception_count, retrys

