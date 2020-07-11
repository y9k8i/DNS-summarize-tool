import collections

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
from kivy.app import App
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import japanize_kivy  # noqa: F401
from matplotlib import rcParams
import matplotlib.pyplot as plt

from dnsgetter import DNSGetter
from numberreplacer import NumberReplacer


class DialogScreen(Screen):
    query_text = ObjectProperty(None)
    res_per = ObjectProperty(None)
    res_aggressive = BooleanProperty(False)

    def on_go_btn_click(self):
        if self.query_text.text != "":
            ProgressScreen.query = self.query_text.text
            ResultScreen.percentage = int(self.res_per.text)
            ResultScreen.aggressive = self.res_aggressive
            self.parent.current = "progress"
        else:
            App.get_running_app().open_popup("検索文字列が\n入力されていません")


class ProgressScreen(Screen):
    query = ""
    query_label = ObjectProperty(None)
    progress = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.query_label.text = "検索文字列: " + self.query
        self.progress.max = 3
        self.progress.value = 0

    def on_enter(self, *args):
        self.dnsGetter = DNSGetter()
        self.dnsGetter.debug = True
        self.dnsGetter.update = True
        domain_name = self.dnsGetter.get_domain_name(self.query)
        self.progress.value = 1
        network_address = self.dnsGetter.get_network_address(domain_name)
        self.progress.value = 2
        file_name = self.dnsGetter.get_DNS(network_address, "addr")
        self.progress.value = 3

        ResultScreen.file_name = file_name
        self.parent.current = "result"

    def on_leave(self, *args):
        del self.dnsGetter


class ResultScreen(Screen):
    file_name = ""
    domain_name = ""
    percentage = 10
    aggressive = False

    def on_enter(self, *args):
        graphview = GraphView()
        res = graphview.summarize_table(
            self.file_name, self.domain_name, self.aggressive, self.percentage)
        fig = graphview.plot_result(res)
        graphview.add_widget(FigureCanvasKivyAgg(fig))
        self.add_widget(graphview)


class GraphView(FloatLayout):
    def summarize_table(self, file_name: str, domain_name: str,
                        aggressive: bool, percentage: int) -> list:
        """
        加工済CSVから集計し結果を配列で返す

                percentage: "その他"に分類する割合の閾値
                aggressive:複数回出現した数字を全て置換するオプション
        """

        # CSVファイルを読み込み加工する
        NR = NumberReplacer()
        res_sorted = collections.Counter(
            NR.replace_number(file_name, domain_name, aggressive))
        del NR

        # 要素の並び替えおよび「その他」への置換
        threshold = int(sum(res_sorted.values()) / (100 / percentage))
        res = [(k, v) for k, v in res_sorted.most_common() if v >= threshold]
        res.append(('その他', sum(
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


class WrappedLabel(Label):
    # https://stackoverflow.com/a/58227983
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
                self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x:
                self.setter('height')(self, self.texture_size[1])
        )


class Popups(FloatLayout):
    errmsg = ObjectProperty(None)

    def open_popup(self, msg: str):
        self.errmsg.text = msg
        self.popupWindow = ErrPopup(title="エラー", title_size=32, content=self,
                                    size_hint=(0.3, 0.4))
        self.popupWindow.open()

    def popup_close(self):
        self.popupWindow.dismiss()


class ErrPopup(Popup):
    pass


class MyApp(App):
    def build(self):
        self.icon = "icon.png"
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(DialogScreen(name="dialog"))
        self.sm.add_widget(ProgressScreen(name="progress"))
        self.sm.add_widget(ResultScreen(name="result"))
        # ResultScreen.file_name = "table/table_dendai_133_20.csv"
        # self.sm.current = "result"
        return self.sm

    def open_popup(self, msg: str):
        show = Popups()
        show.open_popup(msg)


if __name__ == '__main__':
    MyApp().run()
