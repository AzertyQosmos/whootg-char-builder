import json
from copy import deepcopy
import streamlit as st

st.set_page_config(
    page_title="Wandering Heroes of Ogre Gate — Лист персонажа",
    page_icon="🥋",
    layout="wide",
)

SKILL_GROUPS = {
    "combat": {
        "title": "Боевые (Combat)",
        "fixed": [
            ("arm_strike", "Удар рукой (Arm Strike)"),
            ("leg_strike", "Удар ногой (Leg Strike)"),
            ("grapple", "Захват (Grapple)"),
            ("throw", "Бросок (Throw)"),
            ("light_melee", "Лёгкое ближнее (Light Melee)"),
            ("medium_melee", "Среднее ближнее (Medium Melee)"),
            ("heavy_melee", "Тяжёлое ближнее (Heavy Melee)"),
            ("small_ranged", "Малое дальнобойное (Small Ranged)"),
            ("large_ranged", "Большое дальнобойное (Large Ranged)"),
        ],
        "custom": [],
    },
    "specialist": {
        "title": "Специальные (Specialist)",
        "fixed": [
            ("medicine", "Медицина (Medicine)"),
            ("divination", "Прорицание (Divination)"),
            ("meditation", "Медитация (Meditation)"),
        ],
        "custom": [
            ("talent_1", "Талант 1 (Talent)"),
            ("talent_2", "Талант 2 (Talent)"),
            ("trade_1", "Ремесло 1 (Trade)"),
            ("trade_2", "Ремесло 2 (Trade)"),
            ("survival_1", "Выживание 1 (Survival)"),
            ("survival_2", "Выживание 2 (Survival)"),
            ("ritual_1", "Ритуал 1 (Ritual)"),
            ("ritual_2", "Ритуал 2 (Ritual)"),
            ("ritual_3", "Ритуал 3 (Ritual)"),
        ],
    },
    "mental": {
        "title": "Ментальные (Mental)",
        "fixed": [
            ("command", "Командование (Command)"),
            ("persuade", "Убеждение (Persuade)"),
            ("deception", "Обман (Deception)"),
            ("empathy", "Эмпатия (Empathy)"),
            ("reasoning", "Логика (Reasoning)"),
            ("detect", "Наблюдательность (Detect)"),
        ],
        "custom": [],
    },
    "physical": {
        "title": "Физические (Physical)",
        "fixed": [
            ("athletics", "Атлетика (Athletics)"),
            ("swim", "Плавание (Swim)"),
            ("speed", "Скорость (Speed)"),
            ("muscle", "Сила (Muscle)"),
            ("endurance", "Выносливость (Endurance)"),
            ("ride", "Верховая езда (Ride)"),
            ("sail", "Мореходство (Sail)"),
        ],
        "custom": [],
    },
    "knowledge": {
        "title": "Знания (Knowledge)",
        "fixed": [],
        "custom": [
            ("history_1", "История 1 (History)"),
            ("history_2", "История 2 (History)"),
            ("creatures_1", "Существа 1 (Creatures)"),
            ("creatures_2", "Существа 2 (Creatures)"),
            ("places_1", "Места и культуры 1 (Places/Cultures)"),
            ("places_2", "Места и культуры 2 (Places/Cultures)"),
            ("disciplines_1", "Боевые школы 1 (Martial Disciplines)"),
            ("disciplines_2", "Боевые школы 2 (Martial Disciplines)"),
            ("institutions_1", "Институты 1 (Institutions)"),
            ("institutions_2", "Институты 2 (Institutions)"),
            ("language_1", "Язык 1 (Language)"),
            ("language_2", "Язык 2 (Language)"),
            ("script_1", "Письменность 1 (Read Script)"),
            ("script_2", "Письменность 2 (Read Script)"),
            ("religion_1", "Религия и боги 1 (Religion/Gods)"),
            ("religion_2", "Религия и боги 2 (Religion/Gods)"),
            ("classics_1", "Классические тексты 1 (Classics)"),
            ("classics_2", "Классические тексты 2 (Classics)"),
        ],
    },
}

DEFENSES_META = [
    ("hardiness", "Стойкость (Hardiness)", 3, 4),
    ("parry", "Парирование (Parry)", 3, 4),
    ("evade", "Уклонение (Evade)", 3, 4),
    ("stealth", "Скрытность (Stealth)", 6, 1),
    ("wits", "Смекалка (Wits)", 6, 1),
    ("resolve", "Решимость (Resolve)", 6, 1),
]


def triangular_cost(rank: int) -> int:
    r = max(0, int(rank))
    return r * (r + 1) // 2


def calc_group_points(char_data: dict, group_key: str) -> int:
    group = SKILL_GROUPS[group_key]
    total = 0
    for key, _ in group["fixed"]:
        total += triangular_cost(char_data["skills"][group_key][key])
    for key, _ in group["custom"]:
        total += triangular_cost(char_data["skills"][group_key][key]["rank"])
    return total


def calc_all_points(char_data: dict) -> dict:
    by_group = {k: calc_group_points(char_data, k) for k in SKILL_GROUPS}
    return {
        "by_group": by_group,
        "total": sum(by_group.values()),
    }


def get_default_character() -> dict:
    skills = {}
    expertise = {}
    for group_key, group in SKILL_GROUPS.items():
        skills[group_key] = {}
        for key, _ in group["fixed"]:
            skills[group_key][key] = 0
        for key, _ in group["custom"]:
            skills[group_key][key] = {"spec": "", "rank": 0}
        expertise[group_key] = ""

    defenses = {}
    for key, _, base_val, _ in DEFENSES_META:
        defenses[key] = {
            "base": base_val,
            "mod1": 0,
            "mod2": 0,
            "auto": True,
            "manual_total": base_val,
        }

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
        "defenses": defenses,
        "wounds": {
            "auto_max": True,
            "manual_max": 3,
            "current": 3,
        },
        "qi": 1,
        "imbalance": {
            "rating": 0,
            "points": 0,
            "bonus_for_qi": [0, 0, 0, 0, 0, 0],
        },
        "inner_arts": {
            "dianxue": "",
            "waijia": "",
            "qinggong": "",
            "neigong": "",
        },
        "combat_techniques": "",
        "flaws": "",
        "skills": skills,
        "expertise": expertise,
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
            {"normal": "", "counter": "", "stance": ""},
            {"normal": "", "counter": "", "stance": ""},
            {"normal": "", "counter": "", "stance": ""},
        ],
    }


def merge_with_default(loaded: dict) -> dict:
    base = get_default_character()

    def deep_update(dst, src):
        for k, v in src.items():
            if k in dst and isinstance(dst[k], dict) and isinstance(v, dict):
                deep_update(dst[k], v)
            else:
                dst[k] = v

    if isinstance(loaded, dict):
        deep_update(base, loaded)
    return base


if "char" not in st.session_state:
    st.session_state.char = get_default_character()
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

char = st.session_state.char
points_summary = calc_all_points(char)

# --- Боковая панель: Экспорт / Импорт / Сводка очков / Сброс ---
with st.sidebar:
    st.header("📜 Управление листом")

    st.subheader("📊 Потраченные очки навыков")
    st.caption("Расчёт: 1 ранг = 1, 2 ранг = 3, 3 ранг = 6")
    for g_key, g_info in SKILL_GROUPS.items():
        short_title = g_info["title"].split(" (")[0]
        st.write(f"**{short_title}:** {points_summary['by_group'][g_key]} очк.")
    st.metric("Всего очков в навыках", points_summary["total"])

    st.divider()

    file_label = char["identity"]["name"].strip() or "whog_character"
    safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in file_label)

    json_payload = json.dumps(char, ensure_ascii=False, indent=2)
    st.download_button(
        label="💾 Скачать персонажа (JSON)",
        data=json_payload.encode("utf-8"),
        file_name=f"{safe_name}.json",
        mime="application/json",
        use_container_width=True,
        type="primary",
    )

    st.divider()
    st.subheader("📂 Загрузить из JSON")
    uploaded = st.file_uploader(
        "Выберите файл .json",
        type=["json"],
        key=f"json_loader_{st.session_state.uploader_key}",
    )
    if uploaded is not None:
        try:
            raw_data = json.load(uploaded)
            st.session_state.char = merge_with_default(raw_data)
            st.session_state.uploader_key += 1
            st.rerun()
        except Exception as err:
            st.error(f"Ошибка чтения JSON: {err}")

    st.divider()
    if st.button("🗑️ Очистить весь лист", use_container_width=True):
        st.session_state.char = get_default_character()
        st.session_state.uploader_key += 1
        st.rerun()

st.title("🥋 Wandering Heroes of Ogre Gate — Лист персонажа")

tab_front, tab_back = st.tabs(["📄 Лицевая сторона (Основные параметры и навыки)", "📜 Обратная сторона (Семья, снаряжение и техники кунг-фу)"])

# ==============================================================================
# ВКЛАДКА 1: ЛИЦЕВАЯ СТОРОНА ЛИСТА
# ==============================================================================
with tab_front:
    st.subheader("Общие сведения")
    r1 = st.columns([2, 2, 1.5])
    char["identity"]["name"] = r1[0].text_input("Имя (Name)", value=char["identity"]["name"])
    char["identity"]["martial_name"] = r1[1].text_input("Боевое имя (Martial Name)", value=char["identity"]["martial_name"])
    char["identity"]["nickname"] = r1[2].text_input("Прозвище (Nickname)", value=char["identity"]["nickname"])

    r2 = st.columns([2, 2, 1.5])
    char["identity"]["sifu"] = r2[0].text_input("Наставник / Сифу (Sifu)", value=char["identity"]["sifu"])
    char["identity"]["player"] = r2[1].text_input("Игрок (Player)", value=char["identity"]["player"])
    char["identity"]["campaign"] = r2[2].text_input("Кампания (Campaign)", value=char["identity"]["campaign"])

    r3 = st.columns([1.2, 1, 2, 1.8])
    char["identity"]["ht_wt"] = r3[0].text_input("Рост / Вес (Ht./Wt.)", value=char["identity"]["ht_wt"])
    char["identity"]["sex"] = r3[1].text_input("Пол (Sex)", value=char["identity"]["sex"])
    char["identity"]["titles"] = r3[2].text_input("Титулы (Title(s))", value=char["identity"]["titles"])
    char["identity"]["age"] = r3[3].text_input("Возраст (Age)", value=char["identity"]["age"])

    r4 = st.columns([1.5, 1.5, 1.5, 1.5, 1.5])
    char["identity"]["homeland_clan"] = r4[0].text_input("Родина / Клан (Homeland/Clan)", value=char["identity"]["homeland_clan"])
    char["identity"]["sect"] = r4[1].text_input("Секта / Школа (Sect)", value=char["identity"]["sect"])
    char["identity"]["occupation"] = r4[2].text_input("Род занятий (Occupation)", value=char["identity"]["occupation"])
    char["identity"]["family_name"] = r4[3].text_input("Семья (Family)", value=char["identity"]["family_name"])
    char["identity"]["reputation"] = r4[4].text_input("Репутация (Reputation)", value=char["identity"]["reputation"])

    st.divider()

    col_left, col_mid, col_right = st.columns([1.15, 1.1, 1.15], gap="medium")

    # --- ЛЕВАЯ КОЛОНКА: ЗАЩИТЫ + БОЕВЫЕ + СПЕЦИАЛЬНЫЕ + МЕНТАЛЬНЫЕ ---
    with col_left:
        with st.container(border=True):
            st.subheader("🛡️ Защиты (Defenses)")
            st.caption("Формула: База + Мод. 1 + Мод. 2 (снимите «Авто» для ручного ввода)")
            for d_key, d_label, default_base, max_m1 in DEFENSES_META:
                d_obj = char["defenses"][d_key]
                c_name, c_base, c_m1, c_m2, c_tot, c_auto = st.columns([2.2, 1.0, 1.0, 1.0, 1.1, 0.9])
                c_name.markdown(f"**{d_label}**")
                d_obj["base"] = c_base.number_input(
                    "База", value=int(d_obj["base"]), step=1, key=f"def_base_{d_key}", label_visibility="collapsed"
                )
                d_obj["mod1"] = c_m1.number_input(
                    "Мод 1", value=int(d_obj["mod1"]), step=1, key=f"def_m1_{d_key}", label_visibility="collapsed"
                )
                d_obj["mod2"] = c_m2.number_input(
                    "Мод 2", value=int(d_obj["mod2"]), step=1, key=f"def_m2_{d_key}", label_visibility="collapsed"
                )
                d_obj["auto"] = c_auto.checkbox("Авто", value=bool(d_obj["auto"]), key=f"def_auto_{d_key}")

                calc_val = int(d_obj["base"]) + int(d_obj["mod1"]) + int(d_obj["mod2"])
                if d_obj["auto"]:
                    d_obj["manual_total"] = calc_val
                    c_tot.number_input(
                        "Итог", value=calc_val, disabled=True, key=f"def_tot_disp_{d_key}", label_visibility="collapsed"
                    )
                else:
                    d_obj["manual_total"] = c_tot.number_input(
                        "Итог", value=int(d_obj["manual_total"]), step=1, key=f"def_tot_man_{d_key}", label_visibility="collapsed"
                    )

        def render_skill_block(group_key: str):
            group = SKILL_GROUPS[group_key]
            with st.container(border=True):
                h_col1, h_col2 = st.columns([2.4, 1.2])
                h_col1.subheader(group["title"])
                current_pts = calc_group_points(char, group_key)
                h_col2.metric("Очки категории", f"{current_pts}")

                for s_key, s_label in group["fixed"]:
                    sc1, sc2, sc3 = st.columns([2.6, 1.3, 0.7])
                    sc1.write(s_label)
                    rank_val = int(char["skills"][group_key][s_key])
                    new_rank = sc2.radio(
                        s_label,
                        options=[0, 1, 2, 3],
                        index=rank_val,
                        horizontal=True,
                        key=f"sk_{group_key}_{s_key}",
                        label_visibility="collapsed",
                    )
                    char["skills"][group_key][s_key] = new_rank
                    sc3.caption(f"{triangular_cost(new_rank)} очк.")

                for s_key, s_label in group["custom"]:
                    sc1, sc2, sc3 = st.columns([2.6, 1.3, 0.7])
                    char["skills"][group_key][s_key]["spec"] = sc1.text_input(
                        s_label,
                        value=char["skills"][group_key][s_key]["spec"],
                        placeholder=s_label,
                        key=f"sk_spec_{group_key}_{s_key}",
                        label_visibility="collapsed",
                    )
                    rank_val = int(char["skills"][group_key][s_key]["rank"])
                    new_rank = sc2.radio(
                        f"{s_label}_rank",
                        options=[0, 1, 2, 3],
                        index=rank_val,
                        horizontal=True,
                        key=f"sk_rank_{group_key}_{s_key}",
                        label_visibility="collapsed",
                    )
                    char["skills"][group_key][s_key]["rank"] = new_rank
                    sc3.caption(f"{triangular_cost(new_rank)} очк.")

                char["expertise"][group_key] = st.text_area(
                    f"Специализации — {group['title']} (Expertise)",
                    value=char["expertise"][group_key],
                    height=75,
                    key=f"exp_{group_key}",
                )

        render_skill_block("combat")
        render_skill_block("specialist")
        render_skill_block("mental")

    # --- ЦЕНТРАЛЬНАЯ КОЛОНКА: ВНУТРЕННИЕ ИСКУССТВА + ДИСБАЛАНС + ЦИ + БОЕВЫЕ ТЕХНИКИ ---
    with col_mid:
        with st.container(border=True):
            st.subheader("☯️ Внутренние школы (Inner Arts)")
            ia1, ia2 = st.columns(2)
            char["inner_arts"]["dianxue"] = ia1.text_input("Дяньсюэ (Dianxue)", value=char["inner_arts"]["dianxue"])
            char["inner_arts"]["waijia"] = ia2.text_input("Вайцзя (Waijia)", value=char["inner_arts"]["waijia"])
            ia3, ia4 = st.columns(2)
            char["inner_arts"]["qinggong"] = ia3.text_input("Цингун (Qinggong)", value=char["inner_arts"]["qinggong"])
            char["inner_arts"]["neigong"] = ia4.text_input("Нэйгун (Neigong)", value=char["inner_arts"]["neigong"])

        with st.container(border=True):
            st.subheader("🔥 Уровень Ци (Qi)")
            char["qi"] = st.radio(
                "Значение Ци (1–6)",
                options=[1, 2, 3, 4, 5, 6],
                index=max(0, min(5, int(char["qi"]) - 1)),
                horizontal=True,
            )

        with st.container(border=True):
            st.subheader("⚖️ Дисбаланс (Imbalance Rating)")
            char["imbalance"]["rating"] = st.number_input(
                "Рейтинг дисбаланса (Imbalance Rating)",
                min_value=0,
                max_value=20,
                value=int(char["imbalance"]["rating"]),
                step=1,
            )

        with st.container(border=True):
            st.subheader("⚔️ Боевые техники (Combat Techniques)")
            char["combat_techniques"] = st.text_area(
                "Список боевых техник",
                value=char["combat_techniques"],
                height=520,
                label_visibility="collapsed",
                placeholder="Запишите изученные боевые техники, эффекты и требования...",
            )

    # --- ПРАВАЯ КОЛОНКА: РАНЫ + ФИЗИЧЕСКИЕ + ЗНАНИЯ + НЕДОСТАТКИ ---
    with col_right:
        with st.container(border=True):
            st.subheader("❤️ Раны (Wounds)")
            w1, w2, w3 = st.columns([1.3, 1.3, 0.9])
            char["wounds"]["auto_max"] = w3.checkbox(
                "Авто (Ци×2+1)", value=bool(char["wounds"]["auto_max"]), key="wounds_auto"
            )
            calc_wounds = int(char["qi"]) * 2 + 1
            if char["wounds"]["auto_max"]:
                char["wounds"]["manual_max"] = calc_wounds
                w1.number_input("Макс. ран (Max Wounds)", value=calc_wounds, disabled=True, key="wounds_max_disp")
            else:
                char["wounds"]["manual_max"] = w1.number_input(
                    "Макс. ран (Max Wounds)", min_value=1, value=int(char["wounds"]["manual_max"]), step=1, key="wounds_max_man"
                )
            char["wounds"]["current"] = w2.number_input(
                "Текущие раны (Current Wounds)", value=int(char["wounds"]["current"]), step=1, key="wounds_curr"
            )

        render_skill_block("physical")
        render_skill_block("knowledge")

        with st.container(border=True):
            st.subheader("⛓️ Недостатки и изъяны (Flaws)")
            char["flaws"] = st.text_area(
                "Недостатки (Flaws)",
                value=char["flaws"],
                height=140,
                label_visibility="collapsed",
                placeholder="Опишите недостатки персонажа...",
            )

# ==============================================================================
# ВКЛАДКА 2: ОБРАТНАЯ СТОРОНА ЛИСТА
# ==============================================================================
with tab_back:
    top_c1, top_c2, top_c3 = st.columns([1, 1, 1.3], gap="medium")

    with top_c1:
        with st.container(border=True):
            st.subheader("🏮 Семья (Family)")
            f_sub1, f_sub2 = st.columns(2)
            char["family"]["num_siblings"] = f_sub1.text_input("Кол-во братьев/сестёр (No. Siblings)", value=char["family"]["num_siblings"])
            char["family"]["birth_order"] = f_sub2.text_input("Порядок рождения (Birth Order)", value=char["family"]["birth_order"])
            char["family"]["mother"] = st.text_input("Мать (Mother)", value=char["family"]["mother"])
            char["family"]["father"] = st.text_input("Отец (Father)", value=char["family"]["father"])
            char["family"]["sisters"] = st.text_input("Сёстры (Sister(s))", value=char["family"]["sisters"])
            char["family"]["brothers"] = st.text_input("Братья (Brother(s))", value=char["family"]["brothers"])
            char["family"]["sworn_family"] = st.text_input("Названая семья (Sworn Family)", value=char["family"]["sworn_family"])
            char["family"]["others"] = st.text_area("Прочие родственники (Other(s))", value=char["family"]["others"], height=70)

        with st.container(border=True):
            st.subheader("💰 Деньги (Money)")
            m1, m2 = st.columns(2)
            char["money"]["taels"] = m1.text_input("Таэли (Taels)", value=char["money"]["taels"])
            char["money"]["imperials"] = m2.text_input("Империалы (Imperials)", value=char["money"]["imperials"])
            m3, m4 = st.columns(2)
            char["money"]["spades"] = m3.text_input("Монеты-лопаты (Spades)", value=char["money"]["spades"])
            char["money"]["liangs"] = m4.text_input("Ляны (Liangs)", value=char["money"]["liangs"])
            char["money"]["paper_currency"] = st.text_input("Бумажные ассигнации (Paper Currency)", value=char["money"]["paper_currency"])

    with top_c2:
        with st.container(border=True):
            st.subheader("💢 Обиды и вендетты (Grudges)")
            char["grudges"] = st.text_area(
                "Обиды (Grudges)",
                value=char["grudges"],
                height=395,
                label_visibility="collapsed",
                placeholder="Кто, за что и кому должен отомстить...",
            )

        with st.container(border=True):
            st.subheader("✨ Опыт (Experience)")
            char["experience"] = st.text_area(
                "Опыт (Experience)",
                value=char["experience"],
                height=165,
                label_visibility="collapsed",
                placeholder="Текущий / всего заработано очков опыта, заметки по тратам...",
            )

    with top_c3:
        with st.container(border=True):
            st.subheader("🎒 Снаряжение (Equipment)")
            char["equipment"] = st.text_area(
                "Снаряжение (Equipment)",
                value=char["equipment"],
                height=425,
                label_visibility="collapsed",
                placeholder="Оружие, доспехи, целебные травы, артефакты, поклажа...",
            )

        with st.container(border=True):
            st.subheader("🌀 Очки дисбаланса (Imbalance Points)")
            char["imbalance"]["points"] = st.slider(
                "Накопленные очки дисбаланса (0–10)",
                min_value=0,
                max_value=10,
                value=int(char["imbalance"]["points"]),
            )
            st.caption("Бонус за уровень Ци (Bonus for Qi Level 1–6)")
            b_cols = st.columns(6)
            for idx in range(6):
                char["imbalance"]["bonus_for_qi"][idx] = b_cols[idx].number_input(
                    f"Ци {idx + 1}",
                    value=int(char["imbalance"]["bonus_for_qi"][idx]),
                    step=1,
                    key=f"imb_bonus_{idx}",
                )

    st.divider()

    with st.container(border=True):
        h_kf1, h_kf2 = st.columns([3, 1])
        h_kf1.subheader("🐉 Техники кунг-фу (Kung Fu Techniques)")
        if h_kf2.button("➕ Добавить строку техники", use_container_width=True):
            char["kung_fu_techniques"].append({"normal": "", "counter": "", "stance": ""})
            st.rerun()

        col_h1, col_h2, col_h3, col_h4 = st.columns([2.2, 1.5, 1.5, 0.4])
        col_h1.markdown("**Обычная техника (Normal)**")
        col_h2.markdown("**Контратака (Counter)**")
        col_h3.markdown("**Стойка (Stance)**")

        to_delete = None
        for i, row in enumerate(char["kung_fu_techniques"]):
            c1, c2, c3, c4 = st.columns([2.2, 1.5, 1.5, 0.4])
            row["normal"] = c1.text_input(
                f"Normal {i}", value=row["normal"], key=f"kf_norm_{i}", label_visibility="collapsed", placeholder="Название и эффект..."
            )
            row["counter"] = c2.text_input(
                f"Counter {i}", value=row["counter"], key=f"kf_cnt_{i}", label_visibility="collapsed", placeholder="Контратака..."
            )
            row["stance"] = c3.text_input(
                f"Stance {i}", value=row["stance"], key=f"kf_stn_{i}", label_visibility="collapsed", placeholder="Стойка..."
            )
            if len(char["kung_fu_techniques"]) > 1:
                if c4.button("✖", key=f"kf_del_{i}", help="Удалить строку"):
                    to_delete = i

        if to_delete is not None:
            char["kung_fu_techniques"].pop(to_delete)
            st.rerun()
