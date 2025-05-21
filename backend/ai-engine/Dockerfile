FROM python:3.13.3-slim-bookworm

WORKDIR /app

# сначала обновляем pip и setuptools (pkg_resources попадёт в систему),
# а затем ставим все зависимости одним таргетом
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools \
 && pip install --no-cache-dir -r requirements.txt

# копируем исходники
COPY . .

# команда запуска
CMD ["python", "main.py"]
