"""seo刷量node"""

import time
import zipfile
import requests
import threading
import utils
import nodeconfig
from selenium import webdriver


REUQESTS = "requests"
SELENIUM = "selenium"

def set_auth(user, pwd):
    """
    设置用户名密码dict
    :param user: 用户名
    :param pwd: 密码
    :return: auth dict
    """
    auth = {}
    auth["user"] = user
    auth["pwd"] = pwd
    return auth

def set_proxies(proxy, auth=None):
    """
    http代理格式化处理
    无验证的代理 ip:port
    需要验证的代理 username:password@ip:port
    :param proxy: 传入的代理
    :param auth: 代理验证的用户名密码dict
    :return: proxies
    """
    proxies = {
            "http": "http://%(ip)s/" % {"ip": proxy,},
            "https": "https://%(ip)s/" % {"ip": proxy,}
        }
    if auth:
        proxies = {
            "http": "http://%(user)s:%(pwd)s@%(ip)s/" % {'user': auth["user"], 'pwd': auth["pwd"], "ip": proxy,},
            "https": "https://%(user)s:%(pwd)s@%(ip)s/" % {'user': auth["user"], 'pwd': auth["pwd"], "ip": proxy,}
        }
    return proxies

class ParamsException(Exception):
    pass

class ParamsError(ParamsException):
    pass

class Requests:
    def __init__(self, timeout):
        self.timeout = timeout
        self.__name = REUQESTS

    @property
    def name(self):
        return __name

    #@utils.spend_time
    def process(self, url, proxy, auth, headers=None):
        # 如果不需要验证auth可以传递None值
        proxies = set_proxies(proxy, auth)
        try:
            res = requests.get(url, proxies=proxies, headers=nodeconfig.HEADERS_DEFAULT, timeout=self.timeout)
            print(url, res.status_code)
        except Exception as e:
            raise e
            time.sleep(0.5)
            return self.process(url, proxy, auth)
        if headers:
            try:
                res = requests.get(url, proxies=proxies, headers=headers, timeout=self.timeout)
                print(res.text)
            except Exception as e:
                raise e
                time.sleep(0.5)
                return self.process(url, proxy, auth)
        return None

class Selenium:
    def __init__(self, timeout):
        self.timeout = timeout
        self.__name = SELENIUM

    @property
    def name(self):
        return __name

    @staticmethod
    def set_webdirver_proxy_auth(proxy, auth, user_agent=None):
        """
        selenium chrome没有HTTP Basic Authentication的验证方式, 可以通过设置chrome plugin的方式
        参考 https://stackoverflow.com/questions/9888323/how-to-override-basic-authentication-in-selenium2-with-java-using-chrome-driver
        :param proxy: 要设置的代理
        :param auth: 代理的用户名密码dict
        :param user_agent: chrome的header头
        :return dirver:
        """
        proxy_host, proxy_port = proxy.split(":")
        username = auth["user"]
        password = auth["pwd"]

        # 动态生成chrome代理插件代码，再使用zipfile模块打包，最后使用chrome_options.add_extension加载插件
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """
        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http", /*如果使用的是socks代理，这个值改为"socks"即可*/
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy_host, proxy_port, username, password)

        # 设置chrome_webdirver 插件
        chrome_options = webdriver.ChromeOptions()
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Chrome(
            # os.path.join(path, 'chromedriver'),
            chrome_options=chrome_options)
        return driver        

    @utils.spend_time
    def process(self, url, proxy, proxy_auth=False, auth=None):
        """
        发送请求
        :param url: 请求的url
        :param proxy: 使用的代理
        :param proxy_auth: 是否开启代理验证,默认不验证
        :param auth: 代理验证的用户名密码dict
        ：return:
        """
        if proxy_auth:
            # 如果要验证
            try:
                driver = Selenium.set_webdirver_proxy_auth(proxy, auth)
                driver.set_page_load_timeout(self.timeout)
                driver.get(url)
                print(dirver.page_source)
            except Exception as e:
                # 异常暂停0.2s，进行回调
                raise e
                time.sleep(0.5)
                return self.process(url, proxy, auth, proxy_auth=True)
            finally:
                driver.quit()
                return
        
        # 代理不验证
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % proxy) 
            #chrome_options.add_argument('--headless') # 无界面启动
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.timeout)
            driver.get(url)
            print(dirver.page_source)
        except Exception as e:
            raise e
            time.sleep(0.5)
            return self.process(url, proxy, auth)            
        finally:
            driver.quit()
            return


class ReqThead(threading.Thread):
    def __init__(self):
        self.__count = 3

    @property
    def count(self):
        return __count

    def run(self):pass



@utils.spend_time
def ts():
    que = utils.ts()
    ts = Requests(5)
    proxy = "tps136.kdlapi.com:15818"
    auth = set_auth("t17075944217654", "5nr6svkc")
    #while not que.empty():
    while True:
        url = que.get()
        if que.empty():
            break
        for i in range(5):
            #ts.process(url, proxy, auth)
            t = threading.Thread(target=ts.process, args=(url, proxy, auth))
            t.start()
            time.sleep(0.2)


if __name__ == "__main__":
    #proxy = "tps136.kdlapi.com:15818"
    #auth = set_auth("t17075944217654", "5nr6svkc")
    #ts = Requests(5)
    #ts.process("http://dev.kuaidaili.com/testproxy", proxy, auth)
    #ts = Selenium(5)
    #ts.process(url="http://dev.kuaidaili.com/testproxy", proxy=proxy)
    print(dir(ReqThead.start))