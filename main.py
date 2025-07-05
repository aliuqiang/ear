from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

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

def correct_thresholds(raw, sex, age):
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
        "左耳语频平均听阈": round(left_speech, 2),
        "右耳语频平均听阈": round(right_speech, 2),
        "左耳高频平均听阈": round(left_high, 2),
        "右耳高频平均听阈": round(right_high, 2),
        "左耳听阈加权": round(left_weight, 2),
        "右耳听阈加权": round(right_weight, 2),
        "双耳高频平均听阈": round(both_high, 2)
    }

class HearingApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.sex_spinner = Spinner(text='男', values=['男', '女'], size_hint=(1, None), height=44)
        self.age_input = TextInput(hint_text='年龄', input_filter='int', multiline=False, size_hint=(1, None), height=44)
        self.left_input = TextInput(hint_text='左耳6频率,用逗号分隔', multiline=False, size_hint=(1, None), height=44)
        self.right_input = TextInput(hint_text='右耳6频率,用逗号分隔', multiline=False, size_hint=(1, None), height=44)
        self.result_label = Label(text='', size_hint=(1, 1))
        self.calc_btn = Button(text='计算', size_hint=(1, None), height=44)
        self.calc_btn.bind(on_press=self.calculate)
        self.layout.add_widget(Label(text='性别:', size_hint=(1, None), height=30))
        self.layout.add_widget(self.sex_spinner)
        self.layout.add_widget(Label(text='年龄:', size_hint=(1, None), height=30))
        self.layout.add_widget(self.age_input)
        self.layout.add_widget(Label(text='左耳6频率(500,1000,2000,3000,4000,6000Hz):', size_hint=(1, None), height=30))
        self.layout.add_widget(self.left_input)
        self.layout.add_widget(Label(text='右耳6频率(500,1000,2000,3000,4000,6000Hz):', size_hint=(1, None), height=30))
        self.layout.add_widget(self.right_input)
        self.layout.add_widget(self.calc_btn)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        self.layout.add_widget(scroll)
        return self.layout

    def calculate(self, instance):
        try:
            sex = self.sex_spinner.text
            age = int(self.age_input.text)
            left_raw = list(map(float, self.left_input.text.split(',')))
            right_raw = list(map(float, self.right_input.text.split(',')))
            if len(left_raw) != 6 or len(right_raw) != 6:
                self.result_label.text = '请输入6个频率数值'
                return
            left = correct_thresholds(left_raw, sex, age)
            right = correct_thresholds(right_raw, sex, age)
            results = calc_results(left, right)
            txt = f"左耳校正后: {left}\n右耳校正后: {right}\n"
            for k, v in results.items():
                txt += f"{k}: {v}\n"
            self.result_label.text = txt
        except Exception as e:
            self.result_label.text = f'输入有误: {e}'

if __name__ == '__main__':
    HearingApp().run()