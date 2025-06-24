import pyqrcode
import png

qr = pyqrcode.create("https://www.google.com/search?q=John+Doe")
qr.png("static/qrcodes/1.png", scale=6)
print('✅ QR code generated.')