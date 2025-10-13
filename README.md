
# Payment CSV Processor

Процесс для обработки больших CSV-файлов с платежами. Поддерживает **постраничную обработку**, конвертацию валют, агрегацию по клиентам и категориям, а также безопасное сохранение в JSON.

---

## Структура проекта

```
FilesCertification/
│
├─ main.py                # CLI-запуск процесса
├─ processing.py          # Класс PaymentProcessor
├─ storage.py # Хранилище агрегатов в одном JSON
├─ aggregator.py          # Класс Aggregator (агрегация по клиентам и категориям)
├─ config.py              # Конфигурация проекта (пути, chunk_size, курсы валют)
├─ csv_reader.py          # CSVChunkReader — чтение CSV по чанкам
├─ converter.py           # CurrencyConverter — конвертация в RUB
├─ validator.py           # Validator — валидация строк CSV
├─ generate_data.py       # Генерация тестового CSV
├─ tests/                 # Тесты проекта
│   ├─ test_processing.py
│   └─ test_storage.py
└─ README.md
```

---

## Описание модулей

### main.py

CLI-интерфейс для запуска обработки CSV:

```bash
python main.py --input payments.csv --chunk-size 10000 --output-aggregates aggregates.ndjson --offset-file offset.txt
```

### processing.py

`PaymentProcessor` — основной пайплайн:

* Постраничное чтение CSV
* Валидация строк (`Validator`)
* Конвертация валют (`CurrencyConverter`)
* Агрегация (`Aggregator`) и сохранение (`Storage`)
* Логирование ошибок и прогресса через `loguru`

### storage.py

`Storage` для безопасного сохранения агрегатов в **один NDJSON-файл**:

* Поддержка атомарных записей
* Поддержка больших файлов без полной загрузки в память
* Методы: `apply_batch(agg: Aggregator)`, `get_summary()`

### aggregator.py

`Aggregator`:

* Суммирует и считает количество платежей по `client_id`
* Суммирует платежи по `category`
* Поддерживает слияние (`merge`) нескольких агрегатов

### csv\_reader.py

`CSVChunkReader`:

* Чтение CSV по чанкам (постранично)
* Поддержка `start_offset` для возобновления обработки

### converter.py

`CurrencyConverter`:

* Конвертация `amount` в RUB по курсам валют

### validator.py

`Validator`:

* Пропускает строки с:

  * статусом ≠ `completed`
  * невалидной суммой
  * неподдерживаемой валютой

### generate\_data.py

Генерация CSV с тестовыми платежами для проверки проекта

---

## Логирование

* **Ошибки**: `errors.log`
* **Прогресс**: `progress.log` и консоль

Формат прогресса:

```
Мы обработали 12345/50000 записей (24.69%)
```

## Как запускать

1. Установить зависимости:

```bash
pip install loguru
```

2. Сгенерировать CSV:

```bash
python generate_data.py
```

3. Запустить обработку:

```bash
python main.py --input payments.csv --chunk-size 10000 --output-aggregates aggregates.ndjson --offset-file offset.txt
```

4. Проверить `aggregates.ndjson`, `progress.log`, `errors.log`.

---
