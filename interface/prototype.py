import flet as ft
import random


def main(page: ft.Page):
    page.title = "発言量計測アプリ"
    page.window_width = 700
    page.window_height = 500

    least_speaker_text = ft.Text(value="")

    speaker_count = ft.Dropdown(
        width=100,
        options=[ft.dropdown.Option("-")] + [ft.dropdown.Option(str(i)) for i in range(2, 6)],
        value="-",
    )

    name_fields = []
    record_buttons = []
    recording_states = []

    def create_bar_chart(names):
        colors = [ft.colors.AMBER, ft.colors.BLUE, ft.colors.RED, ft.colors.ORANGE, ft.colors.PURPLE]
        bar_groups = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=0,
                        width=40,
                        color=colors[i],
                        tooltip=names[i],
                        border_radius=0,
                    ),
                ],
            )
            for i in range(len(names))
        ]
        return ft.BarChart(
            width=600,
            height=400,
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("発言量"), title_size=40),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=j, label=ft.Container(ft.Text(names[j]), padding=10))
                    for j in range(len(names))
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=50,
            interactive=True,
            expand=False,
        )

    def update_chart(chart):
        total_speech = 0
        speech_amounts = []
        for group in chart.bar_groups:
            speech_amount = random.randint(0, 50)
            speech_amounts.append(speech_amount)
            total_speech += speech_amount

        min_value = float("inf")
        min_index = -1
        for i, group in enumerate(chart.bar_groups):
            percentage = (speech_amounts[i] / total_speech) * 100 if total_speech > 0 else 0
            group.bar_rods[0].to_y = percentage
            if percentage < min_value:
                min_value = percentage
                min_index = i

        least_speaker_text.value = f"発言量が一番少ないのは{chart.bar_groups[min_index].bar_rods[0].tooltip}です"
        page.update()

    def reset_chart(chart):
        for group in chart.bar_groups:
            group.bar_rods[0].to_y = 0
        least_speaker_text.value = ""
        page.update()

    def start_recording(e):
        names = [field.value for field in name_fields]
        chart = create_bar_chart(names)
        page.controls.clear()
        page.add(chart)
        page.add(
            ft.Row(
                [
                    ft.ElevatedButton(text="更新", on_click=lambda e: update_chart(chart)),
                    ft.ElevatedButton(text="リセット", on_click=lambda e: reset_chart(chart)),
                    least_speaker_text,
                ]
            )
        )
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

    def create_name_and_record_fields(num_speakers):
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
            ft.Row([name_fields[i], record_buttons[i]], alignment=ft.MainAxisAlignment.CENTER, height=50)  # 中央に配置
            for i in range(num_speakers)
        ]
        return name_and_record_fields

    def on_speaker_count_change(e):
        if speaker_count.value == "-":
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column(
                        [ft.Text("話者の人数を選択してください:"), speaker_count, start_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
        else:
            num_speakers = int(speaker_count.value)
            name_and_record_fields = create_name_and_record_fields(num_speakers)
            page.controls.clear()
            page.add(
                ft.Container(
                    content=ft.Column(
                        [ft.Text("話者の人数を選択してください:"), speaker_count]
                        + name_and_record_fields
                        + [start_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )
            )
        page.update()

    start_button = ft.ElevatedButton(text="開始", on_click=start_recording)

    speaker_count.on_change = on_speaker_count_change

    page.add(
        ft.Container(
            content=ft.Column(
                [ft.Text("話者の人数を選択してください:"), speaker_count, start_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
    )


ft.app(main)
