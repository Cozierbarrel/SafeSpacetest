"""
Utilitários para o sistema de tracking de humor.
Inclui mapeamento de emojis e geração de gráficos ASCII para relatórios.
"""

from datetime import date, timedelta
from collections import defaultdict


MOOD_EMOJIS = {
    1: "😭",
    2: "😢",
    3: "😐",
    4: "🙂",
    5: "😊",
    6: "😁",
}

MOOD_LABELS = {
    1: "Muito Triste",
    2: "Triste",
    3: "Neutro",
    4: "Bem",
    5: "Feliz",
    6: "Muito Feliz",
}

MOOD_COLORS = {
    1: "red",
    2: "dark_orange",
    3: "yellow",
    4: "chartreuse3",
    5: "green",
    6: "bright_green",
}


def mood_to_emoji(level: int) -> str:
    """
    Converte um nível numérico de humor (1-6) para o emoji correspondente.
    Arredonda o valor caso seja float antes de converter.
    """
    level = max(1, min(6, round(level)))
    return MOOD_EMOJIS.get(level, "😐")


def mood_to_label(level: int) -> str:
    """
    Converte um nível numérico de humor (1-6) para o rótulo textual correspondente.
    """
    level = max(1, min(6, round(level)))
    return MOOD_LABELS.get(level, "Neutro")


def compute_daily_averages(entries: list[dict]) -> dict[date, float]:
    """
    Recebe uma lista de entradas de humor (dicts com 'recorded_at' e 'mood_level')
    e retorna um dicionário {data: média_do_dia}, considerando múltiplos
    registros no mesmo dia.
    """
    daily = defaultdict(list)
    for entry in entries:
        day = entry["recorded_at"].date() if hasattr(entry["recorded_at"], "date") else entry["recorded_at"]
        daily[day].append(entry["mood_level"])

    return {day: sum(vals) / len(vals) for day, vals in daily.items()}


def generate_period_chart(daily_averages: dict[date, float], period_dates: list[date]) -> str:
    """
    Gera um gráfico de barras horizontal em texto para exibição no terminal,
    representando a flutuação de humor ao longo do período.
    Recebe o dicionário de médias diárias e a lista completa de datas do período.
    Retorna a string do gráfico formatado.
    """
    if not period_dates:
        return "Nenhum dado para exibir."

    lines = []
    bar_max = 20

    for day in period_dates:
        avg = daily_averages.get(day)
        date_str = day.strftime("%d/%m")

        if avg is None:
            bar = "─" * 2
            emoji = "  "
            val_str = "  sem dados"
        else:
            bar_len = int((avg / 6) * bar_max)
            bar = "█" * bar_len + "░" * (bar_max - bar_len)
            emoji = mood_to_emoji(avg)
            val_str = f" {avg:.1f}"

        lines.append(f" {date_str} │{bar}│ {emoji}{val_str}")

    return "\n".join(lines)


def compute_period_average(daily_averages: dict[date, float]) -> float | None:
    """
    Calcula a média geral de um período a partir das médias diárias.
    Retorna None se não houver dados.
    """
    if not daily_averages:
        return None
    values = list(daily_averages.values())
    return sum(values) / len(values)


def get_week_dates(reference: date, offset: int = 0) -> list[date]:
    """
    Retorna a lista de 7 datas da semana (seg-dom) com base em uma data de referência.
    O offset permite acessar semanas anteriores (offset=-1 = semana passada).
    """
    monday = reference - timedelta(days=reference.weekday()) + timedelta(weeks=offset)
    return [monday + timedelta(days=i) for i in range(7)]


def get_month_dates(reference: date, offset: int = 0) -> list[date]:
    """
    Retorna a lista de todas as datas do mês com base em uma data de referência.
    O offset permite acessar meses anteriores (offset=-1 = mês passado).
    """
    import calendar
    month = reference.month + offset
    year = reference.year + (month - 1) // 12
    month = ((month - 1) % 12) + 1
    _, days_in_month = calendar.monthrange(year, month)
    return [date(year, month, d) for d in range(1, days_in_month + 1)]
