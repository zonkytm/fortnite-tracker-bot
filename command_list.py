import enum

class Commands(enum.Enum):
     start = "start"
     help = "help"
     epic_stats = "stats"
     shop = "shop"


commands = { 
    Commands.start : "Привет! Этот бот поможет тебе получить твою статистику в Foretnite, инфомрацию о ежедневном магазине, карте и многое другое.",
    Commands.help : "зашлушка",
    Commands.epic_stats: (
        "👤 Информация об аккаунте:\n"
        "📛 Имя: {account_name}\n"
        "🆔 ID: {account_id}\n\n"
        "🎟️ Боевой пропуск:\n"
        "⭐ Уровень: {battle_pass_level}\n"
        "📈 Прогресс: {battle_pass_progress}%\n\n"
        "📊 Общая статистика:\n"
        "🏆 Счёт: {score}\n"
        "🥇 Победы: {wins}\n"
        "🔫 Убийства: {kills}\n"
        "🎮 Матчи: {matches}\n"
        "📊 WinRate: {win_rate}%\n"
    ),
    Commands.shop: ""
   }