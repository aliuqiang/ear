from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
from kivy.config import Config

LabelBase.register(name="SimHei", fn_regular="C:/Windows/Fonts/simhei.ttf")
Config.set('kivy', 'default_font', ['SimHei', 'C:/Windows/Fonts/simhei.ttf', '', '', ''])

correction_table = {
    "20-29": {"男": [0, 0, 0, 0, 0, 0], "女": [0, 0, 0, 0, 0, 0]},
    "30-39": {"男": [1, 1, 1, 2, 2, 3], "女": [1, 1, 1, 1, 1, 2]},
    "40-49": {"男": [2, 2, 3, 6, 8, 9], "女": [2, 2, 2, 4, 4, 6]},
    "50-59": {"男": [4, 4, 7, 12, 16, 18], "女": [4, 4, 6, 8, 9, 12]},
    "60-69": {"男": [6, 7, 12, 20, 28, 32], "女": [6, 7, 11, 13, 16, 21]},
    "70-":   {"男": [9, 11, 19, 31, 43, 49], "女": [9, 11, 16, 20, 24, 32]},
}
freqs = [500, 1000, 2000, 3000, 4000, 6000]

def get_age_group(age):
    if 20 <= age <= 29:
        return "20-29"
    elif 30 <= age <= 39:
        return "30-39"
    elif 40 <= age <= 49:
        return "40-49"
    elif 50 <= age <= 59:
        return "50-59"
    elif 60 <= age <= 69:
        return "60-69"
    else:
        return "70-"

def correct_thresdiaoholds(raw, sex, age):
    group = get_age_group(age)
    correction = correction_table[group][sex]
    return [raw[i] - correction[i] for i in range(6)]

def calc_results(left, right):
    left_speech = sum(left[:3]) / 3
    right_speech = sum(right[:3]) / 3
    left_high = sum(left[3:]) / 3
    right_high = sum(right[3:]) / 3
    left_weight = sum(left[:3]) * 0.3 + left[4] * 0.1
    right_weight = sum(right[:3]) * 0.3 + right[4] * 0.1
    both_high = sum(left[3:] + right[3:]) / 6
    return {
        "左耳语频平均听阈": round(left_speech),
        "右耳语频平均听阈": round(right_speech),
        "左耳高频平均听阈": round(left_high),
        "右耳高频平均听阈": round(right_high),
        "左耳听阈加权": round(left_weight),
        "右耳听阈加权": round(right_weight),
        "双耳高频平均听阈": round(both_high)
    }

class MySpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_name', 'SimHei')
        super().__init__(**kwargs)

class HearingApp(App):
    def build(self):
        from kivy.uix.floatlayout import FloatLayout
        root = FloatLayout()
        with root.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.95, 0.97, 1, 1)  # 这里设置你想要的背景色（淡蓝色，可调整）
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        def update_bg_rect(instance, value):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size
        root.bind(pos=update_bg_rect, size=update_bg_rect)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.sex_spinner = Spinner(
            text='请选择',
            values=['男', '女'],
            size_hint=(0.9, None),
            height=44,
            option_cls=MySpinnerOption,
            font_name='SimHei'
        )
        self.age_input = TextInput(
            hint_text='年龄',
            input_filter='int',
            multiline=False,
            size_hint=(0.9, None),
            height=44,
            font_name="SimHei",
            input_type='number'
        )
        # 性别
        sex_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44)
        sex_box.add_widget(Label(text='性别:',width=50, size_hint=(0.1, 1), font_name="SimHei", color=(0, 0, 0, 1)))
        sex_box.add_widget(self.sex_spinner)
        self.layout.add_widget(sex_box)

        # 年龄
        age_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44)
        age_box.add_widget(Label(text='年龄:',width=50, size_hint=(0.1, 1), font_name="SimHei", color=(0, 0, 0, 1)))
        age_box.add_widget(self.age_input)
        self.layout.add_widget(age_box)

        # 左耳6频率
        left_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44)
        left_box.add_widget(Label(text='左耳6频率:',width=50, size_hint=(0.1, 1), font_name="SimHei", color=(0, 0, 0, 1)))
        self.left_inputs = []
        for i in range(6):
            ti = TextInput(
                hint_text=f'L{i+1}',
                multiline=False,
                size_hint=(0.15, 1),
                font_name="SimHei",
                input_type='number',
                input_filter='int'
            )
            self.left_inputs.append(ti)
            left_box.add_widget(ti)
        self.layout.add_widget(left_box)

        # 右耳6频率
        right_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=44)
        right_box.add_widget(Label(text='右耳6频率:',width=500, size_hint=(0.1, 1), font_name="SimHei", color=(0, 0, 0, 1)))
        self.right_inputs = []
        for i in range(6):
            ti = TextInput(
                hint_text=f'R{i+1}',
                multiline=False,
                size_hint=(0.15, 1),
                font_name="SimHei",
                input_type='number',
                input_filter='int'
            )
            self.right_inputs.append(ti)
            right_box.add_widget(ti)
        self.layout.add_widget(right_box)

        self.result_label = Label(
            text='',
            size_hint=(1, 1),
            font_name="SimHei",
            color=(0, 0, 0, 1)
        )
        self.calc_btn = Button(
            text='计算',
            size_hint=(1, None),
            height=44,
            font_name="SimHei"
        )
        self.calc_btn.bind(on_press=self.calculate)
        self.layout.add_widget(self.calc_btn)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        self.layout.add_widget(scroll)
        root.add_widget(self.layout)
        return root

    def calculate(self, instance):
        try:
            sex = self.sex_spinner.text
            age = int(self.age_input.text)
            left_raw = [int(ti.text) for ti in self.left_inputs]
            right_raw = [int(ti.text) for ti in self.right_inputs]
            if len(left_raw) != 6 or len(right_raw) != 6:
                self.result_label.text = '请输入6个频率数值'
                return

            txt = f"左耳输入: {left_raw}右耳输入: {right_raw}\n"
  
                        
            left = correct_thresdiaoholds(left_raw, sex, age)  
            right = correct_thresdiaoholds(right_raw, sex, age)

            results = calc_results(left, right)
            txt += f"左耳输出: {left}右耳输出: {right}\n"
            for k, v in results.items():
                txt += f"{k}: {v}\n"
            self.result_label.text = txt

        except Exception as e:
            self.result_label.text = f'输入有误: {e}'

if __name__ == '__main__':
    HearingApp().run()