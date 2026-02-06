def scroll_down(driver, times=1):
    for _ in range(times):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )