# DNSを取得するクラス by @y9k8i 2020
import csv
import logging
import os.path
import sys

from bs4 import BeautifulSoup
import pkgutil
if(pkgutil.find_loader('chromedriver_binary') is not None):
    import chromedriver_binary as chrome  # noqa: F401
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class DNSGetter:

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

    def launch_browser(self):
        """ブラウザを起動する"""
        if not hasattr(self, 'driver'):
            self.logger.info("ChromeDriverを起動します")
            options = Options()
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
            if not self.debug:
                options.add_argument('--headless')
            self.driver = webdriver.Chrome(
                DNSGetter.resource_path('chromedriver.exe'),
                options=options)
            self.wait = WebDriverWait(self.driver, 30)
            self.logger.info("ChromeDriverが起動しました")

    def wait_for_browser_validate(self):
        """リクエスト発行後ブラウザの検証が終わるまで待機"""
        self.wait.until(EC.presence_of_all_elements_located)

        class location_to_be_change(object):
            """指定したURL以外になるまで待つカスタム待機条件 アンカー以降は無視"""

            def __init__(self, url):
                self.url = url

            def __call__(self, driver):
                if driver.current_url.split('#')[0] != self.url:
                    return True
                else:
                    return False

        try:
            self.logger.debug("ページ遷移を待ちます")
            err_elements = self.driver.find_elements_by_id('error')
            if len(err_elements) > 0:
                if err_elements[0].text \
                        == "Please wait while we validate your browser.":
                    self.logger.info("サーバ側でブラウザを検証中...")
                    self.wait.until(
                        location_to_be_change("https://bgp.he.net/cc"))
                    self.wait.until(EC.presence_of_all_elements_located)
                elif len(self.driver.find_elements_by_id('tab_error')) > 0:
                    raise Exception(err_elements[0]
                                    .get_attribute("textContent")
                                    .split('.')[0].strip() + '.'
                                    )
            else:
                err_elements = self.driver.find_elements_by_tag_name('h2')
                if len(err_elements) > 0:
                    raise Exception(err_elements[0].text)
            del err_elements
        except TimeoutException:
            raise TimeoutException("時間切れ")

    def get_domain_name(self, query) -> str:
        """検索文字列からドメイン名を検出し返す"""
        print(query + "のドメイン名を取得中...")
        self.launch_browser()
        self.logger.info(f"{query}のドメイン名を検索中...")
        page_url = f"https://www.google.com/search?q={query}"
        self.driver.get(page_url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        domain_name = soup.select_one(".iUh30")
        title = soup.select_one(".LC20lb")
        self.logger.info(f"ページ名「{title.text}」, 検索結果「{domain_name.text}」")
        if '›' in domain_name.text:
            raise Exception("検索結果がトップページではありません")
        return domain_name.text if domain_name is not None else ""

    def get_network_address(self, domain_name) -> str:
        """ドメイン名からネットワークアドレスを検出し返す"""
        print(domain_name + "のネットワークアドレスを取得中...")
        self.launch_browser()
        self.logger.info(f"{domain_name}のネットワークアドレスを取得中...")
        page_url = f"https://bgp.he.net/dns/{domain_name}#_ipinfo"
        self.driver.get(page_url)
        self.wait_for_browser_validate()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        addr = soup.select_one("#ipinfo > a:nth-child(2)")
        return addr.text if addr is not None else ""

    def get_DNS(self, arg, opt) -> str:
        """
        ネットワークアドレスからDNSレコードを取得し保存する 保存したファイル名を返す

            IPアドレスの場合:
            arg:CIDR表記のネットワークアドレス, opt:addr
            DOMを保存したファイルの場合:
            arg:ファイル名（CIDR表記又は`0_0_0_0`形式のネットワークアドレス+.html）, opt:file
        """
        if opt == "addr":
            filename = DNSGetter.resource_path(f"table/table_{arg.split('/')[0].replace('.', '_')}.csv")
            if os.path.exists(filename) and not self.update:
                self.logger.info(f"{filename}が存在するため再利用します")
                return filename
            print(arg + "のDNSレコードを取得中...")
            self.launch_browser()
            self.logger.info(f"{arg}のDNSレコードを取得中...")
            page_url = f"https://bgp.he.net/net/{arg}#_dns"
            self.driver.get(page_url)
            self.wait_for_browser_validate()
            self.wait.until(EC.visibility_of_element_located((By.ID, "dns")))
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
        elif opt == "file":
            filename = arg.rsplit('.', 1)[0] + ".csv"
            if os.path.exists(filename) and not self.update:
                self.logger.info(f"{filename}が存在するため再利用します")
                return filename
            with open(arg) as f:
                soup = BeautifulSoup(f.read(), "html.parser")
        else:
            self.logger.error("get_DNS(): データのタイプが指定されていません")

        rows = soup.select("#dns tr")

        # ファイルに保存
        self.logger.info("取得したDNSレコードを保存中...")
        with open(filename, "w", encoding='utf-8', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow(["IP", "hostname"])
            for row in rows[1:]:
                csvRow = []
                for cell in row.select("td")[:2]:
                    csvRow.append(cell.text)
                writer.writerow(csvRow)
        self.logger.info(f"{filename}に保存しました")
        return filename

    def __init__(self, debug=False, update=False, logger=None):
        self.debug = debug
        self.update = update
        self.logger = logger or logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.logger.debug("DNSGetterのインスタンスが生成されました")

    def __del__(self):
        self.logger.debug("DNSGetterのインスタンスが破棄されます")
        if hasattr(self, 'driver'):
            self.logger.info("ChromeDriverを終了します")
            self.driver.quit()


# 直接実行された場合
if __name__ == "__main__":
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    dnsGetter = DNSGetter()
    if len(sys.argv) == 2:
        try:
            if sys.argv[1].replace('.', '').isdecimal():
                dnsGetter.get_DNS(sys.argv[1], "addr")
            elif sys.argv[1].rsplit('.', 1)[-1] == "html":
                dnsGetter.get_DNS(sys.argv[1], "file")
            elif sys.argv[1].replace('.', '').encode('utf-8').isalnum():
                dnsGetter.get_DNS(
                    dnsGetter.get_network_address(sys.argv[1]), "addr")
            else:
                dnsGetter.get_DNS(dnsGetter.get_network_address(
                    dnsGetter.get_domain_name(sys.argv[1])), "addr")
        except Exception as e:
            logger.error(f"エラー: {e}")
        finally:
            del dnsGetter

    else:
        print(f"usage: {sys.argv[0]} filename or domain_name or ip or query")
