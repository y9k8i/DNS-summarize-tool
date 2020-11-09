import collections
import logging

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
from kivy.app import App
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import ObjectProperty, BooleanProperty
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
    debug = BooleanProperty(False)
    query_text = ObjectProperty(None)
    res_per = ObjectProperty(None)
    res_aggressive = BooleanProperty(False)
    res_update = BooleanProperty(False)

    def on_go_btn_click(self):
        if self.query_text.text != "":
            ProgressScreen.debug = self.debug
            ProgressScreen.query = self.query_text.text
            ResultScreen.percentage = int(self.res_per.text)
            ResultScreen.aggressive = self.res_aggressive
            ResultScreen.update = self.res_update
            self.parent.current = "progress"
        else:
            App.get_running_app().open_popup("検索文字列が\n入力されていません")


class ProgressScreen(Screen):
    debug = False
    query = ""
    update = False
    query_label = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.query_label.text = "検索文字列: " + self.query

    def on_enter(self, *args):
        if self.debug:
            MyApp.logger.setLevel(logging.DEBUG)
        try:
            self.dnsGetter = DNSGetter(
                debug=self.debug, update=self.update, logger=MyApp.logger)
            if self.query.rsplit('/')[0].replace('.', '').isdecimal():
                file_name = self.dnsGetter.get_DNS(self.query, "addr")
            elif self.query.rsplit('.', 1)[-1] == "html":
                file_name = self.dnsGetter.get_DNS(self.query, "file")
            elif self.query.replace('.', '').encode('utf-8').isalnum():
                file_name = self.dnsGetter.get_DNS(
                    self.dnsGetter.get_network_address(self.query), "addr")
            else:
                domain_name = self.dnsGetter.get_domain_name(self.query)
                file_name = self.dnsGetter.get_DNS(
                    self.dnsGetter.get_network_address(domain_name), "addr")
                ResultScreen.domain_name = domain_name
            ResultScreen.file_name = file_name
            # numberreplacer.pyにおけるドメイン自動検出が不完全
        except Exception as e:
            MyApp.logger.error(e, exc_info=self.debug)
            App.get_running_app().open_popup(str(e))
        finally:
            del self.dnsGetter

        self.parent.current = "result"


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
                aggressive: 複数回出現した数字を全て置換するオプション
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
        rcParams['font.size'] = 28

        fig = plt.figure()
        ax = fig.add_subplot()
        ax.pie(counts, counterclock=False, startangle=90, autopct="%.1f%%",
               wedgeprops={'linewidth': 3, 'edgecolor': "white"})
        ax.legend(values, fancybox=True, loc='center left',
                  bbox_to_anchor=(1.0, 0.5))
        plt.title("DNSレコードにおける各種ホスト名の割合",
                  x=0.25, horizontalalignment='left')
        fig.subplots_adjust(left=0, right=0.5, bottom=0)
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

    def open_popup(self, msg: str, my_callback):
        self.errmsg.text = msg
        self.popupWindow = ErrPopup(title="エラー", title_size=32, content=self,
                                    size_hint=(0.3, 0.4), auto_dismiss=False)
        if(my_callback is not None):
            self.popupWindow.bind(on_dismiss=my_callback)
        self.popupWindow.open()

    def popup_close(self):
        self.popupWindow.dismiss()


class ErrPopup(Popup):
    pass


class MyApp(App):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    title = "DNSレコード事前調査ツール"

    def build(self):
        self.icon = "icon.png"
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(DialogScreen(name="dialog"))
        self.sm.add_widget(ProgressScreen(name="progress"))
        self.sm.add_widget(ResultScreen(name="result"))
        # ResultScreen.file_name = "table/table_dendai_133_20.csv"
        # self.sm.current = "result"
        return self.sm

    def open_popup(self, msg: str, on_dismiss=None):
        show = Popups()
        show.open_popup(msg, on_dismiss)


if __name__ == '__main__':
    MyApp().run()
