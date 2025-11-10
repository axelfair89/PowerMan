from __future__ import annotations

from pathlib import Path

SVG_TEMPLATE = """<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 256 256\">\n  <defs>\n    <radialGradient id=\"bg\" cx=\"50%\" cy=\"40%\" r=\"70%\">\n      <stop offset=\"0\" stop-color=\"#ffb347\" />\n      <stop offset=\"1\" stop-color=\"#ff512f\" />\n    </radialGradient>\n    <linearGradient id=\"bolt\" x1=\"0%\" x2=\"0%\" y1=\"0%\" y2=\"100%\">\n      <stop offset=\"0\" stop-color=\"#fff178\" />\n      <stop offset=\"1\" stop-color=\"#ffc400\" />\n    </linearGradient>\n  </defs>\n  <rect width=\"256\" height=\"256\" rx=\"48\" fill=\"url(#bg)\" />\n  <g fill=\"none\" stroke=\"#3b1f14\" stroke-width=\"8\" stroke-linecap=\"round\" stroke-linejoin=\"round\">\n    <path d=\"M76 116c-14-40 40-78 72-46 40-18 74 28 48 68\" fill=\"#ffc48c\" />\n    <path d=\"M76 116c-14-40 40-78 72-46 40-18 74 28 48 68\" />\n    <path d=\"M96 92c12-10 28-12 36 0\" />\n    <path d=\"M122 140c-12 6-26 4-32-8\" />\n    <path d=\"M134 120c16 14 40 10 52-8\" />\n    <path d=\"M82 162c-12 20-36 38-20 48s36-6 44-24\" fill=\"#ffe0c2\" />\n    <path d=\"M174 162c12 20 36 38 20 48s-36-6-44-24\" fill=\"#ffe0c2\" />\n  </g>\n  <path d=\"M134 112l-24 52h26l-14 48 54-74h-30l12-26z\" fill=\"url(#bolt)\" stroke=\"#3b1f14\" stroke-width=\"6\" stroke-linejoin=\"round\" />\n  <circle cx=\"96\" cy=\"188\" r=\"10\" fill=\"#ff8353\" />\n  <circle cx=\"160\" cy=\"188\" r=\"10\" fill=\"#ff8353\" />\n</svg>\n"""

ROOT_LOGO = Path("logo.svg")
INTEGRATION_LOGO = Path("custom_components/powerman/logo.svg")


def write_logo(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SVG_TEMPLATE, encoding="utf-8")


def main() -> None:
    write_logo(ROOT_LOGO)
    write_logo(INTEGRATION_LOGO)


if __name__ == "__main__":
    main()
