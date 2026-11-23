import json
import streamlit as st

st.set_page_config(
    page_title="Wandering Heroes of Ogre Gate — Лист персонажа",
    page_icon="⚔️",
    layout="wide",
)

# --- Справочные структуры полей на основе оригинального листа ---
DEFENSES_CONFIG = [
    ("hardiness", "Стойкость (Hardiness)", 3),
    ("parry", "Парирование (Parry)", 3),
    ("evade", "Уклонение (Evade)", 3),
    ("stealth", "Скрытность (Stealth)", 6),
    ("wits", "Смекалка (Wits)", 6),
    ("resolve", "Решимость (Resolve)", 6),
]

COMBAT_SKILLS = [
    ("arm_strike", "Удар рукой (Arm Strike)"),
    ("leg_strike", "Удар ногой (Leg Strike)"),
    ("grapple", "Захват (Grapple)"),
    ("throw", "Бросок (Throw)"),
    ("light_melee", "Лёгкое ближнее (Light Melee)"),
    ("medium_melee", "Среднее ближнее (Medium Melee)"),
    ("heavy_melee", "Тяжёлое ближнее (Heavy Melee)"),
    ("small_ranged", "Малое дальнобойное (Small Ranged)"),
    ("large_ranged", "Крупное дальнобойное (Large Ranged)"),
]

SPECIALIST_FIXED = [
    ("medicine", "Медицина (Medicine)"),
    ("divination", "Предсказание (Divination)"),
    ("meditation", "Медитация (Meditation)"),
]

SPECIALIST_CUSTOM = [
    ("talent_1", "Талант 1 (Talent)"),
    ("talent_2", "Талант 2 (Talent)"),
    ("trade_1", "Ремесло 1 (Trade)"),
    ("trade_2", "Ремесло 2 (Trade)"),
    ("survival_1", "Выживание 1 (Survival)"),
    ("survival_2", "Выживание 2 (Survival)"),
    ("ritual_1", "Ритуал 1 (Ritual)"),
    ("ritual_2", "Ритуал 2 (Ritual)"),
    ("ritual_3", "Ритуал 3 (Ritual)"),
]

MENTAL_SKILLS = [
    ("command", "Командование (Command)"),
    ("persuade", "Убеждение (Persuade)"),
    ("deception", "Обман (Deception)"),
    ("empathy", "Эмпатия (Empathy)"),
    ("reasoning", "Логика (Reasoning)"),
    ("detect", "Проницательность / Поиск (Detect)"),
]

PHYSICAL_SKILLS = [
    ("athletics", "Атлетика (Athletics)"),
    ("swim", "Плавание (Swim)"),
    ("speed", "Скорость (Speed)"),
    ("muscle", "Мускулы (Muscle)"),
    ("endurance", "Выносливость (Endurance)"),
    ("ride", "Верховая езда (Ride)"),
    ("sail", "Мореходство (Sail)"),
]

KNOWLEDGE_GROUPS = [
    ("history_1", "История 1 (History)"),
    ("history_2", "История 2 (History)"),
    ("creatures_1", "Существа 1 (Creatures)"),
    ("creatures_2", "Существа 2 (Creatures)"),
    ("places_1", "Места и культуры 1 (Places/Cultures)"),
    ("places_2", "Места и культуры 2 (Places/Cultures)"),
    ("disciplines_1", "Боевые школы 1 (Martial Disciplines)"),
    ("disciplines_2", "Боевые школы 2 (Martial Disciplines)"),
    ("institutions_1", "Организации 1 (Institutions)"),
    ("institutions_2", "Организации 2 (Institutions)"),
    ("language_1", "Язык 1 (Language)"),
    ("language_2", "Язык 2 (Language)"),
    ("script_1", "Письменность 1 (Read Script)"),
    ("script_2", "Письменность 2 (Read Script)"),
    ("religion_1", "Религия и боги 1 (Religion/Gods)"),
    ("religion_2", "Религия и боги 2 (Religion/Gods)"),
    ("classics_1", "Классические трактаты 1 (Classics)"),
    ("classics_2", "Классические трактаты 2 (Classics)"),
]

INTERNAL_ARTS = [
    ("dianxue", "Дяньсюэ (Dianxue)"),
    ("waijia", "Вайцзя (Waijia)"),
    ("qinggong", "Цингун (Qinggong)"),
    ("neigong", "Нэйгун (Neigong)"),
]


def get_default_data() -> dict:
    data = {
        # Личная информация
        "name": "",
        "martial_name": "",
        "nickname": "",
        "sifu": "",
        "player": "",
        "ht_wt": "",
        "sex": "",
        "titles": "",
        "campaign": "",
        "homeland_clan": "",
        "sect": "",
        "occupation": "",
        "family_short": "",
        "reputation": "",
        "age": "",
        # Здоровье и Ци
        "qi": 1,
        "max_wounds_auto": True,
        "max_wounds": 3,
        "current_wounds": 0,
        "imbalance_rating": 0,
        "imbalance_points": 0,
        "imbalance_bonus_qi": 1,
        # Защиты
        "defenses": {
            key: {"base": base, "mod1": 0, "mod2": 0, "auto": True, "total": base}
            for key, _, base in DEFENSES_CONFIG
        },
        # Навыки
        "combat_skills": {key: 0 for key, _ in COMBAT_SKILLS},
        "combat_expertise": "",
        "specialist_fixed": {key: 0 for key, _ in SPECIALIST_FIXED},
        "specialist_custom": {key: {"spec": "", "val": 0} for key, _ in SPECIALIST_CUSTOM},
        "specialist_expertise": "",
        "mental_skills": {key: 0 for key, _ in MENTAL_SKILLS},
        "mental_expertise": "",
        "physical_skills": {key: 0 for key, _ in PHYSICAL_SKILLS},
        "physical_expertise": "",
        "knowledge_skills": {key: {"spec": "", "val": 0} for key, _ in KNOWLEDGE_GROUPS},
        "knowledge_expertise": "",
        # Внутренние стили и техники
        "internal_arts": {key: 0 for key, _ in INTERNAL_ARTS},
        "combat_techniques": "",
        "flaws": "",
        # Семья, обиды, снаряжение, деньги, опыт
        "family": {
            "siblings": "",
            "birth_order": "",
            "mother": "",
            "father": "",
            "sisters": "",
            "brothers": "",
            "sworn_family": "",
            "others": "",
        },
        "grudges": "",
        "equipment": "",
        "money": {
            "taels": "",
            "imperials": "",
            "spades": "",
            "liangs": "",
            "paper_currency": "",
        },
        "experience": "",
        # Техники кунг-фу (таблица)
        "kung_fu_techniques": [
            {"normal": "", "counter": "", "stance": ""} for _ in range(8)
        ],
    }
    return data


def sync_state_from_dict(data: dict):
    defaults = get_default_data()

    # Простые поля
    simple_keys = [
        "name", "martial_name", "nickname", "sifu", "player",
        "ht_wt", "sex", "titles", "campaign", "homeland_clan",
        "sect", "occupation", "family_short", "reputation", "age",
        "qi", "max_wounds_auto", "max_wounds", "current_wounds",
        "imbalance_rating", "imbalance_points", "imbalance_bonus_qi",
        "combat_expertise", "specialist_expertise", "mental_expertise",
        "physical_expertise", "knowledge_expertise",
        "combat_techniques", "flaws", "grudges", "equipment", "experience",
    ]
    for k in simple_keys:
        st.session_state[f"w_{k}"] = data.get(k, defaults[k])

    # Защиты
    def_data = data.get("defenses", {})
    for key, _, base in DEFENSES_CONFIG:
        item = def_data.get(key, defaults["defenses"][key])
        st.session_state[f"w_def_{key}_base"] = int(item.get("base", base))
        st.session_state[f"w_def_{key}_mod1"] = int(item.get("mod1", 0))
        st.session_state[f"w_def_{key}_mod2"] = int(item.get("mod2", 0))
        st.session_state[f"w_def_{key}_auto"] = bool(item.get("auto", True))
        st.session_state[f"w_def_{key}_total"] = int(item.get("total", base))

    # Навыки
    for key, _ in COMBAT_SKILLS:
        st.session_state[f"w_cskill_{key}"] = int(data.get("combat_skills", {}).get(key, 0))

    for key, _ in SPECIALIST_FIXED:
        st.session_state[f"w_sskill_{key}"] = int(data.get("specialist_fixed", {}).get(key, 0))

    for key, _ in SPECIALIST_CUSTOM:
        item = data.get("specialist_custom", {}).get(key, {"spec": "", "val": 0})
        st.session_state[f"w_scust_{key}_spec"] = item.get("spec", "")
        st.session_state[f"w_scust_{key}_val"] = int(item.get("val", 0))

    for key, _ in MENTAL_SKILLS:
        st.session_state[f"w_mskill_{key}"] = int(data.get("mental_skills", {}).get(key, 0))

    for key, _ in PHYSICAL_SKILLS:
        st.session_state[f"w_pskill_{key}"] = int(data.get("physical_skills", {}).get(key, 0))

    for key, _ in KNOWLEDGE_GROUPS:
        item = data.get("knowledge_skills", {}).get(key, {"spec": "", "val": 0})
        st.session_state[f"w_kskill_{key}_spec"] = item.get("spec", "")
        st.session_state[f"w_kskill_{key}_val"] = int(item.get("val", 0))

    for key, _ in INTERNAL_ARTS:
        st.session_state[f"w_art_{key}"] = int(data.get("internal_arts", {}).get(key, 0))

    # Семья и деньги
    fam = data.get("family", {})
    for fk in defaults["family"]:
        st.session_state[f"w_fam_{fk}"] = fam.get(fk, "")

    mon = data.get("money", {})
    for mk in defaults["money"]:
        st.session_state[f"w_mon_{mk}"] = mon.get(mk, "")

    # Техники кунг-фу
    kft = data.get("kung_fu_techniques", defaults["kung_fu_techniques"])
    if not isinstance(kft, list) or len(kft) == 0:
        kft = defaults["kung_fu_techniques"]
    st.session_state["kung_fu_rows"] = len(kft)
    for idx, row in enumerate(kft):
        st.session_state[f"w_kft_{idx}_normal"] = row.get("normal", "")
        st.session_state[f"w_kft_{idx}_counter"] = row.get("counter", "")
        st.session_state[f"w_kft_{idx}_stance"] = row.get("stance", "")


def collect_data_from_state() -> dict:
    defenses = {}
    for key, _, base in DEFENSES_CONFIG:
        b = st.session_state.get(f"w_def_{key}_base", base)
        m1 = st.session_state.get(f"w_def_{key}_mod1", 0)
        m2 = st.session_state.get(f"w_def_{key}_mod2", 0)
        auto = st.session_state.get(f"w_def_{key}_auto", True)
        tot = (b + m1 + m2) if auto else st.session_state.get(f"w_def_{key}_total", b + m1 + m2)
        defenses[key] = {
            "base": b,
            "mod1": m1,
            "mod2": m2,
            "auto": auto,
            "total": tot,
        }

    qi_val = st.session_state.get("w_qi", 1)
    mw_auto = st.session_state.get("w_max_wounds_auto", True)
    mw_val = (qi_val * 2 + 1) if mw_auto else st.session_state.get("w_max_wounds", qi_val * 2 + 1)

    rows_count = st.session_state.get("kung_fu_rows", 8)
    kft_list = []
    for idx in range(rows_count):
        kft_list.append({
            "normal": st.session_state.get(f"w_kft_{idx}_normal", ""),
            "counter": st.session_state.get(f"w_kft_{idx}_counter", ""),
            "stance": st.session_state.get(f"w_kft_{idx}_stance", ""),
        })

    return {
        "system": "Wandering Heroes of Ogre Gate",
        "name": st.session_state.get("w_name", ""),
        "martial_name": st.session_state.get("w_martial_name", ""),
        "nickname": st.session_state.get("w_nickname", ""),
        "sifu": st.session_state.get("w_sifu", ""),
        "player": st.session_state.get("w_player", ""),
        "ht_wt": st.session_state.get("w_ht_wt", ""),
        "sex": st.session_state.get("w_sex", ""),
        "titles": st.session_state.get("w_titles", ""),
        "campaign": st.session_state.get("w_campaign", ""),
        "homeland_clan": st.session_state.get("w_homeland_clan", ""),
        "sect": st.session_state.get("w_sect", ""),
        "occupation": st.session_state.get("w_occupation", ""),
        "family_short": st.session_state.get("w_family_short", ""),
        "reputation": st.session_state.get("w_reputation", ""),
        "age": st.session_state.get("w_age", ""),
        "qi": qi_val,
        "max_wounds_auto": mw_auto,
        "max_wounds": mw_val,
        "current_wounds": st.session_state.get("w_current_wounds", 0),
        "imbalance_rating": st.session_state.get("w_imbalance_rating", 0),
        "imbalance_points": st.session_state.get("w_imbalance_points", 0),
        "imbalance_bonus_qi": st.session_state.get("w_imbalance_bonus_qi", 1),
        "defenses": defenses,
        "combat_skills": {k: st.session_state.get(f"w_cskill_{k}", 0) for k, _ in COMBAT_SKILLS},
        "combat_expertise": st.session_state.get("w_combat_expertise", ""),
        "specialist_fixed": {k: st.session_state.get(f"w_sskill_{k}", 0) for k, _ in SPECIALIST_FIXED},
        "specialist_custom": {
            k: {
                "spec": st.session_state.get(f"w_scust_{k}_spec", ""),
                "val": st.session_state.get(f"w_scust_{k}_val", 0),
            }
            for k, _ in SPECIALIST_CUSTOM
        },
        "specialist_expertise": st.session_state.get("w_specialist_expertise", ""),
        "mental_skills": {k: st.session_state.get(f"w_mskill_{k}", 0) for k, _ in MENTAL_SKILLS},
        "mental_expertise": st.session_state.get("w_mental_expertise", ""),
        "physical_skills": {k: st.session_state.get(f"w_pskill_{k}", 0) for k, _ in PHYSICAL_SKILLS},
        "physical_expertise": st.session_state.get("w_physical_expertise", ""),
        "knowledge_skills": {
            k: {
                "spec": st.session_state.get(f"w_kskill_{k}_spec", ""),
                "val": st.session_state.get(f"w_kskill_{k}_val", 0),
            }
            for k, _ in KNOWLEDGE_GROUPS
        },
        "knowledge_expertise": st.session_state.get("w_knowledge_expertise", ""),
        "internal_arts": {k: st.session_state.get(f"w_art_{k}", 0) for k, _ in INTERNAL_ARTS},
        "combat_techniques": st.session_state.get("w_combat_techniques", ""),
        "flaws": st.session_state.get("w_flaws", ""),
        "family": {
            fk: st.session_state.get(f"w_fam_{fk}", "")
            for fk in get_default_data()["family"]
        },
        "grudges": st.session_state.get("w_grudges", ""),
        "equipment": st.session_state.get("w_equipment", ""),
        "money": {
            mk: st.session_state.get(f"w_mon_{mk}", "")
            for mk in get_default_data()["money"]
        },
        "experience": st.session_state.get("w_experience", ""),
        "kung_fu_techniques": kft_list,
    }


# Инициализация при первом запуске
if "initialized" not in st.session_state:
    sync_state_from_dict(get_default_data())
    st.session_state["initialized"] = True
    st.session_state["last_uploaded_id"] = None

# --- Боковая панель: Импорт / Экспорт JSON и Сброс ---
with st.sidebar:
    st.header("📁 Файл персонажа")

    uploaded_file = st.file_uploader(
        "Загрузить персонажа (.json)",
        type=["json"],
        help="Выберите ранее сохранённый JSON-файл листа персонажа.",
    )

    if uploaded_file is not None:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        if st.session_state.get("last_uploaded_id") != file_id:
            try:
                loaded_json = json.loads(uploaded_file.getvalue().decode("utf-8"))
                sync_state_from_dict(loaded_json)
                st.session_state["last_uploaded_id"] = file_id
                st.success("Персонаж успешно загружен!")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка чтения JSON: {e}")

    current_char = collect_data_from_state()
    char_filename = (current_char["name"] or current_char["martial_name"] or "hero").strip()
    char_filename = "".join(c if c.isalnum() or c in ("-", "_", " ") else "_" for c in char_filename)

    st.download_button(
        label="💾 Скачать JSON персонажа",
        data=json.dumps(current_char, ensure_ascii=False, indent=2),
        file_name=f"{char_filename}.json",
        mime="application/json",
        use_container_width=True,
    )

    st.divider()
    if st.button("🗑️ Очистить весь лист", use_container_width=True):
        sync_state_from_dict(get_default_data())
        st.session_state["last_uploaded_id"] = None
        st.rerun()

# --- Заголовок приложения ---
st.title("⚔️ Wandering Heroes of Ogre Gate")
st.caption("Интерактивный конструктор и лист персонажа")

tab_front, tab_back = st.tabs(["📜 Лицевая сторона (Характеристики и навыки)", "📖 Оборотная сторона (Семья, снаряжение и кунг-фу)"])

# ==============================================================================
# ВКЛАДКА 1: ЛИЦЕВАЯ СТОРОНА ЛИСТА
# ==============================================================================
with tab_front:
    # 1. Основная информация
    with st.container(border=True):
        st.subheader("Общие сведения")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input("Имя (Name)", key="w_name")
            st.text_input("Прозвище (Nickname)", key="w_nickname")
            st.text_input("Рост / Вес (Ht./Wt.)", key="w_ht_wt")
            st.text_input("Родина / Клан (Homeland/Clan)", key="w_homeland_clan")
            st.text_input("Род занятий (Occupation)", key="w_occupation")
            st.text_input("Репутация (Reputation)", key="w_reputation")
        with c2:
            st.text_input("Боевое имя (Martial Name)", key="w_martial_name")
            st.text_input("Наставник / Сифу (Sifu)", key="w_sifu")
            st.text_input("Пол (Sex)", key="w_sex")
            st.text_input("Секта / Школа (Sect)", key="w_sect")
            st.text_input("Семья (Family)", key="w_family_short")
            st.text_input("Возраст (Age)", key="w_age")
        with c3:
            st.text_input("Игрок (Player)", key="w_player")
            st.text_input("Титулы (Title(s))", key="w_titles")
            st.text_input("Кампания (Campaign)", key="w_campaign")

    # 2. Три колонки как на оригинальном листе
    col_left, col_mid, col_right = st.columns([1.15, 0.95, 1.15])

    # --- ЛЕВАЯ КОЛОНКА: Защиты, Боевые, Специальные, Ментальные ---
    with col_left:
        with st.container(border=True):
            st.subheader("🛡️ Защиты (Defenses)")
            st.caption("Формула: База + Мод. 1 + Мод. 2 = Итог")
            for key, label, default_base in DEFENSES_CONFIG:
                st.markdown(f"**{label}**")
                d1, d2, d3, d4, d5 = st.columns([1, 1, 1, 1.15, 0.85])
                with d1:
                    b_val = st.number_input("База", min_value=0, max_value=30, key=f"w_def_{key}_base")
                with d2:
                    m1_val = st.number_input("+Мод1", min_value=-10, max_value=20, key=f"w_def_{key}_mod1")
                with d3:
                    m2_val = st.number_input("+Мод2", min_value=-10, max_value=20, key=f"w_def_{key}_mod2")
                with d5:
                    auto_def = st.checkbox("Авто", key=f"w_def_{key}_auto", help="Авторасчет суммы")
                with d4:
                    calc_def = b_val + m1_val + m2_val
                    if auto_def:
                        st.session_state[f"w_def_{key}_total"] = calc_def
                        st.number_input("Итог", value=calc_def, disabled=True, key=f"w_def_{key}_disp")
                    else:
                        st.number_input("Итог", min_value=0, max_value=50, key=f"w_def_{key}_total")

        with st.container(border=True):
            st.subheader("🗡️ Боевые навыки (Combat)")
            for key, label in COMBAT_SKILLS:
                sc1, sc2 = st.columns([2.2, 1])
                with sc1:
                    st.markdown(f"<div style='padding-top:8px'>{label}</div>", unsafe_allow_html=True)
                with sc2:
                    st.number_input(label, min_value=0, max_value=3, label_visibility="collapsed", key=f"w_cskill_{key}")
            st.text_area("Специализации (Expertise — Combat)", height=80, key="w_combat_expertise")

        with st.container(border=True):
            st.subheader("🔮 Специальные навыки (Specialist)")
            for key, label in SPECIALIST_FIXED:
                sc1, sc2 = st.columns([2.2, 1])
                with sc1:
                    st.markdown(f"<div style='padding-top:8px'>{label}</div>", unsafe_allow_html=True)
                with sc2:
                    st.number_input(label, min_value=0, max_value=3, label_visibility="collapsed", key=f"w_sskill_{key}")

            for key, label in SPECIALIST_CUSTOM:
                sc1, sc2 = st.columns([2.2, 1])
                with sc1:
                    st.text_input(label, placeholder=label, label_visibility="collapsed", key=f"w_scust_{key}_spec")
                with sc2:
                    st.number_input(f"{label} ранг", min_value=0, max_value=3, label_visibility="collapsed", key=f"w_scust_{key}_val")
            st.text_area("Специализации (Expertise — Specialist)", height=80, key="w_specialist_expertise")

        with st.container(border=True):
            st.subheader("🧠 Ментальные навыки (Mental)")
            for key, label in MENTAL_SKILLS:
                sc1, sc2 = st.columns([2.2, 1])
                with sc1:
                    st.markdown(f"<div style='padding-top:8px'>{label}</div>", unsafe_allow_html=True)
                with sc2:
                    st.number_input(label, min_value=0, max_value=3, label_visibility="collapsed", key=f"w_mskill_{key}")
            st.text_area("Специализации (Expertise — Mental)", height=80, key="w_mental_expertise")

    # --- ЦЕНТРАЛЬНАЯ КОЛОНКА: Внутренние стили, Дисбаланс, Ци, Боевые техники ---
    with col_mid:
        with st.container(border=True):
            st.subheader("☯️ Внутренние стили (Internal Arts)")
            ia1, ia2 = st.columns(2)
            for idx, (key, label) in enumerate(INTERNAL_ARTS):
                target_col = ia1 if idx % 2 == 0 else ia2
                with target_col:
                    st.number_input(label, min_value=0, max_value=6, key=f"w_art_{key}")

        with st.container(border=True):
            st.subheader("⚖️ Рейтинг дисбаланса (Imbalance Rating)")
            st.number_input(
                "Значение дисбаланса (от -5 до +5)",
                min_value=-5,
                max_value=5,
                key="w_imbalance_rating",
            )

        with st.container(border=True):
            st.subheader("✨ Уровень Ци (Qi)")
            qi_val = st.number_input("Ци (Qi, 1–6)", min_value=1, max_value=6, key="w_qi")

        with st.container(border=True):
            st.subheader("📜 Боевые техники (Combat Techniques)")
            st.text_area(
                "Список известных боевых техник",
                height=520,
                label_visibility="collapsed",
                placeholder="Запишите здесь боевые техники персонажа...",
                key="w_combat_techniques",
            )

    # --- ПРАВАЯ КОЛОНКА: Раны, Физические, Знания, Недостатки ---
    with col_right:
        with st.container(border=True):
            st.subheader("🩸 Раны (Wounds)")
            w1, w2, w3 = st.columns([1.2, 0.8, 1.2])
            with w3:
                mw_auto = st.checkbox("Авто (Ци×2+1)", key="w_max_wounds_auto")
            with w1:
                calc_mw = qi_val * 2 + 1
                if mw_auto:
                    st.session_state["w_max_wounds"] = calc_mw
                    st.number_input("Макс. ран (Max Wounds)", value=calc_mw, disabled=True, key="w_max_wounds_disp")
                else:
                    st.number_input("Макс. ран (Max Wounds)", min_value=1, max_value=50, key="w_max_wounds")
            with w2:
                st.number_input("Текущие раны", min_value=0, max_value=50, key="w_current_wounds")

        with st.container(border=True):
            st.subheader("💪 Физические навыки (Physical)")
            for key, label in PHYSICAL_SKILLS:
                sc1, sc2 = st.columns([2.2, 1])
                with sc1:
                    st.markdown(f"<div style='padding-top:8px'>{label}</div>", unsafe_allow_html=True)
                with sc2:
                    st.number_input(label, min_value=0, max_value=3, label_visibility="collapsed", key=f"w_pskill_{key}")
            st.text_area("Специализации (Expertise — Physical)", height=80, key="w_physical_expertise")

        with st.container(border=True):
            st.subheader("📚 Знания (Knowledge)")
            for key, label in KNOWLEDGE_GROUPS:
                sc1, sc2 = st.columns([2.2, 1])
                with sc1:
                    st.text_input(label, placeholder=label, label_visibility="collapsed", key=f"w_kskill_{key}_spec")
                with sc2:
                    st.number_input(f"{label} ранг", min_value=0, max_value=3, label_visibility="collapsed", key=f"w_kskill_{key}_val")
            st.text_area("Специализации (Expertise — Knowledge)", height=80, key="w_knowledge_expertise")

        with st.container(border=True):
            st.subheader("⚠️ Недостатки и изъяны (Flaws)")
            st.text_area(
                "Недостатки персонажа",
                height=160,
                label_visibility="collapsed",
                placeholder="Запишите недостатки (Flaws)...",
                key="w_flaws",
            )


# ==============================================================================
# ВКЛАДКА 2: ОБОРОТНАЯ СТОРОНА ЛИСТА
# ==============================================================================
with tab_back:
    top_c1, top_c2, top_c3 = st.columns([1, 1, 1.3])

    with top_c1:
        with st.container(border=True):
            st.subheader("🏮 Семья (Family)")
            st.text_input("Кол-во братьев/сестёр (No. Siblings)", key="w_fam_siblings")
            st.text_input("Порядок рождения (Birth Order)", key="w_fam_birth_order")
            st.text_input("Мать (Mother)", key="w_fam_mother")
            st.text_input("Отец (Father)", key="w_fam_father")
            st.text_input("Сёстры (Sister(s))", key="w_fam_sisters")
            st.text_input("Братья (Brother(s))", key="w_fam_brothers")
            st.text_area("Названая семья (Sworn Family)", height=70, key="w_fam_sworn_family")
            st.text_area("Прочие родственники (Other(s))", height=70, key="w_fam_others")

        with st.container(border=True):
            st.subheader("💰 Деньги (Money)")
            st.text_input("Таэли (Taels)", key="w_mon_taels")
            st.text_input("Империалы (Imperials)", key="w_mon_imperials")
            st.text_input("Лопаты / Монеты (Spades)", key="w_mon_spades")
            st.text_input("Ляны (Liangs)", key="w_mon_liangs")
            st.text_area("Бумажные деньги (Paper Currency)", height=70, key="w_mon_paper_currency")

    with top_c2:
        with st.container(border=True):
            st.subheader("💢 Обиды и враги (Grudges)")
            st.text_area(
                "Обиды",
                height=420,
                label_visibility="collapsed",
                placeholder="Запишите кровную месть, долги чести и обиды...",
                key="w_grudges",
            )

        with st.container(border=True):
            st.subheader("⭐ Опыт (Experience)")
            st.text_area(
                "Опыт",
                height=195,
                label_visibility="collapsed",
                placeholder="Текущий / потраченный опыт...",
                key="w_experience",
            )

    with top_c3:
        with st.container(border=True):
            st.subheader("🎒 Снаряжение (Equipment)")
            st.text_area(
                "Снаряжение",
                height=485,
                label_visibility="collapsed",
                placeholder="Оружие, доспехи, артефакты и вещи...",
                key="w_equipment",
            )

        with st.container(border=True):
            st.subheader("🌀 Очки дисбаланса (Imbalance Points)")
            ip1, ip2 = st.columns(2)
            with ip1:
                st.number_input(
                    "Очки дисбаланса (0–10)",
                    min_value=0,
                    max_value=10,
                    key="w_imbalance_points",
                )
            with ip2:
                st.number_input(
                    "Бонус за уровень Ци (1–6)",
                    min_value=1,
                    max_value=6,
                    key="w_imbalance_bonus_qi",
                )

    # Таблица техник кунг-фу внизу оборотной стороны
    with st.container(border=True):
        h_col, btn_add, btn_rem = st.columns([3, 1, 1])
        with h_col:
            st.subheader("🥋 Техники кунг-фу (Kung Fu Techniques)")
        with btn_add:
            if st.button("➕ Добавить строку", use_container_width=True):
                idx = st.session_state["kung_fu_rows"]
                st.session_state[f"w_kft_{idx}_normal"] = ""
                st.session_state[f"w_kft_{idx}_counter"] = ""
                st.session_state[f"w_kft_{idx}_stance"] = ""
                st.session_state["kung_fu_rows"] = idx + 1
                st.rerun()
        with btn_rem:
            if st.button("➖ Убрать строку", use_container_width=True) and st.session_state["kung_fu_rows"] > 1:
                st.session_state["kung_fu_rows"] -= 1
                st.rerun()

        th1, th2, th3 = st.columns(3)
        th1.markdown("**Обычная техника (Normal)**")
        th2.markdown("**Контратака (Counter)**")
        th3.markdown("**Стойка (Stance)**")

        for idx in range(st.session_state["kung_fu_rows"]):
            r1, r2, r3 = st.columns(3)
            with r1:
                st.text_input(
                    f"Normal {idx+1}",
                    label_visibility="collapsed",
                    placeholder="Название и эффект...",
                    key=f"w_kft_{idx}_normal",
                )
            with r2:
                st.text_input(
                    f"Counter {idx+1}",
                    label_visibility="collapsed",
                    placeholder="Контрприём...",
                    key=f"w_kft_{idx}_counter",
                )
            with r3:
                st.text_input(
                    f"Stance {idx+1}",
                    label_visibility="collapsed",
                    placeholder="Стойка...",
                    key=f"w_kft_{idx}_stance",
                )
