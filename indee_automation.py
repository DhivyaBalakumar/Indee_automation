from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize driver
options = Options()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Step 1: Go to login page
driver.get("https://indeedemo-fyc.watch.indee.tv/login")
print("✅ Opened Indee login page")

# Step 2: Enter PIN and submit
try:
    pin_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter your PIN here"]')))
    pin_input.send_keys("WVMVHWBS")
    print("✅ Entered PIN")

    sign_in_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    driver.execute_script("arguments[0].click();", sign_in_button)
    print("✅ Submitted login form")
except Exception as e:
    print("❌ Error during PIN entry or SIGN IN click:", e)
    driver.quit()
    exit()

# Step 3: Click on the left-side brand button
try:
    brand_btn = wait.until(EC.element_to_be_clickable((By.ID, 'brd-01fvc8gs4sa9kjs8wxs6gnsn76')))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", brand_btn)
    time.sleep(2)
    brand_btn.click()
    print("✅ Clicked on the brand")
except Exception as e:
    print("❌ Error clicking brand button:", e)
    driver.quit()
    exit()

# Step 4: Scroll and click "Test automation project"
try:
    time.sleep(3)
    posters = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "poster")))

    target_poster = None
    for _ in range(10):
        for poster in posters:
            alt_text = poster.get_attribute("alt")
            if alt_text and "Test automation project" in alt_text:
                target_poster = poster
                break
        if target_poster:
            break
        else:
            time.sleep(1)
            posters = driver.find_elements(By.CLASS_NAME, "poster")

    if target_poster:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", target_poster)
        time.sleep(2)
        target_poster.click()
        print("🎯 Clicked on 'Test automation project'")
    else:
        print("❌ 'Test automation project' not found after waiting")
        driver.quit()
        exit()

except Exception as e:
    print("❌ Error finding or clicking the project:", e)
    driver.quit()
    exit()

# Step 5: Play video, pause at 10s, resume, pause again at 15s, then go back
try:
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(2)

    # Click Play button
    play_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Play Video"]')))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", play_btn)
    time.sleep(1)
    play_btn.click()
    print("▶️ Clicked main Play button")

    # Switch to iframe
    iframe = wait.until(EC.presence_of_element_located((By.ID, 'video_player')))
    driver.switch_to.frame(iframe)
    print("🔁 Switched to iframe")

    print("⏳ Polling JWPlayer for 10 seconds playback...")

    # Wait for jwplayer object to load
    wait.until(lambda d: d.execute_script("return typeof jwplayer === 'function' && jwplayer().getPosition !== undefined;"))

    # Poll every second until video has played for 10s
    for _ in range(20):
        position = driver.execute_script("return jwplayer().getPosition();")
        if position >= 10:
            driver.execute_script("jwplayer().pause();")
            print("⏸️ Video paused at 10 seconds of actual playback")
            break
        time.sleep(1)
    else:
        raise Exception("JWPlayer did not reach 10 seconds in expected time.")

    time.sleep(3)

    # Resume playback
    driver.execute_script("jwplayer().play();")
    print("▶️ Video resumed after 3-second pause")

    # Wait 5 seconds
    time.sleep(5)

    # Pause again
    driver.execute_script("jwplayer().pause();")
    print("⏸️ Video paused again after 5 seconds")

    # Exit iframe
    driver.switch_to.default_content()

    # Go back to previous page
    driver.back()
    print("🔙 Navigated back in browser to exit player")

    # Step 6: Logout from sidebar
    try:
        logout_btn = wait.until(EC.element_to_be_clickable((By.ID, "signOutSideBar")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", logout_btn)
        time.sleep(1)
        logout_btn.click()
        print("🔒 Successfully logged out")
    except Exception as e:
        print("⚠️ Logout button not found or not clickable:", e)

except Exception as e:
    print("❌ Error during JWPlayer playback control:", e)
    driver.quit()
    exit()
