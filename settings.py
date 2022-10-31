from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
CHANNELS = env.list("CHANNELS")  # Тут у нас будет список чатов куда необходимо отправлять
AUTH_MSG = env.str("AUTH_MSG")  # Секретное сообщение в гитлабе
