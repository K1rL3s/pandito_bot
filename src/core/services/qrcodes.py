from io import BytesIO
from typing import Any

from qrcode.constants import ERROR_CORRECT_L
from qrcode.image.pure import PyPNGImage
from qrcode.main import QRCode

from core.ids import UserId

_UserIdPrefix = "id_"
_TaskIdPrefix = "task_"


class QRCodeService:
    def __init__(self) -> None:
        self.qr = QRCode(
            version=None,
            error_correction=ERROR_CORRECT_L,
            box_size=8,
            border=4,
            image_factory=PyPNGImage,
        )

    def user_id_qrcode(self, bot_name: str, user_id: UserId) -> BytesIO:
        return self._generate_qrcode(bot_name, _UserIdPrefix, user_id)

    def task_id_qrcode(self, bot_name: str, task_id: UserId) -> BytesIO:
        return self._generate_qrcode(bot_name, _TaskIdPrefix, task_id)

    def _generate_qrcode(self, bot_name: str, prefix: str, data: Any) -> BytesIO:
        self.qr.clear()

        deeplink = f"https://t.me/{bot_name}?start={prefix}{data}"
        self.qr.add_data(deeplink)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white")

        self.qr.clear()

        stream = BytesIO()
        img.save(stream=stream)

        return stream


if __name__ == "__main__":
    generator = QRCodeService()
    with open("test.png", "wb") as f:
        image = generator.user_id_qrcode("pandito_bot", 2015866626)
        f.write(image.getvalue())
