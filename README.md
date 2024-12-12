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
    REDIS_PASSWORD=password
    ```
3. Иметь установленный [Docker Engine](https://docs.docker.com/engine/) и [docker compose v2](https://docs.docker.com/compose/releases/migrate/)
4. Собрать и запустить:

    ```
    docker compose up -d --build
    ```


## Команды

`/menu` `/profile` `/balance` `/me`
`/broadcast <message>`
`/delete_product <product_id>`
`/list_products`
`/list_users`
`/logs <user_id>`
`/money <user_id> <amount>` - прибавляет amount коинов
`/price <product_id> <new_price>`
`/product <name> <price> <stock> <description>`
`/stage <user_id> <stage>`
`/stock <product_id> <new_stock>`
`/secret <phrase>`
`/list_secrets`
`/delete_secret <id>`
`/id` - куркод с диплинком на айди
`/help`