from app import app;from PIL import Image
def test_page(): assert app.test_client().get("/").status_code == 200 # Тест 1: Проверка, что сайт вообще открывается
def test_captcha(): #Тест 2: Проверка неверной капчи
    client = app.test_client();client.get("/")
    assert "Неверная CAPTCHA".encode() in client.post("/", data={"captcha": "999"}).data
def test_rotation(): #Тест 3: Проверка поворота картинки
    client = app.test_client();client.get("/")
    with client.session_transaction() as s: answer = s["answer"]
    with open(app.static_folder + "/original.png", "rb") as image: client.post("/", data={"image": image, "angle": "90", "captcha": str(answer)})
    assert Image.open(app.static_folder + "/rotated.png").size == Image.open(app.static_folder + "/original.png").size[::-1]