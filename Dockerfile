# Использовать официальную среду выполнения Python в качестве родительского образа 
FROM python:3.8 

# Установить рабочий каталог в контейнере 
WORKDIR /usr/src/app 

# Скопировать содержимое текущего каталога в контейнер в /usr/src/app 
COPY . . 

# Установить все необходимые пакеты, указанные в requirements.txt 
RUN pip install --no-cache-dir -r requirements.txt 

# Запустить python.py, когда контейнер запустит 
CMD ["python", "./main.py"]
