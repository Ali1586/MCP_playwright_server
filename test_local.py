#!/usr/bin/env python3
"""
Uppdaterat testskript för Playwright MCP Server
Använder lokal HTML-fil för testning (ingen internetkoppling behövs!)
"""

import asyncio
from pathlib import Path
from mcp_playwright_server import (
    open_page, click_element, fill_input, assert_text,
    take_screenshot, close_browser, get_page_title,
    wait_for_element, get_page_content
)


async def test_local_form():
    """Test: Fyll och skicka det lokala formuläret"""
    print("=" * 60)
    print("🧪 TEST: Lokalt Test-Formulär")
    print("=" * 60 + "\n")
    
    # Hämta sökvägen till HTML-filen
    html_path = Path(__file__).parent / "test_page.html"
    file_url = f"file://{html_path.absolute()}"
    
    print(f"1️⃣  Öppnar test-sida: {file_url}\n")
    result = await open_page(file_url)
    print(f"   Resultat: {result}\n")
    
    print("2️⃣  Väntar på formulär att ladda (10 sekunder)...\n")
    result = await wait_for_element("#firstName", timeout=10000)
    print(f"   Resultat: {result}\n")
    
    # Vänta lite extra för att säkerställa DOM är helt laddad
    await asyncio.sleep(2)
    
    print("3️⃣  Hämtar sidrubrik...\n")
    result = await get_page_title()
    print(f"   Sidrubrik: {result.get('title')}\n")
    
    print("4️⃣  Fyller förnamn (John)...\n")
    result = await fill_input("#firstName", "John")
    print(f"   Resultat: {result}\n")
    
    print("5️⃣  Fyller efternamn (Doe)...\n")
    result = await fill_input("#lastName", "Doe")
    print(f"   Resultat: {result}\n")
    
    print("6️⃣  Fyller e-post (john@example.com)...\n")
    result = await fill_input("#email", "john@example.com")
    print(f"   Resultat: {result}\n")
    
    print("7️⃣  Väljer land (Sverige)...\n")
    # Öppna select-dropdown
    await click_element("#country")
    # Välj option
    result = await fill_input("#country", "sweden")
    print(f"   Resultat: {result}\n")
    
    print("8️⃣  Fyller meddelande...\n")
    result = await fill_input("#message", "Detta är ett testmeddelande!")
    print(f"   Resultat: {result}\n")
    
    print("9️⃣  Accepterar villkor (klicka checkbox)...\n")
    result = await click_element("#terms")
    print(f"   Resultat: {result}\n")
    
    print("🔟 Ta skärmbild FÖRE skickning...\n")
    await take_screenshot("test_form_filled.png")
    print("   ✅ Skärmbild sparad: test_form_filled.png\n")
    
    print("1️⃣1️⃣  Klicka Submit-knapp...\n")
    result = await click_element("#submitBtn")
    print(f"   Resultat: {result}\n")
    
    print("1️⃣2️⃣  Vänta på success-meddelande...\n")
    result = await wait_for_element("#successMessage", timeout=5000)
    print(f"   Resultat: {result}\n")
    
    print("1️⃣3️⃣  Verifiera success-meddelande...\n")
    result = await assert_text("#successMessage", "Välkommen, John Doe!")
    if result.get('passed'):
        print(f"   ✅ PASS: Meddelande hittades!\n")
    else:
        print(f"   ❌ FAIL: Meddelande matchade inte")
        print(f"   Faktisk text: {result.get('actual_text')}\n")
    
    print("1️⃣4️⃣  Ta slutlig skärmbild...\n")
    await take_screenshot("test_form_submitted.png")
    print("   ✅ Skärmbild sparad: test_form_submitted.png\n")
    
    print("=" * 60)
    print("✅ ALLA TESTER SLUTFÖRDA MED FRAMGÅNG!")
    print("=" * 60)


async def run_tests():
    """Kör alla tester"""
    try:
        await test_local_form()
    except Exception as e:
        print(f"\n❌ ERROR under testning: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔄 Stänger webbläsare...\n")
        await close_browser()


if __name__ == "__main__":
    print("\n" + "🎭 " * 15)
    print("PLAYWRIGHT MCP - LOKAL TESTNING")
    print("🎭 " * 15 + "\n")
    
    asyncio.run(run_tests())