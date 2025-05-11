from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions as seleniumExceptions
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import json, sys

STATUSES = {"reconnect": 4, "error": 1, "success": 2}

print("Started script")

def get_selector_by(selector: str) -> By:
    selector = selector.strip()
    if any(x in selector for x in [".", "#", " ", ">", "~"]):
        return By.CSS_SELECTOR
    return By.XPATH
        

def spawn_browser(profile_id):
    fp = webdriver.FirefoxProfile(
        "C:\\Users\\username\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\" + profile_id
    )
    fp.set_preference("toolkit.startup.max_resumed_crashes", "-1")
    fp.set_preference("browser.shell.checkDefaultBrowser", "false")
    fp.set_preference("browser.shell.defaultBrowserCheckCount", "0")
    fp.set_preference("browser.shell.didSkipDefaultBrowserCheckOnFirstRun", "false")
    fp.set_preference("browser.shell.didSkipDefaultBrowserCheckOnFirstRun", "false")
    fp.set_preference("browser.shell.skipDefaultBrowserCheckOnFirstRun", "true")
    fp.set_preference("media.volume_scale", "0.0")
    options = webdriver.FirefoxOptions()
    options.profile = fp
    options.add_argument("--allow-downgrade")
    options.add_argument("--width=970")
    options.add_argument("--height=1030")
    options.add_argument("--window-size=970,1030")
    return webdriver.Firefox(options=options)


def login_to_metamask(browser, metamask_uuid, password):
    browser.get(f"moz-extension://{metamask_uuid}/popup.html")

    WebDriverWait(browser, 10).until(
        lambda browser: browser.find_element(By.ID, "password")
    )
    input_el = browser.find_element(By.ID, "password")
    input_el.send_keys(password)
    input_el.submit()


def wait_and_click(selector, browser, timeout=10):
    try:
        WebDriverWait(browser, timeout).until(
            lambda browser: browser.find_element(get_selector_by(selector), selector)
        )
        browser.find_element(get_selector_by(selector), selector).click()
        return True
    except seleniumExceptions.TimeoutException:
        print("!!! Could not find element:", selector)


def wait(selector, browser, timeout=10, ignore_errors=False):
    try:
        WebDriverWait(browser, timeout).until(
            lambda browser: browser.find_element(get_selector_by(selector), selector)
        )
    except seleniumExceptions.TimeoutException:
        print("!!! Could not find element:", selector)
    except Exception as e:
        if not ignore_errors:
            raise e


def wait_and_print(selector, browser, timeout=10):
    try:
        WebDriverWait(browser, timeout).until(
            lambda browser: browser.find_element(get_selector_by(selector), selector)
        )
        print("Button found!")
    except seleniumExceptions.TimeoutException:
        print("!!! Could not find element:", selector)


def click_button_old(selector, browser_index):
    (browser1 if browser_index == 1 else browser2).find_element(
        get_selector_by(selector), selector
    ).click()
    print("Left-clicked on button in browser", browser_index)


def click_button(selector, browser_index):
    (browser1 if browser_index == 1 else browser2).find_element(
        get_selector_by(selector), selector
    ).click()
    print("X-PATH-clicked on button in browser", browser_index)


def right_click_button(selector, browser):
    wait(selector, browser)
    element = browser.find_element(get_selector_by(selector), selector)
    action_chains = ActionChains(browser)
    action_chains.context_click(element).perform()


def js_click(selector, browser):
    browser.execute_script(f"document.querySelector('{selector}').click()")


def send_keys_to_browser(browser, keys):
    actions = ActionChains(browser)
    actions.send_keys(keys)
    actions.perform()


def wait_for_second_window(browser: webdriver.Firefox):
    WebDriverWait(browser, 10).until(lambda browser: len(browser.window_handles) == 2)


def login(metamask1, metamask2, password):
    print("Started login")

    login_to_metamask(browser1, metamask1, password)
    login_to_metamask(browser2, metamask2, password)

    browser1.get("https://lobby.cambria.gg/")
    browser2.get("https://lobby.cambria.gg/")

    selector = "/html/body/div[1]/react-portal-target/react-child/svelte-slot/main/div/div/button"
    wait_and_click(selector, browser1, 20)
    wait_and_click(selector, browser2, 20)

    selector = "/html/body/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[3]/div/button[1]"
    wait_and_click(selector, browser1)
    wait_and_click(selector, browser2)

    def metamask_internal(browser: webdriver.Firefox):
        original_window = browser.current_window_handle
        second_window = next(filter(lambda x: x != original_window, browser.window_handles))
        browser.switch_to.window(second_window)

        internal_selectors = [
            "/html/body/div[2]/div/div/section/div[3]/button",
            "/html/body/div[1]/div/div/div/div[3]/div[2]/footer/button[2]",
            "/html/body/div[1]/div/div/div/div[3]/div[2]/footer/button[2]",
            "/html/body/div[1]/div/div/div/div[5]/footer/button[2]",
        ]
        for internal_selector in internal_selectors:
            wait_and_click(internal_selector, browser)

        browser.switch_to.window(original_window)
        sleep(1)
    def metamask_internal(browser: webdriver.Firefox):
        original_window = browser.window_handles[0]
        browser.switch_to.window(browser.window_handles[1])

        internal_selectors = [
            "/html/body/div[2]/div/div/section/div[3]/button",
            "/html/body/div[1]/div/div/div/div[3]/div[2]/footer/button[2]",
            "/html/body/div[1]/div/div/div/div[3]/div[2]/footer/button[2]",
            # "/html/body/div[1]/div/div/div/div[5]/footer/button[2]",
        ]
        for internal_selector in internal_selectors:
            wait(internal_selector, browser)
            browser.switch_to.window(browser.window_handles[1])
            browser.find_element(By.XPATH, internal_selector).click()

        selector = "button.button:nth-child(2)"
        while True:
            sleep(1)
            try:
                browser.switch_to.window(browser.window_handles[1])
                browser.find_element(By.CSS_SELECTOR, selector)
                break
            except Exception:
                print("Some errror got ignored.")
                pass
        js_click(selector, browser)
        browser.switch_to.window(original_window)

    wait_for_second_window(browser1)
    metamask_internal(browser1)
    wait_for_second_window(browser2)
    metamask_internal(browser2)
    print("Finished metamask internal")

    def sign_in_metamask(browser: webdriver.Firefox):
        original_window = browser.current_window_handle
        second_window = next(
            filter(lambda x: x != original_window, browser.window_handles)
        )
        browser.switch_to.window(second_window)

        sign_in = "/html/body/div[1]/div/div/div/div[4]/footer/button[2]"
        wait_and_click(sign_in, browser)

        browser.switch_to.window(original_window)

    # def defeat_small_black_button(browser, attempts=0):
    #     selector = "/html/body/div[1]/react-portal-target/react-child/svelte-slot/div/main/div/div/button"
    #     wait(selector, browser)
    #     js_click("button.bg-black", browser)
    #     wait_for_second_window(browser)
    #     sign_in_metamask(browser)
    #     sleep(3)
    #     try:
    #         if browser.find_element(By.XPATH, selector) and attempts < 3:
    #             defeat_small_black_button(browser, attempts + 1)
    #     except seleniumExceptions.NoSuchElementException:
    #         pass

    # defeat_small_black_button(browser1)
    # defeat_small_black_button(browser2)
    # print("Small black button was defeated")

    browser1.get("https://play.cambria.gg/")
    browser2.get("https://play.cambria.gg/")
    print("Redirected to play.cambria.gg")

    # def fix_connect_wallet(browser):
    #     global selector
    #     selector = "/html/body/div[1]/div/div[1]/react-portal-target/react-child/svelte-slot/div/section[2]/button"  # connect wallet
    #     try:
    #         if not browser.find_element(By.XPATH, selector):
    #             return
    #         wait_and_click(selector, browser)
    #         selector = "/html/body/div[2]/dialog/div/div/div/div[1]/div[3]/button[1]"  # metamask
    #         wait_and_click(selector, browser)
    #         wait_for_second_window(browser)
    #         original_window = browser.current_window_handle
    #         second_window = next(
    #             filter(lambda x: x != original_window, browser.window_handles)
    #         )
    #         browser.switch_to.window(second_window)
    #         selector = "/html/body/div[1]/div/div/div/div[3]/div[2]/footer/button[2]"
    #         wait_and_click(selector, browser)
    #         sleep(0.1)
    #         wait_and_click(selector, browser)
    #         browser.switch_to.window(original_window)
    #     except Exception:
    #         pass

    # fix_connect_wallet(browser1)
    # fix_connect_wallet(browser2)

    status = enter_world()
    if status == STATUSES["reconnect"]:
        return status

def check_loading(attempts=0):
    global browser1, browser2
    print(f"[loading] start, attempt #{attempts}")
    if attempts > 2:
        return
    browser1.get("https://play.cambria.gg/")
    browser2.get("https://play.cambria.gg/")
    selector = "/html/body/div[1]/div/div[1]/react-portal-target/react-child/svelte-slot/div/section[2]/button" #/html/body/div[1]/div/div[1]/react-portal-target/react-child/svelte-slot/div/section[2]/div/button
    print("[loading] 1st wait")
    wait(selector, browser1)
    wait(selector, browser2)
    print("[loading] 1st click")
    browser1.execute_script(
        '(()=>{window.counteri=0;let e=setInterval(()=>{let t=document.querySelector(".nes-btn");t&&"Enter World"===t.innerText&&(t.click(),clearInterval(e)),window.counteri++>10&&clearInterval(e)},1e3)})();'
    )
    browser2.execute_script(
        '(()=>{window.counteri=0;let e=setInterval(()=>{let t=document.querySelector(".nes-btn");t&&"Enter World"===t.innerText&&(t.click(),clearInterval(e)),window.counteri++>10&&clearInterval(e)},1e3)})();'
    )
    # selector = "/html/body/div[4]/div/div[1]/react-portal-target/react-child/svelte-slot/div/div/section[3]/aside[3]/div[2]/div[4]/div/img"
    selector = ".navigation-bar > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)"
    print("[loading] 2nd wait")
    wait(selector, browser1, ignore_errors=True, timeout=180+33)
    wait(selector, browser2, ignore_errors=True, timeout=180+33)
    print("[loading] 2nd waited")

    try:
        browser1.find_element(By.CSS_SELECTOR, selector)
        print("[loading] 1st browser is loaded")
    except seleniumExceptions.NoSuchElementException:
        print("[loading] 1st browser is not loaded")
        check_loading(attempts + 1)

    try:
        browser2.find_element(By.CSS_SELECTOR, selector)
        print("[loading] 2nd browser is loaded")
    except seleniumExceptions.NoSuchElementException:
        print("[loading] 2nd browser is not loaded")
        check_loading(attempts + 1)

# skipped_intro = False
# def skip_introduction(browser):
#     global skipped_intro
    
#     if skipped_intro:
#         return
    
#     selector = "#main-layout-main > div > div > div.flex.items-center.justify-center.gap-2.mt-auto.px-4 > button"

#     print("[intro] 1st")
#     wait_and_click(selector, browser)

#     selector = "#main-layout-main > div > div > div.flex.items-center.justify-center.gap-2.mt-auto.px-4 > button:nth-child(2)"
#     print("[intro] 2nd")
#     wait_and_click(selector, browser)

#     print("[intro] 3rd")
#     wait(selector, browser, ignore_errors=True)

#     for i in range(5):
#         try:
#             browser.execute_script(
#                 f"document.querySelector('#main-layout-main > div > div > div.flex.items-center.justify-center.gap-2.mt-auto.px-4 > button:nth-child(2)').click()"
#             )
#             sleep(1)
#         except Exception:
#             print(f"[intro] 3rd fail #{i}")
#             pass

#     print("[intro] done")
#     skipped_intro = True


def enter_world():
    global browser1, browser2
    print("Entering world...")
    # region mb this should be deleted
    selector = "#game-overlay > react-portal-target > react-child > svelte-slot > div > section.action.flex.flex-col.justify-center.items-center.gap-1 > button"  # enter world #/html/body/div[1]/div/div[1]/react-portal-target/react-child/svelte-slot/div/div/section[2]/section[1]/div/div/div[3]/button
    ##game-overlay > react-portal-target > react-child > svelte-slot > div > section.action.flex.flex-col.justify-center.items-center.gap-1 > button
    try:
        wait_and_click(selector, browser1, 100) 
    except Exception:
        print("Failed to click enter world button in browser 1")
    try:
        wait_and_click(selector, browser2, 100)
    except Exception:
        print("Failed to click enter world button in browser 2")
    # endregion

    # Click «Enter World» with javascript
    # sleep(2)
    # browser1.execute_script(
    #     '(()=>{window.counteri=0;let e=setInterval(()=>{let t=document.querySelector("html body#body div#main-container.main-container div#game.game div#game-overlay react-portal-target.svelte-1rt0kpf react-child svelte-slot.svelte-1rt0kpf div.connectScene.svelte-15b6h9m section.action.svelte-l3gl0h div.flex.justify-center button.nes-btn.is-warning.loginSceneFormSubmit.ml-4.svelte-l3gl0h");t&&"Enter World"===t.innerText&&(t.click(),clearInterval(e)),window.counteri++>10&&clearInterval(e)},1e3)})();'
    # )
    # browser2.execute_script(
    #     '(()=>{window.counteri=0;let e=setInterval(()=>{let t=document.querySelector("html body#body div#main-container.main-container div#game.game div#game-overlay react-portal-target.svelte-1rt0kpf react-child svelte-slot.svelte-1rt0kpf div.connectScene.svelte-15b6h9m section.action.svelte-l3gl0h div.flex.justify-center button.nes-btn.is-warning.loginSceneFormSubmit.ml-4.svelte-l3gl0h");t&&"Enter World"===t.innerText&&(t.click(),clearInterval(e)),window.counteri++>10&&clearInterval(e)},1e3)})();'
    # )
     
    selector = ".lg-btn"
    wait(selector, browser1, timeout=100, ignore_errors=True)
    wait(selector, browser2, timeout=100, ignore_errors=True)
    print("World entered!")
    

    # print("Checking if the world has been entered...")
    # check_loading()
    # print("The world has been loaded.")

    # status = check_reconnect(352, click_reconnect_button=True)
    # if status == STATUSES["reconnect"]:
    #     # print("Reconnect button found while entering world. Waiting 5 seconds.")
    #     # sleep(5)
    #     # return enter_world()
    #     return status
    
    # skip_introduction(browser1)
    # skip_introduction(browser2)

    # print("Introduction skipped, world entered.")


def check_reconnect(print_id, click_reconnect_button=False) -> bool:
    """Returns True if the script must be restarted"""
    global browser1, browser2
    selector = ".error-message > div > div > .nes-btn"
    result = False
    try:
        button = browser1.find_element(By.CSS_SELECTOR, selector)
        print(f"Reconnect found in 1st browser (#{print_id})")
        if click_reconnect_button:
            button.click()
        result = True
    except seleniumExceptions.NoSuchElementException:
        pass

    try:
        button = browser2.find_element(By.CSS_SELECTOR, selector)
        print(f"Reconnect found in 2nd browser (#{print_id})")
        if click_reconnect_button:
            button.click()
        result = True
    except seleniumExceptions.NoSuchElementException:
        pass

    print(f"No reconnect found (#{print_id})")
    return result


def send_duel_request():
    # if check_reconnect(340):
    #     return STATUSES["reconnect"]
    send_keys_to_browser(browser1, "4")  # inventory (to skip friendslist)
    print("Clicked inventory")

    # selector = "/html/body/div[4]/div/div[1]/react-portal-target/react-child/svelte-slot/div/div/section[2]/section[2]/aside/div[1]/div/div[2]/button"
    # wait_and_click(selector, browser2)  # duel chat
    # print("Clicked duel chat")
    selector = "div.tab-container:nth-child(2) > button:nth-child(1)" #duel chat
    WebDriverWait(browser2, 10).until(
        lambda browser: browser.find_element(By.CSS_SELECTOR, selector)
    )
    js_click(selector, browser2)
    print("Clicked duel chat")

    send_keys_to_browser(browser1, "6")  # friend list
    sleep(2)

    # if check_reconnect(358):
    #     return STATUSES["reconnect"]
    selector = ".hover\\:bg-stone-500" #/html/body/div[1]/div/div[1]/react-portal-target/react-child/svelte-slot/div/div/section[3]/aside[3]/div[1]/div/div[2]/div
    right_click_button(selector, browser1)  # right click friend 
    print("Friend clicked") 
    sleep(4)

    # if check_reconnect(365):
    #     return STATUSES["reconnect"]
    selector = "button.menu-option:nth-child(2)" #/html/body/div[1]/div/div[1]/react-portal-target/react-child/svelte-slot/div/div/section[2]/section[1]/div/div[2]/button[2]
    wait_and_click(selector, browser1)  # send duel
    print("Duel request sent")

restarted = False

def accept_duel(browser: webdriver.Firefox, attempts=0):
    # global restarted
    sleep(0.5)
    print(f"Accepting duel, attempt #{attempts}...")
    # if check_reconnect(385) or restarted:
    #     restarted = False
    #     return STATUSES["reconnect"]
    
    # if attempts > 20:
    #     print("Couldn't find a duel")
    #     return STATUSES["reconnect"]
    if attempts > 10:
        status = send_duel_request()
        if status == STATUSES["reconnect"]:
            return status
    try:
        requests = browser.find_elements(By.CSS_SELECTOR, ".chat-message")
        for req in requests:
            nick = req.find_element(By.CSS_SELECTOR, "p").text.strip().split(" ")[0]
            accept_button = req.find_element(By.CSS_SELECTOR, "div > button")
            if nick == "deepcool_ak620" or nick == "kUert0v":
                accept_button.click()
                print("Accepted duel request!")
                return

            # if nick == "undefined" and attempts > 5:
            #     # restart both browsers
            #     browser1.refresh()
            #     browser2.refresh()
            #     status = enter_world()
            #     if status == STATUSES["reconnect"]:
            #         return status
            #     restarted = True
            #     return start_duel()

        return accept_duel(browser, attempts + 1)
    except seleniumExceptions.NoSuchElementException as e:
        accept_duel(browser, attempts + 1)
    except Exception as e:
        print("!!!!!!!!! Unexpected error while accepting duel")
        raise e
        
def start_duel():
    global restarted
    print("Starting duel...")

    status = send_duel_request()
    print("Status:", status)
    # if status == STATUSES["reconnect"]:
    #     return status

    # if check_reconnect(422) or restarted:
    #     restarted = False
    #     return STATUSES["reconnect"]
    
    status = accept_duel(browser2)
    print("Duel accepted in chat")
    
    # if status == STATUSES["reconnect"] or check_reconnect(427):
    #     return STATUSES["reconnect"]

    selector = ".\\!px-2" #.max-h-\\[467px\\] > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) 
    wait_and_click(selector, browser1, timeout=20)
    wait_and_click(selector, browser2, timeout=20)
    print("Accepted duel request!")

    def click_on_canvas(browser: webdriver.Firefox, offsetX: int):
        try:
            canvas = browser.find_element(By.CSS_SELECTOR, "#game > canvas")
            ActionChains(browser).move_to_element_with_offset(
                canvas, offsetX, 0
            ).click().perform()
        except seleniumExceptions.MoveTargetOutOfBoundsException:
            print(
                "MoveTargetOutOfBoundsException:",
                offsetX,
                "Canvas size:",
                canvas.size,
            )

    def duel_has_started(browser):
        try:
            messages = browser.find_elements(
                By.CSS_SELECTOR, ".chat-message-text > span"
            )
            if any(msg.text == "Duel starting in 1..." for msg in messages):
                return True
        except Exception:
            pass

    WebDriverWait(browser1, 20).until(duel_has_started)
    # if check_reconnect(460):
    #     return STATUSES["reconnect"]
    print("Started clicking")
    for i in range(20):
        offset = 20 + i
        click_on_canvas(browser1, -offset)
        sleep(0.3)
    print("Ended clicking")

    # if check_reconnect(469):
    #     return STATUSES["reconnect"]
    selector = "/html/body/div[1]/div/div[1]/react-portal-target/react-child/svelte-slot/div/div/section[2]/section[1]/div/div/div[2]/div/div[2]/div/div[4]/button"  # close duel message
    js_selector = ".footer-content > div > button"
    wait(selector, browser1, timeout=100)
    wait(selector, browser2, timeout=100)
    js_click(js_selector, browser1)
    js_click(js_selector, browser2)
    print("Closed duel end pop-up!")

    # print("Finished 666 seconds timeout!")
    # sleep(666)
    return STATUSES["success"]


if len(sys.argv) < 2:
    print("Usage: python cumbria_x2.py paramsN.json")
    exit(1)

browser1 = None
browser2 = None

def setup():
    global browser1, browser2
    config = json.loads(open(sys.argv[1]).read())

    if browser1 is not None:
        browser1.close()

    if browser2 is not None:
        browser2.close()

    browser1 = spawn_browser(config["profile1"])
    browser1.set_window_position(0, 0)
    browser2 = spawn_browser(config["profile2"])
    browser2.set_window_position(960, 0)

    status = login(config["metamask1"], config["metamask2"], config["password"])
    if status == STATUSES["reconnect"]:
        setup()

def main():
    global browser1, browser2
    setup()
    while True:
        sleep(0.1)
        print("Looping...")
        try:
            status = start_duel()
            if status == STATUSES["reconnect"]:
                # browser1.get("https://play.cambria.gg/")
                # browser2.get("https://play.cambria.gg/")
                # sleep(5)
                # enter_world()
                setup()
                sleep(5)
            if status == STATUSES["success"]:
                print("Success, waiting 10 seconds.")
                sleep(10)
        except Exception as e:
            # print(e)
            # sleep(10)
            # enter_world()
            print("Unexpected error", e)
            sleep(5)
            setup()

if __name__ == "__main__":
    main()

# while True:
#     sleep(0.1)

#     if is_pressed("ctrl+1"):
#         Thread(target=asyncio.run, args=(run(),)).start()
#         print("started")
#     if is_pressed("ctrl+2"):
#         from os import kill, getpid

#         print("killing")
#         kill(getpid(), 9)
#     if is_pressed("ctrl+3"):
#         all_windows = browser1.window_handles
#         print(all_windows)
