import os
import sys

linux_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(linux_dir)

from database.db_handler import DBHandler
from utils.helium import HeliumSuggestionEngine


def test_snippets_and_helium():
    db_path = "test_shellixa_snippets.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = DBHandler(db_path)
    snippet_id = db.add_snippet("Restart Nginx", "sudo systemctl restart nginx", "nginx,service")
    snippets = db.get_snippets()
    assert len(snippets) == 1
    assert snippets[0]["title"] == "Restart Nginx"

    db.update_snippet(snippet_id, tags="nginx,service,ops")
    updated = db.get_snippets("ops")
    assert len(updated) == 1
    assert updated[0]["tags"] == "nginx,service,ops"

    db.increment_snippet_usage(snippet_id)
    used = db.get_snippets()[0]
    assert used["usage_count"] == 1

    engine = HeliumSuggestionEngine()
    suggestions = engine.suggest(
        "systemctl",
        history=["systemctl reload nginx"],
        snippets=db.get_snippets(),
    )
    assert any(item.startswith("systemctl") for item in suggestions)

    db.delete_snippet(snippet_id)
    assert db.get_snippets() == []
    db.close()
    os.remove(db_path)


if __name__ == "__main__":
    test_snippets_and_helium()