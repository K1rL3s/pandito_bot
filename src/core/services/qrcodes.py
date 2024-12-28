from io import BytesIO

from qrcode.constants import ERROR_CORRECT_L
from qrcode.image.pure import PyPNGImage
from qrcode.main import QRCode


class QRCodeService:
    def __init__(self) -> None:
        self.qr = QRCode(
            version=None,
            error_correction=ERROR_CORRECT_L,
            box_size=8,
            border=4,
            image_factory=PyPNGImage,
        )

    def generate_qrcode(self, user_id: int, bot_name: str) -> BytesIO:
        self.qr.clear()

        deeplink = f"https://t.me/{bot_name}?start={user_id}"
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
        data = generator.generate_qrcode(2015866626, "pandito_bot")
        f.write(data.getvalue())
