import flet as ft
import threading
import subprocess
import sys
import re
from .chart import create_bar_chart, update_chart, reset_chart
from flet_timer.flet_timer import Timer
from datetime import timedelta, datetime
from speaker_diarization.diarization import MySpeakerDiarization
import time
import os
import queue


# サブプロセスのインスタンスを保存する変数
# process = None


class AppState:
    def __init__(self):
        self.process = None
        self.auto_update_running = True
        self.ui_queue = queue.Queue()


app_state = AppState()


def create_name_and_record_fields(
    num_speakers, name_fields, record_buttons, recording_states, toggle_recording, is_manual
):
    name_fields.clear()
    record_buttons.clear()
    recording_states.clear()
    for i in range(num_speakers):
        name_field = ft.TextField(label=f"話者{i+1}の名前")
        name_fields.append(name_field)
        if is_manual == False:
            record_button = ft.IconButton(icon=ft.icons.VOICE_OVER_OFF, icon_color=ft.colors.RED, icon_size=40)
            record_button.on_click = toggle_recording(i)
            record_buttons.append(record_button)
            recording_states.append(False)

    if is_manual == False:
        name_and_record_fields = [
            ft.Row(
                [name_fields[i], record_buttons[i]],
                alignment=ft.MainAxisAlignment.CENTER,
                height=50,
            )
            for i in range(num_speakers)
        ]
    else:
        name_and_record_fields = [
            ft.Row(
                [name_fields[i]],
                alignment=ft.MainAxisAlignment.CENTER,
                height=50,
            )
            for i in range(num_speakers)
        ]
    return name_and_record_fields


def create_centered_container(content_list):
    return ft.Container(
        content=ft.Column(
            content_list,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,  # ここでスクロールバーを追加
        ),
        alignment=ft.alignment.center,
        expand=True,
    )


def create_manual_button_list(names):
    for i in range(len(names)):
        manual_button = ft.Switch()
        manual_button_label = ft.Text(names[i])
    manual_button_list = ft.Column([ft.Row([ft.Switch(), ft.Text(names[i])]) for i in range(len(names))])
    return manual_button_list


def toggle_pause(button: ft.ElevatedButton, page: ft.Page):
    # 一時停止ボタンを押したときの処理

    app_state.auto_update_running = not app_state.auto_update_running
    if app_state.auto_update_running:
        button.text = "一時停止"
        button.color = ft.colors.PINK
        MySpeakerDiarization.clear_file()
    else:
        button.text = "再開"
        button.color = ft.colors.PRIMARY
    page.update()


def main():
    def main_app(page: ft.Page):

        page.title = "発言量計測アプリ"
        page.window_width = 700
        page.window_height = 700

        def event(e):
            if e.data == "close":
                finish_meeting()

        # page.window.prevent_close = True
        # page.window.on_event = event

        least_speaker_text = ft.Text(value="")
        alert_timer = ft.Text(value="", color="red", size=20)

        speaker_count = ft.Dropdown(
            width=100,
            options=[ft.dropdown.Option("-")] + [ft.dropdown.Option(str(i)) for i in range(2, 11)],
            value="-",
        )

        name_fields = []
        record_buttons = []
        recording_states = []
        time_input = ft.TextField(label="時間 (hh:mm:ss)", value=timedelta(seconds=300), width=200)
        timer_button = ft.ElevatedButton(text="タイマー開始", on_click=lambda e: start_timer())

        # 会議情報入力時、エラーメッセージを出力する
        def show_error_init(message):
            error_message.value = message
            error_message.visible = True
            page.update()

        def invisible_error():
            error_message.visible = False
            page.update()

        def start_recording(e):
            # 人数が入力されていない
            if speaker_count.value == "-":
                show_error_init("エラー: 人数を入力してください")
                return

            # 名前が全員文入力されていない
            names = [field.value for field in name_fields]
            for name in names:
                if name == "":
                    show_error_init("エラー: 全員の名前を入力してください")
                    return

            # 名前に重複がある
            if len(names) != len(set(names)):
                show_error_init("エラー: 全員が異なる名前にしてください")
                return

            for _, record_button in enumerate(record_buttons):
                if record_button.icon is not ft.icons.CHECK:
                    show_error_init("エラー: 全員の音声を登録してください")
                    return

            MySpeakerDiarization.clear_file()
            chart = create_bar_chart(names)
            manual_button_list = create_manual_button_list(names)
            page.controls.clear()
            error_message.visible = False
            page.add(ft.Container(padding=2))
            page.add(
                ft.Row(
                    [
                        timer_button,
                        time_input,
                        ft.ElevatedButton(text="タイマーリセット", on_click=lambda e: reset_timer()),
                        memo_button,
                    ],
                ),
                alert_timer,
                error_message,
            )
            page.add(ft.Container(padding=10))
            page.add(
                ft.Row(
                    [
                        chart,
                        manual_button_list,
                        ft.Container(padding=3),
                        ft.Column(controls=[memo_text_field], expand=True, alignment="start"),
                    ]
                )
            )
            pause_button = ft.ElevatedButton(
                text="一時停止", on_click=lambda e: toggle_pause(pause_button, page), color=ft.colors.PINK
            )
            page.add(
                ft.Row(
                    [
                        pause_button,
                        ft.ElevatedButton(
                            text="リセット",
                            on_click=lambda e: reset_chart(chart, least_speaker_text, page),
                        ),
                        ft.ElevatedButton(text="会議終了", on_click=lambda e: finish_meeting()),
                    ]
                )
            )
            page.add(ft.Row([least_speaker_text]))

            page.update()
            start_auto_update(chart)

        def start_auto_update(chart):
            def auto_update():
                while True:
                    time.sleep(5)  # 5秒ごとに実行
                    if app_state.auto_update_running:
                        update_chart(chart, least_speaker_text, page)

            threading.Thread(target=auto_update, daemon=True).start()

        # 会議を終了する(アプリを終了する)
        def finish_meeting():
            # global process
            if app_state.process is not None:
                app_state.process.terminate()  # サブプロセスを終了する
                app_state.process.wait()  # 終了を待つ
            page.window_destroy()  # アプリを終了する

        def refresh():
            if timer_button.text != "タイマー停止":
                return
            if time_input.value.total_seconds() == 0:
                alert_timer.value = "Timer is expired"
                reset_timer()
                return
            if timer_button.text == "タイマー停止":
                time_input.value = timedelta(seconds=time_input.value.total_seconds() - 1)
                page.update()

        timer = Timer(name="timer", interval_s=1, callback=refresh)

        def start_timer():
            time_list = str(time_input.value).split(":")
            if not re.fullmatch(
                r"([0-1]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])",
                str(time_input.value),
            ):
                show_error_init("時間のフォーマットに合わせてください %H:%M:%S")
                page.update()
                return

            error_message.visible = False
            hour = time_list[0]
            minute = time_list[1]
            second = time_list[2]
            time_input.value = timedelta(seconds=60 * 60 * int(hour) + 60 * int(minute) + int(second))
            timer_button.text = "タイマー停止"
            timer_button.on_click = lambda e: stop_timer()
            alert_timer.value = ""
            page.add(timer, time_input)
            page.update()

        def stop_timer():
            timer_button.text = "タイマー再開"
            timer_button.on_click = lambda e: start_timer()
            page.update()

        def reset_timer():
            timer_button.text = "タイマー開始"
            timer_button.on_click = lambda e: start_timer()
            time_input.value = timedelta(seconds=300)
            page.update()

        # メモ帳を開閉
        memo_button = ft.ElevatedButton(text="メモ帳を開く", on_click=lambda e: open_memo())

        memo_text_field = ft.TextField(
            multiline=True,
            width=400,
            height=320,
            label="メモ帳",
            hint_text="ここにテキストを入力してください...\n",
            visible=False,
            max_lines=20,
            min_lines=20,
        )

        def open_memo():
            page.window_width = 1100
            memo_text_field.visible = True

            memo_button.text = "メモ帳を閉じる"
            memo_button.on_click = lambda e: close_memo()
            page.update()

        def close_memo():
            page.window_width = 700
            memo_text_field.visible = False

            memo_button.text = "メモ帳を開く"
            memo_button.on_click = lambda e: open_memo()
            page.update()

        def toggle_recording(index):
            def handler(e):
                invisible_error()
                recording_state = recording_states[index]
                if recording_state is False:
                    if not all(state is False for state in recording_states):
                        show_error_init("エラー: 他の人の登録作業中です。")
                        return
                    if name_fields[index].value == "":
                        show_error_init("エラー: 名前を入力してください")
                        return

                recording_states[index] = True

                if recording_state is False:
                    record_buttons[index].icon = ft.icons.RECORD_VOICE_OVER
                    record_buttons[index].icon_color = ft.colors.BLUE
                    MySpeakerDiarization.clear_file()
                    page.update()
                else:
                    invisible_error()
                    is_registered = MySpeakerDiarization.register_id(name_fields[index].value)
                    if is_registered:
                        record_buttons[index].icon = ft.icons.CHECK
                        record_buttons[index].icon_color = ft.colors.GREEN
                    else:
                        show_error_init("エラー: 音声が検出できませんでした。もう一度録音してください。")
                        record_buttons[index].icon = ft.icons.VOICE_OVER_OFF
                        record_buttons[index].icon_color = ft.colors.RED
                    recording_states[index] = False
                    page.update()

            return handler

        def toggle_changed(e):
            on_speaker_count_change(e)
            page.update()

        # 手動記録モード
        manual_record_toggle = ft.Switch(on_change=toggle_changed)
        # ローディングアニメーションの追加
        loading_animation = ft.ProgressRing()

        # UI更新用キューを作成
        app_state.ui_queue = queue.Queue()
        description_text = ft.Text("話者の人数を選択してください:")

        def on_speaker_count_change(e):
            global description_text
            if speaker_count.value == "-":
                centered_container = create_centered_container(
                    [
                        ft.Text("手動記録モード:"),
                        manual_record_toggle,
                        ft.Container(height=10),
                        description_text,
                        speaker_count,
                        start_button,
                        error_message,
                    ]
                )
                page.controls.clear()
                page.add(centered_container)
            else:
                num_speakers = int(speaker_count.value)
                speaker_count.visible = False
                start_button.visible = False

                description_text = ft.Text("それぞれの話者の名前を入力し、声を登録してください:")
                MySpeakerDiarization.register_speaker_num(num_speakers)

                log_file = "subprocess_log.txt"
                with open(log_file, "w") as f:
                    app_state.process = subprocess.Popen(
                        [
                            sys.executable,
                            "-u",
                            "speaker_diarization/diarization.py",
                            str(num_speakers),
                        ],
                        stdout=f,
                        stderr=f,
                        bufsize=1,  # 行バッファリングモードを有効にする
                        universal_newlines=True,  # テキストモードで出力
                    )

                # サブプロセスの起動を監視するスレッドを開始

                def monitor_log():

                    with open(log_file, "r") as f:

                        while True:
                            line = f.readline()
                            if not line:
                                time.sleep(3)
                                continue
                            # 'Streaming' という単語を検出
                            if "Streaming" in line.split():
                                print("Streaming has started")
                                app_state.ui_queue.put("streaming_started")
                                break

                threading.Thread(target=monitor_log, daemon=True).start()

                name_and_record_fields = create_name_and_record_fields(
                    num_speakers,
                    name_fields,
                    record_buttons,
                    recording_states,
                    toggle_recording,
                    manual_record_toggle.value,
                )
                centered_container = create_centered_container(
                    # 怪しい
                    [
                        ft.Text("手動記録モード:"),
                        manual_record_toggle,
                        ft.Container(height=10),
                        description_text,
                        speaker_count,
                    ]
                    +
                    # ここまで
                    [description_text, speaker_count]
                    + name_and_record_fields
                    + [start_button]
                    + [error_message]
                    + [loading_animation]  # 準備中テキストとローディングアニメーションを追加
                )
                for _, record_button in enumerate(record_buttons):
                    record_button.visible = False
                page.controls.clear()
                page.add(centered_container)
            page.update()

        def ui_update_thread():
            while True:
                message = app_state.ui_queue.get()
                if message == "streaming_started":
                    loading_animation.visible = False
                    start_button.visible = True
                    for i, record_button in enumerate(record_buttons):
                        record_button.visible = True
                    page.update()
                    break

        # UI更新スレッドを開始
        threading.Thread(target=ui_update_thread, daemon=True).start()

        start_button = ft.ElevatedButton(text="開始", on_click=start_recording)
        error_message = ft.Text("", color=ft.colors.RED, visible=False)
        speaker_count.on_change = on_speaker_count_change

        centered_container = create_centered_container(
            [
                ft.Text("手動記録モード:"),
                manual_record_toggle,
                ft.Container(height=10),
                description_text,
                speaker_count,
                start_button,
                error_message,
            ]
        )
        page.add(centered_container)

    ft.app(target=main_app)
