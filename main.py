import json
from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder


def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    chrome = webdriver.Chrome(options=options, service=service)
    print(event)
    chrome.set_window_rect(width=800, height=600)
    if event is None:
        return {"nope":"nononoi"}
    if "body" in event:
        actions = json.loads(event['body']).get("actions", [])
    else:
        actions = event.get("actions", [])
    responses = []
    for a in actions:
        print(a)
        if a['command'] == "navigate":
            chrome.get(a['url'])
        elif a['command'] == 'screenshot':
            pass
        elif a['command'] == 'scroll':
            action = ActionChains(chrome)
            action.scroll_by_amount(int(a.get("scroll_x",0)), int(a.get("scroll_y", 0)))\
                  .perform()
        elif a['command'] == 'click':
            action = ActionBuilder(chrome)
            action.pointer_action.move_to_location(int(a["cursor_x"]), int(a["cursor_y"])).click()
            action.perform()

        responses.append({"screen": chrome.get_screenshot_as_base64()})
        
    return {"responses": responses}
