def test_home_redirect_and_username(browser):
    # Open the base URL
    browser.get("http://localhost:5000/")

    # Check that we are redirected to /home
    assert browser.current_url.endswith("/home")

    # Get the full page body text
    body_text = browser.find_element("tag name", "body").text

    # Check that the username is displayed somewhere on the page
    assert "dluo" in body_text


def test_home_buttons_exist(browser):
    browser.get("http://localhost:5000/home")

    expected_titles = [
        "Student Management",
        "Teacher Management",
        "Course Management",
        "Class Management",
        "Academic Management",
        "Financial Management"
    ]

    buttons = browser.find_elements("css selector", ".home-button-block .title")
    button_titles = [b.text for b in buttons]

    for title in expected_titles:
        assert title in button_titles
