from PIL import Image, ImageOps
import glob, os, json
SRC='/Users/sethchurch/fairbankscp-website/'
DST='/Users/sethchurch/fairbankscp-v2/'

# Authoritative: from each listing page's <meta itemprop="image">
LISTING_IMG = {
 'AST-2BR-FURN':      '4fc6aa5eaeb102da802452110e39533e.jpg',
 'AST-2BR-FURN-02':   '8a622499a73cb33718401cc00146bf24.jpg',
 'AST-2BR-FURN-03':   '381dd7a95dfb6ce2210c851192ce6e3d.jpg',
 'AST-2BR-UNFURN':    'dba0537082eecdbd091f3cd72e7df4fc.jpg',
 'AST-2BR-UNFURN-02': '2de03daa2ccd4431fc684aa4e1acabae.jpg',
 'AST-2BR-UNFURN-03': '9ea5581bb3cd6102da399a03cf7ca4da.jpg',
 'NWD-STUDIO-MKT':    'ddd24df9ba5b5d9ed7cc68aca3f713b5.png',
 'NWD-STUDIO-LIHTC':  'f5f90904caee9a69279246d784860ecd.png',
 'NWD-1BR-MKT':       '4a32aa2310ff2ae495f34087723bcc1c.png',
 'NWD-1BR-LIHTC':     '021e25146f228a88570bd0634cacde58.jpg',
 'NWD-2BR-MKT':       'fc17d02461d47e385752c13edf675ebd.png',
 'NWD-2BR-MKT-725':   'd1670ee1ca2d85971ed66535a3d6f7c7.png',
 'NWD-2BR-LIHTC':     '2672abbb8478ca045fd5e6fd3846c293.png',
 'HLM-WH-IND':        '9bc1fdf56e42a21a28f44ee4c7a93008.png',
 'HLM-OFFICE':        'c0c8373e1c380f23cb7e53f365ebca92.jpg',
 'BRN-OFFICE':        '77ab2cf0061bde4740878b484b05f614.jpg',
 'FTR-IND-FACILITY':  '90fd8e1a1846e308dc6c6beda9636627.jpg',
 'NPL-WH-OFFICE':     '034dfd56913feee7327a8ecd81874251.jpg',
 'DHS-IND-CREW':      '01-hangars-from-airfield.jpg',   # Seth's own photo of the hangars
}
EXTRA = {
 'northward-exterior': 'photo_2026-08-19_05-.jpg',
 'astreet-townhouses': 'image_293.jpg',
 'unit-before':        'image_294.jpg',
 'unit-after':         'image_295.jpg',
}
idx={}
for f in glob.glob(SRC+'assets/**/*', recursive=True):
    if os.path.isfile(f) and '/-/' not in f:
        idx.setdefault(os.path.basename(f), f)

def emit(src, stem, outdir, widths=(1600,800)):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    out={}
    for w in widths:
        c = im.copy()
        if c.width > w:
            c = c.resize((w, round(c.height*w/c.width)), Image.LANCZOS)
        suf = '' if w==max(widths) else f'-{w}'
        p = f'{outdir}/{stem}{suf}.webp'
        c.save(DST+p, 'WEBP', quality=80, method=5)
        out[w]=(p, c.width, c.height)
    return out

man={'listing':{}, 'extra':{}, 'deadhorse':[]}
for sku, fn in LISTING_IMG.items():
    if fn not in idx: print('MISSING', sku, fn); continue
    man['listing'][sku] = emit(idx[fn], sku.lower(), 'assets/img/property')
for stem, fn in EXTRA.items():
    if fn not in idx: print('MISSING', stem, fn); continue
    man['extra'][stem] = emit(idx[fn], stem, 'assets/img/property')
# Seth's own aurora
man['extra']['aurora'] = emit(SRC+'assets/property/frontier/aurora-frontier-wide.jpg','frontier-aurora','assets/img/property',(1900,1000))
# Seth's own Deadhorse set
dm = json.load(open(SRC+'assets/property/deadhorse/manifest.json'))
for e in dm:
    stem = e['file'].rsplit('.',1)[0]
    r = emit(SRC+'assets/property/deadhorse/'+e['file'], stem, 'assets/img/deadhorse', (1400,700))
    man['deadhorse'].append({'stem':stem,'alt':e['alt'],'sizes':r})
json.dump(man, open(DST+'assets/img/manifest.json','w'), indent=1)
tot=sum(os.path.getsize(f) for f in glob.glob(DST+'assets/img/**/*.webp',recursive=True))
print('images written:', len(glob.glob(DST+'assets/img/**/*.webp',recursive=True)), ' total KB:', tot//1024)
