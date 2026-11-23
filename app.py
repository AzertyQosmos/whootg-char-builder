import streamlit as st
import json

st.set_page_config(page_title="Wandering Heroes of Ogre Gate - Лист персонажа", layout="wide")

# Инициализация хранилища данных в сессии
if "char_data" not in st.session_state:
    st.session_state.char_data = {}

# Функция для получения текущего значения (из загруженного JSON или по умолчанию)
def get_val(key, default=""):
    return st.session_state.char_data.get(key, default)

def get_num(key, default=0):
    return st.session_state.char_data.get(key, default)

st.title("🐉 Создание персонажа: Wandering Heroes of Ogre Gate")

# Боковая панель для загрузки и сброса
with st.sidebar:
    st.header("📁 Управление файлом")
    uploaded_file = st.file_uploader("Загрузить персонажа (JSON)", type=["json"])
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            st.session_state.char_data = data
            st.success("Персонаж успешно загружен!")
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка загрузки: {e}")
            
    if st.button("🗑️ Очистить все поля", use_container_width=True):
        st.session_state.char_data = {}
        st.rerun()

# Создаем вкладки для удобства
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📜 Основное", 
    "💪 Характеристики и Защита", 
    "📖 Навыки", 
    "👊 Боевые техники и Стойки", 
    "🎒 Снаряжение и История"
])

# Собираем все данные в один словарь при каждом изменении
data = {}

with tab1:
    st.subheader("Личные данные")
    col1, col2, col3 = st.columns(3)
    with col1:
        data["Name"] = st.text_input("Имя", value=get_val("Name"))
        data["Nickname"] = st.text_input("Прозвище", value=get_val("Nickname"))
        data["HtWt"] = st.text_input("Рост / Вес", value=get_val("HtWt"))
        data["Homeland"] = st.text_input("Родина / Клан", value=get_val("Homeland"))
        data["Occupation"] = st.text_input("Профессия", value=get_val("Occupation"))
        data["Reputation"] = st.text_input("Репутация", value=get_val("Reputation"))
    with col2:
        data["MartialName"] = st.text_input("Боевое имя", value=get_val("MartialName"))
        data["Sifu"] = st.text_input("Сифу (Учитель)", value=get_val("Sifu"))
        data["Sex"] = st.text_input("Пол", value=get_val("Sex"))
        data["Sect"] = st.text_input("Секта", value=get_val("Sect"))
        data["Family"] = st.text_input("Семья", value=get_val("Family"))
        data["Age"] = st.text_input("Возраст", value=get_val("Age"))
    with col3:
        data["Player"] = st.text_input("Игрок", value=get_val("Player"))
        data["Title"] = st.text_input("Титулы", value=get_val("Title"))
        data["Campaign"] = st.text_input("Кампания", value=get_val("Campaign"))
    
    st.divider()
    st.subheader("Раны и Ци")
    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        data["MaxWounds"] = st.text_input("Макс. Раны", value=get_val("MaxWounds"))
        data["CurrentWounds"] = st.text_input("Текущие Раны", value=get_val("CurrentWounds"))
    with col_w2:
        data["Qi"] = st.number_input("Уровень Ци (Qi)", min_value=1, max_value=6, value=get_num("Qi", 1))
        data["Imbalance"] = st.text_input("Дисбаланс (Imbalance Rating)", value=get_val("Imbalance"))

with tab2:
    st.subheader("Защита (Defenses)")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        data["Hardiness"] = st.text_input("Стойкость (Hardiness)", value=get_val("Hardiness"))
        data["Parry"] = st.text_input("Парирование (Parry)", value=get_val("Parry"))
        data["Evade"] = st.text_input("Уклонение (Evade)", value=get_val("Evade"))
    with col_d2:
        data["Stealth"] = st.text_input("Скрытность (Stealth)", value=get_val("Stealth"))
        data["Wits"] = st.text_input("Сообразительность (Wits)", value=get_val("Wits"))
        data["Resolve"] = st.text_input("Решимость (Resolve)", value=get_val("Resolve"))

    st.divider()
    st.subheader("Характеристики (Attributes)")
    st.caption("Всего 3 кружка на навык (0-3)")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("**Физические (Physical)**")
        phys_skills = ["Athletics", "Swim", "Speed", "Muscle", "Endurance", "Ride", "Sail"]
        for skill in phys_skills:
            data[f"Phys_{skill}"] = st.slider(skill, 0, 3, value=get_num(f"Phys_{skill}"))
    with col_a2:
        st.markdown("**Знания (Knowledge)**")
        know_skills = ["History 1", "History 2", "Creatures 1", "Creatures 2", "Places/Cultures 1", "Places/Cultures 2", 
                       "Martial Disciplines 1", "Martial Disciplines 2", "Institutions 1", "Institutions 2", 
                       "Language 1", "Language 2", "Read Script 1", "Read Script 2", "Religion/Gods 1", "Religion/Gods 2", "Classics 1", "Classics 2"]
        for skill in know_skills:
            data[f"Know_{skill}"] = st.slider(skill, 0, 3, value=get_num(f"Know_{skill}"))

with tab3:
    st.subheader("Боевые навыки (Combat)")
    combat_skills = ["Arm Strike", "Leg Strike", "Grapple", "Throw", "Light Melee", "Medium Melee", "Heavy Melee", "Small Ranged", "Large Ranged"]
    col_c1, col_c2, col_c3 = st.columns(3)
    for i, skill in enumerate(combat_skills):
        with [col_c1, col_c2, col_c3][i % 3]:
            data[f"Combat_{skill}"] = st.slider(skill, 0, 3, value=get_num(f"Combat_{skill}"))

    st.divider()
    st.subheader("Специальные навыки (Specialist)")
    spec_skills = ["Medicine", "Divination", "Meditation", "Talent 1", "Talent 2", "Trade 1", "Trade 2", 
                   "Survival 1", "Survival 2", "Ritual 1", "Ritual 2", "Ritual 3"]
    col_s1, col_s2, col_s3 = st.columns(3)
    for i, skill in enumerate(spec_skills):
        with [col_s1, col_s2, col_s3][i % 3]:
            data[f"Spec_{skill}"] = st.slider(skill, 0, 3, value=get_num(f"Spec_{skill}"))

    st.divider()
    st.subheader("Ментальные навыки (Mental)")
    ment_skills = ["Command", "Persuade", "Deception", "Empathy", "Reasoning", "Detect"]
    col_m1, col_m2, col_m3 = st.columns(3)
    for i, skill in enumerate(ment_skills):
        with [col_m1, col_m2, col_m3][i % 3]:
            data[f"Ment_{skill}"] = st.slider(skill, 0, 3, value=get_num(f"Ment_{skill}"))

    st.divider()
    st.subheader("Экспертиза (Expertise)")
    data["Expertise_General"] = st.text_area("Общая экспертиза", value=get_val("Expertise_General"), height=100)

with tab4:
    st.subheader("Кунг-фу техники (Kung Fu Techniques)")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        data["Tech_Normal"] = st.text_area("Обычные (Normal)", value=get_val("Tech_Normal"), height=300)
    with col_t2:
        data["Tech_Counter"] = st.text_area("Контратаки (Counter)", value=get_val("Tech_Counter"), height=300)
    with col_t3:
        data["Tech_Stance"] = st.text_area("Стойки (Stance)", value=get_val("Tech_Stance"), height=300)

with tab5:
    st.subheader("Снаряжение (Equipment)")
    data["Equipment"] = st.text_area("Инвентарь", value=get_val("Equipment"), height=200)

    st.divider()
    st.subheader("Деньги (Money)")
    col_mo1, col_mo2, col_mo3, col_mo4 = st.columns(4)
    with col_mo1: data["Money_Taels"] = st.text_input("Taels", value=get_val("Money_Taels"))
    with col_mo2: data["Money_Imperials"] = st.text_input("Imperials", value=get_val("Money_Imperials"))
    with col_mo3: data["Money_Spades"] = st.text_input("Spades", value=get_val("Money_Spades"))
    with col_mo4: data["Money_Liangs"] = st.text_input("Liangs (Бумажные)", value=get_val("Money_Liangs"))

    st.divider()
    st.subheader("Семья (Family)")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        data["Family_Siblings"] = st.text_input("Кол-во братьев/сестер", value=get_val("Family_Siblings"))
        data["Family_BirthOrder"] = st.text_input("Порядок рождения", value=get_val("Family_BirthOrder"))
        data["Family_Mother"] = st.text_input("Мать", value=get_val("Family_Mother"))
        data["Family_Father"] = st.text_input("Отец", value=get_val("Family_Father"))
    with col_f2:
        data["Family_Sister"] = st.text_input("Сестра(ы)", value=get_val("Family_Sister"))
        data["Family_Brother"] = st.text_input("Брат(ы)", value=get_val("Family_Brother"))
        data["Family_Sworn"] = st.text_input("Названная семья", value=get_val("Family_Sworn"))
        data["Family_Other"] = st.text_area("Другое", value=get_val("Family_Other"), height=68)

    st.divider()
    st.subheader("Опыт и Обиды (Experience & Grudges)")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        data["Experience"] = st.text_area("Опыт", value=get_val("Experience"), height=150)
    with col_e2:
        data["Grudges"] = st.text_area("Обиды / Враги", value=get_val("Grudges"), height=150)
        data["Flaws"] = st.text_area("Изъяны (Flaws)", value=get_val("Flaws"), height=68)

# Обновляем данные в сессии
st.session_state.char_data.update(data)

# Кнопка скачивания JSON
st.divider()
json_str = json.dumps(st.session_state.char_data, ensure_ascii=False, indent=4)
st.download_button(
    label="💾 Скачать персонажа в JSON",
    data=json_str,
    file_name=f"{st.session_state.char_data.get('Name', 'hero')}_ogre_gate.json",
    mime="application/json",
    type="primary",
    use_container_width=True
)