from google import genai
import re


class Model:
    def __init__(self):
        self.prompt_categorization = '''You are an expert at classifying image descriptions into categories. As an expert, you will analyze the entire description and assign a category, prioritizing the following options: 'landscapes', 'abstract', or 'fashion'. If the description does not clearly fit into any of these, you are free to assign another category that fits better, but always giving priority to the three mentioned above.

Respond only with the name of the category, without quotes or explanations:

Consider the following examples:
Description: a purple forest at dusk
Category: landscapes

Description: gray wool coat with a faux fur collar
Category: fashion

Description: a lighthouse overlooking the ocean
Category: landscapes

Description: burgundy corduroy pants with patch pockets and silver buttons
Category: fashion

Description: orange corduroy overalls
Category: fashion

Description: a purple silk scarf with tassel trim
Category: fashion

Description: a green lagoon under a cloudy sky
Category: landscapes

Description: crimson rectangles forming a chaotic grid
Category: abstract

Description: purple pyramids spiraling around a bronze cone
Category: abstract

Description: magenta trapezoids layered on a transluscent silver sheet
Category: abstract

Description: a snowy plain
Category: landscapes

Description: black and white checkered pants
Category: fashion

Description: a starlit night over snow-covered peaks
Category: landscapes

Description: khaki triangles and azure crescents
Category: abstract

Description: a maroon dodecahedron interwoven with teal threads
Category: abstract'''
        self.prompt_improve_description='''You are an expert at transforming simple image descriptions into exceptionally detailed, vivid, and captivating descriptions, specifically optimized for AI models that generate images in SVG format from text.

Your goal is to elevate the following description to the highest level of clarity and visual richness, making it not only precise and accurate, but also evocative and inspiring — so that the SVG code generated will faithfully and beautifully capture every nuance.
Include intricate details such as exact colors, distinct shapes, precise positions, realistic proportions, textures, lighting, and stylistic elements wherever possible.
Maintain the original intent but amplify it with expressive, structured, and imaginative language.
'''
        self.prompt_svg = '''You are an expert SVG code generator.
Your task is to generate clean, minimal, and valid SVG code that matches a given description and category.
Each input consists of:
- a natural language description of the image to draw
- a category that reflects the theme of the description (e.g., landscape, fashion, abstract)

Your output should be:
- only the <svg> code
- without any explanations, comments, or extra text
STRICT RULES you must follow:
1. The SVG must not exceed 10,000 characters.
2. ONLY the following ELEMENTS are allowed: svg, g, defs, symbol, use, marker, pattern, linearGradient, radialGradient, stop, filter, feBlend, feFlood, feOffset, path, rect, circle, ellipse, line, polyline, polygon.
3. ONLY the following ATTRIBUTES are allowed for each group of elements:
   - Common: id, clip-path, clip-rule, color, color-interpolation, color-interpolation-filters, color-rendering, display, fill, fill-opacity, fill-rule, filter, flood-color, flood-opacity, lighting-color, marker-end, marker-mid, marker-start, mask, opacity, paint-order, stop-color, stop-opacity, stroke, stroke-dasharray, stroke-dashoffset, stroke-linecap, stroke-linejoin, stroke-miterlimit, stroke-opacity, stroke-width, transform.
   - svg: width, height, viewBox, preserveAspectRatio.
   - g: viewBox.
   - symbol: viewBox, x, y, width, height.
   - use: x, y, width, height, href.
   - marker: viewBox, preserveAspectRatio, refX, refY, markerUnits, markerWidth, markerHeight, orient.
   - pattern: viewBox, preserveAspectRatio, x, y, width, height, patternUnits, patternContentUnits, patternTransform, href.
   - linearGradient: x1, x2, y1, y2, gradientUnits, gradientTransform, spreadMethod, href.
   - radialGradient: cx, cy, r, fx, fy, fr, gradientUnits, gradientTransform, spreadMethod, href.
   - stop: offset.
   - filter: x, y, width, height, filterUnits, primitiveUnits.
   - feBlend: result, in, in2, mode.
   - feFlood: result.
   - feOffset: result, in, dx, dy.
   - path: d.
   - rect: x, y, width, height, rx, ry.
   - circle: cx, cy, r.
   - ellipse: cx, cy, rx, ry.
   - line: x1, y1, x2, y2.
   - polyline, polygon: points.
4. It is FORBIDDEN to use any attributes not explicitly listed above. DO NOT DO THIS UNDER ANY CIRCUMSTANCES.
5. Your response must be valid <svg> code only. Do not include any additional text, explanations, or XML headers.
6. The SVG must be valid and renderable as PNG.Consider the following examples:Description: a purple forest at dusk
Category:landscapes

SVG:
<svg width="800" height="600" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="skyGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4b0082"/>
      <stop offset="1" stop-color="#8a2be2"/>
    </linearGradient>
    <linearGradient id="mountainGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2e0854"/>
      <stop offset="1" stop-color="#4b0082"/>
    </linearGradient>
    <linearGradient id="treeGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#6a0dad"/>
      <stop offset="1" stop-color="#4b0082"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="800" height="600" fill="url(#skyGradient)"/>
  <path d="M0 400 Q200 300 400 400 T800 400 L800 600 L0 600 Z" fill="url(#mountainGradient)"/>
  <g>
    <path d="M100 450 L120 400 L140 450 Z" fill="url(#treeGradient)"/>
    <path d="M180 460 L200 410 L220 460 Z" fill="url(#treeGradient)"/>
    <path d="M260 470 L280 420 L300 470 Z" fill="url(#treeGradient)"/>
    <path d="M340 460 L360 410 L380 460 Z" fill="url(#treeGradient)"/>
    <path d="M420 450 L440 400 L460 450 Z" fill="url(#treeGradient)"/>
    <path d="M500 460 L520 410 L540 460 Z" fill="url(#treeGradient)"/>
    <path d="M580 470 L600 420 L620 470 Z" fill="url(#treeGradient)"/>
    <path d="M660 460 L680 410 L700 460 Z" fill="url(#treeGradient)"/>
  </g>
  <g>
    <path d="M130 500 L150 450 L170 500 Z" fill="url(#treeGradient)"/>
    <path d="M210 510 L230 460 L250 510 Z" fill="url(#treeGradient)"/>
    <path d="M290 520 L310 470 L330 520 Z" fill="url(#treeGradient)"/>
    <path d="M370 510 L390 460 L410 510 Z" fill="url(#treeGradient)"/>
    <path d="M450 500 L470 450 L490 500 Z" fill="url(#treeGradient)"/>
    <path d="M530 510 L550 460 L570 510 Z" fill="url(#treeGradient)"/>
    <path d="M610 520 L630 470 L650 520 Z" fill="url(#treeGradient)"/>
    <path d="M690 510 L710 460 L730 510 Z" fill="url(#treeGradient)"/>
  </g>
</svg>

Description: gray wool coat with a faux fur collar
Category:fashion

SVG:
<svg width="200" height="300" viewBox="0 0 200 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grayGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#888"/>
      <stop offset="1" stop-color="#444"/>
    </linearGradient>
    <linearGradient id="furGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ccc"/>
      <stop offset="1" stop-color="#999"/>
    </linearGradient>
  </defs>
  <g>
    <path d="M60 40 C55 80, 55 120, 60 260 L80 260 C85 180, 85 100, 80 40 Z" fill="url(#grayGradient)" stroke="#333" stroke-width="1"/>
    <path d="M140 40 C145 80, 145 120, 140 260 L120 260 C115 180, 115 100, 120 40 Z" fill="url(#grayGradient)" stroke="#333" stroke-width="1"/>
    <path d="M80 40 C85 60, 115 60, 120 40 C110 30, 90 30, 80 40 Z" fill="url(#furGradient)" stroke="#666" stroke-width="0.5"/>
    <path d="M60 40 C65 20, 85 20, 80 40 C70 30, 60 30, 60 40 Z" fill="url(#furGradient)" stroke="#666" stroke-width="0.5"/>
    <path d="M140 40 C135 20, 115 20, 120 40 C130 30, 140 30, 140 40 Z" fill="url(#furGradient)" stroke="#666" stroke-width="0.5"/>
    <rect x="97" y="80" width="6" height="100" fill="#222"/>
    <circle cx="100" cy="100" r="2" fill="#555"/>
    <circle cx="100" cy="120" r="2" fill="#555"/>
    <circle cx="100" cy="140" r="2" fill="#555"/>
    <circle cx="100" cy="160" r="2" fill="#555"/>
    <circle cx="100" cy="180" r="2" fill="#555"/>
  </g>
</svg>

Description: a lighthouse overlooking the ocean
Category:landscapes

SVG:
<svg width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="skyGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#87ceeb"/>
      <stop offset="1" stop-color="#ffffff"/>
    </linearGradient>
    <linearGradient id="oceanGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1e90ff"/>
      <stop offset="1" stop-color="#00008b"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="200" height="100" fill="url(#skyGradient)"/>
  <rect x="0" y="100" width="200" height="100" fill="url(#oceanGradient)"/>
  <path d="M140 80 L145 40 L155 40 L160 80 Z" fill="#ffffff" stroke="#000000" stroke-width="1"/>
  <rect x="145" y="30" width="10" height="10" fill="#ff0000" stroke="#000000" stroke-width="1"/>
  <rect x="147" y="20" width="6" height="10" fill="#ffff00" stroke="#000000" stroke-width="1"/>
  <path d="M147 20 L150 10 L153 20 Z" fill="#ffff00" stroke="#000000" stroke-width="1"/>
  <path d="M0 100 Q50 90 100 100 T200 100 L200 200 L0 200 Z" fill="#1e90ff" opacity="0.3"/>
</svg>

Description: burgundy corduroy pants with patch pockets and silver buttons
Category:fashion

SVG:
<svg width="200" height="400" viewBox="0 0 200 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="corduroy" x1="0" y1="0" x2="0" y2="1" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="#800020"/>
      <stop offset="1" stop-color="#4B0010"/>
    </linearGradient>
  </defs>
  <g>
    <path d="M60 20 C55 100 55 200 60 380 L90 380 C95 200 95 100 90 20 Z" fill="url(#corduroy)" stroke="#3A0010" stroke-width="2"/>
    <path d="M110 20 C105 100 105 200 110 380 L140 380 C145 200 145 100 140 20 Z" fill="url(#corduroy)" stroke="#3A0010" stroke-width="2"/>
    <rect x="65" y="100" width="20" height="30" fill="#5A0015" stroke="#3A0010" stroke-width="1"/>
    <rect x="115" y="100" width="20" height="30" fill="#5A0015" stroke="#3A0010" stroke-width="1"/>
    <circle cx="75" cy="95" r="3" fill="#C0C0C0"/>
    <circle cx="125" cy="95" r="3" fill="#C0C0C0"/>
    <circle cx="75" cy="135" r="3" fill="#C0C0C0"/>
    <circle cx="125" cy="135" r="3" fill="#C0C0C0"/>
  </g>
</svg>

Description: orange corduroy overalls
Category:fashion

SVG:
<svg width="200" height="300" viewBox="0 0 200 300" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="corduroy" x1="0" y1="0" x2="0" y2="1" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="#FFA500"/>
      <stop offset="1" stop-color="#CC8400"/>
    </linearGradient>
    <pattern id="corduroyPattern" patternUnits="userSpaceOnUse" width="4" height="4">
      <rect x="0" y="0" width="2" height="4" fill="#CC8400"/>
    </pattern>
  </defs>
  <g>
    <rect x="60" y="60" width="80" height="160" rx="10" fill="url(#corduroy)"/>
    <rect x="60" y="60" width="80" height="160" rx="10" fill="url(#corduroyPattern)" fill-opacity="0.3"/>
    <rect x="60" y="60" width="20" height="40" fill="#FFA500"/>
    <rect x="120" y="60" width="20" height="40" fill="#FFA500"/>
    <circle cx="70" cy="60" r="4" fill="#804000"/>
    <circle cx="130" cy="60" r="4" fill="#804000"/>
    <rect x="75" y="100" width="50" height="40" rx="5" fill="#CC8400"/>
    <line x1="75" y1="100" x2="125" y2="100" stroke="#804000" stroke-width="2"/>
    <line x1="75" y1="120" x2="125" y2="120" stroke="#804000" stroke-width="2"/>
    <line x1="75" y1="140" x2="125" y2="140" stroke="#804000" stroke-width="2"/>
    <rect x="60" y="220" width="30" height="40" rx="5" fill="#FFA500"/>
    <rect x="90" y="220" width="30" height="40" rx="5" fill="#FFA500"/>
    <line x1="75" y1="220" x2="75" y2="260" stroke="#804000" stroke-width="2"/>
    <line x1="105" y1="220" x2="105" y2="260" stroke="#804000" stroke-width="2"/>
  </g>
</svg>

Description: a purple silk scarf with tassel trim
Category:fashion

SVG:
<svg width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="silkGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#a64ca6" stop-opacity="1"/>
      <stop offset="1" stop-color="#d1a3d1" stop-opacity="1"/>
    </linearGradient>
  </defs>
  <g>
    <path d="M50,50 C30,70 30,130 50,150 C70,170 130,170 150,150 C170,130 170,70 150,50 C130,30 70,30 50,50 Z" fill="url(#silkGradient)" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="50" y1="150" x2="48" y2="160" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="60" y1="155" x2="58" y2="165" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="70" y1="160" x2="68" y2="170" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="80" y1="165" x2="78" y2="175" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="90" y1="168" x2="88" y2="178" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="100" y1="170" x2="98" y2="180" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="110" y1="170" x2="112" y2="180" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="120" y1="168" x2="122" y2="178" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="130" y1="165" x2="132" y2="175" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="140" y1="160" x2="142" y2="170" stroke="#7a3d7a" stroke-width="2"/>
    <line x1="150" y1="155" x2="152" y2="165" stroke="#7a3d7a" stroke-width="2"/>
  </g>
</svg>

Description: a green lagoon under a cloudy sky
Category:landscapes

SVG:
<svg width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="skyGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#cfd8dc"/>
      <stop offset="1" stop-color="#90a4ae"/>
    </linearGradient>
    <linearGradient id="lagoonGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#66bb6a"/>
      <stop offset="1" stop-color="#2e7d32"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="200" height="100" fill="url(#skyGradient)"/>
  <g>
    <ellipse cx="50" cy="30" rx="25" ry="10" fill="#ffffff" fill-opacity="0.7"/>
    <ellipse cx="100" cy="40" rx="30" ry="12" fill="#ffffff" fill-opacity="0.7"/>
    <ellipse cx="150" cy="25" rx="20" ry="8" fill="#ffffff" fill-opacity="0.7"/>
    <ellipse cx="130" cy="50" rx="25" ry="10" fill="#ffffff" fill-opacity="0.6"/>
  </g>
  <rect x="0" y="100" width="200" height="100" fill="url(#lagoonGradient)"/>
  <ellipse cx="100" cy="150" rx="90" ry="30" fill="#43a047" fill-opacity="0.8"/>
</svg>

Description: crimson rectangles forming a chaotic grid
Category:abstract

SVG:
<svg width="500" height="500" viewBox="0 0 500 500">
  <g fill="crimson">
    <rect x="10" y="20" width="80" height="40" transform="rotate(5 50 40)"/>
    <rect x="100" y="30" width="60" height="30" transform="rotate(-10 130 45)"/>
    <rect x="180" y="60" width="90" height="50" transform="rotate(15 225 85)"/>
    <rect x="270" y="40" width="70" height="35" transform="rotate(-20 305 57.5)"/>
    <rect x="350" y="70" width="100" height="60" transform="rotate(10 400 100)"/>
    <rect x="30" y="120" width="75" height="45" transform="rotate(-15 67.5 142.5)"/>
    <rect x="120" y="140" width="65" height="35" transform="rotate(20 152.5 157.5)"/>
    <rect x="200" y="130" width="85" height="55" transform="rotate(-5 242.5 157.5)"/>
    <rect x="290" y="150" width="60" height="30" transform="rotate(25 320 165)"/>
    <rect x="370" y="130" width="95" height="50" transform="rotate(-10 417.5 155)"/>
    <rect x="50" y="210" width="90" height="40" transform="rotate(15 95 230)"/>
    <rect x="140" y="220" width="70" height="30" transform="rotate(-25 175 235)"/>
    <rect x="220" y="200" width="80" height="60" transform="rotate(10 260 230)"/>
    <rect x="310" y="210" width="65" height="35" transform="rotate(-15 342.5 227.5)"/>
    <rect x="390" y="230" width="85" height="45" transform="rotate(20 432.5 252.5)"/>
    <rect x="70" y="290" width="60" height="30" transform="rotate(-10 100 305)"/>
    <rect x="150" y="300" width="100" height="50" transform="rotate(5 200 325)"/>
    <rect x="250" y="280" width="70" height="40" transform="rotate(-20 285 300)"/>
    <rect x="330" y="300" width="90" height="60" transform="rotate(15 375 330)"/>
    <rect x="420" y="280" width="60" height="30" transform="rotate(-5 450 295)"/>
    <rect x="30" y="370" width="85" height="45" transform="rotate(10 72.5 392.5)"/>
    <rect x="120" y="380" width="75" height="35" transform="rotate(-15 157.5 397.5)"/>
    <rect x="210" y="360" width="65" height="30" transform="rotate(20 242.5 375)"/>
    <rect x="290" y="370" width="95" height="50" transform="rotate(-10 337.5 395)"/>
    <rect x="380" y="390" width="70" height="40" transform="rotate(15 415 410)"/>
  </g>
</svg>

Description: purple pyramids spiraling around a bronze cone
Category:abstract

SVG:
<svg width="500" height="500" viewBox="0 0 500 500">
  <defs>
    <linearGradient id="bronzeGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#cd7f32"/>
      <stop offset="1" stop-color="#8c5a2b"/>
    </linearGradient>
    <linearGradient id="purpleGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#800080"/>
      <stop offset="1" stop-color="#dda0dd"/>
    </linearGradient>
  </defs>
  <g transform="translate(250,250)">
    <path d="M0,-150 L-40,150 L40,150 Z" fill="url(#bronzeGradient)"/>
    <g>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(0) translate(0,-130)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(30) translate(0,-120)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(60) translate(0,-110)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(90) translate(0,-100)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(120) translate(0,-90)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(150) translate(0,-80)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(180) translate(0,-70)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(210) translate(0,-60)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(240) translate(0,-50)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(270) translate(0,-40)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(300) translate(0,-30)"/>
      <polygon points="0,-20 10,0 -10,0" fill="url(#purpleGradient)" transform="rotate(330) translate(0,-20)"/>
    </g>
  </g>
</svg>

Description: magenta trapezoids layered on a transluscent silver sheet
Category:abstract

SVG:
<svg width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="silverGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#c0c0c0" stop-opacity="0.6"/>
      <stop offset="1" stop-color="#f0f0f0" stop-opacity="0.6"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="200" height="200" fill="url(#silverGradient)"/>
  <path d="M40 30 L80 30 L70 60 L50 60 Z" fill="magenta"/>
  <path d="M60 50 L100 50 L90 80 L70 80 Z" fill="magenta"/>
  <path d="M80 70 L120 70 L110 100 L90 100 Z" fill="magenta"/>
  <path d="M100 90 L140 90 L130 120 L110 120 Z" fill="magenta"/>
  <path d="M120 110 L160 110 L150 140 L130 140 Z" fill="magenta"/>
</svg>

Description: a snowy plain
Category:landscapes

SVG:
<svg width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="skyGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#b0d0ff"/>
      <stop offset="1" stop-color="#ffffff"/>
    </linearGradient>
    <linearGradient id="snowGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#e0f0ff"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="200" height="200" fill="url(#skyGradient)"/>
  <path d="M0 140 Q50 130 100 140 T200 140 L200 200 L0 200 Z" fill="url(#snowGradient)"/>
  <circle cx="30" cy="50" r="2" fill="#ffffff"/>
  <circle cx="60" cy="70" r="1.5" fill="#ffffff"/>
  <circle cx="90" cy="40" r="2" fill="#ffffff"/>
  <circle cx="120" cy="60" r="1.5" fill="#ffffff"/>
  <circle cx="150" cy="50" r="2" fill="#ffffff"/>
  <circle cx="180" cy="70" r="1.5" fill="#ffffff"/>
  <circle cx="45" cy="90" r="1.5" fill="#ffffff"/>
  <circle cx="75" cy="100" r="2" fill="#ffffff"/>
  <circle cx="105" cy="85" r="1.5" fill="#ffffff"/>
  <circle cx="135" cy="95" r="2" fill="#ffffff"/>
  <circle cx="165" cy="80" r="1.5" fill="#ffffff"/>
</svg>

Description: black and white checkered pants
Category:fashion

SVG:
<svg width="200" height="400" viewBox="0 0 200 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="checker" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <rect x="0" y="0" width="10" height="10" fill="black"/>
      <rect x="10" y="10" width="10" height="10" fill="black"/>
      <rect x="0" y="10" width="10" height="10" fill="white"/>
      <rect x="10" y="0" width="10" height="10" fill="white"/>
    </pattern>
  </defs>
  <g>
    <path d="M60 50 C55 150,55 300,60 380 L90 380 C95 300,95 150,90 50 Z" fill="url(#checker)" stroke="black" stroke-width="1"/>
    <path d="M110 50 C105 150,105 300,110 380 L140 380 C145 300,145 150,140 50 Z" fill="url(#checker)" stroke="black" stroke-width="1"/>
  </g>
</svg>

Description: a starlit night over snow-covered peaks
Category:landscapes

SVG:
<svg width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <linearGradient id="skyGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0b0c2a"/>
      <stop offset="1" stop-color="#1a1c3b"/>
    </linearGradient>
    <linearGradient id="mountainGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#dce3f4"/>
      <stop offset="1" stop-color="#aab8d4"/>
    </linearGradient>
    <linearGradient id="foregroundMountain" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#bfcfe6"/>
      <stop offset="1" stop-color="#8fa3c1"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="800" height="600" fill="url(#skyGradient)"/>
  <g>
    <circle cx="100" cy="100" r="1.5" fill="#ffffff"/>
    <circle cx="200" cy="150" r="1" fill="#ffffff"/>
    <circle cx="300" cy="80" r="1.2" fill="#ffffff"/>
    <circle cx="400" cy="120" r="1.3" fill="#ffffff"/>
    <circle cx="500" cy="60" r="1.1" fill="#ffffff"/>
    <circle cx="600" cy="90" r="1.4" fill="#ffffff"/>
    <circle cx="700" cy="130" r="1.2" fill="#ffffff"/>
    <circle cx="750" cy="50" r="1.3" fill="#ffffff"/>
    <circle cx="650" cy="160" r="1" fill="#ffffff"/>
    <circle cx="550" cy="110" r="1.5" fill="#ffffff"/>
    <circle cx="350" cy="140" r="1.1" fill="#ffffff"/>
    <circle cx="250" cy="100" r="1.4" fill="#ffffff"/>
    <circle cx="150" cy="170" r="1.2" fill="#ffffff"/>
  </g>
  <path d="M0 400 L100 300 L200 380 L300 270 L400 350 L500 290 L600 370 L700 310 L800 400 L800 600 L0 600 Z" fill="url(#mountainGradient)"/>
  <path d="M0 500 L150 400 L250 480 L350 390 L450 470 L550 410 L650 490 L750 430 L800 500 L800 600 L0 600 Z" fill="url(#foregroundMountain)"/>
</svg>

Description: khaki triangles and azure crescents
Category:abstract

SVG:
<svg width="200" height="200" viewBox="0 0 200 200">
  <g>
    <polygon points="50,10 90,90 10,90" fill="khaki"/>
    <polygon points="150,20 190,100 110,100" fill="khaki"/>
    <polygon points="60,110 100,190 20,190" fill="khaki"/>
    <polygon points="160,120 180,180 140,180" fill="khaki"/>
    <path d="M70,50 A20,20 0 1,1 69.9,50 Z" fill="azure"/>
    <path d="M130,60 A15,15 0 1,1 129.9,60 Z" fill="azure"/>
    <path d="M80,150 A25,25 0 1,1 79.9,150 Z" fill="azure"/>
    <path d="M160,160 A18,18 0 1,1 159.9,160 Z" fill="azure"/>
  </g>
</svg>

Description: a maroon dodecahedron interwoven with teal threads
Category:abstract

SVG:
<svg width="200" height="200" viewBox="0 0 200 200">
  <g fill="maroon" stroke="black" stroke-width="1">
    <polygon points="100,30 130,50 140,85 120,115 85,120 60,100 55,70 75,45"/>
    <polygon points="100,30 75,45 55,70 60,100 85,120 120,115 140,85 130,50"/>
    <polygon points="60,100 40,130 70,150 100,140 85,120"/>
    <polygon points="120,115 100,140 130,160 160,130 140,85"/>
    <polygon points="55,70 30,90 40,130 60,100"/>
    <polygon points="140,85 160,90 170,120 160,130"/>
    <polygon points="75,45 60,30 30,50 30,90 55,70"/>
    <polygon points="130,50 140,30 170,50 160,90 140,85"/>
  </g>
  <g stroke="teal" stroke-width="2" fill="none">
    <path d="M40,130 C80,110 120,110 160,130"/>
    <path d="M30,90 C70,80 130,80 170,90"/>
    <path d="M60,30 C90,60 110,60 140,30"/>
    <path d="M30,50 C70,70 130,70 170,50"/>
    <path d="M60,100 C90,90 110,90 140,100"/>
    <path d="M75,45 C95,75 105,75 125,45"/>
    <path d="M55,70 C80,95 120,95 145,70"/>
    <path d="M85,120 C100,130 110,130 125,120"/>
  </g>
</svg>'''
        self.client = genai.Client()
        self.MODEL_ID = "models/gemini-2.5-flash-preview-04-17"
    def predict(self, description,verbose=False):
        #PREPARAR CATEGORIZACION
        input_user_categorization = (
            f"Description: {description}\n"
            "Category:\n")
        contents_categorization = [self.prompt_categorization,input_user_categorization]
        response = self.client.models.generate_content(
            model=self.MODEL_ID,
            contents=contents_categorization)
        des_category=response.text #Category of description
        #PREPARAR MEJORA DE DESCRIPCION
        input_user_description = (
            f"Description: {description}\n"
            "Refined description: ")
        contents_description = [self.prompt_improve_description,input_user_description]
        response = self.client.models.generate_content(
            model=self.MODEL_ID,
            contents=contents_description,)
        des_improved=response.text #Description improved
        #GENERACION CODIGO SVG
        input_user_svg = (
            f"Description: {des_improved}\n"
            f"Category: {des_category}\n"
            "SVG:\n")
        contents_svg = [self.prompt_svg,input_user_svg]


        response = self.client.models.generate_content(
            model=self.MODEL_ID,
            contents=contents_svg)
        svg_code=re.search(r'<svg[\s\S]*?</svg>', response.text).group(0)
        if verbose:
          print(f'Description:{description}')
          print(f'Category: {des_category}')
          print(f'Description improved:{des_improved}')
        return svg_code

if __name__ == "__main__":
    model = Model()
    description = "a red apple on a wooden table"
    svg_code = model.predict(description, verbose=True)
    print(svg_code)