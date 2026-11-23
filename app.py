import json
import streamlit as st

st.set_page_config(
    page_title="Wandering Heroes of Ogre Gate — Лист персонажа",
    page_icon="⚔️",
    layout="wide",
)

DEFENSES_CONFIG = [
    ("hardiness", "Стойкость (Hardiness)", 3, 4),
    ("parry", "Парирование (Parry)", 3, 4),
    ("evade", "Уклонение (Evade)", 3, 4),
    ("stealth", "Скрытность (Stealth)", 6, 1),
    ("wits", "Смекалка (Wits)", 6, 1),
    ("resolve", "Решимость (Resolve)", 6, 1),
]

COMBAT_SKILLS = [
    ("arm_strike", "Удар рукой (Arm Strike)"),
    ("leg_strike", "Удар ногой (Leg Strike)"),
    ("grapple", "Захват (Grapple)"),
    ("throw", "Бросок (Throw)"),
    ("light_melee", "Лёгкое оружие (Light Melee)"),
    ("medium_melee", "Среднее оружие (Medium Melee)"),
    ("heavy_melee", "Тяжёлое оружие (Heavy Melee)"),
    ("small_ranged", "Малое дальнобойное (Small Ranged)"),
    ("large_ranged", "Большое дальнобойное (Large Ranged)"),
]

SPECIALIST_SKILLS = [
    ("medicine", "Медицина (Medicine)"),
    ("divination", "Гадание (Divination)"),
    ("meditation", "Медитация (Meditation)"),
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
    ("detect", "Проницательность (Detect)"),
]

PHYSICAL_SKILLS = [
    ("athletics", "Атлетика (Athletics)"),
    ("swim", "Плавание (Swim)"),
    ("speed", "Скорость (Speed)"),
    ("muscle", "Сила / Мускулы (Muscle)"),
    ("endurance", "Выносливость (Endurance)"),
    ("ride", "Верховая езда (Ride)"),
    ("sail", "Мореходство (Sail)"),
]

KNOWLEDGE_SKILLS = [
    ("history_1", "История 1 (History)"),
    ("history_2", "История 2 (History)"),
    ("creatures_1", "Существа 1 (Creatures)"),
    ("creatures_2", "Существа 2 (Creatures)"),
    ("places_1", "Места / Культуры 1 (Places/Cultures)"),
    ("places_2", "Места / Культуры 2 (Places/Cultures)"),
    ("martial_1", "Боевые школы 1 (Martial Disciplines)"),
    ("martial_2", "Боевые школы 2 (Martial Disciplines)"),
    ("institutions_1", "Институты 1 (Institutions)"),
    ("institutions_2", "Институты 2 (Institutions)"),
    ("language_1", "Язык 1 (Language)"),
    ("language_2", "Язык 2 (Language)"),
    ("script_1", "Письменность 1 (Read Script)"),
    ("script_2", "Письменность 2 (Read Script)"),
    ("religion_1", "Религия / Боги 1 (Religion/Gods)"),
    ("religion_2", "Религия / Боги 2 (Religion/Gods)"),
    ("classics_1", "Классика 1 (Classics)"),
    ("classics_2", "Классика 2 (Classics)"),
]

ARTS_LIST = [
    ("dianxue", "Дяньсюэ (Dianxue)"),
    ("waijia", "Вайцзя (Waijia)"),
    ("qinggong", "Цингун (Qinggong)"),
    ("neigong", "Нэйгун (Neigong)"),
]


def skill_cost(rank: int) -> int:
    return rank * (rank + 1) // 2


def default_state() -> dict:
    state = {
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
        "qi_level": 1,
        "max_wounds_auto": True,
        "max_wounds": 3,
        "current_wounds": 3,
        "imbalance_rating": 0,
        "imbalance_points": 0,
        "imbalance_bonus_qi": 1,
        "combat_techniques": "",
        "flaws": "",
        "family_siblings_count": "",
        "family_birth_order": "",
        "family_mother": "",
        "family_father": "",
        "family_sisters": "",
        "family_brothers": "",
        "family_sworn": "",
        "family_other": "",
        "grudges": "",
        "equipment": "",
        "money_taels": "",
        "money_imperials": "",
        "money_spades": "",
        "money_liangs": "",
        "money_paper": "",
        "experience": "",
        "kung_fu_techniques": [
            {"normal": "", "counter": "", "stance": ""} for _ in range(5)
        ],
    }

    for key, _, base, _ in DEFENSES_CONFIG:
        state[f"def_{key}_base"] = base
        state[f"def_{key}_m1"] = 0
        state[f"def_{key}_m2"] = 0
        state[f"def_{key}_auto"] = True
        state[f"def_{key}_total"] = base

    for art_key, _ in ARTS_LIST:
        state[f"art_{art_key}"] = 0

    for group_key, skills in [
        ("combat", COMBAT_SKILLS),
        ("specialist", SPECIALIST_SKILLS),
        ("mental", MENTAL_SKILLS),
        ("physical", PHYSICAL_SKILLS),
        ("knowledge", KNOWLEDGE_SKILLS),
    ]:
        state[f"exp_{group_key}"] = ""
        for sk_key, _ in skills:
            state[f"skill_{sk_key}"] = 0

    return state


def init_session():
    defaults = default_state()
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def load_from_json(data: dict):
    defaults = default_state()
    for k, default_val in defaults.items():
        if k in data:
            val = data[k]
            if k.startswith("art_") and isinstance(val, bool):
                val = 1 if val else 0
            st.session_state[k] = val
        else:
            st.session_state[k] = default_val


def export_to_json() -> str:
    defaults = default_state()
    out = {}
    for k in defaults:
        out[k] = st.session_state.get(k, defaults[k])
    return json.dumps(out, ensure_ascii=False, indent=2)


def render_skill_group(title: str, group_key: str, skills: list[tuple[str, str]]) -> int:
    header_col, total_col = st.columns([3, 1])
    with header_col:
        st.subheader(title)
    total_placeholder = total_col.empty()

    group_points = 0
    for sk_key, sk_label in skills:
        c1, c2, c3 = st.columns([2.3, 2.2, 0.7])
        with c1:
            st.markdown(f"<div style='padding-top: 6px;'>{sk_label}</div>", unsafe_allow_html=True)
        with c2:
            rank = st.radio(
                sk_label,
                options=[0, 1, 2, 3],
                horizontal=True,
                label_visibility="collapsed",
                key=f"skill_{sk_key}",
            )
        cost = skill_cost(rank)
        group_points += cost
        with c3:
            st.markdown(
                f"<div style='padding-top: 6px; color: #aaa; font-size: 0.9em;'>{cost} очк.</div>",
                unsafe_allow_html=True,
            )

    total_placeholder.metric("Очки категории", group_points)
    st.text_area(
        f"Специализации — {title} (Expertise)",
        key=f"exp_{group_key}",
        height=85,
        placeholder="Укажите специализации для этой категории...",
    )
    return group_points


init_session()

st.title("⚔️ Wandering Heroes of Ogre Gate — Лист персонажа")

with st.sidebar:
    st.header("📜 Управление листом")
    points_summary_placeholder = st.empty()

    st.divider()
    st.download_button(
        label="💾 Скачать персонажа (JSON)",
        data=export_to_json(),
        file_name=f"{st.session_state.get('name') or 'whog_character'}.json",
        mime="application/json",
        use_container_width=True,
        type="primary",
    )

    uploaded = st.file_uploader("📂 Загрузить персонажа (JSON)", type=["json"])
    if uploaded is not None:
        file_id = f"{uploaded.name}_{uploaded.size}"
        if st.session_state.get("_last_uploaded_id") != file_id:
            try:
                parsed = json.load(uploaded)
                load_from_json(parsed)
                st.session_state["_last_uploaded_id"] = file_id
                st.rerun()
            except Exception as exc:
                st.error(f"Ошибка чтения JSON: {exc}")

    if st.button("🗑️ Очистить лист", use_container_width=True):
        defaults = default_state()
        for k, v in defaults.items():
            st.session_state[k] = v
        st.session_state.pop("_last_uploaded_id", None)
        st.rerun()

tab1, tab2 = st.tabs(["📄 Страница 1: Характеристики и навыки", "📖 Страница 2: Кунг-фу, семья и имущество"])

with tab1:
    with st.container(border=True):
        st.subheader("Общие сведения")
        r1 = st.columns(2)
        r1[0].text_input("Имя (Name)", key="name")
        r1[1].text_input("Боевое имя (Martial Name)", key="martial_name")

        r2 = st.columns(3)
        r2[0].text_input("Прозвище (Nickname)", key="nickname")
        r2[1].text_input("Сифу / Наставник (Sifu)", key="sifu")
        r2[2].text_input("Игрок (Player)", key="player")

        r3 = st.columns(4)
        r3[0].text_input("Рост / Вес (Ht./Wt.)", key="ht_wt")
        r3[1].text_input("Пол (Sex)", key="sex")
        r3[2].text_input("Титул(ы) (Title(s))", key="titles")
        r3[3].text_input("Кампания (Campaign)", key="campaign")

        r4 = st.columns(4)
        r4[0].text_input("Родина / Клан (Homeland/Clan)", key="homeland_clan")
        r4[1].text_input("Секта / Школа (Sect)", key="sect")
        r4[2].text_input("Род занятий (Occupation)", key="occupation")
        r4[3].text_input("Семья (Family)", key="family_short")

        r5 = st.columns(2)
        r5[0].text_input("Репутация (Reputation)", key="reputation")
        r5[1].text_input("Возраст (Age)", key="age")

    st.divider()

    top_left, top_mid, top_right = st.columns([1.25, 1.0, 1.15], gap="medium")

    with top_left:
        with st.container(border=True):
            st.subheader("Защиты (Defenses)")
            st.caption("База + Мод. 1 + Мод. 2 = Итог (снимите «Авто» для ручного ввода)")
            for key, label, default_base, max_m1 in DEFENSES_CONFIG:
                cols = st.columns([1.8, 0.85, 0.85, 0.85, 0.95, 0.7])
                cols[0].markdown(f"<div style='padding-top: 6px;'><b>{label}</b></div>", unsafe_allow_html=True)
                base_val = cols[1].number_input(
                    "База",
                    min_value=0,
                    max_value=30,
                    step=1,
                    key=f"def_{key}_base",
                    label_visibility="collapsed",
                )
                m1_val = cols[2].number_input(
                    "Мод. 1",
                    min_value=0,
                    max_value=max_m1,
                    step=1,
                    key=f"def_{key}_m1",
                    label_visibility="collapsed",
                )
                m2_val = cols[3].number_input(
                    "Мод. 2",
                    min_value=0,
                    max_value=10,
                    step=1,
                    key=f"def_{key}_m2",
                    label_visibility="collapsed",
                )
                auto = cols[5].checkbox("Авто", key=f"def_{key}_auto")
                if auto:
                    st.session_state[f"def_{key}_total"] = base_val + m1_val + m2_val
                cols[4].number_input(
                    "Итог",
                    min_value=0,
                    max_value=50,
                    step=1,
                    key=f"def_{key}_total",
                    disabled=auto,
                    label_visibility="collapsed",
                )

    with top_mid:
        with st.container(border=True):
            st.subheader("Пути и Ци (Arts & Qi)")
            for art_key, art_label in ARTS_LIST:
                ac1, ac2 = st.columns([1.4, 2.2])
                with ac1:
                    st.markdown(f"<div style='padding-top: 6px;'><b>{art_label}</b></div>", unsafe_allow_html=True)
                with ac2:
                    st.radio(
                        art_label,
                        options=[0, 1, 2, 3, 4, 5, 6],
                        horizontal=True,
                        label_visibility="collapsed",
                        key=f"art_{art_key}",
                    )

            st.divider()
            qi_val = st.radio(
                "Уровень Ци (Qi)",
                options=[1, 2, 3, 4, 5, 6],
                horizontal=True,
                key="qi_level",
            )
            st.number_input(
                "Уровень дисбаланса (Imbalance Rating)",
                min_value=0,
                max_value=30,
                step=1,
                key="imbalance_rating",
            )

    with top_right:
        with st.container(border=True):
            st.subheader("Раны (Wounds)")
            auto_wounds = st.checkbox(
                "Авторасчёт макс. ран (Ци × 2 + 1)",
                key="max_wounds_auto",
            )
            if auto_wounds:
                st.session_state["max_wounds"] = qi_val * 2 + 1

            w1, w2 = st.columns(2)
            w1.number_input(
                "Макс. раны (Max Wounds)",
                min_value=1,
                max_value=100,
                step=1,
                key="max_wounds",
                disabled=auto_wounds,
            )
            w2.number_input(
                "Текущие раны (Current Wounds)",
                min_value=-50,
                max_value=100,
                step=1,
                key="current_wounds",
            )

        with st.container(border=True):
            st.subheader("Боевые техники (Combat Techniques)")
            st.text_area(
                "Список боевых техник",
                key="combat_techniques",
                height=165,
                label_visibility="collapsed",
                placeholder="Впишите известные боевые техники...",
            )

    st.divider()

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        with st.container(border=True):
            pts_combat = render_skill_group("Боевые (Combat)", "combat", COMBAT_SKILLS)

        with st.container(border=True):
            pts_specialist = render_skill_group("Специальные (Specialist)", "specialist", SPECIALIST_SKILLS)

        with st.container(border=True):
            pts_mental = render_skill_group("Ментальные (Mental)", "mental", MENTAL_SKILLS)

    with col_right:
        with st.container(border=True):
            pts_physical = render_skill_group("Физические (Physical)", "physical", PHYSICAL_SKILLS)

        with st.container(border=True):
            pts_knowledge = render_skill_group("Знания (Knowledge)", "knowledge", KNOWLEDGE_SKILLS)

        with st.container(border=True):
            st.subheader("Недостатки (Flaws)")
            st.text_area(
                "Недостатки персонажа",
                key="flaws",
                height=140,
                label_visibility="collapsed",
                placeholder="Впишите недостатки персонажа...",
            )

with tab2:
    top2_left, top2_mid, top2_right = st.columns([1.1, 1.0, 1.2], gap="medium")

    with top2_left:
        with st.container(border=True):
            st.subheader("Семья (Family)")
            st.text_input("Кол-во братьев/сестёр (No. Siblings)", key="family_siblings_count")
            st.text_input("Порядок рождения (Birth Order)", key="family_birth_order")
            st.text_input("Мать (Mother)", key="family_mother")
            st.text_input("Отец (Father)", key="family_father")
            st.text_input("Сёстры (Sister(s))", key="family_sisters")
            st.text_input("Братья (Brother(s))", key="family_brothers")
            st.text_input("Названая семья (Sworn Family)", key="family_sworn")
            st.text_area("Прочие (Other(s))", key="family_other", height=80)

    with top2_mid:
        with st.container(border=True):
            st.subheader("Обиды и враги (Grudges)")
            st.text_area(
                "Обиды",
                key="grudges",
                height=445,
                label_visibility="collapsed",
                placeholder="Запишите обиды, долги чести и врагов...",
            )

    with top2_right:
        with st.container(border=True):
            st.subheader("Снаряжение (Equipment)")
            st.text_area(
                "Снаряжение",
                key="equipment",
                height=445,
                label_visibility="collapsed",
                placeholder="Оружие, доспехи, одежда, особые предметы...",
            )

    mid2_left, mid2_mid, mid2_right = st.columns([1.0, 1.0, 1.3], gap="medium")

    with mid2_left:
        with st.container(border=True):
            st.subheader("Деньги (Money)")
            st.text_input("Ляны / Таэли (Taels)", key="money_taels")
            st.text_input("Империалы (Imperials)", key="money_imperials")
            st.text_input("Лопаты / Монеты (Spades)", key="money_spades")
            st.text_input("Ляны (Liangs)", key="money_liangs")
            st.text_input("Бумажные деньги (Paper Currency)", key="money_paper")

    with mid2_mid:
        with st.container(border=True):
            st.subheader("Опыт (Experience)")
            st.text_area(
                "Очки опыта",
                key="experience",
                height=265,
                label_visibility="collapsed",
                placeholder="Текущий и потраченный опыт...",
            )

    with mid2_right:
        with st.container(border=True):
            st.subheader("Очки дисбаланса (Imbalance Points)")
            st.slider(
                "Текущие очки дисбаланса (0–10)",
                min_value=0,
                max_value=10,
                step=1,
                key="imbalance_points",
            )
            st.radio(
                "Бонус за уровень Ци (Bonus for Qi Level)",
                options=[1, 2, 3, 4, 5, 6],
                horizontal=True,
                key="imbalance_bonus_qi",
            )

    st.divider()

    with st.container(border=True):
        st.subheader("Техники Кунг-фу (Kung Fu Techniques)")
        b_add, b_rem, _ = st.columns([1, 1, 4])
        if b_add.button("➕ Добавить строку"):
            st.session_state["kung_fu_techniques"].append({"normal": "", "counter": "", "stance": ""})
            st.rerun()
        if b_rem.button("➖ Удалить строку") and len(st.session_state["kung_fu_techniques"]) > 1:
            st.session_state["kung_fu_techniques"].pop()
            st.rerun()

        h1, h2, h3 = st.columns([2, 1.2, 1.2])
        h1.markdown("**Обычная техника (Normal)**")
        h2.markdown("**Контрприём (Counter)**")
        h3.markdown("**Стойка (Stance)**")

        for idx, row in enumerate(st.session_state["kung_fu_techniques"]):
            c1, c2, c3 = st.columns([2, 1.2, 1.2])
            row["normal"] = c1.text_area(
                f"Normal {idx+1}",
                value=row.get("normal", ""),
                key=f"kf_normal_{idx}",
                height=75,
                label_visibility="collapsed",
            )
            row["counter"] = c2.text_area(
                f"Counter {idx+1}",
                value=row.get("counter", ""),
                key=f"kf_counter_{idx}",
                height=75,
                label_visibility="collapsed",
            )
            row["stance"] = c3.text_area(
                f"Stance {idx+1}",
                value=row.get("stance", ""),
                key=f"kf_stance_{idx}",
                height=75,
                label_visibility="collapsed",
            )

total_skill_points = (
    pts_combat + pts_specialist + pts_mental + pts_physical + pts_knowledge
)

with points_summary_placeholder.container():
    st.subheader("📊 Потраченные очки навыков")
    st.caption("Расчёт: 1 ранг = 1, 2 ранг = 3, 3 ранг = 6")
    st.markdown(f"**Боевые:** {pts_combat} очк.")
    st.markdown(f"**Специальные:** {pts_specialist} очк.")
    st.markdown(f"**Ментальные:** {pts_mental} очк.")
    st.markdown(f"**Физические:** {pts_physical} очк.")
    st.markdown(f"**Знания:** {pts_knowledge} очк.")
    st.metric("Всего очков в навыки", total_skill_points)
