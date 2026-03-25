#!/usr/bin/env python3
"""
MCP Server för Playwright Web Testing
Junior testare kan använda detta för att automatisera webbtestning
"""

import asyncio
import json
import base64
from pathlib import Path
from typing import Any
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global browser och page
browser: Browser | None = None
page: Page | None = None
playwright_instance = None


async def init_browser():
    """Initialisera webbrowser"""
    global browser, playwright_instance
    if not browser:
        playwright_instance = await async_playwright().start()
        # Visa webbläsaren på Mac/GUI-system
        browser = await playwright_instance.chromium.launch(headless=False)
        logger.info("✓ Chrome Browser startad (GUI mode - du kan se den!)")
    return browser


async def get_or_create_page():
    """Hämta eller skapa en ny sida"""
    global page, browser
    await init_browser()
    if not page:
        page = await browser.new_page()
        logger.info("✓ Ny sida skapad")
    return page


async def open_page(url: str) -> dict:
    """Öppna en webbsida"""
    try:
        p = await get_or_create_page()
        await p.goto(url, wait_until="load")
        title = await p.title()
        logger.info(f"✓ Öppnade: {url}")
        return {"success": True, "message": f"Sida öppnad: {title}"}
    except Exception as e:
        logger.error(f"✗ Fel vid öppning: {e}")
        return {"success": False, "error": str(e)}


async def click_element(selector: str) -> dict:
    """Klicka på ett element"""
    try:
        p = await get_or_create_page()
        await p.click(selector)
        logger.info(f"✓ Klickade på: {selector}")
        return {"success": True, "message": f"Klickad på element: {selector}"}
    except Exception as e:
        logger.error(f"✗ Fel vid klick: {e}")
        return {"success": False, "error": str(e)}


async def fill_input(selector: str, text: str) -> dict:
    """Fyll ett inputfält"""
    try:
        p = await get_or_create_page()
        await p.fill(selector, text)
        logger.info(f"✓ Fyllt inputfält: {selector}")
        return {"success": True, "message": f"Text fylld: {text}"}
    except Exception as e:
        logger.error(f"✗ Fel vid ifyllning: {e}")
        return {"success": False, "error": str(e)}


async def submit_form(selector: str = "button[type='submit']") -> dict:
    """Skicka ett formulär"""
    try:
        p = await get_or_create_page()
        await p.click(selector)
        await p.wait_for_load_state("networkidle")
        logger.info("✓ Formulär skickat")
        return {"success": True, "message": "Formulär skickat"}
    except Exception as e:
        logger.error(f"✗ Fel vid skickning: {e}")
        return {"success": False, "error": str(e)}


async def assert_text(selector: str, expected_text: str) -> dict:
    """Verifiera att en text finns på sidan"""
    try:
        p = await get_or_create_page()
        text = await p.text_content(selector)
        
        if text and expected_text.lower() in text.lower():
            logger.info(f"✓ PASS: Text hittad: {expected_text}")
            return {
                "success": True,
                "passed": True,
                "message": f"Text verifierad: {expected_text}",
                "actual_text": text
            }
        else:
            logger.warning(f"✗ FAIL: Text inte hittad")
            return {
                "success": True,
                "passed": False,
                "message": f"Text inte hittad: {expected_text}",
                "actual_text": text
            }
    except Exception as e:
        logger.error(f"✗ Fel vid assertion: {e}")
        return {"success": False, "error": str(e)}


async def take_screenshot(filename: str | None = None) -> dict:
    """Ta en skärmbild"""
    try:
        p = await get_or_create_page()
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        filepath = Path("/tmp") / filename
        await p.screenshot(path=str(filepath))
        logger.info(f"✓ Skärmbild sparad: {filepath}")
        return {"success": True, "message": f"Skärmbild sparad: {filename}", "path": str(filepath)}
    except Exception as e:
        logger.error(f"✗ Fel vid skärmbild: {e}")
        return {"success": False, "error": str(e)}


async def get_page_content() -> dict:
    """Hämta hela sidans HTML-innehål"""
    try:
        p = await get_or_create_page()
        content = await p.content()
        logger.info("✓ Sidinnehål hämtat")
        return {"success": True, "content": content}
    except Exception as e:
        logger.error(f"✗ Fel vid hämtning: {e}")
        return {"success": False, "error": str(e)}


async def get_page_title() -> dict:
    """Hämta sidans titel"""
    try:
        p = await get_or_create_page()
        title = await p.title()
        logger.info(f"✓ Titel hämtad: {title}")
        return {"success": True, "title": title}
    except Exception as e:
        logger.error(f"✗ Fel: {e}")
        return {"success": False, "error": str(e)}


async def wait_for_element(selector: str, timeout: int = 5000) -> dict:
    """Vänta på att ett element dyker upp"""
    try:
        p = await get_or_create_page()
        await p.wait_for_selector(selector, timeout=timeout)
        logger.info(f"✓ Element hittad: {selector}")
        return {"success": True, "message": f"Element hittad: {selector}"}
    except Exception as e:
        logger.error(f"✗ Element inte hittad: {e}")
        return {"success": False, "error": str(e)}


async def hover_element(selector: str) -> dict:
    """Hovra över ett element"""
    try:
        p = await get_or_create_page()
        await p.hover(selector)
        logger.info(f"✓ Hovrade över: {selector}")
        return {"success": True, "message": f"Hovrad över: {selector}"}
    except Exception as e:
        logger.error(f"✗ Fel: {e}")
        return {"success": False, "error": str(e)}


async def get_attribute(selector: str, attribute: str) -> dict:
    """Hämta ett attribut från ett element"""
    try:
        p = await get_or_create_page()
        value = await p.get_attribute(selector, attribute)
        logger.info(f"✓ Attribut hämtat: {attribute}")
        return {"success": True, "attribute": attribute, "value": value}
    except Exception as e:
        logger.error(f"✗ Fel: {e}")
        return {"success": False, "error": str(e)}


async def select_dropdown(selector: str, value: str) -> dict:
    """Välj ett värde i en dropdown"""
    try:
        p = await get_or_create_page()
        await p.select_option(selector, value)
        logger.info(f"✓ Dropdown vald: {value}")
        return {"success": True, "message": f"Värde valt: {value}"}
    except Exception as e:
        logger.error(f"✗ Fel: {e}")
        return {"success": False, "error": str(e)}


async def close_browser() -> dict:
    """Stäng webbläsaren"""
    try:
        global browser, page, playwright_instance
        if page:
            await page.close()
        if browser:
            await browser.close()
        if playwright_instance:
            await playwright_instance.stop()
        logger.info("✓ Browser stängd")
        browser = None
        page = None
        playwright_instance = None
        return {"success": True, "message": "Browser stängd"}
    except Exception as e:
        logger.error(f"✗ Fel: {e}")
        return {"success": False, "error": str(e)}


# Mappning av alla tools
TOOLS = {
    "open_page": {
        "description": "Öppna en webbsida (tex. https://example.com)",
        "params": {"url": "string"},
        "handler": open_page
    },
    "click_element": {
        "description": "Klicka på ett element med CSS-selector",
        "params": {"selector": "string"},
        "handler": click_element
    },
    "fill_input": {
        "description": "Fyll ett inputfält med text",
        "params": {"selector": "string", "text": "string"},
        "handler": fill_input
    },
    "submit_form": {
        "description": "Skicka ett formulär",
        "params": {"selector": "string (default: button[type='submit'])"},
        "handler": submit_form
    },
    "assert_text": {
        "description": "Verifiera att en text finns på sidan (TESTNING)",
        "params": {"selector": "string", "expected_text": "string"},
        "handler": assert_text
    },
    "take_screenshot": {
        "description": "Ta en skärmbild av sidan",
        "params": {"filename": "string (optional)"},
        "handler": take_screenshot
    },
    "get_page_content": {
        "description": "Hämta hela sidans HTML-innehål",
        "params": {},
        "handler": get_page_content
    },
    "get_page_title": {
        "description": "Hämta sidans titel",
        "params": {},
        "handler": get_page_title
    },
    "wait_for_element": {
        "description": "Vänta på att ett element dyker upp",
        "params": {"selector": "string", "timeout": "int (milliseconds)"},
        "handler": wait_for_element
    },
    "hover_element": {
        "description": "Hovra över ett element",
        "params": {"selector": "string"},
        "handler": hover_element
    },
    "get_attribute": {
        "description": "Hämta ett attribut från ett element",
        "params": {"selector": "string", "attribute": "string"},
        "handler": get_attribute
    },
    "select_dropdown": {
        "description": "Välj ett värde i en dropdown",
        "params": {"selector": "string", "value": "string"},
        "handler": select_dropdown
    },
    "close_browser": {
        "description": "Stäng webbläsaren",
        "params": {},
        "handler": close_browser
    }
}


async def handle_tool_call(tool_name: str, tool_input: dict) -> str:
    """Hantera ett tool-anrop"""
    if tool_name not in TOOLS:
        return json.dumps({"error": f"Okänd tool: {tool_name}"})
    
    tool = TOOLS[tool_name]
    handler = tool["handler"]
    
    try:
        # Anropa handler med korrekt parametrar
        if tool_input:
            result = await handler(**tool_input)
        else:
            result = await handler()
        return json.dumps(result)
    except Exception as e:
        logger.error(f"Error calling {tool_name}: {e}")
        return json.dumps({"error": str(e)})


async def main():
    """Huvudfunktion - enkel test"""
    print("🎭 Playwright MCP Server - Test Mode\n")
    print("Tillgängliga tools:")
    for name, tool in TOOLS.items():
        print(f"  • {name}: {tool['description']}")
    
    print("\n📝 Startar testsekvens...\n")
    
    # Exempel testsekvens
    print("1️⃣  Öppnar Google...")
    result = await open_page("https://www.google.com")
    print(f"   {json.dumps(result, ensure_ascii=False)}\n")
    
    print("2️⃣  Tar skärmbild...")
    result = await take_screenshot("google_homepage.png")
    print(f"   {json.dumps(result, ensure_ascii=False)}\n")
    
    print("3️⃣  Hämtar sidrubrik...")
    result = await get_page_title()
    print(f"   {json.dumps(result, ensure_ascii=False)}\n")
    
    print("4️⃣  Stänger browser...")
    result = await close_browser()
    print(f"   {json.dumps(result, ensure_ascii=False)}\n")
    
    print("✅ Test slutfört!")


if __name__ == "__main__":
    asyncio.run(main())