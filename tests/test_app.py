from streamlit.testing.v1 import AppTest


def test_dashboard_title():
    at = AppTest.from_file("../app.py")
    at.run()
    assert at.title[0].value == "BasketCraft Dashboard"