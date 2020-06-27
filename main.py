from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
from kivy.app import App
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import collections
from dnsgetter import DNSGetter
import numberreplacer
from matplotlib import rcParams
import matplotlib.pyplot as plt
import japanize_kivy


class DialogScreen(Screen):
    query_text = ObjectProperty(None)

    def on_go_btn_click(self):
        if self.query_text.text != "":
            ProgressScreen.query = self.query_text.text
        else:
            show = Popups(popup_close=self.popup_close)
            show.errmsg.text = "検索文字列が\n入力されていません"
            self.popupWindow = Popup(title="エラー", title_size=32, content=show,
                                     size_hint=(0.3, 0.4))
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

        ResultScreen.filename = filename
        ResultScreen.percentage = 10
        ResultScreen.aggressive = False


class ResultScreen(Screen):
    filename = ObjectProperty(None)
    percentage = ObjectProperty(None)
    aggressive = BooleanProperty(None)

    def on_enter(self, *args):
        graphview = GraphView()
        # res = graphview.summarize_table(
        #         self.filename.text, self.percentage.text, self.aggressive)
        res = graphview.summarize_table("table/table_dendai_133_20.csv", 10, False)
        fig = graphview.plot_result(res)
        graphview.add_widget(FigureCanvasKivyAgg(fig))
        self.add_widget(graphview)


class GraphView(FloatLayout):
    def summarize_table(
            self, filename, percentage=1, aggressive=False) -> list:
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
        res.append(
            ('その他', sum(
                [v for k, v in res_sorted.most_common() if v < threshold])))
        return res

    def plot_result(self, res) -> plt.figure:
        # 結果を分解する
        values, counts = zip(*res)

        # フォントの設定 順にmacOS, Windows, Ubuntuで使用できるゴシック体
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro',
                                       'Yu Gothic', 'Noto Sans CJK JP']
        rcParams['font.size'] = 15

        fig = plt.figure(dpi=120)
        ax = fig.add_subplot()
        ax.pie(counts, startangle=90, autopct="%.1f%%",
               wedgeprops={'linewidth': 3, 'edgecolor': "white"})
        ax.legend(values, fancybox=True, loc='center left',
                  bbox_to_anchor=(1.0, 0.5))
        plt.title("DNSレコードにおける各種ホスト名の割合")
        fig.subplots_adjust(left=0, right=0.6)
        return fig


class Popups(FloatLayout):
    errmsg = ObjectProperty(None)
    popup_close = ObjectProperty(None)


class MyApp(App):
    def build(self):
        self.icon = "icon.png"
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(DialogScreen(name="dialog"))
        self.sm.add_widget(ProgressScreen(name="progress"))
        self.sm.add_widget(ResultScreen(name="result"))
        ResultScreen.filename = "table/table_dendai_133_20.csv"
        # self.sm.current = "result"
        return self.sm


if __name__ == '__main__':
    MyApp().run()
