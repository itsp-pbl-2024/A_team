import flet as ft
import threading
import subprocess
import sys
from .chart import create_bar_chart, update_chart, reset_chart
from speaker_diarization.diarization import MySpeakerDiarization


def create_name_and_record_fields(
    num_speakers, name_fields, record_buttons, recording_states, toggle_recording
):
    name_fields.clear()
    record_buttons.clear()
    recording_states.clear()
    for i in range(num_speakers):
        name_field = ft.TextField(label=f"話者{i+1}の名前")
        record_button = ft.IconButton(
            icon=ft.icons.MIC_OFF, icon_color=ft.colors.RED, icon_size=40
        )
        record_button.on_click = toggle_recording(i)
        name_fields.append(name_field)
        record_buttons.append(record_button)
        recording_states.append(False)

    name_and_record_fields = [
        ft.Row(
            [name_fields[i], record_buttons[i]],
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

        speaker_count = ft.Dropdown(
            width=100,
            options=[ft.dropdown.Option("-")]
            + [ft.dropdown.Option(str(i)) for i in range(2, 6)],
            value="-",
        )

        name_fields = []
        record_buttons = []
        recording_states = []

        def start_recording(e):
            MySpeakerDiarization.clear_file()
            names = [field.value for field in name_fields]
            chart = create_bar_chart(names)
            page.controls.clear()
            page.add(ft.Container(padding=2))
            page.add(
                ft.Row(
                    [
                        ft.ElevatedButton(text="タイマー開始", on_click=lambda e: finish_meeting()),
                        ft.ElevatedButton(text="メモ帳", on_click=lambda e: finish_meeting()),
                        ft.ElevatedButton(text="会議終了", on_click=lambda e: finish_meeting()),
                    ]
                )
            )
            page.add(ft.Container(padding=10))
            page.add(chart)
            page.add(
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="更新",
                            on_click=lambda e: update_chart(
                                chart, least_speaker_text, page
                            ),
                        ),
                        ft.ElevatedButton(
                            text="リセット",
                            on_click=lambda e: reset_chart(
                                chart, least_speaker_text, page
                            ),
                        ),
                        least_speaker_text,
                    ]
                )
            )

            page.update()

        # 会議を終了する(アプリを終了する)
        def finish_meeting():
            page.window_destroy()

        def toggle_recording(index):
            def handler(e):
                recording_states[index] = not recording_states[index]
                if recording_states[index]:
                    record_buttons[index].icon = ft.icons.MIC
                    record_buttons[index].icon_color = ft.colors.GREEN
                    MySpeakerDiarization.clear_file()
                else:
                    record_buttons[index].icon = ft.icons.MIC_OFF
                    record_buttons[index].icon_color = ft.colors.RED
                    MySpeakerDiarization.register_id(name_fields[index].value)

                page.update()

            return handler

        def on_speaker_count_change(e):
            if speaker_count.value == "-":
                page.controls.clear()
                page.add(
                    create_centered_container(
                        [
                            ft.Text("話者の人数を選択してください:"),
                            speaker_count,
                            start_button,
                        ]
                    )
                )
            else:
                num_speakers = int(speaker_count.value)
                subprocess.Popen(
                    [
                        sys.executable,
                        "speaker_diarization/diarization.py",
                        str(num_speakers),
                    ]
                )
                name_and_record_fields = create_name_and_record_fields(
                    num_speakers,
                    name_fields,
                    record_buttons,
                    recording_states,
                    toggle_recording,
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

        page.add(
            create_centered_container(
                [ft.Text("話者の人数を選択してください:"), speaker_count, start_button]
            )
        )

    ft.app(target=main_app)
