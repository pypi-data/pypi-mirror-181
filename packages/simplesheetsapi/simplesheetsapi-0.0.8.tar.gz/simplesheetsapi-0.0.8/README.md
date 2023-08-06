# Простой фреймворк для работы с api google spreadsheets

---
### Перед использованием:

+ зайти на https://developers.google.com/sheets/api/quickstart/python#enable_the_api и выполнить инструкции по получению credentials.json

+ credentials.json должен находиться в одной папке с программой

---
## Установка
    pip install simplesheetsapi
---

## Работа с фреймворком
+ Инициализация:
```python 
sheet = SheetsApiTry("id_таблицы", os.getcwd())
```

+ Получение содержимого ячейки:
```python 
print(sheet.get_cell_value("колонка", "строка", "название_листа")
```

+ Установка содержимого ячеек:
```python 
sheet.update_cell("ячейка_начала:ячейка_конца", "название_листа", [[значения_строки_1, ...], [значения_строки_2, ...]])
```

+ Поиск строк по значению в каких-то её ячейках:
```python 
print(sheet.find_rows("поисковое_значение", "название_листа"))
```

---

## По вопросам можно писать:
- [Вконтакте](https://vk.com/krokokroko)
- [Телеграмм](https://t.me/Therealkroko): Therealkroko

---
## Код можно посмотреть нажав [сюда](https://github.com/Kroko72/sheetsapitry)