from flask import Flask, render_template, request, session
from PIL import Image;from io import BytesIO;import base64;import math;import random;import os
import matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
app = Flask(__name__);app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.secret_key = os.environ.get("SECRET_KEY", "lab3-local-secret")
def to_html(image):
    buffer = BytesIO();image.save(buffer, "PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
def histogram(image):
    fig, ax = plt.subplots()
    for channel, color in zip(image.split(), ("red", "green", "blue")):
        ax.plot(channel.histogram(), color=color)
    ax.set(title="Распределение цветов RGB",xlabel="Интенсивность (0–255)",ylabel="Количество пикселей")
    ax.grid(alpha=0.3);buffer = BytesIO();fig.savefig(buffer, format="png");plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
@app.route("/", methods=["GET", "POST"])
def index():
    data = {}
    error = None
    if request.method == "POST":
        try:
            answer = session.pop("answer", None)
            if answer is None or request.form.get("captcha") != str(answer):
                raise ValueError("Неверный ответ CAPTCHA.")
            angle = float(request.form["angle"])
            if not math.isfinite(angle) or abs(angle) > 360:
                raise ValueError("Угол должен быть от -360 до 360.")
            image = Image.open(request.files["image"].stream)
            if image.format not in ("JPEG", "PNG"):
                raise ValueError("Выберите JPG или PNG.")
            if image.width * image.height > 20_000_000:
                raise ValueError("Изображение слишком большое.")
            image = image.convert("RGB");rotated = image.rotate(angle, expand=True, fillcolor="white")
            data = {"original": to_html(image),"rotated": to_html(rotated),"graph1": histogram(image),"graph2": histogram(rotated)}
        except (ValueError, KeyError, OSError) as exc:
            error = str(exc) or "Проверьте файл и угол поворота."
    a, b = random.randint(1, 9), random.randint(1, 9)
    session["answer"] = a + b
    return render_template("index.html", data=data, error=error, captcha=f"{a} + {b}")
@app.errorhandler(413)
def too_large(error):return "Файл больше 10 МБ.", 413
if __name__ == "__main__":app.run(debug=True)