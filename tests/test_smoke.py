"""Smoke tests — confirm the package imports cleanly and the API boots."""

from fastapi.testclient import TestClient


def test_import() -> None:
    import trov  # noqa: F401
    assert trov.__version__


def test_health_endpoint() -> None:
    from trov.api.main import app

    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok", "service": "trov"}


def test_i18n_loads_both_languages() -> None:
    from trov.db.models import Language
    from trov.i18n import t

    en = t("help", Language.EN)
    km = t("help", Language.KM)
    assert "SrokWork" in en
    assert "SrokWork" in km
    assert en != km  # actually translated, not just a fallback
