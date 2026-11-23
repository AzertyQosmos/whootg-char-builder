import json
import streamlit as st

st.set_page_config(
    page_title="Генератор персонажа — Wandering Heroes of Ogre Gate",
    page_icon="🗡️",
    layout="wide",
)

RANK_COST = {0: 0, 1: 1, 2: 3, 3: 6}

DEFENSES_SCHEMA = [
    ("hardiness", "Стойкость (Hardiness)", 3, 3, 4),
    ("parry", "Парирование (Parry)", 3, 3, 4),
    ("evade", "Уклонение (Evade)", 3, 3, 4),
    ("stealth", "Скрытность (Stealth)", 6, 3, 1),
    ("wits", "Смекалка (Wits)", 6, 3, 1),
    ("resolve", "Решимость (Resolve)", 6, 3, 1),
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

SPECIALIST_SKILLS = [
    ("medicine", "Медицина (Medicine)", False),
    ("divination", "Гадание (Divination)", False),
    ("meditation", "Медитация (Meditation)", False),
    ("talent_1", "Талант 1 (Talent)", True),
    ("talent_2", "Талант 2 (Talent)", True),
    ("trade_1", "Ремесло 1 (Trade)", True),
    ("trade_2", "Ремесло 2 (Trade)", True),
    ("survival_1", "Выживание 1 (Survival)", True),
    ("survival_2", "Выживание 2 (Survival)", True),
    ("ritual_1", "Ритуал 1 (Ritual)", True),
    ("ritual_2", "Ритуал 2 (Ritual)", True),
    ("ritual_3", "Ритуал 3 (Ritual)", True),
]

MENTAL_SKILLS = [
    ("command", "Командование (Command)"),
    ("persuade", "Убеждение (Persuade)"),
    ("deception", "Обман (Deception)"),
    ("empathy", "Эмпатия (Empathy)"),
    ("reasoning", "Логика (Reasoning)"),
    ("detect", "Проницательность (Detect)"),
]

PHYSICAL_SKILLS = [
    ("athletics", "Атлетика (Athletics)"),
    ("swim", "Плавание (Swim)"),
    ("speed", "Скорость (Speed)"),
    ("muscle", "Сила (Muscle)"),
    ("endurance", "Выносливость (Endurance)"),
    ("ride", "Верховая езда (Ride)"),
    ("sail", "Мореходство (Sail)"),
]

KNOWLEDGE_SKILLS = [
    ("history_1", "История 1 (History)"),
    ("history_2", "История 2 (History)"),
    ("creatures_1", "Существа 1 (Creatures)"),
    ("creatures_2", "Существа 2 (Creatures)"),
    ("places_1", "Места и культуры 1 (Places/Cultures)"),
    ("places_2", "Места и культуры 2 (Places/Cultures)"),
    ("martial_1", "Боевые школы 1 (Martial Disciplines)"),
    ("martial_2", "Боевые школы 2 (Martial Disciplines)"),
    ("institutions_1", "Организации 1 (Institutions)"),
    ("institutions_2", "Организации 2 (Institutions)"),
    ("language_1", "Язык 1 (Language)"),
    ("language_2", "Язык 2 (Language)"),
    ("script_1", "Письменность 1 (Read Script)"),
    ("script_2", "Письменность 2 (Read Script)"),
    ("religion_1", "Религия и боги 1 (Religion/Gods)"),
    ("religion_2", "Религия и боги 2 (Religion/Gods)"),
    ("classics_1", "Классические труды 1 (Classics)"),
    ("classics_2", "Классические труды 2 (Classics)"),
]


def calc_category_points(category_prefix: str, skill_keys: list[str]) -> int:
    total = 0
    for key in skill_keys:
        rank = int(st.session_state.get(f"{category_prefix}_val_{key}", 0))
        total += RANK_COST.get(rank, 0)
    return total


def get_default_data() -> dict:
    return {
        "meta": {"system": "Wandering Heroes of Ogre Gate", "version": 2},
        "identity": {
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
            "family_name": "",
            "reputation": "",
            "age": "",
        },
        "defenses": {
            k: {"base": base, "mod1": 0, "mod2": 0, "total": base, "auto": True}
            for k, _, base, _, _ in DEFENSES_SCHEMA
        },
        "arts": {
            "dianxue": False,
            "waijia": False,
            "qinggong": False,
            "neigong": False,
            "imbalance_rating": 0,
            "imbalance_points": 0,
            "imbalance_bonus_qi": 1,
            "qi": 1,
        },
        "wounds": {
            "max": 3,
            "max_auto": True,
            "current": 0,
        },
        "skills": {
            "combat": {
                "values": {k: 0 for k, _ in COMBAT_SKILLS},
                "expertise": "",
            },
            "specialist": {
                "values": {k: {"spec": "", "rank": 0} for k, _, _ in SPECIALIST_SKILLS},
                "expertise": "",
            },
            "mental": {
                "values": {k: 0 for k, _ in MENTAL_SKILLS},
                "expertise": "",
            },
            "physical": {
                "values": {k: 0 for k, _ in PHYSICAL_SKILLS},
                "expertise": "",
            },
            "knowledge": {
                "values": {k: {"spec": "", "rank": 0} for k, _ in KNOWLEDGE_SKILLS},
                "expertise": "",
            },
        },
        "combat_techniques": "",
        "flaws": "",
        "family": {
            "num_siblings": "",
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
        "kung_fu_techniques": [
            {"normal": "", "counter": "", "stance": ""} for _ in range(8)
        ],
    }


def apply_data_to_state(data: dict):
    defaults = get_default_data()

    for section, values in defaults.items():
        if section not in data:
            data[section] = values
        elif isinstance(values, dict):
            for k, v in values.items():
                if k not in data[section]:
                    data[section][k] = v

    for k, v in data["identity"].items():
        st.session_state[f"id_{k}"] = str(v)

    for k, _, base, _, _ in DEFENSES_SCHEMA:
        d = data["defenses"].get(k, {"base": base, "mod1": 0, "mod2": 0, "total": base, "auto": True})
        st.session_state[f"def_{k}_base"] = int(d.get("base", base))
        st.session_state[f"def_{k}_mod1"] = int(d.get("mod1", 0))
        st.session_state[f"def_{k}_mod2"] = int(d.get("mod2", 0))
        st.session_state[f"def_{k}_auto"] = bool(d.get("auto", True))
        if st.session_state[f"def_{k}_auto"]:
            st.session_state[f"def_{k}_total"] = (
                st.session_state[f"def_{k}_base"]
                + st.session_state[f"def_{k}_mod1"]
                + st.session_state[f"def_{k}_mod2"]
            )
        else:
            st.session_state[f"def_{k}_total"] = int(d.get("total", base))

    arts = data["arts"]
    st.session_state["art_dianxue"] = bool(arts.get("dianxue", False))
    st.session_state["art_waijia"] = bool(arts.get("waijia", False))
    st.session_state["art_qinggong"] = bool(arts.get("qinggong", False))
    st.session_state["art_neigong"] = bool(arts.get("neigong", False))
    st.session_state["art_imbalance_rating"] = int(arts.get("imbalance_rating", 0))
    st.session_state["art_imbalance_points"] = int(arts.get("imbalance_points", 0))
    st.session_state["art_imbalance_bonus_qi"] = int(arts.get("imbalance_bonus_qi", 1))
    st.session_state["art_qi"] = int(arts.get("qi", 1))

    wounds = data["wounds"]
    st.session_state["wounds_auto"] = bool(wounds.get("max_auto", True))
    if st.session_state["wounds_auto"]:
        st.session_state["wounds_max"] = st.session_state["art_qi"] * 2 + 1
    else:
        st.session_state["wounds_max"] = int(wounds.get("max", 3))
    st.session_state["wounds_current"] = int(wounds.get("current", 0))

    skills = data["skills"]
    for k, _ in COMBAT_SKILLS:
        st.session_state[f"combat_val_{k}"] = int(skills["combat"]["values"].get(k, 0))
    st.session_state["combat_expertise"] = str(skills["combat"].get("expertise", ""))

    for k, _, has_spec in SPECIALIST_SKILLS:
        item = skills["specialist"]["values"].get(k, {"spec": "", "rank": 0})
        if isinstance(item, dict):
            st.session_state[f"spec_val_{k}"] = int(item.get("rank", 0))
            if has_spec:
                st.session_state[f"spec_name_{k}"] = str(item.get("spec", ""))
        else:
            st.session_state[f"spec_val_{k}"] = int(item)
            if has_spec:
                st.session_state[f"spec_name_{k}"] = ""
    st.session_state["spec_expertise"] = str(skills["specialist"].get("expertise", ""))

    for k, _ in MENTAL_SKILLS:
        st.session_state[f"mental_val_{k}"] = int(skills["mental"]["values"].get(k, 0))
    st.session_state["mental_expertise"] = str(skills["mental"].get("expertise", ""))

    for k, _ in PHYSICAL_SKILLS:
        st.session_state[f"phys_val_{k}"] = int(skills["physical"]["values"].get(k, 0))
    st.session_state["phys_expertise"] = str(skills["physical"].get("expertise", ""))

    for k, _ in KNOWLEDGE_SKILLS:
        item = skills["knowledge"]["values"].get(k, {"spec": "", "rank": 0})
        if isinstance(item, dict):
            st.session_state[f"know_val_{k}"] = int(item.get("rank", 0))
            st.session_state[f"know_name_{k}"] = str(item.get("spec", ""))
        else:
            st.session_state[f"know_val_{k}"] = int(item)
            st.session_state[f"know_name_{k}"] = ""
    st.session_state["know_expertise"] = str(skills["knowledge"].get("expertise", ""))

    st.session_state["combat_techniques"] = str(data.get("combat_techniques", ""))
    st.session_state["flaws"] = str(data.get("flaws", ""))

    for k, v in data["family"].items():
        st.session_state[f"fam_{k}"] = str(v)

    st.session_state["grudges"] = str(data.get("grudges", ""))
    st.session_state["equipment"] = str(data.get("equipment", ""))

    for k, v in data["money"].items():
        st.session_state[f"money_{k}"] = str(v)

    st.session_state["experience"] = str(data.get("experience", ""))

    kft = data.get("kung_fu_techniques", [])
    if not isinstance(kft, list) or len(kft) == 0:
        kft = [{"normal": "", "counter": "", "stance": ""}]
    st.session_state["kft_rows"] = [
        {
            "normal": str(row.get("normal", "")),
            "counter": str(row.get("counter", "")),
            "stance": str(row.get("stance", "")),
        }
        for row in kft
    ]


def collect_data_from_state() -> dict:
    combat_pts = calc_category_points("combat", [k for k, _ in COMBAT_SKILLS])
    spec_pts = calc_category_points("spec", [k for k, _, _ in SPECIALIST_SKILLS])
    mental_pts = calc_category_points("mental", [k for k, _ in MENTAL_SKILLS])
    phys_pts = calc_category_points("phys", [k for k, _ in PHYSICAL_SKILLS])
    know_pts = calc_category_points("know", [k for k, _ in KNOWLEDGE_SKILLS])

    return {
        "meta": {"system": "Wandering Heroes of Ogre Gate", "version": 2},
        "skill_points_summary": {
            "combat": combat_pts,
            "specialist": spec_pts,
            "mental": mental_pts,
            "physical": phys_pts,
            "knowledge": know_pts,
            "total": combat_pts + spec_pts + mental_pts + phys_pts + know_pts,
        },
        "identity": {
            k: st.session_state.get(f"id_{k}", "")
            for k in get_default_data()["identity"]
        },
        "defenses": {
            k: {
                "base": st.session_state.get(f"def_{k}_base", base),
                "mod1": st.session_state.get(f"def_{k}_mod1", 0),
                "mod2": st.session_state.get(f"def_{k}_mod2", 0),
                "total": st.session_state.get(f"def_{k}_total", base),
                "auto": st.session_state.get(f"def_{k}_auto", True),
            }
            for k, _, base, _, _ in DEFENSES_SCHEMA
        },
        "arts": {
            "dianxue": st.session_state.get("art_dianxue", False),
            "waijia": st.session_state.get("art_waijia", False),
            "qinggong": st.session_state.get("art_qinggong", False),
            "neigong": st.session_state.get("art_neigong", False),
            "imbalance_rating": st.session_state.get("art_imbalance_rating", 0),
            "imbalance_points": st.session_state.get("art_imbalance_points", 0),
            "imbalance_bonus_qi": st.session_state.get("art_imbalance_bonus_qi", 1),
            "qi": st.session_state.get("art_qi", 1),
        },
        "wounds": {
            "max": st.session_state.get("wounds_max", 3),
            "max_auto": st.session_state.get("wounds_auto", True),
            "current": st.session_state.get("wounds_current", 0),
        },
        "skills": {
            "combat": {
                "values": {k: st.session_state.get(f"combat_val_{k}", 0) for k, _ in COMBAT_SKILLS},
                "expertise": st.session_state.get("combat_expertise", ""),
            },
            "specialist": {
                "values": {
                    k: {
                        "spec": st.session_state.get(f"spec_name_{k}", "") if has_spec else "",
                        "rank": st.session_state.get(f"spec_val_{k}", 0),
                    }
                    for k, _, has_spec in SPECIALIST_SKILLS
                },
                "expertise": st.session_state.get("spec_expertise", ""),
            },
            "mental": {
                "values": {k: st.session_state.get(f"mental_val_{k}", 0) for k, _ in MENTAL_SKILLS},
                "expertise": st.session_state.get("mental_expertise", ""),
            },
            "physical": {
                "values": {k: st.session_state.get(f"phys_val_{k}", 0) for k, _ in PHYSICAL_SKILLS},
                "expertise": st.session_state.get("phys_expertise", ""),
            },
            "knowledge": {
                "values": {
                    k: {
                        "spec": st.session_state.get(f"know_name_{k}", ""),
                        "rank": st.session_state.get(f"know_val_{k}", 0),
                    }
                    for k, _ in KNOWLEDGE_SKILLS
                },
                "expertise": st.session_state.get("know_expertise", ""),
            },
        },
        "combat_techniques": st.session_state.get("combat_techniques", ""),
        "flaws": st.session_state.get("flaws", ""),
        "family": {
            k: st.session_state.get(f"fam_{k}", "")
            for k in get_default_data()["family"]
        },
        "grudges": st.session_state.get("grudges", ""),
        "equipment": st.session_state.get("equipment", ""),
        "money": {
            k: st.session_state.get(f"money_{k}", "")
            for k in get_default_data()["money"]
        },
        "experience": st.session_state.get("experience", ""),
        "kung_fu_techniques": st.session_state.get("kft_rows", []),
    }


if "initialized" not in st.session_state:
    apply_data_to_state(get_default_data())
    st.session_state["initialized"] = True

# --- БОКОВАЯ ПАНЕЛЬ (ЗАГРУЗКА / ВЫГРУЗКА / ОЧКИ) ---
with st.sidebar:
    st.title("📜 Управление листом")

    st.subheader("📤 Загрузить персонажа (JSON)")
    uploaded_file = st.file_uploader("Выберите JSON-файл", type=["json"], label_visibility="collapsed")
    if uploaded_file is not None:
        if st.button("Применить загруженный файл", use_container_width=True, type="primary"):
            try:
                loaded_json = json.load(uploaded_file)
                apply_data_to_state(loaded_json)
                st.success("Персонаж загружен!")
                st.rerun()
            except Exception as exc:
                st.error(f"Ошибка чтения JSON: {exc}")

    st.divider()
    sidebar_points_placeholder = st.empty()

    st.divider()
    sidebar_download_placeholder = st.empty()

    st.divider()
    if st.button("🗑️ Очистить весь лист", use_container_width=True):
        apply_data_to_state(get_default_data())
        st.rerun()

# --- ЗАГОЛОВОК ---
st.title("🗡️ Wandering Heroes of Ogre Gate — Лист персонажа")

tab_front, tab_back = st.tabs(["📄 Лицевая сторона (Характеристики и навыки)", "📜 Оборотная сторона (Техники, семья и имущество)"])

# =====================================================================
# ВКЛАДКА 1: ЛИЦЕВАЯ СТОРОНА
# =====================================================================
with tab_front:
    # 1. ОСНОВНАЯ ИНФОРМАЦИЯ
    with st.container(border=True):
        st.subheader("Общие сведения")
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            st.text_input("Имя (Name)", key="id_name")
        with r1c2:
            st.text_input("Боевое имя (Martial Name)", key="id_martial_name")

        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            st.text_input("Прозвище (Nickname)", key="id_nickname")
        with r2c2:
            st.text_input("Наставник / Сифу (Sifu)", key="id_sifu")
        with r2c3:
            st.text_input("Игрок (Player)", key="id_player")

        r3c1, r3c2, r3c3, r3c4 = st.columns([1.2, 0.8, 1.5, 1.5])
        with r3c1:
            st.text_input("Рост / Вес (Ht./Wt.)", key="id_ht_wt")
        with r3c2:
            st.text_input("Пол (Sex)", key="id_sex")
        with r3c3:
            st.text_input("Титул(ы) (Title(s))", key="id_titles")
        with r3c4:
            st.text_input("Кампания (Campaign)", key="id_campaign")

        r4c1, r4c2, r4c3, r4c4 = st.columns(4)
        with r4c1:
            st.text_input("Родина / Клан (Homeland/Clan)", key="id_homeland_clan")
        with r4c2:
            st.text_input("Секта / Школа (Sect)", key="id_sect")
        with r4c3:
            st.text_input("Род занятий (Occupation)", key="id_occupation")
        with r4c4:
            st.text_input("Семья (Family)", key="id_family_name")

        r5c1, r5c2 = st.columns([3, 1])
        with r5c1:
            st.text_input("Репутация (Reputation)", key="id_reputation")
        with r5c2:
            st.text_input("Возраст (Age)", key="id_age")

    # 2. ВЕРХНИЙ БЛОК: ЗАЩИТЫ | ВНУТРЕННИЕ ИСКУССТВА И ЦИ | РАНЫ
    col_left, col_mid, col_right = st.columns([1.35, 1.0, 1.15])

    # --- ЗАЩИТЫ ---
    with col_left:
        with st.container(border=True):
            st.subheader("Защиты (Defenses)")
            st.caption("Формула: База + Мод. 1 + Мод. 2 = Итог (снимите «Авто» для ручного ввода)")
            for key, label, default_base, max_m1, max_m2 in DEFENSES_SCHEMA:
                c_lbl, c_base, c_m1, c_m2, c_tot, c_auto = st.columns([2.2, 0.9, 0.9, 0.9, 1.0, 0.9])
                with c_lbl:
                    st.markdown(f"**{label}**")
                with c_base:
                    st.number_input("База", min_value=0, max_value=30, step=1, key=f"def_{key}_base", label_visibility="collapsed")
                with c_m1:
                    st.number_input("Мод 1", min_value=0, max_value=max_m1, step=1, key=f"def_{key}_mod1", label_visibility="collapsed")
                with c_m2:
                    st.number_input("Мод 2", min_value=0, max_value=max_m2, step=1, key=f"def_{key}_mod2", label_visibility="collapsed")
                with c_auto:
                    is_auto = st.checkbox("Авто", key=f"def_{key}_auto")
                if is_auto:
                    st.session_state[f"def_{key}_total"] = (
                        st.session_state[f"def_{key}_base"]
                        + st.session_state[f"def_{key}_mod1"]
                        + st.session_state[f"def_{key}_mod2"]
                    )
                with c_tot:
                    st.number_input(
                        "Итог",
                        min_value=0,
                        max_value=99,
                        step=1,
                        key=f"def_{key}_total",
                        disabled=is_auto,
                        label_visibility="collapsed",
                    )

    # --- ВНУТРЕННИЕ ИСКУССТВА, ДИСБАЛАНС, ЦИ ---
    with col_mid:
        with st.container(border=True):
            st.subheader("Пути и Ци (Arts & Qi)")
            ac1, ac2 = st.columns(2)
            with ac1:
                st.checkbox("Дяньсюэ (Dianxue)", key="art_dianxue")
                st.checkbox("Цингун (Qinggong)", key="art_qinggong")
            with ac2:
                st.checkbox("Вайцзя (Waijia)", key="art_waijia")
                st.checkbox("Нэйгун (Neigong)", key="art_neigong")

            st.divider()
            st.radio("Уровень Ци (Qi)", options=[1, 2, 3, 4, 5, 6], horizontal=True, key="art_qi")
            st.slider("Рейтинг дисбаланса (Imbalance Rating)", min_value=0, max_value=10, step=1, key="art_imbalance_rating")

    # --- РАНЫ ---
    with col_right:
        with st.container(border=True):
            st.subheader("Раны (Wounds)")
            w_auto = st.checkbox("Авторасчёт Макс. ран (Ци × 2 + 1)", key="wounds_auto")
            if w_auto:
                st.session_state["wounds_max"] = st.session_state["art_qi"] * 2 + 1
            wc1, wc2 = st.columns(2)
            with wc1:
                st.number_input("Макс. раны (Max Wounds)", min_value=1, max_value=99, step=1, key="wounds_max", disabled=w_auto)
            with wc2:
                st.number_input("Текущие раны (Current Wounds)", min_value=0, max_value=99, step=1, key="wounds_current")

    # 3. ОСНОВНАЯ СЕТКА НАВЫКОВ И ТЕХНИК
    col_skills_left, col_skills_center, col_skills_right = st.columns([1.15, 0.95, 1.25])

    # --- ЛЕВАЯ КОЛОНКА: COMBAT, SPECIALIST, MENTAL ---
    with col_skills_left:
        # COMBAT
        with st.container(border=True):
            h_col, p_col = st.columns([2.2, 1])
            with h_col:
                st.subheader("Боевые (Combat)")
            p_combat_box = p_col.empty()

            for key, label in COMBAT_SKILLS:
                sc1, sc2, sc3 = st.columns([1.5, 1.7, 0.65])
                with sc1:
                    st.markdown(label)
                with sc2:
                    st.radio(label, [0, 1, 2, 3], horizontal=True, key=f"combat_val_{key}", label_visibility="collapsed")
                with sc3:
                    cost = RANK_COST[st.session_state.get(f"combat_val_{key}", 0)]
                    st.caption(f"{cost} очк.")
            st.text_area("Специализации — Боевые (Combat Expertise)", key="combat_expertise", height=70)
            combat_pts = calc_category_points("combat", [k for k, _ in COMBAT_SKILLS])
            p_combat_box.metric("Очки категории", combat_pts)

        # SPECIALIST
        with st.container(border=True):
            h_col, p_col = st.columns([2.2, 1])
            with h_col:
                st.subheader("Специальные (Specialist)")
            p_spec_box = p_col.empty()

            for key, label, has_spec in SPECIALIST_SKILLS:
                if has_spec:
                    sc1, sc2, sc3 = st.columns([1.4, 1.6, 0.65])
                    with sc1:
                        st.text_input(label, placeholder=label, key=f"spec_name_{key}", label_visibility="collapsed")
                    with sc2:
                        st.radio(label, [0, 1, 2, 3], horizontal=True, key=f"spec_val_{key}", label_visibility="collapsed")
                    with sc3:
                        cost = RANK_COST[st.session_state.get(f"spec_val_{key}", 0)]
                        st.caption(f"{cost} очк.")
                else:
                    sc1, sc2, sc3 = st.columns([1.4, 1.6, 0.65])
                    with sc1:
                        st.markdown(label)
                    with sc2:
                        st.radio(label, [0, 1, 2, 3], horizontal=True, key=f"spec_val_{key}", label_visibility="collapsed")
                    with sc3:
                        cost = RANK_COST[st.session_state.get(f"spec_val_{key}", 0)]
                        st.caption(f"{cost} очк.")
            st.text_area("Специализации — Специальные (Specialist Expertise)", key="spec_expertise", height=70)
            spec_pts = calc_category_points("spec", [k for k, _, _ in SPECIALIST_SKILLS])
            p_spec_box.metric("Очки категории", spec_pts)

        # MENTAL
        with st.container(border=True):
            h_col, p_col = st.columns([2.2, 1])
            with h_col:
                st.subheader("Ментальные (Mental)")
            p_mental_box = p_col.empty()

            for key, label in MENTAL_SKILLS:
                sc1, sc2, sc3 = st.columns([1.5, 1.7, 0.65])
                with sc1:
                    st.markdown(label)
                with sc2:
                    st.radio(label, [0, 1, 2, 3], horizontal=True, key=f"mental_val_{key}", label_visibility="collapsed")
                with sc3:
                    cost = RANK_COST[st.session_state.get(f"mental_val_{key}", 0)]
                    st.caption(f"{cost} очк.")
            st.text_area("Специализации — Ментальные (Mental Expertise)", key="mental_expertise", height=70)
            mental_pts = calc_category_points("mental", [k for k, _ in MENTAL_SKILLS])
            p_mental_box.metric("Очки категории", mental_pts)

    # --- ЦЕНТРАЛЬНАЯ КОЛОНКА: COMBAT TECHNIQUES ---
    with col_skills_center:
        with st.container(border=True):
            st.subheader("Боевые приёмы (Combat Techniques)")
            st.text_area(
                "Список приёмов (Combat Techniques)",
                key="combat_techniques",
                height=820,
                placeholder="Впишите изученные боевые приёмы...",
                label_visibility="collapsed",
            )

    # --- ПРАВАЯ КОЛОНКА: PHYSICAL, KNOWLEDGE, FLAWS ---
    with col_skills_right:
        # PHYSICAL
        with st.container(border=True):
            h_col, p_col = st.columns([2.2, 1])
            with h_col:
                st.subheader("Физические (Physical)")
            p_phys_box = p_col.empty()

            for key, label in PHYSICAL_SKILLS:
                sc1, sc2, sc3 = st.columns([1.5, 1.7, 0.65])
                with sc1:
                    st.markdown(label)
                with sc2:
                    st.radio(label, [0, 1, 2, 3], horizontal=True, key=f"phys_val_{key}", label_visibility="collapsed")
                with sc3:
                    cost = RANK_COST[st.session_state.get(f"phys_val_{key}", 0)]
                    st.caption(f"{cost} очк.")
            st.text_area("Специализации — Физические (Physical Expertise)", key="phys_expertise", height=70)
            phys_pts = calc_category_points("phys", [k for k, _ in PHYSICAL_SKILLS])
            p_phys_box.metric("Очки категории", phys_pts)

        # KNOWLEDGE
        with st.container(border=True):
            h_col, p_col = st.columns([2.2, 1])
            with h_col:
                st.subheader("Знания (Knowledge)")
            p_know_box = p_col.empty()

            for key, label in KNOWLEDGE_SKILLS:
                sc1, sc2, sc3 = st.columns([1.5, 1.5, 0.6])
                with sc1:
                    st.text_input(label, placeholder=label, key=f"know_name_{key}", label_visibility="collapsed")
                with sc2:
                    st.radio(label, [0, 1, 2, 3], horizontal=True, key=f"know_val_{key}", label_visibility="collapsed")
                with sc3:
                    cost = RANK_COST[st.session_state.get(f"know_val_{key}", 0)]
                    st.caption(f"{cost} очк.")
            st.text_area("Специализации — Знания (Knowledge Expertise)", key="know_expertise", height=70)
            know_pts = calc_category_points("know", [k for k, _ in KNOWLEDGE_SKILLS])
            p_know_box.metric("Очки категории", know_pts)

        # FLAWS
        with st.container(border=True):
            st.subheader("Изъяны (Flaws)")
            st.text_area(
                "Изъяны (Flaws)",
                key="flaws",
                height=160,
                placeholder="Впишите изъяны и недостатки персонажа...",
                label_visibility="collapsed",
            )

# =====================================================================
# ВКЛАДКА 2: ОБОРОТНАЯ СТОРОНА
# =====================================================================
with tab_back:
    b_col1, b_col2, b_col3 = st.columns([1.1, 1.0, 1.3])

    # --- СЕМЬЯ И ДЕНЬГИ ---
    with b_col1:
        with st.container(border=True):
            st.subheader("Семья (Family)")
            st.text_input("Кол-во братьев и сестёр (No. Siblings)", key="fam_num_siblings")
            st.text_input("Порядок рождения (Birth Order)", key="fam_birth_order")
            st.text_input("Мать (Mother)", key="fam_mother")
            st.text_input("Отец (Father)", key="fam_father")
            st.text_input("Сёстры (Sister(s))", key="fam_sisters")
            st.text_input("Братья (Brother(s))", key="fam_brothers")
            st.text_area("Названая семья (Sworn Family)", key="fam_sworn_family", height=80)
            st.text_area("Прочие (Other(s))", key="fam_others", height=80)

        with st.container(border=True):
            st.subheader("Деньги (Money)")
            st.text_input("Ляны / Таэли (Taels)", key="money_taels")
            st.text_input("Империалы (Imperials)", key="money_imperials")
            st.text_input("Монеты-лопаты (Spades)", key="money_spades")
            st.text_input("Ляны серебра (Liangs)", key="money_liangs")
            st.text_area("Бумажные ассигнации (Paper Currency)", key="money_paper_currency", height=70)

    # --- ОБИДЫ И ОПЫТ ---
    with b_col2:
        with st.container(border=True):
            st.subheader("Обиды и вражда (Grudges)")
            st.text_area(
                "Обиды (Grudges)",
                key="grudges",
                height=430,
                placeholder="Запишите кровную месть, долги чести и обиды...",
                label_visibility="collapsed",
            )

        with st.container(border=True):
            st.subheader("Опыт (Experience)")
            st.text_area(
                "Опыт (Experience)",
                key="experience",
                height=215,
                placeholder="Записи о полученном и потраченном опыте...",
                label_visibility="collapsed",
            )

    # --- СНАРЯЖЕНИЕ И ОЧКИ ДИСБАЛАНСА ---
    with b_col3:
        with st.container(border=True):
            st.subheader("Снаряжение (Equipment)")
            st.text_area(
                "Снаряжение (Equipment)",
                key="equipment",
                height=480,
                placeholder="Оружие, доспехи, целебные травы, вещи...",
                label_visibility="collapsed",
            )

        with st.container(border=True):
            st.subheader("Очки дисбаланса (Imbalance Points)")
            st.number_input("Текущие очки дисбаланса (0–10)", min_value=0, max_value=10, step=1, key="art_imbalance_points")
            st.radio("Бонус за уровень Ци (Bonus for Qi Level)", options=[1, 2, 3, 4, 5, 6], horizontal=True, key="art_imbalance_bonus_qi")

    # --- ТЕХНИКИ КУНГ-ФУ ---
    with st.container(border=True):
        st.subheader("Техники Кунг-Фу (Kung Fu Techniques)")
        st.caption("Заполните приёмы по категориям: Обычные (Normal), Контратаки (Counter) и Стойки (Stance)")

        h1, h2, h3, h4 = st.columns([3, 3, 3, 0.5])
        h1.markdown("**Обычные (Normal)**")
        h2.markdown("**Контратаки (Counter)**")
        h3.markdown("**Стойки (Stance)**")

        rows = st.session_state.get("kft_rows", [])
        row_to_delete = None

        for idx, row in enumerate(rows):
            c1, c2, c3, c4 = st.columns([3, 3, 3, 0.5])
            with c1:
                row["normal"] = st.text_input(
                    f"Normal {idx}",
                    value=row["normal"],
                    key=f"kft_norm_{idx}",
                    label_visibility="collapsed",
                )
            with c2:
                row["counter"] = st.text_input(
                    f"Counter {idx}",
                    value=row["counter"],
                    key=f"kft_cnt_{idx}",
                    label_visibility="collapsed",
                )
            with c3:
                row["stance"] = st.text_input(
                    f"Stance {idx}",
                    value=row["stance"],
                    key=f"kft_st_{idx}",
                    label_visibility="collapsed",
                )
            with c4:
                if len(rows) > 1 and st.button("✖", key=f"kft_del_{idx}", help="Удалить строку"):
                    row_to_delete = idx

        if row_to_delete is not None:
            st.session_state["kft_rows"].pop(row_to_delete)
            st.rerun()

        if st.button("➕ Добавить строку техник"):
            st.session_state["kft_rows"].append({"normal": "", "counter": "", "stance": ""})
            st.rerun()

# --- ЗАПОЛНЕНИЕ СВОДКИ В БОКОВОЙ ПАНЕЛИ ПОСЛЕ РЕНДЕРА ВСЕХ ВИДЖЕТОВ ---
total_skill_points = combat_pts + spec_pts + mental_pts + phys_pts + know_pts

with sidebar_points_placeholder.container():
    st.subheader("📊 Потраченные очки навыков")
    st.caption("Расчёт: 1 ранг = 1, 2 ранг = 3, 3 ранг = 6")
    st.markdown(
        f"""
        - **Боевые (Combat):** {combat_pts} очк.
        - **Специальные (Specialist):** {spec_pts} очк.
        - **Ментальные (Mental):** {mental_pts} очк.
        - **Физические (Physical):** {phys_pts} очк.
        - **Знания (Knowledge):** {know_pts} очк.
        """
    )
    st.metric("Всего очков в навыки", total_skill_points)

with sidebar_download_placeholder.container():
    char_data = collect_data_from_state()
    char_name = char_data["identity"]["name"].strip() or "ogre_gate_character"
    safe_filename = "".join(c if c.isalnum() or c in ("-", "_", " ") else "_" for c in char_name).strip() + ".json"

    st.download_button(
        label="💾 Скачать персонажа (JSON)",
        data=json.dumps(char_data, ensure_ascii=False, indent=2),
        file_name=safe_filename,
        mime="application/json",
        use_container_width=True,
        type="primary",
    )
