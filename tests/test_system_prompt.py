import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.prompts.loader import load_system_prompt
from src.knowledge.loader import load_knowledge


def test_system_prompt_conversation_flow_rules():
    prompt = load_system_prompt()

    # Memoria de identificación
    assert "Si ya los dio" in prompt
    assert "confirmación" in prompt.lower()
    assert "1167462412" in prompt
    assert "vuelvas a pedir" in prompt.lower() or "re-pedir" in prompt.lower()
    assert "sin etiquetas" in prompt or "una sola línea" in prompt

    # Timing: no solo síntoma
    assert "síntoma" in prompt or "malestar" in prompt
    assert "me duele la espalda" in prompt

    # Lenguaje sin registro operativo falso
    assert "he registrado tu consulta" in prompt
    assert "No podés" in prompt or "no lo simules" in prompt

    # Plantilla derivación útil
    assert "get_current_datetime" in prompt
    assert "verbalizá" in prompt or "fecha concreta" in prompt
    assert "Informar" in prompt or "informar" in prompt
    assert "Instagram" in prompt or "canal de contacto" in prompt


def test_system_prompt_forbids_fake_enrollment():
    prompt = load_system_prompt()
    assert "LÍMITES: INFORMACIÓN VS. FORMALIZACIÓN" in prompt
    assert "procedo a registrar tu inscripción" in prompt
    assert "confirmación de inscripción" not in prompt
    assert "horario asignado" not in prompt


def test_system_prompt_temporal_tool_and_concrete_day():
    prompt = load_system_prompt()
    assert "hoy" in prompt and "mañana" in prompt
    assert "get_current_datetime" in prompt
    assert "mañabna" in prompt or "typos" in prompt
    assert "día/fecha concreta" in prompt or "fecha concreta" in prompt


def test_system_prompt_services_with_appointment_rules():
    prompt = load_system_prompt()
    assert "servicios con cita" in prompt
    assert "seña" in prompt.lower()
    assert "coordinar directamente" in prompt
    assert "pegá el dato concreto" in prompt or "URL" in prompt
    assert "no inventes" in prompt.lower()
    assert "WhatsApp de consultas" in prompt
    assert "horario" in prompt.lower()
    assert "no afirmes que no hay whatsapp" in prompt.lower()
    assert "ficha BIO" in prompt or "BIO" in prompt
    assert "enumeres cada clase" in prompt.lower()
    assert "/static/salones/" in prompt
    assert "Clases virtuales" in prompt or "clases virtuales" in prompt.lower()
    assert "[foto](" in prompt
    assert "[recorrido](" in prompt
    assert "foto · recorrido" in prompt or " · " in prompt
    assert "Sala Calma" in prompt
    assert "[foto](/static/salones/calma.jpg)" in prompt
    assert "[recorrido](/static/salones/calma.mp4)" in prompt
    assert "aunque no hayan preguntado" in prompt.lower() or "no hace falta que pregunten" in prompt.lower()
    assert "además" in prompt.lower()
    assert "WhatsApp de una profesional" in prompt or "whatsapp de una profesional" in prompt.lower()
    assert "turno programado" in prompt.lower()
    assert "demanda" in prompt.lower() and "espontánea" in prompt.lower()


def test_knowledge_massages_fiche():
    knowledge = load_knowledge()
    assert "# AGENDA DE SERVICIOS" in knowledge
    assert "## 1. Masajes" in knowledge
    assert "### Disponibilidad y reserva" in knowledge
    assert "$50.000" in knowledge
    assert "seña del 50%" in knowledge
    assert "equipo de TRAMA" in knowledge
    assert "coordinar directamente" not in knowledge.lower()
    assert "WhatsApp de consultas" in knowledge
    assert "+54 11 6956-6115" in knowledge
    assert "Instagram/Facebook de esta base) son complemento" in knowledge or "son complemento" in knowledge


def test_knowledge_lactancia_fiche():
    knowledge = load_knowledge()
    assert "## 2. Consultorio de Lactancia" in knowledge
    assert "### Disponibilidad y reserva" in knowledge
    assert "08:00 a 12:00" in knowledge
    assert "10:00 a 13:00" in knowledge
    assert "14:00 a 18:00" in knowledge
    assert "Natalia" in knowledge
    assert "+54 11 3198-9930" in knowledge
    assert "wa.me/541131989930" in knowledge
    assert "+54 11 6956-6115" in knowledge
    assert "wa.me/541169566115" in knowledge
    assert "$50.000" in knowledge
    assert "seña del 50%" in knowledge
    assert "turno programado" in knowledge.lower()
    assert "demanda espontánea" in knowledge.lower()
    assert "Consultorio" in knowledge
    assert "@trama.lomas" not in knowledge
    servicios = knowledge.split("# AGENDA DE SERVICIOS", 1)[1]
    lactancia = servicios.split("## 2. Consultorio de Lactancia", 1)[1]
    assert "Natalia no es el único canal" in lactancia or "no reemplaza" in lactancia.lower()
    assert "recomendable" in lactancia.lower()
    assert "no un requisito" in lactancia.lower() or "no requiere seña" in lactancia.lower()
    equipo = knowledge.split("# EQUIPO", 1)[1].split("# SALONES", 1)[0]
    assert "### Natalia" not in equipo


def test_knowledge_four_salons_split_by_use():
    knowledge = load_knowledge()
    assert "# SALONES" in knowledge
    assert "cuatro" in knowledge.lower()
    assert "Sala Tierra" in knowledge
    assert "Sala Aire" in knowledge
    assert "Consultorio" in knowledge
    assert "Sala Calma" in knowledge
    assert "asistencia psicológica" in knowledge.lower()
    assert "kinesiolog" in knowledge.lower()
    assert "demanda espontánea" in knowledge.lower()
    assert "turnos programados" in knowledge.lower()
    assert "Hay dos salas para servicios" not in knowledge
    assert "El espacio cuenta con dos salas" not in knowledge
    salones = knowledge.split("# SALONES", 1)[1].split("# AGENDA DE ACTIVIDADES GRUPALES", 1)[0]
    assert "Consultorio" in salones
    assert "asistencia psicológica" in salones.lower()
    assert "Lactancia" in salones
    assert "Sala Calma" in salones
    assert "masajes" in salones.lower()
    assert "kinesiolog" in salones.lower()
    for slug in ("tierra", "aire", "calma", "consultorio"):
        assert f"/static/salones/{slug}.jpg" in salones
        assert f"/static/salones/{slug}.mp4" in salones
    assert "[foto](" in salones
    assert "[recorrido](" in salones


def test_knowledge_drops_static_media_line_if_file_missing(tmp_path, monkeypatch):
    from src.knowledge import loader as knowledge_loader

    monkeypatch.setattr(knowledge_loader, "STATIC_ROOT", tmp_path)
    assert knowledge_loader._line_keeps_existing_static_files("sin media") is True
    assert (
        knowledge_loader._line_keeps_existing_static_files(
            "  - Foto: /static/salones/no-existe.jpg"
        )
        is False
    )
    (tmp_path / "salones").mkdir()
    (tmp_path / "salones" / "tierra.jpg").write_bytes(b"x")
    assert (
        knowledge_loader._line_keeps_existing_static_files(
            "  - Foto: /static/salones/tierra.jpg"
        )
        is True
    )


def test_knowledge_whatsapp_primary_contact_and_caro_bio():
    knowledge = load_knowledge()
    assert "+54 11 6956-6115" in knowledge
    assert "wa.me/541169566115" in knowledge
    assert "lunes a viernes" in knowledge.lower()
    assert "09 a 21" in knowledge
    assert "No hay WhatsApp" not in knowledge
    assert "# EQUIPO" in knowledge
    assert 'Carolina Losada ("Caro")' in knowledge
    assert "Creadora de Maternar y TRAMA" in knowledge
    assert "Partera, Profe de Yoga, Doula y Puericultora" in knowledge
    assert "movimiento consciente" in knowledge
    assert "Bio pendiente" not in knowledge


def test_knowledge_chi_kung_fiche_and_marta_bio():
    knowledge = load_knowledge()
    assert "chi kung terapéutico" in knowledge.lower()
    assert "## 11. Chi Kung Terapéutico" in knowledge
    assert "Marta Pistasoli" in knowledge
    assert "Sala Tierra" in knowledge
    assert "16:30–17:30" in knowledge or "16:30-17:30" in knowledge
    assert "09:00–10:00" in knowledge or "09:00-10:00" in knowledge
    assert "4 clases (1x/semana): $50.000" in knowledge
    assert "8 clases (2x/semana): $78.000" in knowledge
    assert "Clase suelta/prueba: $15.000" in knowledge
    assert "Chi-Kung" in knowledge
    assert "Qi Gong" in knowledge
    assert "@marti_chikungterapeutico" not in knowledge.split("## 11. Chi Kung Terapéutico", 1)[1].split("# AGENDA DE SERVICIOS", 1)[0]
    equipo = knowledge.split("# EQUIPO", 1)[1].split("# SALONES", 1)[0]
    assert equipo.find('Carolina Losada ("Caro")') < equipo.find("### Marta Pistasoli")
    assert "Dicta Chi Kung Terapéutico" in equipo
    assert "https://www.instagram.com/marti_chikungterapeutico/" in equipo
    assert "Soy Marta" not in equipo
    assert "WhatsApp" not in equipo.split("### Marta Pistasoli", 1)[1]
