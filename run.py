from spongebobcards.main import app
from spongebobcards import config

app.config.update(
    DEBUG=True
)

app.run(
    port=5000,
    host='0.0.0.0'
)
