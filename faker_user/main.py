from fastapi import FastAPI, Form, Request, Cookie, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from faker import Faker
from utils import rename, generate, download_file
from localisation.reader import translate

app = FastAPI() # Екземпляр класу API

# Налаштування розташування статичних файлів і шаблонів
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Ендпоінт - home_page бере локалізацію значення функції, яка завантажує значення мови з кукі
# Повертає користувачу .html шаблон з формою для заповнення данних або змінення локалізації
@app.get("/home_page", response_class=HTMLResponse)
async def show_form(request: Request, locate: str = Cookie(default="en_US")):
    texts = await translate(locate)
    request = templates.TemplateResponse("form.html", {"request": request, "texts": texts})
    return request

# Ендпоінт для встановлення кукі-файлів на сервері зі значенням вказаним в формі, і повертає користувача на попередню сторінку
@app.get('/set_cookie_file')
async def set_cookies(request: Request, locate: str = "en_US"):
    response = RedirectResponse(url="/home_page")
    response.set_cookie(key='locate', value=locate)
    
    return response

# Ендпоінт для відображення згенерованої інформації для користувача
@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    locate: str = Cookie(default="en_US"), # locate - мова, якою хоче відображати для себе користувач, і передає її у ф-ю translate
    locale: str = Form(default="en_US"), # locale - данні під певну країну
    checkbox1: bool = Form(default=None),
    checkbox2: bool = Form(default=None),
    checkbox3: bool = Form(default=None),
    checkbox4: bool = Form(default=None),
    checkbox5: bool = Form(default=None),
    checkbox6: bool = Form(default=None),
    checkbox7: bool = Form(default=None),
    checkbox8: bool = Form(default=None),
    checkbox9: bool = Form(default=None),
    SLD: str = Form(default='example'),
    TLD: str = Form(default='org'),
    selected_complexity: int = Form(default=2), 
    len_password: int = Form(default=8),
):
    fake = Faker(locale) # Екземпляр класу бібліотеки для генерування фейкових данних
    texts = await translate(locate) # Повертає json файл з перекладом
    generated_data = {} # Словник із згенерованими данними
    if checkbox1:
        generated_data['first_name'] = fake.first_name()

    if checkbox2:
        generated_data['last_name'] = fake.last_name()

    if checkbox3:
        generated_data['email'] = await rename(fake.email(), SLD, TLD) # використовує додаткові параметри для задання уточнень про генерацію emeil

    if checkbox4:
        generated_data['phone_number'] = fake.phone_number()

    if checkbox5:
        generated_data['address'] = fake.address()

    if checkbox6:
        generated_data['postalcode'] = fake.postcode()

    if checkbox7:
        generated_data['date_of_birth'] = fake.date_of_birth().strftime('%Y-%m-%d')

    if checkbox8:
        generated_data['login'] = fake.user_name()

    if checkbox9:
        generated_data['password'] = generate(selected_complexity, len_password) 


    if generated_data:
        await download_file(generated_data)
        return templates.TemplateResponse("result.html", {"request": request, "generated_data": generated_data, 'texts': texts})
    # Повернення помилки статусу 400, якщо користувач не вибрав данні для генерації (відправив пустий словник)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The generated data cannot be empty")

@app.get("/download", response_class=FileResponse)
async def download_generated_file():
    file_path = "data.txt" 
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream", 
        filename="data.txt" 
    )