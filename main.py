# coding:utf-8
# Kivy関連のインポートおよび設定
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
import japanize_kivy
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

# グラフ関連インポート
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams

# データ処理関連インポート
from dnsgetter import DNSGetter
import numberreplacer
import collections

Builder.load_string('''
#<KvLang>
<DialogScreen>:
	query_text: query_text
	FloatLayout:
		Label:
			text:"検索文字列: "
			font_size: (root.width + root.height) / 6**2
			pos_hint: {"x":0.1, "top":0.9}
			size_hint: 0.35, 0.1
		TextInput:
			id: query_text
			font_size: (root.width + root.height) / 6**2
			multiline: False
			pos_hint: {"x": 0.45 , "top":0.9}
			size_hint: 0.4, 0.1
		Button:
			pos_hint:{"x":0.2,"y":0.05}
			size_hint: 0.6, 0.2
			font_size: root.height / 3**2
			text: "Go!"
			on_release:
				root.on_go_btn_click()

<ProgressScreen>:
	query: "クエリ"
	query_label: query_label
	progress: progress
	BoxLayout:
		orientation: "vertical"
		Label:
			id: query_label
			text: "検索文字列: "
			font_size: (root.width + root.height) / 6**2
			pos_hint: {"x":0.1, "top":0.9}
			size_hint: 0.35, 0.1
		ProgressBar:
			id: progress

<ResultScreen>:
	BoxLayout:
		orientation: "vertical"
		Button:
			size: (120, 60)
			size_hint: (None, None)
			font_size: root.height / 4**2
			text: "Back"
			on_release:
				root.manager.current = 'dialog'

<Popups>
	errmsg: errmsg
	Label:
		id: errmsg
		font_size: root.height / 7
		size_hint: 0.6, 0.2
		pos_hint: {"x":0.2, "y":0.7}
	Button:
		text: "閉じる"
		font_size: root.height / 7
		size_hint: 1, 0.4
		pos_hint: {"x":0, "y":0}
		on_release: root.popup_close()
#</KvLang>
''')

class DialogScreen(Screen):
	query_text = ObjectProperty(None)

	def on_go_btn_click(self):
		if self.query_text.text != "":
			sm.get_screen("progress").query = self.query_text.text
			sm.current = "progress"
		else:
			show = Popups(popup_close=self.popup_close)
			show.errmsg.text = "検索文字列が\n入力されていません"
			self.popupWindow = Popup(title = "エラー", title_size = 32, content = show,
                        size_hint =(0.3, 0.4))
			self.popupWindow.open()

	def popup_close(self):
		self.popupWindow.dismiss()

class ProgressScreen(Screen):
	query = StringProperty(None)
	query_label = ObjectProperty(None)
	progress = ObjectProperty(None)

	def on_pre_enter(self, *args):
		self.query_label.text += self.query
		self.progress.max = 3
		self.progress.value = 0

	def on_enter(self, *args):
		dnsGetter = DNSGetter()
		dnsGetter.debug = True
		dnsGetter.update = True
		domain_name = dnsGetter.get_domain_name(self.query)
		self.progress.value = 1
		network_address = dnsGetter.get_network_address(domain_name)
		self.progress.value = 2
		filename = dnsGetter.get_DNS(network_address, "addr")
		self.progress.value = 3

		sm.get_screen("result").filename = filename
		sm.get_screen("result").percentage = 10
		sm.get_screen("result").aggressive = False
		sm.current = "result"

class ResultScreen(Screen):
	filename = ObjectProperty(None)
	percentage = ObjectProperty(None)
	aggressive = BooleanProperty(None)

	def on_enter(self, *args):
		graphview = GraphView()
		# res = graphview.summarize_table(self.filename.text, self.percentage.text, self.aggressive)
		res = graphview.summarize_table("table_133_20_0_0.csv", 10, False)
		fig = graphview.plot_result(res)
		graphview.add_widget(FigureCanvasKivyAgg(fig))
		self.add_widget(graphview)

class GraphView(FloatLayout):
	def summarize_table(self, filename, percentage=1, aggressive=False) -> list:
		"""
		加工済CSVから集計し結果を配列で返す

			percentage: "その他"に分類する割合の閾値
			aggressive:複数回出現した数字を全て置換するオプション
		"""

		# CSVファイルを読み込み加工する
		res_sorted = collections.Counter(
			numberreplacer.replace_number(filename, None, aggressive))

		# 要素の並び替えおよび「その他」への置換
		threshold = int(sum(res_sorted.values()) / (100/percentage))
		res = [(k, v) for k, v in res_sorted.most_common() if v >= threshold]
		res.append( ('その他', sum([v for k, v in res_sorted.most_common() if v < threshold])) )
		return res

	def plot_result(self, res) -> plt.figure:
		# 結果を分解する
		values, counts = zip(*res)

		# フォントの設定
		rcParams['font.family'] = 'sans-serif'
		rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro']
		rcParams['font.size'] = 15

		fig = plt.figure(dpi=120)
		ax = fig.add_subplot()
		ax.pie(counts, startangle=90, autopct="%.1f%%", wedgeprops={'linewidth': 3, 'edgecolor': "white"})
		ax.legend(values,fancybox=True,loc='center left',bbox_to_anchor=(1.0,0.5))
		plt.title("DNSレコードにおける各種ホスト名の割合")
		fig.subplots_adjust(left=0,right=0.6)
		return fig

class Popups(FloatLayout):
	errmsg = ObjectProperty(None)
	popup_close = ObjectProperty(None)

sm = ScreenManager(transition=FadeTransition())
sm.add_widget(DialogScreen(name="dialog"))
sm.add_widget(ProgressScreen(name="progress"))
sm.add_widget(ResultScreen(name="result"))

class TestApp(App):
	def build(self):
		self.icon = "icon.png"
		# sm.current = "result"
		return sm

if __name__ == '__main__':
	TestApp().run()
