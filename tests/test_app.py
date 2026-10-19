import sys;from pathlib import Path
from io import BytesIO;from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app
def test_page():
    client = app.test_client();response = client.get("/")
    assert response.status_code == 200
def test_captcha():
    client = app.test_client();client.get("/")
    response = client.post("/", data={"captcha": "999"})
    assert "Неверный ответ CAPTCHA" in response.get_data(as_text=True)
def test_rotation():
    client = app.test_client();client.get("/")
    with client.session_transaction() as session:
        answer = session["answer"]
    image = Image.new("RGB", (100, 50), "red")
    buffer = BytesIO();image.save(buffer, "PNG");buffer.seek(0)
    response = client.post("/", data={"image": (buffer, "test.png"),"angle": "90","captcha": str(answer)})
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert html.count("data:image/png;base64,") == 4