# Pandito Бот

## Запуск

1. Склонировать репозиторий и перейти в него:

    ```
    git clone https://github.com/whatochka/pandito_bot
    cd ./pandito_bot
    ```

2. Создать и заполнить файл `.env` в корневой папке (пример: `.env.example`)
    ```
    BOT_TOKEN=Token
    OWNER_ID=123456789
    DB_URL=postgresql+psycopg://user:password@address:port/name
    DB_NAME=name
    DB_USER=user
    DB_PASSWORD=password
    ```
3. Иметь установленный [Docker Engine](https://docs.docker.com/engine/) и [docker compose v2](https://docs.docker.com/compose/releases/migrate/)
4. Собрать и запустить:

    ```
    docker compose up -d --build
    ```


## Команды

`/start` `/menu` `/profile` `/balance` `/me` - Старт
`/help` - Описание бота
`/shop` - Товары на продаже
`/cart` - Купленные товары
`/transfer` - Перевод денег между юзерами
`/task` - Активное задание
`/id` - Куркод с диплинком на юзера
`/secret <phrase>` - Ввод секрета

`/admin` `/panel` - Админ панель
`/broadcast` - Рассылка

`/product <name> <price> <stock> <description>` - Создать товар  СТАРОЕ
`/list_products` - Список товаров  СТАРОЕ
`/delete_product <product_id>` - Удалить товар  СТАРОЕ
`/price <product_id> <new_price>` - Изменить цену товара product_id на new_price  СТАРОЕ
`/stock <product_id> <new_stock>` - Изменить количество товара на складе  СТАРОЕ

`/money <user_id> <amount>` - Прибавить amount пятаков юзеру user_id  СТАРОЕ
`/logs <user_id>` - Логи юзера  СТАРОЕ
