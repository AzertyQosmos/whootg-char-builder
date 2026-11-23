import json
import streamlit as st

st.set_page_config(
    page_title="Wandering Heroes of Ogre Gate — Лист персонажа",
    page_icon="⚔️",
    layout="wide",
)

SKILL_CATEGORIES = [
    (
        "combat",
        "Боевые (Combat)",
        [
            ("arm_strike", "Удар рукой (Arm Strike)"),
            ("blade", "Клинок (Blade)"),
            ("bow", "Лук (Bow)"),
            ("cudgel", "Дубина / Посох (Cudgel)"),
            ("foot_strike", "Удар ногой (Foot Strike)"),
            ("grapple", "Захват / Борьба (Grapple)"),
            ("improvised_weapon", "Импровизированное оружие (Improvised Weapon)"),
            ("polearm", "Древковое оружие (Polearm)"),
            ("special_weapon", "Особое оружие (Special Weapon)"),
            ("thrown_weapon", "Метательное оружие (Thrown Weapon)"),
            ("whip", "Кнут / Цепь (Whip)"),
        ],
    ),
    (
        "specialist",
        "Специальные (Specialist)",
        [
            ("command", "Командование (Command)"),
            ("convince", "Убеждение (Convince)"),
            ("disguise", "Маскировка (Disguise)"),
            ("intimidate", "Запугивание (Intimidate)"),
            ("seduce", "Соблазнение (Seduce)"),
            ("sense", "Чутьё / Проницательность (Sense)"),
            ("steal", "Воровство (Steal)"),
            ("trade", "Торговля (Trade)"),
        ],
    ),
    (
        "mental",
        "Ментальные (Mental)",
        [
            ("acting", "Актёрское мастерство (Acting)"),
            ("animal_handling", "Обращение с животными (Animal Handling)"),
            ("art", "Искусство (Art)"),
            ("crafting", "Ремесло (Crafting)"),
            ("gambling", "Азартные игры (Gambling)"),
            ("healing", "Врачевание (Healing)"),
            ("investigate", "Расследование (Investigate)"),
            ("navigation", "Навигация (Navigation)"),
            ("strategy", "Стратегия (Strategy)"),
            ("survival", "Выживание (Survival)"),
        ],
    ),
    (
        "physical",
        "Физические (Physical)",
        [
            ("acrobatics", "Акробатика (Acrobatics)"),
            ("athletics", "Атлетика (Athletics)"),
            ("endurance", "Выносливость (Endurance)"),
            ("escape", "Побег / Освобождение (Escape)"),
            ("feats_of_strength", "Подвиги силы (Feats of Strength)"),
            ("ride", "Верховая езда (Ride)"),
            ("sneak", "Скрытность / Красться (Sneak)"),
        ],
    ),
    (
        "knowledge",
        "Знания (Knowledge)",
        [
            ("academic", "Академические (Academic)"),
            ("folklore", "Фольклор (Folklore)"),
            ("geography", "География (Geography)"),
            ("history", "История (History)"),
            ("law", "Закон (Law)"),
            ("medicine", "Медицина (Medicine)"),
            ("occult", "Оккультизм (Occult)"),
            ("politics", "Политика (Politics)"),
            ("underworld", "Преступный мир (Underworld)"),
        ],
    ),
]

DEFENSES = [
    ("hardiness", "Стойкость (Hardiness)", 3),
    ("parry", "Парирование (Parry)", 3),
    ("evade", "Уклонение (Evade)", 3),
    ("stealth", "Скрытность (Stealth)", 6),
    ("wits", "Смекалка (Wits)", 6),
    ("resolve", "Решимость (Resolve)", 6),
]

ARTS = [
    ("dianxue", "Дяньсюэ (Dianxue)"),
    ("waijia", "Вайцзя (Waijia)"),
    ("qinggong", "Цингун (Qinggong)"),
    ("neigong", "Нэйгун (Neigong)"),
]

TECHNIQUE_TYPES = ["Normal", "Counter", "Stance"]


def skill_cost(rank: int) -> int:
    r = max(0, int(rank))
    return r * (r + 1) // 2


def default_state() -> dict:
    state = {
        "name": "",
        "concept": "",
        "sect": "",
        "virtues": "",
        "flaws": "",
        "combat_techniques": "",
        "qi": 1,
        "wounds_current": 0,
        "wounds_max_auto": True,
        "wounds_max_manual": 3,
        "imbalance_yin": 0,
        "imbalance_yang": 0,
        "family_title": "",
        "family_description": "",
        "grievances": "",
        "silver": 0,
        "copper": 0,
        "gold": 0,
        "jade": 0,
        "equipment": "",
        "xp_available": 0,
        "xp_total": 0,
        "notes": "",
        "kung_fu_techniques": [
            {"name": "", "type": "Normal", "notes": ""}
        ],
    }

    for key, _, base_val in DEFENSES:
        state[f"def_{key}_base"] = base_val
        state[f"def_{key}_mod1"] = 0
        state[f"def_{key}_mod2"] = 0
        state[f"def_{key}_auto"] = True
        state[f"def_{key}_manual"] = base_val

    for key, _ in ARTS:
        state[f"art_{key}"] = 0

    for _, _, skills in SKILL_CATEGORIES:
        for sk_key, _ in skills:
            state[f"sk_{sk_key}_rank"] = 0
            state[f"sk_{sk_key}_exp"] = ""

    return state


def init_session():
    defaults = default_state()
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def load_json_data(raw: dict):
    defaults = default_state()
    for k, default_val in defaults.items():
        if k in raw:
            val = raw[k]
            if k.startswith("art_") and isinstance(val, bool):
                val = 1 if val else 0
            st.session_state[k] = val
        else:
            st.session_state[k] = default_val


def export_json_data() -> str:
    defaults = default_state()
    data = {}
    for k in defaults:
        data[k] = st.session_state.get(k, defaults[k])
    return json.dumps(data, ensure_ascii=False, indent=2)


init_session()

st.title("⚔️ Wandering Heroes of Ogre Gate — Лист персонажа")

with st.sidebar:
    st.header("📜 Управление листом")

    st.subheader("Загрузить персонажа (JSON)")
    uploaded = st.file_uploader(
        "Выберите JSON-файл",
        type=["json"],
        label_visibility="collapsed",
    )
    if uploaded is not None:
        file_id = f"{uploaded.name}_{uploaded.size}"
        if st.session_state.get("_last_uploaded_id") != file_id:
            try:
                parsed = json.loads(uploaded.read().decode("utf-8"))
                load_json_data(parsed)
                st.session_state["_last_uploaded_id"] = file_id
                st.success("Персонаж загружен!")
                st.rerun()
            except Exception as exc:
                st.error(f"Ошибка чтения JSON: {exc}")

    st.divider()

    sidebar_points_placeholder = st.empty()

    st.divider()

    download_placeholder = st.empty()

    st.divider()
    if st.button("🗑️ Сбросить лист", use_container_width=True):
        load_json_data(default_state())
        st.session_state.pop("_last_uploaded_id", None)
        st.rerun()

tab_main, tab_skills, tab_kungfu = st.tabs(
    ["1. Основное, защиты и Ци", "2. Навыки (Skills)", "3. Кунг-фу, семья и имущество"]
)

with tab_main:
    st.subheader("Общие сведения")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.text_input("Имя (Name)", key="name")
    with c2:
        st.text_input("Концепт (Concept)", key="concept")
    with c3:
        st.text_input("Секта / Школа (Sect)", key="sect")

    c_v, c_f, c_ct = st.columns(3)
    with c_v:
        st.text_area("Добродетели (Virtues)", key="virtues", height=110)
    with c_f:
        st.text_area("Изъяны (Flaws)", key="flaws", height=110)
    with c_ct:
        st.text_area("Боевые приёмы (Combat Techniques)", key="combat_techniques", height=110)

    st.divider()

    col_def, col_qi = st.columns([3, 2], gap="large")

    with col_def:
        st.subheader("Защиты (Defenses)")
        h1, h2, h3, h4, h5, h6 = st.columns([2.2, 1, 1, 1, 1.2, 0.9])
        h1.caption("Защита")
        h2.caption("База")
        h3.caption("Мод. 1")
        h4.caption("Мод. 2")
        h5.caption("Итог")
        h6.caption("Авто")

        for key, label, _ in DEFENSES:
            r1, r2, r3, r4, r5, r6 = st.columns([2.2, 1, 1, 1, 1.2, 0.9])
            with r1:
                st.markdown(f"**{label}**")
            with r2:
                base_v = st.number_input(
                    f"База {key}",
                    min_value=0,
                    max_value=99,
                    step=1,
                    key=f"def_{key}_base",
                    label_visibility="collapsed",
                )
            with r3:
                mod1_v = st.number_input(
                    f"Мод1 {key}",
                    min_value=-99,
                    max_value=99,
                    step=1,
                    key=f"def_{key}_mod1",
                    label_visibility="collapsed",
                )
            with r4:
                mod2_v = st.number_input(
                    f"Мод2 {key}",
                    min_value=-99,
                    max_value=99,
                    step=1,
                    key=f"def_{key}_mod2",
                    label_visibility="collapsed",
                )
            with r6:
                is_auto = st.checkbox(
                    "Авто",
                    key=f"def_{key}_auto",
                    label_visibility="collapsed",
                )
            calc_total = int(base_v) + int(mod1_v) + int(mod2_v)
            with r5:
                if is_auto:
                    st.session_state[f"def_{key}_manual"] = calc_total
                    st.number_input(
                        f"Итог {key}",
                        value=calc_total,
                        disabled=True,
                        key=f"_disp_def_{key}",
                        label_visibility="collapsed",
                    )
                else:
                    st.number_input(
                        f"Итог {key}",
                        min_value=0,
                        max_value=999,
                        step=1,
                        key=f"def_{key}_manual",
                        label_visibility="collapsed",
                    )

    with col_qi:
        st.subheader("Ци и Раны (Qi & Wounds)")
        qi_val = st.number_input(
            "Уровень Ци (Qi)",
            min_value=0,
            max_value=20,
            step=1,
            key="qi",
        )

        w1, w2, w3 = st.columns([1.2, 1.2, 0.8])
        with w1:
            st.number_input(
                "Текущие раны",
                min_value=0,
                max_value=999,
                step=1,
                key="wounds_current",
            )
        with w3:
            st.write("")
            st.write("")
            w_auto = st.checkbox("Авто", key="wounds_max_auto")

        auto_max_wounds = int(qi_val) * 2 + 1
        with w2:
            if w_auto:
                st.session_state["wounds_max_manual"] = auto_max_wounds
                st.number_input(
                    "Макс. раны (Ци×2+1)",
                    value=auto_max_wounds,
                    disabled=True,
                    key="_disp_wounds_max",
                )
            else:
                st.number_input(
                    "Макс. раны",
                    min_value=0,
                    max_value=999,
                    step=1,
                    key="wounds_max_manual",
                )

        st.divider()
        st.subheader("Дисбаланс (Imbalance)")
        imb1, imb2 = st.columns(2)
        with imb1:
            st.number_input(
                "Инь (Yin)",
                min_value=0,
                max_value=50,
                step=1,
                key="imbalance_yin",
            )
        with imb2:
            st.number_input(
                "Ян (Yang)",
                min_value=0,
                max_value=50,
                step=1,
                key="imbalance_yang",
            )

        st.divider()
        st.subheader("Пути / Искусства (Arts)")
        art_cols = st.columns(2)
        for idx, (art_key, art_label) in enumerate(ARTS):
            with art_cols[idx % 2]:
                st.number_input(
                    art_label,
                    min_value=0,
                    max_value=99,
                    step=1,
                    key=f"art_{art_key}",
                )

with tab_skills:
    st.caption(
        "Стоимость рангов в категории: 1 ранг = 1 очко, 2 ранг = 3 очка, 3 ранг = 6 очков "
        "(прогрессивная сумма: 1 + 2 + 3 + ...)."
    )

    category_totals = {}
    left_cats = SKILL_CATEGORIES[:2]
    right_cats = SKILL_CATEGORIES[2:]

    col_left, col_right = st.columns(2, gap="large")

    def render_skill_category(cat_key: str, cat_title: str, skills: list):
        header_col, metric_col = st.columns([3, 1.3])
        with header_col:
            st.subheader(cat_title)
        cat_metric_placeholder = metric_col.empty()

        cat_sum = 0
        for sk_key, sk_label in skills:
            c_name, c_rank, c_cost, c_exp = st.columns([2.2, 1.1, 0.8, 1.7])
            with c_name:
                st.markdown(f"<div style='padding-top: 6px;'>{sk_label}</div>", unsafe_allow_html=True)
            with c_rank:
                rk = st.number_input(
                    f"Ранг {sk_key}",
                    min_value=0,
                    max_value=20,
                    step=1,
                    key=f"sk_{sk_key}_rank",
                    label_visibility="collapsed",
                )
            cost = skill_cost(rk)
            cat_sum += cost
            with c_cost:
                st.markdown(f"<div style='padding-top: 6px; color: gray;'>{cost} очк.</div>", unsafe_allow_html=True)
            with c_exp:
                st.text_input(
                    f"Специализация {sk_key}",
                    placeholder="Специализация...",
                    key=f"sk_{sk_key}_exp",
                    label_visibility="collapsed",
                )

        cat_metric_placeholder.metric("Очки категории", cat_sum)
        category_totals[cat_title] = cat_sum
        st.divider()

    with col_left:
        for ck, ct, sks in left_cats:
            render_skill_category(ck, ct, sks)

    with col_right:
        for ck, ct, sks in right_cats:
            render_skill_category(ck, ct, sks)

with tab_kungfu:
    st.subheader("Техники Кунг-фу (Kung Fu Techniques)")
    techniques = st.session_state["kung_fu_techniques"]

    t_h1, t_h2, t_h3, t_h4 = st.columns([2.5, 1.3, 3.5, 0.5])
    t_h1.caption("Название техники")
    t_h2.caption("Тип (Normal / Counter / Stance)")
    t_h3.caption("Эффект / Описание")
    t_h4.caption("")

    to_delete = None
    for idx, tech in enumerate(techniques):
        tc1, tc2, tc3, tc4 = st.columns([2.5, 1.3, 3.5, 0.5])
        with tc1:
            tech["name"] = st.text_input(
                f"Техника имя {idx}",
                value=tech.get("name", ""),
                key=f"_kf_name_{idx}",
                label_visibility="collapsed",
            )
        with tc2:
            cur_type = tech.get("type", "Normal")
            type_idx = TECHNIQUE_TYPES.index(cur_type) if cur_type in TECHNIQUE_TYPES else 0
            tech["type"] = st.selectbox(
                f"Техника тип {idx}",
                TECHNIQUE_TYPES,
                index=type_idx,
                key=f"_kf_type_{idx}",
                label_visibility="collapsed",
            )
        with tc3:
            tech["notes"] = st.text_input(
                f"Техника заметки {idx}",
                value=tech.get("notes", ""),
                key=f"_kf_notes_{idx}",
                label_visibility="collapsed",
            )
        with tc4:
            if len(techniques) > 1:
                if st.button("✕", key=f"_kf_del_{idx}", help="Удалить технику"):
                    to_delete = idx

    if to_delete is not None:
        techniques.pop(to_delete)
        st.rerun()

    if st.button("➕ Добавить технику кунг-фу"):
        techniques.append({"name": "", "type": "Normal", "notes": ""})
        st.rerun()

    st.divider()

    col_fam, col_gear = st.columns(2, gap="large")

    with col_fam:
        st.subheader("Семья и Обиды (Family & Grievances)")
        st.text_input("Семья / Клан (Название)", key="family_title")
        st.text_area("Описание семьи / Узы", key="family_description", height=120)
        st.text_area("Обиды / Долги чести (Grievances)", key="grievances", height=120)

    with col_gear:
        st.subheader("Деньги (Money)")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.number_input("Серебро (Silver)", min_value=0, step=1, key="silver")
        with m2:
            st.number_input("Медь (Copper)", min_value=0, step=1, key="copper")
        with m3:
            st.number_input("Золото (Gold)", min_value=0, step=1, key="gold")
        with m4:
            st.number_input("Нефрит (Jade)", min_value=0, step=1, key="jade")

        st.subheader("Снаряжение (Equipment)")
        st.text_area("Список снаряжения", key="equipment", height=130, label_visibility="collapsed")

        st.subheader("Опыт (Experience)")
        xp1, xp2 = st.columns(2)
        with xp1:
            st.number_input("Доступный опыт", min_value=0, step=1, key="xp_available")
        with xp2:
            st.number_input("Всего опыта", min_value=0, step=1, key="xp_total")

    st.divider()
    st.subheader("Заметки (Notes)")
    st.text_area("Дополнительные заметки", key="notes", height=120, label_visibility="collapsed")

with sidebar_points_placeholder.container():
    st.subheader("📊 Потраченные очки навыков")
    st.caption("Расчёт: 1 ранг = 1, 2 ранг = 3, 3 ранг = 6")
    total_skill_points = 0
    for cat_title, pts in category_totals.items():
        short_title = cat_title.split(" (")[0]
        st.write(f"**{short_title}:** {pts} очк.")
        total_skill_points += pts
    st.metric("Всего очков в навыки", total_skill_points)

safe_name = (st.session_state.get("name") or "character").strip().replace(" ", "_")
download_placeholder.download_button(
    label="💾 Скачать персонажа (JSON)",
    data=export_json_data(),
    file_name=f"{safe_name}.json",
    mime="application/json",
    use_container_width=True,
    type="primary",
)
