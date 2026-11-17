"""End-to-end checks for balvinder1002.github.io.

The hero shows Playwright locators as labels. These tests run those same
locators, so a label on the page can never claim something that fails.
"""
import io
import re
from pathlib import Path

import pytest
from PIL import Image
from playwright.sync_api import Page, expect

SCREENSHOTS = Path(__file__).resolve().parent / "screenshots"
SECTIONS = ["about", "projects", "roadmap", "experience", "contact"]


# ---------- page basics ----------

def test_title_and_name(home: Page):
    expect(home).to_have_title(re.compile("Balvinder Singh"))
    expect(home.get_by_role("heading", level=1)).to_have_text("Balvinder Singh")


def test_no_console_errors(home: Page):
    home.wait_for_load_state("networkidle")
    # A missing resume.pdf is expected: the page probes it and hides the buttons.
    real = [e for e in home.console_errors if "404" not in e]
    assert real == []


@pytest.mark.parametrize("section", SECTIONS)
def test_every_section_renders(home: Page, section: str):
    expect(home.locator(f"#{section} h2")).to_be_visible()


# ---------- the hero's own locator labels ----------

def test_hero_labels_are_real_locators(home: Page):
    """Each label must resolve to exactly one element (Playwright strict mode)."""
    labels = home.locator("#top .target").evaluate_all(
        "els => els.map(e => e.dataset.loc)"
    )
    assert len(labels) == 3
    for label in labels:
        locator = eval("home." + to_python(label))
        expect(locator).to_have_count(1)
        expect(locator).to_be_visible()


def to_python(js_locator: str) -> str:
    """getByRole('x', { name: 'y' }) -> get_by_role('x', name='y')"""
    py = re.sub(r"getBy(\w+)", lambda m: "get_by_" + m.group(1).lower(), js_locator)
    return re.sub(r",\s*\{\s*name:\s*('[^']*')\s*\}", r", name=\1", py)


def test_lens_visits_each_target_in_order_then_leaves(home: Page):
    """One lens steps through the three hero targets, showing each one's locator."""
    lens = home.locator("#lens")
    tag = lens.locator(".lens-loc")
    targets = home.locator("#top .target")
    expected = targets.evaluate_all("els => els.map(e => e.dataset.loc)")
    expect(lens).to_be_visible(timeout=3000)
    for step, loc in enumerate(expected, start=1):
        expect(lens).to_have_attribute("data-step", str(step), timeout=3000)
        expect(tag).to_have_attribute("data-loc", loc, timeout=1000)
        # the lens sits on its target (within a few pixels of the 14/10px padding)
        lb, tb = lens.bounding_box(), targets.nth(step - 1).bounding_box()
        assert abs(lb["x"] + 14 - tb["x"]) < 4 and abs(lb["y"] + 10 - tb["y"]) < 4
    expect(home.locator("html")).to_have_attribute("data-lens", "done", timeout=4000)
    expect(lens).to_be_hidden()


def test_reduced_motion_skips_lens_and_orb_settle(browser, site_url):
    context = browser.new_context(reduced_motion="reduce")
    page = context.new_page()
    page.goto(site_url)
    expect(page.locator("html")).to_have_attribute("data-lens", "skipped", timeout=3000)
    expect(page.locator("#lens")).to_be_hidden()
    assert page.locator(".orb-1").evaluate("e => getComputedStyle(e).animationName") == "none"
    context.close()


def test_lens_skipped_on_deep_link(browser, site_url):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto(site_url + "#projects")
    expect(page.locator("html")).to_have_attribute("data-lens", "skipped", timeout=3000)
    context.close()


# ---------- navigation and links ----------

def test_nav_links_point_to_real_sections(home: Page):
    links = home.get_by_role("navigation", name="Sections").get_by_role("link")
    expect(links).to_have_count(len(SECTIONS))
    for href in links.evaluate_all("els => els.map(e => e.getAttribute('href'))"):
        expect(home.locator(href)).to_have_count(1)


def test_nav_click_scrolls_to_section(home: Page):
    home.get_by_role("link", name="Projects").click()
    expect(home.locator("#projects")).to_be_in_viewport()


def test_external_links_open_safely(home: Page):
    for link in home.locator('a[target="_blank"]').all():
        expect(link).to_have_attribute("rel", re.compile("noopener"))


def test_contact_links(home: Page):
    contact = home.locator("#contact")
    expect(contact.get_by_role("link", name=re.compile("Email"))).to_have_attribute(
        "href", re.compile(r"^mailto:")
    )
    expect(contact.get_by_role("link", name=re.compile("LinkedIn"))).to_be_visible()
    expect(contact.get_by_role("link", name=re.compile("GitHub"))).to_be_visible()
    expect(home.locator('a[href^="tel:"]')).to_have_count(0)  # phone kept private


def test_resume_buttons_hidden_without_pdf(home: Page, site_url):
    has_pdf = home.request.head(site_url + "resume.pdf").ok
    buttons = home.get_by_role("link", name="Download resume")
    if has_pdf:
        expect(buttons.first).to_be_visible()
    else:
        expect(buttons).to_have_count(0)


# ---------- content ----------

def test_project_status_marks(home: Page):
    rows = home.locator("#projects .prow")
    expect(rows).to_have_count(7)
    automated = rows.filter(has_text="✓ Automated")
    manual = rows.filter(has_text="○ Manual")
    expect(automated).to_have_count(5)
    expect(manual).to_have_count(2)


def test_one_current_roadmap_step(home: Page):
    expect(home.locator("#roadmap .step.current")).to_have_count(1)


# ---------- themes and layout ----------

def test_dark_mode_changes_colours(browser, site_url):
    colours = {}
    for scheme in ("light", "dark"):
        context = browser.new_context(color_scheme=scheme)
        page = context.new_page()
        page.goto(site_url)
        colours[scheme] = page.evaluate("getComputedStyle(document.body).backgroundColor")
        context.close()
    assert colours["light"] != colours["dark"]


@pytest.mark.parametrize("width", [375, 900, 1440])
def test_no_sideways_scroll_and_screenshot(browser, site_url, width: int):
    context = browser.new_context(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    page = context.new_page()
    page.goto(site_url)
    page.wait_for_load_state("networkidle")
    overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    assert overflow <= 0, f"page is {overflow}px wider than a {width}px screen"
    nav = page.get_by_role("navigation", name="Sections")
    expect(nav).to_be_hidden() if width <= 900 else expect(nav).to_be_visible()
    SCREENSHOTS.mkdir(exist_ok=True)
    page.screenshot(path=SCREENSHOTS / f"home-{width}.png", full_page=True)
    context.close()


@pytest.mark.parametrize("scheme", ["dark", "light"])
@pytest.mark.parametrize("width", [375, 1440])
def test_text_contrast_on_glass(browser, site_url, scheme: str, width: int):
    """Measure every text element against the real composited background:
    the glass over the orbs, as rendered, with the text itself hidden."""
    context = browser.new_context(
        viewport={"width": width, "height": 900}, color_scheme=scheme, reduced_motion="reduce"
    )
    page = context.new_page()
    page.goto(site_url)
    page.wait_for_load_state("networkidle")
    texts = page.evaluate(TEXT_SAMPLES_JS)
    page.add_style_tag(content="*{color:transparent!important;text-shadow:none!important}"
                               ".lens-loc::before{content:none!important}")
    shot = Image.open(io.BytesIO(page.screenshot(full_page=True))).convert("RGB")
    context.close()

    failures = []
    for t in texts:
        box = (int(t["x"]), int(t["y"]), int(t["x"] + t["w"]), int(t["y"] + t["h"]))
        pixels = list(shot.crop(box).get_flattened_data())
        if not pixels:
            continue
        ratios = sorted(contrast(t["rgb"], p) for p in pixels)
        worst = ratios[len(ratios) // 50]          # 2nd percentile: ignores stray edge pixels
        need = 3.0 if t["large"] else 4.5
        if worst < need:
            failures.append(f'{worst:.2f} < {need} "{t["text"][:40]}"')
    assert not failures, f"{scheme} @ {width}px:\n" + "\n".join(failures)


TEXT_SAMPLES_JS = """() => {
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode, el = node.parentElement;
    if (!node.textContent.trim() || !el || el.closest('[aria-hidden="true"], [hidden]')) continue;
    const range = document.createRange(); range.selectNodeContents(node);
    const r = range.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    const cs = getComputedStyle(el);
    const rgb = cs.color.match(/[\\d.]+/g).slice(0, 3).map(Number);
    const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight) >= 700;
    out.push({ text: node.textContent.trim(), rgb, large: size >= 24 || (bold && size >= 18.66),
               x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height });
  }
  return out;
}"""


def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def test_buttons_meet_touch_size(home: Page):
    for button in home.locator(".btn").all():
        box = button.bounding_box()
        assert box and box["height"] >= 44
