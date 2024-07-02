import flet as ft
from .chart import create_bar_chart, update_chart, reset_chart
from flet_timer.flet_timer import Timer
from datetime import timedelta, datetime


def create_name_and_record_fields(num_speakers, name_fields, record_buttons, recording_states, toggle_recording):
    name_fields.clear()
    record_buttons.clear()
    recording_states.clear()
    for i in range(num_speakers):
        name_field = ft.TextField(label=f"話者{i+1}の名前")
        record_button = ft.IconButton(icon=ft.icons.MIC, icon_color=ft.colors.RED, icon_size=40)
        record_button.on_click = toggle_recording(i)
        name_fields.append(name_field)
        record_buttons.append(record_button)
        recording_states.append(False)

    name_and_record_fields = [
        ft.Row([name_fields[i], record_buttons[i]], alignment=ft.MainAxisAlignment.CENTER, height=50)
        for i in range(num_speakers)
    ]
    return name_and_record_fields


def create_centered_container(content_list):
    return ft.Container(
        content=ft.Column(
            content_list,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
    )


def main():
    def main_app(page: ft.Page):
        page.title = "発言量計測アプリ"
        page.window_width = 700
        page.window_height = 600

        least_speaker_text = ft.Text(value="")
        alert_timer = ft.Text(value="", color="red", size=20)

        speaker_count = ft.Dropdown(
            width=100,
            options=[ft.dropdown.Option("-")] + [ft.dropdown.Option(str(i)) for i in range(2, 6)],
            value="-",
        )

        name_fields = []
        record_buttons = []
        recording_states = []

        time_input = ft.TextField(label="時間 (hh:mm:ss)", value=timedelta(seconds=300), width=200)
        timer_button = ft.ElevatedButton(text="タイマー開始", on_click=lambda e: start_timer())

        def start_recording(e):
            names = [field.value for field in name_fields]
            chart = create_bar_chart(names)
            page.controls.clear()
            page.add(ft.Container(padding=2))
            page.add(
                ft.Row(
                    [
                        timer_button,
                        time_input,
                        ft.ElevatedButton(text="メモ帳", on_click=lambda e: finish_meeting()),
                        ft.ElevatedButton(text="会議終了", on_click=lambda e: finish_meeting()),
                    ],
                ),
                alert_timer
            )
            page.add(ft.Container(padding=10))
            page.add(chart)
            page.add(
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="更新", on_click=lambda e: update_chart(chart, least_speaker_text, page)
                        ),
                        ft.ElevatedButton(
                            text="リセット", on_click=lambda e: reset_chart(chart, least_speaker_text, page)
                        ),
                        ft.ElevatedButton(text="タイマーリセット", on_click=lambda e: reset_timer()),
                        least_speaker_text,
                    ]
                )
            )

            page.update()

        # 会議を終了する(アプリを終了する)
        def finish_meeting():
            page.window_destroy()

        def refresh():
            if time_input.value.total_seconds() == 0:
               alert_timer.value = "Timer is expired"
               reset_timer()
               return
            if timer_button.text == "タイマー停止":
                time_input.value = timedelta(seconds=time_input.value.total_seconds() - 1)
                page.update()

        timer = Timer(name="timer", interval_s=1, callback=refresh)

        def start_timer():
            req_time = datetime.strptime(str(time_input.value), "%H:%M:%S")
            hour = req_time.strftime("%H")
            minute = req_time.strftime("%M")
            second = req_time.strftime("%S")
            time_input.value = timedelta(seconds=60 * 60 * int(hour) + 60 * int(minute) + int(second))
            timer_button.text = "タイマー停止"
            timer_button.on_click = lambda e: stop_timer()
            alert_timer.value = ""
            page.add(timer, time_input)
            page.update()

        def stop_timer():
            timer_button.text = "タイマー再開"
            timer_button.on_click = lambda e: restart_timer()
            page.update()

        def restart_timer():
            timer_button.text = "タイマー停止"
            timer_button.on_click = lambda e: stop_timer()
            page.update()

        def reset_timer():
            timer_button.text = "タイマー開始"
            timer_button.on_click = lambda e: start_timer()
            time_input.value = timedelta(seconds=300)
            page.update()

        def toggle_recording(index):
            def handler(e):
                recording_states[index] = not recording_states[index]
                if recording_states[index]:
                    record_buttons[index].icon = ft.icons.MIC
                    record_buttons[index].icon_color = ft.colors.GREEN
                else:
                    record_buttons[index].icon = ft.icons.MIC_OFF
                    record_buttons[index].icon_color = ft.colors.RED
                page.update()

            return handler

        def on_speaker_count_change(e):
            if speaker_count.value == "-":
                page.controls.clear()
                page.add(
                    create_centered_container([ft.Text("話者の人数を選択してください:"), speaker_count, start_button])
                )
            else:
                num_speakers = int(speaker_count.value)
                name_and_record_fields = create_name_and_record_fields(
                    num_speakers, name_fields, record_buttons, recording_states, toggle_recording
                )
                page.controls.clear()
                page.add(
                    create_centered_container(
                        [ft.Text("話者の人数を選択してください:"), speaker_count]
                        + name_and_record_fields
                        + [start_button]
                    )
                )
            page.update()

        start_button = ft.ElevatedButton(text="開始", on_click=start_recording)
        speaker_count.on_change = on_speaker_count_change

        page.add(create_centered_container([ft.Text("話者の人数を選択してください:"), speaker_count, start_button]))

    ft.app(target=main_app)
