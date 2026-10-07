from agent import spusti_sql


def test_select_vrati_data():
    assert "Košický" in spusti_sql("SELECT kraj FROM kraje")


def test_ai_nemoze_mazat():
    assert spusti_sql("DELETE FROM naklady").startswith("Chyba")