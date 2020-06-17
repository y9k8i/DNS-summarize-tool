# coding:utf-8
# DNSを取得するクラス by @y9k8i 2020
import csv
import os.path
import sys
import traceback
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

class DNSGetter:

	def launch_browser(self):
		"""ブラウザを起動する"""
		if not hasattr(self, 'driver'):
			options = Options()
			if not self.debug:
				options.add_argument('--headless')
			self.driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
			self.wait = WebDriverWait(self.driver, 30)


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
			err_elements = self.driver.find_elements_by_id('error')
			if len(err_elements) > 0 and err_elements[0].text \
					== "Please wait while we validate your browser.":
				print("サーバ側でブラウザを検証中...")
				self.wait.until(location_to_be_change("https://bgp.he.net/cc"))
				self.wait.until(EC.presence_of_all_elements_located)
			if len(self.driver.find_elements_by_id('tab_error')) > 0:
				raise Exception(
					"エラー発生: " + self.driver.find_element_by_id('error').text)
			else:
				err_elements = self.driver.find_elements_by_tag_name('h2')
				if len(err_elements) > 0:
					raise Exception("サーバ側エラー発生: " + err_elements[0].text)
			del err_elements
		except TimeoutException:
			raise TimeoutException("エラー発生 時間切れ")
		except Exception as e:
			print(e, file=sys.stderr)
			pass


	def get_domain_name(self, query) -> str:
		"""検索文字列からドメイン名を検出し返す"""
		print(query + "のドメイン名を取得中...")
		self.launch_browser()
		page_url = "https://www.google.com/search?q=" + query
		self.driver.get(page_url)
		soup = BeautifulSoup(self.driver.page_source, "html.parser")
		domain_name = soup.select_one(".iUh30")
		title = soup.select_one(".LC20lb")
		print(title.text + "のドメイン名は" + domain_name.text)
		return domain_name.text


	def get_network_address(self, domain_name) -> str:
		"""ドメイン名からネットワークアドレスを検出し返す"""
		print(domain_name + "のネットワークアドレスを取得中...")
		self.launch_browser()
		page_url = "https://bgp.he.net/dns/" + domain_name + "#_ipinfo"
		self.driver.get(page_url)
		self.wait_for_browser_validate()
		soup = BeautifulSoup(self.driver.page_source, "html.parser")
		addr = soup.select_one("#ipinfo > a:nth-child(2)")
		return addr.text


	def get_DNS(self, arg, opt) -> str:
		"""
		ネットワークアドレスからDNSレコードを取得し保存する 保存したファイル名を返す

			IPアドレスの場合:
			arg:CIDR表記のネットワークアドレス, opt:addr
			DOMを保存したファイルの場合:
			arg:ファイル名（CIDR表記又は`0_0_0_0`形式のネットワークアドレス+.html）, opt:file
		"""
		if opt == "addr":
			filename = "table/table_" + arg.split('/')[0].replace('.', '_') + ".csv"
			if os.path.exists(filename) and not self.update:
				print(filename + "が存在するため再利用します")
				return filename
			print(arg + "のDNSレコードを取得中...")
			self.launch_browser()
			page_url = "https://bgp.he.net/net/" + arg + "#_dns"
			self.driver.get(page_url)
			self.wait_for_browser_validate()
			self.wait.until(EC.visibility_of_element_located((By.ID, "dns")))
			soup = BeautifulSoup(self.driver.page_source, "html.parser")
		elif opt == "file":
			filename = arg.rsplit('.', 1)[0] + ".csv"
			if os.path.exists(filename) and not self.update:
				print(filename + "が存在するため再利用します")
				return filename
			with open(arg) as f:
				soup = BeautifulSoup(f.read(), "html.parser")
		else:
			print("get_DNS()でエラー: 処理するデータのタイプが指定されていません", file=sys.stderr)

		rows = soup.select("#dns tr")

		# ファイルに保存
		print("取得したDNSレコードをCSV形式で保存中...")
		with open(filename, "w", encoding='utf-8') as file:
			writer = csv.writer(file)
			writer.writerow(["IP", "hostname"])
			for row in rows[1:]:
				csvRow = []
				for cell in row.select("td")[:2]:
					csvRow.append(cell.text)
				writer.writerow(csvRow)
		print(filename + "に保存しました")
		return filename


	def __init__(self, debug=False, update=False):
		self.debug = debug
		self.update = update


	def __del__(self):
		if hasattr(self, 'driver'):
			self.driver.quit()


# 直接実行された場合
if __name__ == "__main__":
	dnsGetter = DNSGetter(debug=True)
	if len(sys.argv) is 2:
		try:
			if sys.argv[1].replace('.', '').isdecimal():
				dnsGetter.get_DNS(sys.argv[1], "addr")
			elif sys.argv[1].rsplit('.', 1)[-1] == "html":
				dnsGetter.get_DNS(sys.argv[1], "file")
			elif sys.argv[1].replace('.', '').encode('utf-8').isalnum():
				dnsGetter.get_DNS(dnsGetter.get_network_address(sys.argv[1]), "addr")
			else:
				dnsGetter.get_DNS(dnsGetter.get_network_address(
					dnsGetter.get_domain_name(sys.argv[1])), "addr")
		except Exception as e:
			print(e, file=sys.stderr)
		finally:
			del dnsGetter

	else:
		print("usage: " + sys.argv[0] + " filename or domain_name or ip or query")
