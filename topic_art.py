"""Large minimal line drawings, one per guide topic, shown beside the article title.

One vocabulary for all of them: 300x220 canvas, 2.5px round strokes in brand teal (.s), one lime
fill for the thing that matters (.a), faint dashes for air (.f), and page-ground fills (.g) so
shapes can sit in front of each other. Colours come from style.css, never from the SVG.
"""

_OPEN = ('<svg class="topic-art" viewBox="0 0 300 220" fill="none" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">')

_FAINT_LEFT = '<path class="f" d="M18 96h22M10 118h30M22 140h18"/>'
_FAINT_RIGHT = '<path class="f" d="M258 150h24M262 172h30M258 194h16"/>'

ART = {
    # A road that bends away to a pin, with the dashboard gauge a mileage log starts from.
    "Mileage": (
        '<path class="f" d="M150 22h34M196 22h10M20 60h16"/>'
        '<path class="s road" d="M40 190C118 190 96 122 160 110S232 64 262 58"/>'
        '<path class="g road-in" d="M40 190C118 190 96 122 160 110S232 64 262 58"/>'
        '<path class="s dash" d="M40 190C118 190 96 122 160 110S232 64 262 58"/>'
        '<circle class="a s" cx="40" cy="190" r="8"/>'
        '<path class="g s" d="M262 62c-11-15-17-23-17-32a17 17 0 0 1 34 0c0 9-6 17-17 32z"/>'
        '<circle class="a" cx="262" cy="30" r="6.5"/>'
        '<path class="s" d="M46 92a34 34 0 0 1 68 0"/><path class="s" d="M40 92h80"/>'
        '<path class="s" d="M80 92l20-24"/><circle class="a s" cx="80" cy="92" r="5"/>'
        '<path class="f" d="M54 74l4 4M80 58v6M106 74l-4 4"/>'
    ),
    # A till receipt with its total picked out, and the tick that says it is safely recorded.
    "Receipts": (
        _FAINT_LEFT + _FAINT_RIGHT +
        '<path class="g s" d="M92 22h116v166l-11.600-10-11.600 10-11.600-10-11.600 10-11.600-10-11.600 10-11.600-10-11.600 10-11.600-10L92 188z"/>'
        '<path class="s" d="M114 52h46"/><path class="f" d="M114 74h72M114 94h60M114 114h72"/>'
        '<rect class="a" x="108" y="134" width="84" height="26" rx="7"/>'
        '<path class="s" d="M118 147h26M160 147h22"/>'
        '<circle class="g s" cx="212" cy="46" r="22"/><path class="s" d="M202 47l7 7 13-15"/>'
    ),
    # A phone with a shield on it, and the cloud it does not talk to.
    "Privacy": (
        _FAINT_LEFT +
        '<rect class="g s" x="104" y="16" width="92" height="188" rx="16"/><path class="s" d="M138 32h24"/>'
        '<path class="a s" d="M150 66l30 11v24c0 22-15 35-30 42-15-7-30-20-30-42V77z"/>'
        '<path class="s" d="M137 104l9 9 17-19"/>'
        '<path class="f" d="M226 84a14 14 0 0 1 27-5 12 12 0 0 1 3 23h-32a10 10 0 0 1 2-18z"/>'
        '<path class="s" d="M218 112l44-40"/>'
    ),
    # The box the paperwork lives in, and the calendar that says how long.
    "Records": (
        _FAINT_LEFT +
        '<rect class="g s" x="58" y="62" width="184" height="32" rx="9"/>'
        '<path class="g s" d="M70 94h160v84a10 10 0 0 1-10 10H80a10 10 0 0 1-10-10z"/>'
        '<rect class="a s" x="124" y="116" width="52" height="18" rx="9"/>'
        '<path class="f" d="M92 160h116"/>'
        '<rect class="g s" x="214" y="14" width="58" height="52" rx="9"/><path class="s" d="M214 32h58M230 8v12M256 8v12"/>'
        '<circle class="a" cx="243" cy="49" r="6"/>'
    ),
    # A tax invoice, the percent sign, and the stamp of a record that will pass.
    "UAE VAT": (
        _FAINT_LEFT + _FAINT_RIGHT +
        '<path class="g s" d="M98 20h82l32 32v134a10 10 0 0 1-10 10H98a10 10 0 0 1-10-10V30a10 10 0 0 1 10-10z"/>'
        '<path class="s" d="M180 20v22a10 10 0 0 0 10 10h22"/>'
        '<circle class="s" cx="126" cy="94" r="10"/><circle class="s" cx="174" cy="142" r="10"/><path class="s" d="M178 88l-56 60"/>'
        '<path class="f" d="M110 172h56"/>'
        '<circle class="a s" cx="214" cy="166" r="26"/><path class="s" d="M202 167l8 8 15-17"/>'
    ),
    # A code window, for the essays about how the apps are built.
    "Building": (
        _FAINT_LEFT + _FAINT_RIGHT +
        '<rect class="g s" x="44" y="34" width="212" height="152" rx="14"/><path class="s" d="M44 66h212"/>'
        '<circle class="a" cx="66" cy="50" r="5"/><circle class="s" cx="84" cy="50" r="5"/><circle class="s" cx="102" cy="50" r="5"/>'
        '<path class="s" d="M118 104l-22 20 22 20M182 104l22 20-22 20M162 96l-24 58"/>'
        '<circle class="a s" cx="246" cy="178" r="22"/><path class="s" d="M236 179l7 7 13-15"/>'
    ),
}


def topic_art(topic):
    body = ART.get(topic) or ART["Receipts"]
    return _OPEN + body.replace(".600", ".6") + "</svg>"
