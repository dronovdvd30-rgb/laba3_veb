from flask import Flask, render_template, request, session
from PIL import Image;import matplotlib.pyplot as plt;import random
app = Flask(__name__);app.secret_key = "lab3"
def graph(image, name):
    r, g, b = image.split()
    plt.figure();plt.plot(r.histogram(), "r"); plt.plot(g.histogram(), "g"); plt.plot(b.histogram(), "b")
    plt.title("RGB"); plt.xlabel("Интенсивность"); plt.ylabel("Количество пикселей")
    plt.savefig(app.static_folder + "/" + name); plt.close()
@app.route("/", methods=["GET", "POST"])
def index():
    result = False;error = None 
    if request.method == "POST":
        if request.form["captcha"] == str(session["answer"]):
            image = Image.open(request.files["image"]).convert("RGB")
            rotated = image.rotate(int(request.form["angle"]), expand=True, fillcolor="white")
            image.save(app.static_folder + "/original.png");rotated.save(app.static_folder + "/rotated.png")
            graph(image, "graph1.png"); graph(rotated, "graph2.png")
            result = True
        else:
            error = "Неверная CAPTCHA"
    a = random.randint(1, 9); b = random.randint(1, 9);session["answer"] = a + b
    return render_template("index.html", data=result, error=error, captcha=f"{a} + {b}")
if __name__ == "__main__":app.run(debug=True)