import os

images_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\static\images"

product_1_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#fef08a"/>
  <rect x="50" y="50" width="300" height="200" rx="20" fill="#eab308"/>
  <text x="200" y="140" font-family="sans-serif" font-size="40" font-weight="bold" fill="#b91c1c" text-anchor="middle">MAGGI</text>
  <text x="200" y="180" font-family="sans-serif" font-size="24" font-weight="600" fill="#ffffff" text-anchor="middle">2-Minute Noodles</text>
  <path d="M 120 220 Q 200 280 280 220" stroke="#b91c1c" stroke-width="8" fill="none" stroke-linecap="round"/>
</svg>"""

fallback_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" fill="#f1f5f9"/>
  <g transform="translate(200, 130)" fill="#94a3b8">
    <path d="M-40,10 L-40,40 L40,40 L40,10 Z" fill="#cbd5e1"/>
    <path d="M-50,-20 L50,-20 L50,10 L-50,10 Z" fill="#94a3b8"/>
    <rect x="-15" y="-10" width="30" height="15" rx="4" fill="#ffffff" opacity="0.5"/>
  </g>
  <text x="200" y="210" font-family="sans-serif" font-size="18" font-weight="600" fill="#94a3b8" text-anchor="middle">Product Image Unavailable</text>
</svg>"""

with open(os.path.join(images_dir, 'product_1.svg'), 'w', encoding='utf-8') as f:
    f.write(product_1_svg)

with open(os.path.join(images_dir, 'fallback.svg'), 'w', encoding='utf-8') as f:
    f.write(fallback_svg)

print("SVG assets created.")
