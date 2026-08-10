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


def test_knowledge_massages_fiche():
    knowledge = load_knowledge()
    assert "# AGENDA DE SERVICIOS" in knowledge
    assert "## 1. Masajes" in knowledge
    assert "### Disponibilidad y reserva" in knowledge
    assert "$50.000" in knowledge
    assert "seña del 50%" in knowledge
    assert "equipo de TRAMA" in knowledge
    assert "coordinar directamente" not in knowledge.lower()
