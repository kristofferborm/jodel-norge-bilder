"""Generator for fotballhumor-poster: tekst på fargebakgrunn, 1080x1350."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(BASE, "fonts")
OUT = os.path.join(BASE, "poster")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350
MARGIN = 96
HANDLE = "@offside_norge"

# Fargeprofiler: bakgrunn, tekst, aksent
PAL = {
    # Husfarger (generelle/tidløse poster)
    "kveld":  ("#111418", "#FFFFFF", "#3DDC84"),
    "gress":  ("#1F6B3F", "#FFFFFF", "#F4F1EA"),
    "kritt":  ("#F4F1EA", "#111418", "#1F6B3F"),
    # Klubb-/landslagsfarger (når posten handler om et lag)
    "norge":  ("#BA0C2F", "#FFFFFF", "#FFFFFF"),
    "manutd": ("#DA291C", "#FFFFFF", "#FBE122"),
    "palace": ("#1B458F", "#FFFFFF", "#FF6B7D"),
    "viking": ("#002F6C", "#FFFFFF", "#FFD100"),  # aksent = Glimt-gul i gullkampen
    "glimt":  ("#FFD100", "#111111", "#111111"),
    "start":  ("#111111", "#FFD200", "#FFD200"),
    "brann":  ("#D7141A", "#FFFFFF", "#FFFFFF"),
    "rbk":    ("#FFFFFF", "#111111", "#111111"),
}

POSTS = [
    # --- Kristoffers favoritter ---
    ("f01", "start",  "", "Start ligger sist på tabellen.\n\nNavnet er altså mer et ønske enn en beskrivelse."),
    ("f02", "kveld",  "", "Landslagspausen er over. Nå er det tilbake til hverdagsfotballen.\n\nDet føles som å komme hjem fra Syden til en mandag i januar."),
    ("f03", "norge",  "", "Danmark trengte bare uavgjort.\n\nHaaland i 97. minutt: «Nei.»"),
    ("f04", "kritt",  "", "Sesongkort: Du betaler for å fryse i mars og november og blir skuffet i alle rundene imellom."),
    ("f05", "kveld",  "", "Ting man sier etter 0–4-tap:\n\n«Vi var faktisk bedre de første ti minuttene.»"),
    ("f06", "kveld",  "", "Regnet kommer sidelengs, kaffen er kald før lokket er av, og det står 0–0 etter 85 minutter.\n\nJa, jeg kommer igjen neste helg."),
    ("f07", "kritt",  "", "Ingen vet bedre hvordan et lag skal spilles enn en mann som må stoppe to ganger i trappa opp til tribunen."),
    # --- Nye forslag ---
    ("n01", "kveld",  "", "Ting man sier i 80. minutt når det står 0–3:\n\n«Ett mål nå, så er vi med.»"),
    ("n02", "kritt",  "", "Bortetur med supporterbussen: Seks timer hver vei, 0–2-tap, og dagens høydepunkt var en pølse på en bensinstasjon på Dombås."),
    ("n03", "gress",  "", "Mannen bak meg på tribunen har ropt «DOMMER!» 46 ganger i dag.\n\nDommeren har ikke snudd seg én gang. Respekt til begge."),
    ("n04", "kveld",  "", "Mars: «I år skjer det.»\n\nMai: «Vi må bare få litt flyt.»\n\nOktober: «Neste år skjer det.»"),
    ("n05", "kritt",  "", "Ingenting i livet er like sikkert som at spissen dere solgte i fjor scorer mot dere."),
    ("n06", "gress",  "", "Termos, ullsokker, to lag ull og en lue fra 2009.\n\nNei, jeg skal ikke på fjelltur. Jeg skal på kamp."),
    ("n07", "kveld",  "", "Treneren etter kampen: «Vi tar med oss mye positivt.»\n\nOversatt: «Vi tapte 0–4.»"),
    ("n08", "kritt",  "", "Supporterens fem stadier:\n1. Fornektelse\n2. Sinne\n3. Forhandling\n4. Depresjon\n5. Fornyer sesongkortet"),
    ("n09", "gress",  "", "Han på bedriftslaget varmer opp i fem minutter og tøyer i tjue.\n\nSå spiller han i tolv."),
    ("n10", "kveld",  "", "Ingen er mer optimistiske enn norske fotballsupportere i januar.\n\nIngen er mer realistiske enn norske fotballsupportere i april."),
    ("n11", "kritt",  "", "Samboeren: «Hvorfor blir du så sur av fotball?»\n\nMeg: «Jeg blir ikke sur av fotball. Jeg blir sur av laget mitt.»"),
    ("n12", "brann",  "", "Brann-supportere har sagt «i år tar vi gullet» så lenge at det nå regnes som en vanlig hilsen i Bergen."),
    ("n13", "rbk",    "", "Rosenborg-supportere snakker om 90-tallet slik andre snakker om sin første kjærlighet.\n\nMed blanke øyne og et lite sukk."),
    ("n14", "glimt",  "", "Glimt i januar: Trener i snøstorm på Aspmyra.\n\nGlimt i mars: «Hvorfor er alle de andre så slitne?»"),
    ("n15", "viking", "", "Viking og Glimt i gullkampen er som to brødre som krangler om den siste kjøttkaka.\n\nRosenborg sitter ved bordet og later som de også er sultne."),
    ("n16", "manutd", "", "Stillingsannonse, Manchester United:\n\nSøker: Trener\nTiltredelse: Snarest\nVarighet: Se historikken"),
    ("n17", "norge",  "", "Danske kommentatorer i 90. minutt: «Dette er avgjort.»\n\nHaaland: *legger ballen på straffemerket*"),
    ("n18", "norge",  "", "Trekningen til EM-kvaliken er 6. desember.\n\nNordmenn har allerede bestemt seg for at det blir «en overkommelig gruppe»."),
    ("n19", "kveld",  "", "Han som sier «det er bare et spill» har aldri sett laget sitt slippe inn i 94. minutt."),
    ("n20", "gress",  "", "Fotballtrener for åttenåringer:\n10 % taktikk\n20 % skolisser\n70 % «HVEM SIN DRIKKEFLASKE ER DETTE?»"),
]


def font(weight, size):
    return ImageFont.truetype(os.path.join(FONT, f"Poppins-{weight}.ttf"), size)


def wrap(draw, text, f, maxw):
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        cur = ""
        for word in para.split(" "):
            test = (cur + " " + word).strip()
            if draw.textlength(test, font=f) <= maxw:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def layout(draw, text, maxw, maxh):
    for size in range(78, 40, -2):
        f = font("SemiBold", size)
        lines = wrap(draw, text, f, maxw)
        lh = int(size * 1.32)
        gap = int(size * 0.55)  # tom linje = mindre luft enn full linje
        h = sum(gap if l == "" else lh for l in lines)
        if h <= maxh:
            return f, lines, lh, gap, h
    return f, lines, lh, gap, h


def render(pid, pal, tag, text):
    bg, fg, ac = PAL[pal]
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    maxw = W - 2 * MARGIN
    f, lines, lh, gap, th = layout(d, text, maxw, 820)

    # Merkelapp øverst
    if tag:
        tf = font("Bold", 30)
        x = MARGIN
        for ch in tag:
            d.text((x, MARGIN), ch, font=tf, fill=ac)
            x += d.textlength(ch, font=tf) + 4

    # Aksentstrek + tekst, vertikalt sentrert
    block = 14 + 44 + th
    y = (H - block) // 2
    d.rectangle([MARGIN, y, MARGIN + 110, y + 14], fill=ac)
    y += 14 + 44
    for l in lines:
        if l == "":
            y += gap
            continue
        d.text((MARGIN, y), l, font=f, fill=fg)
        y += lh

    # Signatur nede
    hf = font("Medium", 28)
    hw = d.textlength(HANDLE, font=hf)
    d.text((W - MARGIN - hw, H - MARGIN - 20), HANDLE, font=hf, fill=fg)

    path = os.path.join(OUT, f"{pid}.png")
    img.save(path)
    return path


def kontaktark(paths, out):
    cols, tw = 5, 324
    th = int(tw * H / W)
    pad = 16
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + pad + 40) + pad), "#E9E9E9")
    d = ImageDraw.Draw(sheet)
    lf = font("SemiBold", 24)
    for i, p in enumerate(paths):
        im = Image.open(p).resize((tw, th), Image.LANCZOS)
        cx = pad + (i % cols) * (tw + pad)
        cy = pad + (i // cols) * (th + pad + 40)
        sheet.paste(im, (cx, cy))
        d.text((cx, cy + th + 6), os.path.basename(p)[:-4], font=lf, fill="#222")
    sheet.save(out)


if __name__ == "__main__":
    paths = [render(*p) for p in POSTS]
    kontaktark([p for p in paths if "/f" in p[-8:]], os.path.join(BASE, "favoritter.png"))
    kontaktark([p for p in paths if "/n" in p[-8:]], os.path.join(BASE, "nye_forslag.png"))
    print(len(paths), "poster generert")
