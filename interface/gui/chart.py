import flet as ft
import random


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
                ft.ChartAxisLabel(value=j, label=ft.Container(ft.Text(names[j]), padding=10)) for j in range(len(names))
            ],
            labels_size=40,
        ),
        horizontal_grid_lines=ft.ChartGridLines(color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]),
        tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
        max_y=50,
        interactive=True,
        expand=False,
    )


def update_chart(chart, least_speaker_text, page):
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


def reset_chart(chart, least_speaker_text, page):
    for group in chart.bar_groups:
        group.bar_rods[0].to_y = 0
    least_speaker_text.value = ""
    page.update()
