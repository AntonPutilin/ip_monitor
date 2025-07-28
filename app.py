import streamlit as st
import requests

# Заголовок приложения
st.set_page_config(page_title="IP Monitor", page_icon="🌐")
st.title("🌐 Мониторинг Публичного IP-адреса")

def get_public_ip():
    """Получает текущий публичный IP-адрес из внешнего сервиса."""
    try:
        # Используем сервис, который возвращает IP в текстовом виде
        response = requests.get("https://api.ipify.org", timeout=5)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.text.strip()
    except requests.RequestException:
        return "Ошибка сети"

# --- Логика приложения ---

# Используем состояние сессии, чтобы "помнить" предыдущий IP
# Инициализируем, если еще не было установлено
if 'previous_ip' not in st.session_state:
    st.session_state.previous_ip = None

# Получаем текущий IP
current_ip = get_public_ip()

# Отображаем текущий IP с помощью виджета st.metric
st.metric(label="Текущий IP-адрес", value=current_ip)

# Сравниваем с предыдущим IP из состояния сессии
if st.session_state.previous_ip is not None:
    if current_ip != st.session_state.previous_ip and current_ip != "Ошибка сети":
        st.success(f"✅ IP-адрес изменился! Предыдущий был: {st.session_state.previous_ip}")
    elif current_ip != "Ошибка сети":
        st.info("ℹ️ IP-адрес не изменился.")

# Обновляем "предыдущий" IP в состоянии сессии на текущий
if current_ip != "Ошибка сети":
    st.session_state.previous_ip = current_ip

# Кнопка для ручного обновления страницы
st.button("🔄 Обновить")

# Добавляем небольшую инструкцию
st.caption("Нажмите кнопку 'Обновить', чтобы перепроверить IP-адрес.")