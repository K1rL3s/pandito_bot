def menu_text(uid: int, balance: int, stage: int, is_admin: bool = False) -> str:
    text = f"<b>Главное меню</b>\n\nВаш id: {uid}\nБаланс: {balance} <b>Ит</b>."
    if stage == 1:
        text += "\n\n<u>Вы — этапщик</u>\n"
    elif stage == 2:
        text += "\n\n<u>Вы — продавец</u>\n"
    elif stage == 3:
        text += "\n\n<u>Вы — RTUITLab</u>\n"
    elif is_admin:
        text += "\n\n<u>Вы — администратор</u>\n"
    return text
