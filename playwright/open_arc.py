import httpx
from rich import inspect, print  # noqa

from playwright.sync_api import sync_playwright


def open_arc_with_viewer() -> None:
    with sync_playwright() as p:
        # 使用带有Chrome引擎的自定义浏览器路径
        context_options = {"viewport": {"width": 1280, "height": 800}, "ignore_https_errors": True}

        browser = p.chromium.launch(
            headless=False,
            channel=None,  # 不使用内置channel
            executable_path="/Applications/Arc.app/Contents/MacOS/Arc",
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )

        page = browser.new_page(**context_options)
        page.goto("https://google.com")

        # 等待一段时间以查看页面
        page.wait_for_timeout(3000)

        browser.close()


def get_arc_ws_endpoint():
    try:
        response = httpx.get("http://localhost:9222/json/version")
        if response.status_code != 200:
            print("[bold red]无法连接到浏览器调试端口。请确保Arc浏览器已使用远程调试模式启动[/bold red]")
            print("[bold yellow]使用命令：open -a Arc --args --remote-debugging-port=9222[/bold yellow]")
            return
        data: dict = response.json()
        return data.get("webSocketDebuggerUrl")
    except Exception as e:
        print(f"获取WebSocket URL失败: {e}")
        return None


def open_arc_with_headless() -> None:
    try:
        with sync_playwright() as p:
            # browser = p.chromium.launch(
            #     headless=True,  # Set to False if you need debugging visuals
            #     executable_path="/Applications/Arc.app/Contents/MacOS/Arc",
            #     args=["--no-sandbox", "--disable-dev-shm-usage"],
            # )

            # 通过http://localhost:9222/json获取Arc浏览器进程的WebSocket URL
            # response = httpx.get("ws://127.0.0.1:9222/devtools/browser/60510391-1a2a-4bc2-8a7a-d8f468d6377e")
            # data = response.json()
            # inspect(data)

            # 获取Arc浏览器进程的WebSocket URL
            ws_url = get_arc_ws_endpoint()
            if ws_url is None:
                print("[bold red]无法获取WebSocket URL[/bold red]")
                return
            browser = p.chromium.connect_over_cdp(ws_url)

            page = browser.new_page()

            # Navigate to Google homepage
            page.goto("https://www.google.com?q=pornhub", wait_until="networkidle")

            search_input = page.locator("textarea[name='q']")
            # search_input.fill("pornhub")

            # Simulate pressing Enter to submit the form
            search_input.press("Enter")

            # Wait for the search results to appear (look for the first result heading)
            page.wait_for_selector("h3", state="visible", timeout=10000)

            # Print the first search result title
            print(f"pornhub title: [bold green]{page.locator('h3').first.text_content()}[/bold green]")

            # 打印所有h3父级为a的元素
            # a_elements = page.locator("h3 >> xpath=parent::a").all()
            # for a_element in a_elements:
            #     print(f"a_element: [bold green]{a_element.get_attribute('href')}[/bold green]")

            # 找到父级元素为 a 的元素
            a_element = page.locator("h3 >> xpath=parent::a").first
            # 打印 pornhub url 地址
            print(f"pornhub url: [bold green]{a_element.get_attribute('href')}[/bold green]")

            # Take a screenshot for debugging purposes
            page.screenshot(path="google_search.png", full_page=True)

            # Close the browser
            browser.close()

    except Exception as e:
        print(f"[bold red]An error occurred: {e}[/bold red]")


if __name__ == "__main__":
    open_arc_with_headless()
