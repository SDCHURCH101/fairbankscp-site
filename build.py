#!/usr/bin/env python3
"""Fairbanks Commercial Properties — static site generator. Original work, 2026."""
import os, json, shutil, hashlib, html, re

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.fairbankscp.com"

ORG = dict(
    name="Fairbanks Commercial Properties", short="FCP",
    phone="(907) 456-4274", tel="+19074564274",
    email="maiia@fairbankscp.com",
    street="300 Barnette Street, Suite 202",
    city="Fairbanks", region="AK", zip="99701",
    lat=64.842743881055, lon=-147.724546270771,
)
ADDR_1L = f"{ORG['street']}, {ORG['city']}, {ORG['region']} {ORG['zip']}"
FORM = "https://formsubmit.co/" + ORG["email"]

STATS = [
    ("400,000", "Sq ft under management", ""),
    ("201", "Homes in Fairbanks", ""),
    ("234", "Bedrooms on the North Slope", ""),
]

# ---------------------------------------------------------------- properties
P = [
 dict(slug="northward-building", name="Northward Building", loc="Downtown Fairbanks, Alaska",
      kind="Mixed use", img="northward-exterior",
      alt="The Northward Building on a Fairbanks street in autumn, with storefronts at pavement level",
      facts=["177 residential units", "6 commercial units", "Studio to 2 bedroom"],
      body="The largest building in the portfolio and the busiest. Apartments above, commercial tenants at street level, "
           "in the middle of downtown Fairbanks. Units run from studios at 510 square feet to two bedrooms at 1,065. "
           "Part of the building is let at market rents and part is income qualified, so the rent roll holds up whether "
           "the local economy is running hot or cold."),
 dict(slug="a-street-apartments", name="A Street Apartments", loc="Fairbanks, Alaska",
      kind="Residential", img="astreet-townhouses",
      alt="A row of blue sided two storey townhouses at A Street with lawn and mature trees",
      facts=["24 residential units", "2 bedroom townhouses", "Furnished and unfurnished"],
      body="Twenty four two bedroom townhouses on their own grounds. Each unit has its own entrance rather than a shared "
           "corridor, which is what tenants here ask for. We keep roughly half the units furnished for contract workers "
           "and rotating crews, and the rest unfurnished on standard leases."),
 dict(slug="barnette-street", name="300 Barnette Street", loc="Downtown Fairbanks, Alaska",
      kind="Office", img="brn-office",
      alt="Interior corridor of the 300 Barnette Street office building with daylight from the street frontage",
      facts=["Professional office space", "Downtown", "Our own head office"],
      body="A downtown office building that we own and work out of. Our own team is on the second floor, which means "
           "problems in this building get found quickly. Suites are let to professional tenants on conventional terms."),
 dict(slug="helmericks-avenue", name="Helmericks Avenue", loc="Fairbanks, Alaska",
      kind="Industrial and office", img="hlm-wh-ind",
      alt="Clear span interior of a Helmericks Avenue warehouse with concrete floor and overhead lighting",
      facts=["3 warehouses", "Attached office space", "Drive in access"],
      body="Three warehouses with office space attached, serving Fairbanks contractors and distributors. Clear span floors, "
           "drive in doors, and heat that holds through the winter. This is the asset where the gap between what we paid "
           "and what it is now worth is widest."),
 dict(slug="north-pole", name="North Pole Facility", loc="North Pole, Alaska",
      kind="Warehouse and office", img="npl-wh-office",
      alt="The North Pole warehouse and office facility seen from the gravel yard under an open sky",
      facts=["Warehouse and office", "Yard space", "Highway access"],
      body="A warehouse and office building just outside Fairbanks with yard space around it. Useful to tenants who need "
           "to park plant and trailers on site rather than hunt for storage somewhere else."),
 dict(slug="frontier-industrial", name="Frontier Industrial", loc="Prudhoe Bay, Alaska",
      kind="Industrial", img="ftr-ind-facility",
      alt="Aerial view of the Frontier industrial site at Prudhoe Bay with buildings laid out across the tundra",
      facts=["8 warehouses", "North Slope", "Shop and storage"],
      body="Eight warehouses on the North Slope. Shop space, heated storage and laydown for operators working the "
           "Prudhoe Bay field. Materials come up the Dalton Highway by truck, and building new on the Slope still "
           "costs a multiple of what it costs in Fairbanks, which is most of the reason existing slope industrial "
           "holds its value."),
 dict(slug="frontier-housing", name="Frontier Workforce Housing", loc="Prudhoe Bay, Alaska",
      kind="Workforce housing", img="frontier-aurora", wide=True,
      alt="The Frontier shop at Prudhoe Bay beneath the northern lights on a clear winter night",
      facts=["208 bedrooms", "Crew accommodation", "North Slope"],
      body="Two hundred and eight bedrooms of crew accommodation at Prudhoe Bay, with the kitchen, laundry and common "
           "rooms that go with housing rotating crews. Occupancy here follows slope activity rather than the Fairbanks "
           "housing market, which is a useful thing for the portfolio to own."),
 dict(slug="deadhorse-fbo", name="Deadhorse FBO and Hangars", loc="Deadhorse Airport, Prudhoe Bay, Alaska",
      kind="Hangars and crew facility", img="dhs-ind-crew",
      alt="The two Deadhorse hangars seen from the airfield road under a clear northern sky",
      facts=["Two hangars", "One hangar 10,000 sq ft", "26 bedrooms"],
      body="Two hangars on the field at Deadhorse Airport, the larger of them 10,000 square feet, with warehouse bays, "
           "a mezzanine tool room, offices and 26 bedrooms of crew accommodation attached. There is very little hangar "
           "space at Deadhorse and none of it is easy to replace.",
      gallery=True),
]


# ------------------------------------------------------------------- people
TEAM = [
 dict(name="Seth Church", role="Managing Member and CEO", initials="SC", bio=[
   "Sets acquisition strategy and carries final responsibility for how each asset performs.",
   "Owner and principal across Jewel Isaac, LLC, A Street Apartments, LLC, Frontier Equipment Company, "
   "Deadhorse FBO, LLC, OFD, LLC, MAMI Properties, LLC and Sabe Capital, LLC.",
   "Came up through construction and field operations, which is where the practical side of capital planning comes from.",
   "Serves as a Regent of the University of Alaska.",
 ]),
 dict(name="Maiia Makarovskaia", role="Managing Member and CFO", initials="MM"),
 dict(name="Anastasia Ponomarov", role="Property Manager", initials="AP"),
 dict(name="Karina Lushnikov", role="Assistant Manager", initials="KL"),
 dict(name="Dymytrii Ponomarov", role="Director of Property Operations", initials="DP"),
 dict(name="Yaroslav Lushnikov", role="Maintenance Technician", initials="YL"),
]

# ------------------------------------------------------------------- spaces
def S(sku, name, prop, group, price, **kw):
    d = dict(sku=sku, name=name, prop=prop, group=group, price=price)
    d.update(kw); return d

SPACES = [
 S("AST-2BR-FURN",      "2 Bedroom Furnished Townhouse, Apartment 1",   "A Street Apartments", "residential", 1800, beds=2, furn="Furnished",   prog="Market rate"),
 S("AST-2BR-FURN-02",   "2 Bedroom Furnished Townhouse, Apartment 2",   "A Street Apartments", "residential", 1800, beds=2, furn="Furnished",   prog="Market rate"),
 S("AST-2BR-FURN-03",   "2 Bedroom Furnished Townhouse, Apartment 3",   "A Street Apartments", "residential", 1800, beds=2, furn="Furnished",   prog="Market rate"),
 S("AST-2BR-UNFURN",    "2 Bedroom Unfurnished Townhouse, Apartment 1", "A Street Apartments", "residential", 1550, beds=2, furn="Unfurnished", prog="Market rate"),
 S("AST-2BR-UNFURN-02", "2 Bedroom Unfurnished Townhouse, Apartment 2", "A Street Apartments", "residential", 1550, beds=2, furn="Unfurnished", prog="Market rate"),
 S("AST-2BR-UNFURN-03", "2 Bedroom Unfurnished Townhouse, Apartment 3", "A Street Apartments", "residential", 1550, beds=2, furn="Unfurnished", prog="Market rate"),
 S("NWD-2BR-MKT",       "2 Bedroom Apartment, Market Rate",             "Northward Building", "residential", 1450, beds=2, sqft="1,065", prog="Market rate"),
 S("NWD-2BR-MKT-725",   "2 Bedroom Apartment, Market Rate, Unit 725",   "Northward Building", "residential", 1450, beds=2, sqft="1,065", prog="Market rate"),
 S("NWD-2BR-LIHTC",     "2 Bedroom Apartment, Income Qualified",        "Northward Building", "residential", 1350, beds=2, sqft="1,065", prog="Income qualified"),
 S("NWD-1BR-MKT",       "1 Bedroom Apartment, Market Rate",             "Northward Building", "residential", 1250, beds=1, sqft="660",   prog="Market rate"),
 S("NWD-1BR-LIHTC",     "1 Bedroom Apartment, Income Qualified",        "Northward Building", "residential", 1140, beds=1, sqft="660",   prog="Income qualified"),
 S("NWD-STUDIO-MKT",    "Studio Apartment, Market Rate",                "Northward Building", "residential", 1000, beds=0, sqft="510",   prog="Market rate"),
 S("NWD-STUDIO-LIHTC",  "Studio Apartment, Income Qualified",           "Northward Building", "residential",  915, beds=0, sqft="510",   prog="Income qualified"),
 S("BRN-OFFICE",        "Barnette Street Office Space",                 "300 Barnette Street", "office",      None),
 S("HLM-OFFICE",        "Helmericks Avenue Office Space",               "Helmericks Avenue",   "office",      None),
 S("HLM-WH-IND",        "Helmericks Avenue Warehouse and Industrial Space", "Helmericks Avenue", "industrial", None),
 S("NPL-WH-OFFICE",     "North Pole Warehouse and Office Facility",     "North Pole Facility", "industrial",  None),
 S("FTR-IND-FACILITY",  "Frontier Industrial Facility",                 "Frontier Industrial", "industrial",  None),
 S("DHS-IND-CREW",      "Deadhorse FBO, Two Hangars at Deadhorse Airport", "Deadhorse FBO and Hangars", "industrial", None, sqft="10,000"),
]

ALT = {
 "AST-2BR-FURN": "Kitchen and bathroom of a furnished two bedroom townhouse at A Street",
 "AST-2BR-FURN-02": "Furnished bedroom in an A Street townhouse with a window to the yard",
 "AST-2BR-FURN-03": "Living space in a furnished A Street townhouse",
 "AST-2BR-UNFURN": "Empty living room of an unfurnished A Street townhouse",
 "AST-2BR-UNFURN-02": "Unfurnished A Street townhouse with wood floors and a window",
 "AST-2BR-UNFURN-03": "Unfurnished room in an A Street townhouse",
 "NWD-2BR-MKT": "Empty two bedroom apartment in the Northward Building",
 "NWD-2BR-MKT-725": "Two bedroom apartment in the Northward Building with a table by the window",
 "NWD-2BR-LIHTC": "Income qualified two bedroom apartment in the Northward Building",
 "NWD-1BR-MKT": "One bedroom apartment in the Northward Building with a sofa and corner windows",
 "NWD-1BR-LIHTC": "Kitchen of an income qualified one bedroom apartment in the Northward Building",
 "NWD-STUDIO-MKT": "Furnished studio apartment in the Northward Building",
 "NWD-STUDIO-LIHTC": "Income qualified studio apartment in the Northward Building",
 "BRN-OFFICE": "Office space at 300 Barnette Street with daylight along the frontage",
 "HLM-OFFICE": "The Helmericks Avenue office building seen from the street",
 "HLM-WH-IND": "Clear span warehouse interior at Helmericks Avenue",
 "NPL-WH-OFFICE": "The North Pole warehouse and office facility from the yard",
 "FTR-IND-FACILITY": "Aerial view of the Frontier industrial site at Prudhoe Bay",
 "DHS-IND-CREW": "The two hangars at Deadhorse Airport seen from the airfield road",
}
GROUPS = [("all","All spaces"),("residential","Apartments"),("office","Office"),("industrial","Industrial and hangar")]

VALUE = [
 ("A Street Apartments", 1475000, 2700000),
 ("300 Barnette Street",  675000, 2000000),
 ("Helmericks Avenue",    100000, 6300000),
]



# ---------------------------------------------------------------- insights
PUBDATE = "2026-11-24"
PUBHUMAN = "24 November 2026"
INSIGHTS = [
 dict(slug="rental-demand-and-the-limits-of-new-supply", kind="Market commentary",
      title="Why Fairbanks rents hold up when new building stalls",
      dek="Interior Alaska has a short construction season and a long list of reasons new housing does not get built. "
          "That shapes what happens to the buildings already standing.",
      body="""
<p>People who look at Fairbanks from outside tend to assume the rental market behaves like a Lower 48 city of a
similar size. It does not, and the reason is supply.</p>
<h2>New supply arrives slowly, or not at all</h2>
<p>Building here is constrained in ways that have nothing to do with demand. The season you can pour concrete and
frame in is short. Materials come up the Dalton Highway by truck or in by barge and aircraft, and they cost what
that journey implies. Labor has to be found, housed and kept through a winter. By the time a developer has worked
through all of that, the rent a new building would need to charge is well above what the market is paying.</p>
<p>The result is that very little new rental stock gets added in any given year. When demand moves, supply cannot
move with it. That is the single most important fact about this market.</p>
<h2>Demand does not rest on one employer</h2>
<p>Fairbanks has several demand sources that do not move together. There is a substantial military presence. There is
the University of Alaska. There is healthcare, and there are the trades that serve the Interior and the North Slope.
A single closure or a bad year in one sector does not empty the town the way it can in a place built around one
industry.</p>
<p>That combination, constrained supply and a demand base with several legs, is what makes occupancy in good
buildings here more stable than people expect.</p>
<h2>What it means for an existing building</h2>
<p>If nobody can economically add new units, the competitive set for a well run apartment is not a new development
down the road. It is the other existing buildings, most of which have deferred maintenance of their own. A unit that
has been properly brought back is competing against tired stock rather than against something newer and better.</p>
<p>We see this in our own buildings. Where we have taken a tired property and actually fixed the units, occupancy
has followed, vacancies have come down steadily, and a renovated unit now re-lets in a fraction of the time it used
to take. The constraint was never demand. It was condition.</p>
<p class="pullq">The demand was always there. What was missing was somewhere worth renting.</p>
<h2>The limits of the argument</h2>
<p>None of this makes a building safe on its own. Constrained supply protects an owner who maintains the asset and
runs it properly. It does nothing for an owner who does not, because a tired unit in a tight market is still a
tired unit. And conditions change: a large employer could expand or contract, and construction costs could fall.
What is written here describes the market as we find it, not a forecast.</p>
"""),
 dict(slug="targeted-capital-work-on-legacy-buildings", kind="Asset update",
      title="What targeted capital work actually fixes",
      dek="Roofs, boilers, windows and units. The least interesting work in real estate is the work that decides "
          "whether a building performs.",
      body="""
<p>There is a version of property investment that happens in spreadsheets, and there is the version that happens in
a mechanical room in February. The second one is what moves the numbers.</p>
<h2>Start with what the building needs, not what shows</h2>
<p>When we take on a legacy building, the temptation is to spend first on what a prospective tenant sees: paint,
flooring, a new sign. We do the opposite, because the things that drive a tenant out are rarely cosmetic. They are
heat that fails, water that does not run hot, a window that leaks cold air across a living room, a common area that
feels unsafe at night.</p>
<p>So the order is systems first, then the unit interiors, then common areas. It costs more up front and it shows
less, but it is the difference between a tenant who renews and a tenant who serves notice in March.</p>
<h2>Do the work before the unit goes back on the market</h2>
<p>A unit that is re-let in poor condition sets the rent for the next several years and brings its problems with it.
Doing the work first takes the unit out of service for longer, which looks worse in a monthly report, and then
produces a unit that fills faster and holds.</p>
<p>We see that directly in our own turnover. Buildings that arrived with no meaningful benchmark for how quickly a
vacant apartment could be re-let now fill a renovated unit in a matter of weeks.</p>
<h2>What it does to operating performance</h2>
<p>Capital work is usually discussed as a cost. In a building that has been under-invested in, it is better
understood as the thing that unlocks the income already available in the asset.</p>
<p>On the assets we have taken all the way through this process, operating income has improved by a wide margin
against where it sat when we bought. The buildings did not change location and the market did not transform. What
changed was the condition of the units and how the building is run.</p>
<p>On the larger buildings still in progress, the gap between the operating margin we inherited and the one we are
working toward is substantial. That gap is what disciplined capital work and in house management are for. It is a
target rather than a result, and the work is still going on.</p>
<h2>The part that does not finish</h2>
<p>Capital work is not a project with an end date. A building that has been brought back will need the same
attention again, on a longer cycle. Owners who treat the renovation as a one off and then stop spending end up
exactly where the previous owner was, which is how these buildings became available to us in the first place.</p>
"""),
 dict(slug="why-we-hold-income-property-in-alaska", kind="Investment perspective",
      title="Why we hold income property in Alaska instead of trading it",
      dek="Long term ownership, downside protection, and why operational control matters more here than it does in "
          "a liquid market.",
      body="""
<p>Our holding period is measured in years and decades. That is a deliberate choice, and in Alaska it is close to a
necessary one.</p>
<h2>The exit is not reliable, so do not depend on it</h2>
<p>In a deep market you can underwrite a sale in year five with some confidence that a buyer will be there. Interior
Alaska is not a deep market. The pool of buyers for a 177 unit building in downtown Fairbanks is small, and it is
smallest exactly when you would most want to sell.</p>
<p>If the exit cannot be relied on, the return has to come from somewhere else, and that leaves rent. Once you accept
that, a great deal of your behavior changes. You stop deferring the roof to protect a disposal date. You take the
tenant who will still be there in four years over the one who will pay more for one.</p>
<p class="pullq">An owner who cannot sell easily is forced to become a good operator. That turns out to be an
advantage.</p>
<h2>Operational control is the whole thing</h2>
<p>We do not subcontract the parts of this business that determine whether a building works. Diligence, capital
decisions, leasing and day to day operations all sit with the same team, in the same office, in the same town as
the buildings.</p>
<p>Third party management is a reasonable model in a city with a deep bench of managers competing for the work. Here,
handing a building to an outside manager means the person deciding whether a boiler gets replaced this year has no
stake in whether it fails in three. We would rather carry that ourselves.</p>
<h2>What protects the downside</h2>
<p>Three things, in our experience. Supply that cannot respond quickly, which supports occupancy in maintained
buildings. A demand base with several independent legs, so no single employer dictates the market. And a mix of
asset types across the portfolio: roughly 400,000 square feet spanning 201 homes in Fairbanks, office and industrial
space, and 234 bedrooms of crew accommodation on the North Slope. Fairbanks apartments and Slope industrial follow
different economics and rarely go soft at the same time.</p>
<h2>What this is not</h2>
<p>It is not a claim that Alaska real estate cannot lose money. Buildings here are expensive to heat and expensive to
repair, the labor pool is thin, and a single major employer changing course would be felt across the whole Interior.
Long term ownership does not remove those risks. It changes which of them you are equipped to manage, and it gives
you time, which is usually the thing a struggling asset needs most.</p>
<p>Nothing here is an offer to sell or a solicitation to buy any security, and past results on our assets describe
what has happened rather than what will.</p>
"""),
]

# -------------------------------------------------------------- case studies
# Every figure below is taken from the company's own published asset records.
CASES = [
 dict(name="A Street Apartments", status="Stabilized", slug="a-street-apartments",
      type="Multifamily · 24 units", addr="500 A Street, Fairbanks, AK 99701",
      sub="Built 1950 · Entered the portfolio 2024",
      metrics=[
        ("Occupancy", "~70%", "At acquisition", "100%", "Stabilized, re-letting inside 30 days"),
        ("Net operating income", "$63,145", "2023 actual", "$280,387", "2026 forecast"),
        ("Appraised market value", "$631,446", "2023", "$2,700,000", "Appraised 9 January 2026"),
      ],
      note="Cost basis $1,475,000."),
 dict(name="Northward Building", status="Repositioning in progress", slug="northward-building",
      type="177 apartments + ground floor commercial", addr="455 3rd Avenue, Fairbanks, AK",
      sub="The largest asset in the portfolio",
      metrics=[
        ("Vacant apartments", "50 units", "October 2025", "28 units", "May 2026"),
        ("Re-letting speed", "No benchmark", "Under prior ownership", "~2 weeks", "Per renovated unit"),
        ("NOI margin", "3.0% to 4.5%", "2020 to 2024, prior ownership", "18% to 22%", "Target at stabilization"),
      ],
      note="Work is ongoing. The figures on the right are current performance and stated targets, not results."),
 dict(name="300 Barnette Street", status="In stabilization", slug="barnette-street",
      type="Office · 11,442 sq ft + 3,104 sq ft lower level", addr="300 Barnette Street, Fairbanks, AK 99701",
      sub="Built 1969 · Also our own head office",
      metrics=[
        ("Occupancy", "Approximately 61%", "Current", "Letting up", "Suites available now"),
        ("In place rent", "$1.35 to $1.50", "Per sq ft, average", "$2.00", "Per sq ft, target"),
        ("Cost basis against value", "$675,000", "Cost basis", "$2,000,000", "2026 implied value"),
      ]),
 dict(name="Helmericks Avenue", status="Letting up", slug="helmericks-avenue",
      type="Office · 5,677 sq ft + industrial · 58,615 sq ft · 64,292 sq ft total",
      addr="399 Helmericks Avenue, Fairbanks, AK",
      sub="Sandwich leasehold over an Alaska Railroad ground lease",
      metrics=[
        ("Industrial occupancy", "0%", "March 2024", "79%", "August 2024, target 92.5%"),
        ("Stabilized NOI", "Not applicable", "At acquisition", "$732,546", "Appraiser pro forma"),
        ("Appraised market value", "$100,000", "Cost basis", "$4,650,000", "As is. $6,440,746 stabilized"),
      ],
      note="The summary table above uses the rounded $6.3M appraised figure for this asset."),
]

# old Tilda-era URLs that search engines already know, mapped to their new home
OLD_LISTINGS = {
 "164142343624-2-bedroom-furnished-townhouse-a-street-a": "AST-2BR-FURN-02",
 "178868325974-studio-apartment-northward-building-mark": "NWD-STUDIO-MKT",
 "195388089764-2-bedroom-unfurnished-townhouse-a-street": "AST-2BR-UNFURN-03",
 "269074241434-helmericks-ave-warehouse-amp-industrial":  "HLM-WH-IND",
 "291626867514-2-bedroom-apartment-northward-building-m": "NWD-2BR-MKT",
 "312157367694-2-bedroom-furnished-townhouse-a-street-a": "AST-2BR-FURN",
 "322149948754-barnette-office-space":                    "BRN-OFFICE",
 "346407217824-2-bedroom-apartment-northward-building-i": "NWD-2BR-LIHTC",
 "462094620354-frontier-industrial-facility":             "FTR-IND-FACILITY",
 "532404153134-2-bedroom-unfurnished-townhouse-a-street": "AST-2BR-UNFURN",
 "655018097224-helmericks-ave-office-space":              "HLM-OFFICE",
 "674026031594-1-bedroom-apartment-northward-building-m": "NWD-1BR-MKT",
 "780507136604-deadhorse-industrial-facility-amp-crew-a": "DHS-IND-CREW",
 "789535993894-2-bedroom-unfurnished-townhouse-a-street": "AST-2BR-UNFURN-02",
 "804606232674-2-bedroom-furnished-townhouse-a-street-a": "AST-2BR-FURN-03",
 "833633610574-studio-apartment-northward-building-inco": "NWD-STUDIO-LIHTC",
 "941587680164-1-bedroom-apartment-northward-building-i": "NWD-1BR-LIHTC",
 "977600447254-north-pole-warehouse-amp-office-facility": "NPL-WH-OFFICE",
 "996823136874-2-bedroom-apartment-northward-building-m": "NWD-2BR-MKT-725",
}
OLD_PAGES = {"leasing": "/availability/", "portfolio_fairbanks": "/portfolio/"}
OLD_POSTS = {
 "5sz3vyj4r1-why-we-focus-on-durable-income-producing": "why-we-hold-income-property-in-alaska",
 "95681ig0z1-why-we-focus-on-durable-income-producing": "why-we-hold-income-property-in-alaska",
 "ec87m3inz1-fairbanks-rental-demand-and-the-limits-o": "rental-demand-and-the-limits-of-new-supply",
 "ortoynbu21-fairbanks-rental-demand-and-the-limits-o": "rental-demand-and-the-limits-of-new-supply",
 "ozeem1rja1-improving-legacy-buildings-through-targe": "targeted-capital-work-on-legacy-buildings",
 "vxbz4k7c11-improving-legacy-buildings-through-targe": "targeted-capital-work-on-legacy-buildings",
}

PAGES = []          # (path, title) for the sitemap
def ver(rel):
    p = os.path.join(OUT, rel.lstrip("/"))
    try:
        return rel + "?v=" + hashlib.md5(open(p,"rb").read()).hexdigest()[:8]
    except OSError:
        return rel
def e(s): return html.escape(str(s), quote=True)
def money(n): return "${:,}".format(n)

_DIMS = {}
def dims(rel):
    """Intrinsic pixel size of a built image, so the browser reserves the box."""
    if rel not in _DIMS:
        try:
            from PIL import Image
            with Image.open(os.path.join(OUT, rel.lstrip("/"))) as im: _DIMS[rel] = im.size
        except Exception:
            _DIMS[rel] = None
    return _DIMS[rel]

def pic(stem, alt, d="property", cls="", eager=False, big=1600, small=800, sizes="(max-width:700px) 100vw, 600px"):
    base = f"/assets/img/{d}/{stem}"
    srcset = f"{base}-{small}.webp {small}w, {base}.webp {big}w"
    c = f' class="{cls}"' if cls else ""
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    wh = dims(f"{base}.webp")
    size = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    return (f'<img src="{base}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{e(alt)}"{c}{size} {load} decoding="async">')

# The investors page is still built by investors() but is NOT published.
# Flip PUBLISH_INVESTORS to True to restore it everywhere.
PUBLISH_INVESTORS = False
NAV = ([("/", "Home"), ("/portfolio/", "Portfolio"), ("/availability/", "Availability")]
       + ([("/investors/", "Investors")] if PUBLISH_INVESTORS else [])
       + [("/insights/", "Insights"), ("/about/", "About")])

def shell(path, title, desc, body, schema=None, og_img="/assets/img/property/frontier-aurora.webp"):
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == path else '', t) for h, t in NAV
    ) + '<a class="btn btn--primary btn--sm btn--in-nav" href="/contact/">Contact</a>'
    ld = f'<script type="application/ld+json">{json.dumps(schema, separators=(",",":"))}</script>' if schema else ""
    canon = SITE + path
    PAGES.append(path)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(ORG['name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAF8F4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0C1118" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{ver('/assets/css/site.css')}">
<script>(function(){{try{{var t=localStorage.getItem("fcp-theme");if(t)document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})();</script>
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div id="intl" class="intl-bar"></div>
<header class="hdr">
  <div class="wrap hdr__in">
    <a class="brand" href="/" aria-label="Fairbanks Commercial Properties, home">
      <img class="brand__logo brand__logo--light" src="/assets/img/logo.svg" alt="Fairbanks Commercial Properties" width="164" height="41">
      <img class="brand__logo brand__logo--dark" src="/assets/img/logo-dark.svg" alt="" aria-hidden="true" width="164" height="41">
    </a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
    <a class="btn btn--primary btn--sm" href="/contact/">Contact</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__top">
      <div>
        <div class="brand" style="margin-bottom:16px">
          <img class="brand__logo brand__logo--light" src="/assets/img/logo.svg" alt="Fairbanks Commercial Properties" width="164" height="41">
          <img class="brand__logo brand__logo--dark" src="/assets/img/logo-dark.svg" alt="" aria-hidden="true" width="164" height="41">
        </div>
        <p class="dim" style="font-size:14px;max-width:34ch">Investing in the homes, workplaces and industrial facilities Interior Alaska depends on.</p>
      </div>
      <div><h2>Explore</h2><ul>
        <li><a href="/portfolio/">Portfolio</a></li>
        <li><a href="/availability/">Availability</a></li>
        <li><a href="/insights/">Insights</a></li>
        <li><a href="/about/">About</a></li>
      </ul></div>
      <div><h2>Spaces</h2><ul>
        <li><a href="/availability/?type=residential">Apartments</a></li>
        <li><a href="/availability/?type=office">Office</a></li>
        <li><a href="/availability/?type=industrial">Industrial</a></li>
        <li><a href="/contact/">Inquire</a></li>
      </ul></div>
      <div><h2>Contact</h2><ul>
        <li><a href="tel:{ORG['tel']}">{ORG['phone']}</a></li>
        <li><a href="mailto:{ORG['email']}">{ORG['email']}</a></li>
        <li class="dim" style="line-height:1.5">{ORG['street']}<br>{ORG['city']}, {ORG['region']} {ORG['zip']}</li>
      </ul></div>
    </div>
    <div class="ftr__bot">
      <span>&copy; <span data-year>2026</span> {e(ORG['name'])}. All rights reserved.</span>
      <nav aria-label="Legal"><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a>
      <button class="tog" data-theme-toggle type="button">Dark mode</button></nav>
    </div>
  </div>
</footer>
<script src="{ver('/assets/js/site.js')}" defer></script>
<script src="{ver('/assets/js/intl.js')}" defer></script>
</body>
</html>"""

def write(path, content):
    full = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

ORG_LD = {
 "@type": "RealEstateAgent", "@id": SITE + "/#org", "name": ORG["name"], "url": SITE + "/",
 "logo": SITE + "/assets/img/logo.svg", "image": SITE + "/assets/img/logo.svg",
 "description": "Privately held owner and operator investing in the homes, workplaces and industrial facilities Interior Alaska depends on, across Fairbanks, North Pole and Prudhoe Bay.",
 "telephone": "+1-907-456-4274", "email": ORG["email"],
 "address": {"@type":"PostalAddress","streetAddress":ORG["street"],"addressLocality":ORG["city"],
             "addressRegion":ORG["region"],"postalCode":ORG["zip"],"addressCountry":"US"},
 "geo": {"@type":"GeoCoordinates","latitude":ORG["lat"],"longitude":ORG["lon"]},
 "areaServed": [{"@type":"City","name":n} for n in ("Fairbanks","North Pole","Prudhoe Bay","Deadhorse")],
}
def graph(*nodes): return {"@context":"https://schema.org","@graph":[ORG_LD]+list(nodes)}

def band(h, p, a1=("Contact us","/contact/"), a2=("See what is available","/availability/")):
    return f"""<section class="band"><div class="wrap band__in">
  <div><h2>{h}</h2><p style="margin:14px 0 0">{p}</p></div>
  <div class="band__cta"><a class="btn btn--primary" href="{a1[1]}">{a1[0]}</a>
  <a class="btn btn--ghost" href="{a2[1]}">{a2[0]}</a></div>
</div></section>"""

# ============================================================== page: home
def prop_card(p):
    facts = "".join(f"<li>{e(f)}</li>" for f in p["facts"])
    return f"""<a class="card" href="/portfolio/#{p['slug']}">
  <div class="card__img">{pic(p['img'], p['alt'], **( {'big':1900,'small':1000} if p.get('wide') else {} ))}<span class="card__tag">{e(p['kind'])}</span></div>
  <div class="card__b"><h3>{e(p['name'])}</h3><p class="card__loc">{e(p['loc'])}</p>
  <ul class="card__facts">{facts}</ul></div></a>"""

def home():
    stats = "".join(f'<div><div class="n">{n}</div><div class="l">{l}</div></div>' for n, l, _ in STATS)
    cards = "".join(prop_card(p) for p in P)
    steps = [
      ("We take on buildings others have given up on",
       "Interior Alaska has sound structures in locations that still matter, sitting under years of deferred "
       "maintenance. Those are the ones we go after. Bringing one back puts housing and workspace into service that "
       "the community would otherwise lose."),
      ("We put real capital into them",
       "Roofs, boilers, windows, whole units. The work happens on our own account before the space goes back on the "
       "market, because people deserve somewhere that has actually been fixed rather than painted over."),
      ("We answer for them ourselves",
       "Leasing, tenant relations, maintenance and vendors all sit with our own team at 300 Barnette Street. When a "
       "heater fails at two in the morning in February, the person who picks up works for the owner."),
      ("We stay",
       "Our return comes from rent collected year after year, not from selling the building on. That lets us make "
       "decisions a short term owner cannot, and it means our tenants are not meeting a new landlord every few years."),
    ]
    steps_h = "".join(f'<div><div class="num"></div><h3>{e(t)}</h3><p>{e(b)}</p></div>' for t, b in steps)
    where = [
      ("Fairbanks", "The second largest city in Alaska and the service center for everything north of the Alaska "
                    "Range. Most of our apartments are here, including income qualified homes for households the "
                    "open market prices out."),
      ("North Pole", "Ten miles southeast of Fairbanks on the highway, where local contractors and tradespeople can "
                     "get yard space alongside a building instead of hunting for storage across town."),
      ("Prudhoe Bay and Deadhorse", "Industrial buildings, hangars and crew accommodation on the North Slope. "
                     "Everything up here came up the Dalton Highway by truck, or in by barge and aircraft, so "
                     "keeping what already stands in service is the only practical way to house and supply the "
                     "people working the field."),
    ]
    where_h = "".join(f'<div><h3>{e(t)}</h3><p>{e(b)}</p></div>' for t, b in where)
    why = [
      ("Very little gets built here",
       "New construction in Interior Alaska is slow, costly and limited by the weather. That puts a floor under "
       "demand for existing buildings that have been properly looked after."),
      ("Infrastructure is moving",
       "Energy, transportation and regional development work across the Interior could lift economic activity over "
       "the long run. Demand for homes and workspace tends to follow it."),
      ("Demand does not rest on one employer",
       "The military bases, the University of Alaska, healthcare and the trades all draw people to Fairbanks. "
       "No single closure takes the whole market down with it."),
      ("Real buildings hold up",
       "Well located property in a market where supply cannot react quickly has tended to hold its value through "
       "inflation better than most things a person can own."),
    ]
    why_h = "".join(f'<div><h3>{e(t)}</h3><p>{e(b)}</p></div>' for t, b in why)
    avail_n = len(SPACES)
    body = f"""
<section class="hero">
  <div class="hero__bg">{pic('frontier-aurora','The Frontier shop on the North Slope beneath the northern lights',eager=True,big=1900,small=1000,sizes='100vw')}</div>
  <div class="wrap hero__in">
    <p class="eyebrow">Fairbanks &middot; North Pole &middot; Prudhoe Bay</p>
    <h1>We invest in the places Interior Alaska depends on.</h1>
    <p class="lede">Fairbanks Commercial Properties puts long term capital into the homes, workplaces and industrial
      facilities this region runs on. We take on buildings that matter to the community, bring them back into good
      order, and stay to look after them.</p>
    <div class="hero__cta">
      <a class="btn btn--primary" href="/availability/">See {avail_n} available spaces</a>
      <a class="btn btn--light" href="/portfolio/">View the portfolio</a>
    </div>
    <div class="hero__stats">{stats}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="shead"><p class="eyebrow">Portfolio</p>
      <h2>Homes, workplaces and facilities, from downtown Fairbanks to the Deadhorse airfield</h2>
      <p class="lede">Every property here is owned and operated by us. When something goes wrong in one of these
        buildings, the person who answers for it lives and works in the same town.</p></div>
    <div class="grid grid--3">{cards}</div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="shead"><p class="eyebrow">How we work</p><h2>What we commit to, on every building</h2></div>
    <div class="steps">{steps_h}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="shead"><p class="eyebrow">Why Interior Alaska</p><h2>Why we keep putting money into this region</h2>
      <p class="lede">We are not diversified across the Lower 48 and we are not trying to be. This is the market we
        know, and these are the reasons we are still buying in it.</p></div>
    <div class="steps">{why_h}</div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="shead"><p class="eyebrow">Where we operate</p><h2>Three communities, one team</h2></div>
    <div class="steps">{where_h}</div>
  </div>
</section>

{band("Looking for space in Fairbanks or on the Slope?",
      "Tell us what you need and the size of space you are after. You will hear back from the people who own the building, not a call center.",
      ("Get in touch","/contact/"), ("Browse availability","/availability/"))}
"""
    return shell("/", f"{ORG['name']} | Apartments, Offices and Industrial Space in Interior Alaska",
      "We invest in the homes, workplaces and industrial facilities Interior Alaska depends on. 400,000 sq ft across "
      "Fairbanks, North Pole and Prudhoe Bay, owned and operated by us.", body,
      graph({"@type":"WebSite","@id":SITE+"/#website","url":SITE+"/","name":ORG["name"],"publisher":{"@id":SITE+"/#org"}}))

# ========================================================== page: portfolio
def portfolio():
    man = json.load(open(os.path.join(OUT, "assets/img/manifest.json")))
    secs = []
    for i, p in enumerate(P):
        facts = "".join(f"<li>{e(f)}</li>" for f in p["facts"])
        spaces = [s for s in SPACES if s["prop"] == p["name"]]
        link = (f'<p style="margin-top:20px"><a class="btn btn--ghost btn--sm" href="/availability/?type={spaces[0]["group"]}">'
                f'{len(spaces)} space{"s" if len(spaces)!=1 else ""} available here</a></p>') if spaces else ""
        gal = ""
        if p.get("gallery"):
            shots = "".join(
              f'<button data-full="/assets/img/deadhorse/{d["stem"]}.webp" data-alt="{e(d["alt"])}" aria-label="Open photo: {e(d["alt"])}">'
              f'<img src="/assets/img/deadhorse/{d["stem"]}-700.webp" alt="{e(d["alt"])}" loading="lazy" decoding="async" width="700" height="525"></button>'
              for d in man["deadhorse"])
            gal = (f'<div style="margin-top:34px"><h3 style="margin-bottom:16px">Inside the Deadhorse facility</h3>'
                   f'<div class="gal" data-gallery>{shots}</div></div>')
        rev = ' style="direction:rtl"' if i % 2 else ""
        inner = ' style="direction:ltr"' if i % 2 else ""
        secs.append(f"""<section id="{p['slug']}" class="{'alt' if i%2 else ''}">
  <div class="wrap">
    <div class="split"{rev}><div{inner}>
      <p class="eyebrow">{e(p['kind'])}</p>
      <h2>{e(p['name'])}</h2>
      <p class="dim" style="margin:8px 0 18px">{e(p['loc'])}</p>
      <p class="lede">{e(p['body'])}</p>
      <ul class="card__facts" style="border:0;padding-top:6px">{facts}</ul>
      {link}
    </div><figure class="figure" style="margin:0"{inner}>{pic(p['img'], p['alt'], sizes='(max-width:860px) 100vw, 540px', **( {'big':1900,'small':1000} if p.get('wide') else {} ))}</figure></div>
    {gal}
  </div></section>""")
    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Portfolio</nav></div>
<section class="tight"><div class="wrap">
  <div class="shead"><p class="eyebrow">Portfolio</p><h1>The places we look after</h1>
  <p class="lede">Eight properties across Fairbanks, North Pole and the North Slope. Roughly 400,000 square feet in
    total: 201 homes, office and warehouse space for local businesses, and 234 bedrooms of crew accommodation above
    the Arctic Circle.</p></div>
  <div class="figrow">{''.join(f'<div><div class="n">{n}</div><div class="l">{l}</div></div>' for n,l,_ in STATS)}</div>
</div></section>
{''.join(secs)}
{band("Want the detail on a particular building?",
      "We can send floor plans, current rent rolls where appropriate, and arrange a walk through.",
      ("Ask about a property","/contact/"), ("See available spaces","/availability/"))}
"""
    return shell("/portfolio/", f"Portfolio | {ORG['name']}",
      "Eight property holdings in Fairbanks, North Pole and Prudhoe Bay: the Northward Building, A Street Apartments, "
      "300 Barnette Street, Helmericks Avenue, North Pole, Frontier and the Deadhorse hangars.", body,
      graph({"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Portfolio","item":SITE+"/portfolio/"}]}))

# ======================================================= page: availability
def slug(s): return s["sku"].lower()
def price_txt(s): return (money(s["price"]) + "<span>/month</span>") if s["price"] else 'Price on request'
def facts_of(s):
    f = []
    if s.get("beds") == 0: f.append("Studio")
    elif s.get("beds"): f.append(f"{s['beds']} bedroom")
    if s.get("sqft"): f.append(f"{s['sqft']} sq ft")
    if s.get("furn"): f.append(s["furn"])
    if s.get("prog"): f.append(s["prog"])
    return f

def space_card(s, lvl="h3"):
    facts = "".join(f"<li>{e(x)}</li>" for x in facts_of(s))
    return f"""<a class="card" href="/availability/{slug(s)}/" data-space data-group="{s['group']}">
  <div class="card__img">{pic(slug(s), ALT[s['sku']])}<span class="card__tag">{e(s['prop'])}</span></div>
  <div class="card__b"><{lvl}>{e(s['name'])}</{lvl}><p class="card__loc">{e(s['prop'])}</p>
  <ul class="card__facts">{facts}</ul>
  <div class="card__price">{price_txt(s)}</div></div></a>"""

def availability():
    chips = "".join(f'<button class="chip" type="button" data-group="{g}" aria-pressed="{"true" if g=="all" else "false"}">{e(l)}</button>' for g, l in GROUPS)
    cards = "".join(space_card(s, "h2") for s in SPACES)
    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Availability</nav></div>
<section class="tight"><div class="wrap">
  <div class="shead"><p class="eyebrow">Availability</p><h1>Space available now</h1>
  <p class="lede">Apartments in downtown Fairbanks and at A Street, office suites, warehouse and industrial space,
    and hangar and crew facilities at Deadhorse. Rents shown are monthly and current.</p></div>
  <div class="filters" id="filters">{chips}<span class="fcount" id="fcount">{len(SPACES)} spaces</span></div>
  <div class="grid grid--3">{cards}</div>
  <p class="empty" id="fempty" hidden>Nothing matches that filter at the moment. <a href="/contact/">Tell us what you need</a> and we will let you know when something opens up.</p>
</div></section>
{band("Not seeing the right fit?",
      "Space turns over regularly and some of it never reaches this page. Tell us what you are looking for and we will keep you in mind.",
      ("Register your interest","/contact/"), ("View the portfolio","/portfolio/"))}
"""
    items = [{"@type":"ListItem","position":i+1,"url":f"{SITE}/availability/{slug(s)}/","name":s["name"]} for i, s in enumerate(SPACES)]
    return shell("/availability/", f"Available Space | {ORG['name']}",
      "Apartments, office suites, warehouse and industrial space available to let in Fairbanks, North Pole and "
      "Prudhoe Bay, Alaska. Current rents and full specifications.", body,
      graph({"@type":"ItemList","name":"Available space","numberOfItems":len(SPACES),"itemListElement":items},
            {"@type":"BreadcrumbList","itemListElement":[
              {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
              {"@type":"ListItem","position":2,"name":"Availability","item":SITE+"/availability/"}]}))

def space_page(s):
    prop = next((p for p in P if p["name"] == s["prop"]), None)
    spec = []
    if s.get("beds") == 0: spec.append(("Type", "Studio apartment"))
    elif s.get("beds"): spec.append(("Bedrooms", str(s["beds"])))
    if s.get("sqft"): spec.append(("Floor area", s["sqft"] + " sq ft"))
    if s.get("furn"): spec.append(("Furnishing", s["furn"]))
    if s.get("prog"): spec.append(("Program", s["prog"]))
    spec += [("Property", s["prop"]), ("Location", prop["loc"] if prop else ORG["city"]), ("Reference", s["sku"])]
    spec_h = "".join(f'<li><span class="k">{e(k)}</span><span class="v">{e(v)}</span></li>' for k, v in spec)

    if s["group"] == "residential":
        lead = (f"A {('studio' if s.get('beds')==0 else str(s['beds'])+' bedroom')} unit at {s['prop']}"
                + (f", {s['sqft']} square feet" if s.get("sqft") else "")
                + (f", let {s['furn'].lower()}" if s.get("furn") else "") + ".")
        extra = ("Income qualified units are let at a reduced rent to households that meet the program limits. "
                 "We will walk you through whether you qualify."
                 if s.get("prog") == "Income qualified" else
                 "Let on standard terms at the market rent. Ask us about availability dates and what is included.")
    else:
        lead = f"Commercial space at {s['prop']}, {prop['loc'] if prop else ORG['city']}."
        extra = ("Terms depend on the size of space taken and the length of lease. Tell us what the space is for and "
                 "we will come back with a figure and a date you could be in by.")
    rel = [x for x in SPACES if x["prop"] == s["prop"] and x["sku"] != s["sku"]][:3] \
          or [x for x in SPACES if x["group"] == s["group"] and x["sku"] != s["sku"]][:3]
    rel_h = "".join(space_card(x) for x in rel)
    offer = ({"@type":"Offer","price":s["price"],"priceCurrency":"USD","availability":"https://schema.org/InStock",
              "priceSpecification":{"@type":"UnitPriceSpecification","price":s["price"],"priceCurrency":"USD",
                                    "unitCode":"MON","billingDuration":1}}
             if s["price"] else {"@type":"Offer","availability":"https://schema.org/InStock","priceCurrency":"USD"})
    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>
  <a href="/availability/">Availability</a><span>/</span>{e(s['name'])}</nav></div>
<div class="wrap dhead"><p class="eyebrow">{e(s['prop'])}</p><h1>{e(s['name'])}</h1></div>
<div class="wrap"><div class="dgrid">
  <div>
    <figure class="figure dhero" style="margin:0 0 26px" data-gallery>
      <button class="dhero__btn" data-full="/assets/img/property/{slug(s)}.webp" data-alt="{e(ALT[s['sku']])}"
              aria-label="Open the full photo: {e(ALT[s['sku']])}">
        {pic(slug(s), ALT[s['sku']], eager=True, sizes='(max-width:900px) 100vw, 680px')}
      </button>
      <figcaption>{e(ALT[s['sku']])} <span class="dim">Click to enlarge.</span></figcaption></figure>
    <p class="lede">{e(lead)}</p>
    <p>{e(extra)}</p>
    <h2 style="font-size:24px;margin:34px 0 14px">Specification</h2>
    <div class="panel"><ul class="spec">{spec_h}</ul></div>
  </div>
  <aside>
    <div class="panel panel--sticky">
      <p class="price-lg">{price_txt(s)}</p>
      <p class="dim" style="font-size:14px;margin:10px 0 20px">Reference {e(s['sku'])}</p>
      <a class="btn btn--primary" style="width:100%" href="/contact/?ref={e(s['sku'])}">Inquire about this space</a>
      <p style="margin:18px 0 0;font-size:14.5px" class="dim">Or call us directly on
        <a href="tel:{ORG['tel']}" style="color:var(--accent);text-decoration:none">{ORG['phone']}</a>.</p>
      <ul class="clist" style="margin-top:18px;border-top:1px solid var(--line);padding-top:6px">
        <li><div class="k">Email</div><div class="v"><a href="mailto:{ORG['email']}">{ORG['email']}</a></div></li>
        <li><div class="k">Office</div><div class="v" style="font-size:15.5px">{e(ADDR_1L)}</div></li>
      </ul>
    </div>
  </aside>
</div></div>
<section><div class="wrap">
  <div class="shead"><h2 style="font-size:30px">Other space you might want</h2></div>
  <div class="grid grid--3">{rel_h}</div>
  <p style="margin-top:28px"><a class="btn btn--ghost" href="/availability/">All available space</a></p>
</div></section>
"""
    desc = f"{s['name']} at {s['prop']}, {prop['loc'] if prop else ORG['city']}. " + \
           (f"{money(s['price'])} per month. " if s["price"] else "Price on request. ") + "Contact Fairbanks Commercial Properties."
    return shell(f"/availability/{slug(s)}/", f"{s['name']} | {s['prop']} | {ORG['name']}", desc, body,
      graph({"@type":"Accommodation" if s["group"]=="residential" else "Place",
             "name":s["name"],"description":desc,"sku":s["sku"],
             "image":f"{SITE}/assets/img/property/{slug(s)}.webp",
             "address":{"@type":"PostalAddress","addressLocality":ORG["city"],"addressRegion":"AK","addressCountry":"US"},
             "offers":offer},
            {"@type":"BreadcrumbList","itemListElement":[
              {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
              {"@type":"ListItem","position":2,"name":"Availability","item":SITE+"/availability/"},
              {"@type":"ListItem","position":3,"name":s["name"],"item":f"{SITE}/availability/{slug(s)}/"}]}),
      og_img=f"/assets/img/property/{slug(s)}.webp")

# ========================================================== page: investors
def investors():
    mx = max(v for _, _, v in VALUE)
    rows = ""
    for name, cost, val in VALUE:
        up = round((val / cost - 1) * 100)
        rows += (f'<tr><td data-l="Asset">{e(name)}</td>'
                 f'<td data-l="Cost basis">{money(cost)}<span class="bar" style="width:{max(2,round(cost/mx*100))}%"></span></td>'
                 f'<td data-l="Appraised value">{money(val)}<span class="bar v" style="width:{round(val/mx*100)}%"></span></td>'
                 f'<td data-l="Uplift" class="up">+{up:,}%</td></tr>')
    tc, tv = sum(c for _, c, _ in VALUE), sum(v for _, _, v in VALUE)
    tu = round((tv / tc - 1) * 100)

    stages = [
      ("Acquire", "We look for legacy buildings in Alaska markets that are running below what they are capable of, "
                  "where the price reflects the condition rather than the location."),
      ("Reposition", "Capital improvements, modernization and a reset of how the building is run, to release the "
                     "value already sitting inside it."),
      ("Stabilize", "Fill the building and keep it full, on lease terms that produce income we can rely on rather "
                    "than a headline rent that does not last."),
      ("Hold and optimize", "Long term income and protection of the asset itself, through management that does not "
                            "stop once the building is full."),
    ]
    stages_h = "".join(f'<div><div class="num"></div><h3>{e(t)}</h3><p>{e(b)}</p></div>' for t, b in stages)

    cs_h = ""
    for c in CASES:
        mets = ""
        for label, bv, bc, av, ac in c["metrics"]:
            mets += (f'<div class="metric"><div class="metric__l">{e(label)}</div><div class="metric__pair">'
                     f'<div class="metric__side"><span class="metric__v">{e(bv)}</span><span class="metric__c">{e(bc)}</span></div>'
                     f'<div class="metric__arrow" aria-hidden="true">&rarr;</div>'
                     f'<div class="metric__side"><span class="metric__v is-now">{e(av)}</span><span class="metric__c">{e(ac)}</span></div>'
                     f'</div></div>')
        note = f'<p class="cs__note">{e(c["note"])}</p>' if c.get("note") else ""
        cs_h += (f'<article class="cs" id="case-{c["slug"]}">'
                 f'<div class="cs__head"><span class="cs__status">{e(c["status"])}</span>'
                 f'<h3>{e(c["name"])}</h3>'
                 f'<p class="cs__meta">{e(c["type"])}</p>'
                 f'<p class="cs__addr">{e(c["addr"])}<br>{e(c["sub"])}</p></div>'
                 f'<div class="cs__metrics">{mets}</div>{note}'
                 f'<p class="cs__link"><a href="/portfolio/#{c["slug"]}">See this property &rarr;</a></p></article>')

    pipe = [
      ("Energy efficient by design", "Lower utility and maintenance cost per door than the housing stock it replaces, which matters most in a place with our heating bills."),
      ("Modular and prefabricated", "Built in a factory rather than outdoors in February. A shorter build cycle and a predictable standard of finish."),
      ("Attainable without subsidy", "Priced to work for ordinary Fairbanks households on the economics alone, rather than depending on a subsidy program."),
      ("Ready to go", "The operating platform already exists and the track record is on this page. The pipeline is the next part."),
    ]
    pipe_h = "".join(f'<div><h3>{e(t)}</h3><p>{e(b)}</p></div>' for t, b in pipe)

    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Investors</nav></div>
<section class="tight"><div class="wrap">
  <div class="shead"><p class="eyebrow">Investors</p><h1>We put our own capital in first</h1>
  <p class="lede">Fairbanks Commercial Properties buys, repositions and holds real property in Interior Alaska and on
    the North Slope. We co-invest in every deal we bring to a partner, and we operate what we buy. Multifamily,
    mixed use, office and industrial, held through the cycle.</p>
  <p style="margin-top:24px"><a class="btn btn--primary" href="/contact/?ref=Investor%20overview">Request the investor overview</a>
     <a class="btn btn--ghost" href="/contact/?ref=Strategy%20call">Schedule a conversation</a></p></div>
  <div class="figrow">
    <div><div class="n">400,000</div><div class="l">Sq ft under management</div></div>
    <div><div class="n">8</div><div class="l">Holdings</div><div class="s">Across three Alaska markets</div></div>
    <div><div class="n">201</div><div class="l">Homes</div><div class="s">Market rate and income qualified</div></div>
    <div><div class="n">234</div><div class="l">North Slope bedrooms</div><div class="s">Crew accommodation</div></div>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="shead"><p class="eyebrow">How we invest</p><h2>The same four steps on every asset</h2></div>
  <div class="steps">{stages_h}</div>
</div></section>

<section><div class="wrap">
  <div class="shead"><p class="eyebrow">Value creation</p><h2>Cost basis against appraised value</h2>
  <p>Three assets we have already taken through acquisition, repositioning and stabilization. The cost basis is what
     we paid. The appraised value is the most recent third party appraisal.</p></div>
  <table class="vtable">
    <caption>Figures in US dollars. Appraised values are point in time and are not a forecast.</caption>
    <thead><tr><th scope="col">Asset</th><th scope="col">Cost basis</th><th scope="col">Appraised value</th><th scope="col">Uplift</th></tr></thead>
    <tbody>{rows}</tbody>
    <tfoot><tr><td data-l="Total">Total</td><td data-l="Cost basis">{money(tc)}</td>
      <td data-l="Appraised value">{money(tv)}</td><td data-l="Uplift" class="up">+{tu:,}%</td></tr></tfoot>
  </table>
  <p class="dim" style="font-size:13.5px;margin-top:20px;max-width:70ch">Past results on these three assets describe what
    has happened, not what will happen. Nothing on this page is an offer to sell or a solicitation to buy any security.</p>
</div></section>

<section class="alt"><div class="wrap">
  <div class="shead"><p class="eyebrow">Case studies</p><h2>Asset by asset, before and now</h2>
    <p class="lede">The detail behind the table. Where an asset is still being worked on we say so, and the figure on
      the right is a target rather than a result.</p></div>
  <div class="cases">{cs_h}</div>
</div></section>

<section><div class="wrap">
  <div class="split">
    <div>
      <p class="eyebrow">Repositioning</p>
      <h2>What the work actually looks like</h2>
      <p class="lede">A unit comes back to us tired. We strip it, deal with whatever is behind the walls, and put it
        back on the market at a rent the condition now justifies. Multiply that by two hundred.</p>
      <p>This is unglamorous and it is most of the job. It is also where the gap between cost basis and appraised
        value in the table above comes from.</p>
    </div>
    <div class="grid" style="grid-template-columns:1fr 1fr;gap:12px">
      <figure class="figure" style="margin:0">{pic('unit-before','A unit mid renovation with the old fittings stripped out',sizes='(max-width:860px) 50vw, 260px')}<figcaption>Before</figcaption></figure>
      <figure class="figure" style="margin:0">{pic('unit-after','The same class of unit finished and furnished, ready to let',sizes='(max-width:860px) 50vw, 260px')}<figcaption>After</figcaption></figure>
    </div>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="shead"><p class="eyebrow">What comes next</p><h2>Beyond repositioning: new housing</h2>
    <p class="lede">Bringing old buildings back only goes so far. Interior Alaska also needs homes that do not exist
      yet, and the cheapest way to build them here is not the traditional way.</p></div>
  <div class="steps">{pipe_h}</div>
</div></section>

<section><div class="wrap">
  <div class="shead"><p class="eyebrow">Partnership</p><h2>How we structure it</h2></div>
  <div class="steps">
    <div><h3>Equity partnerships</h3><p>Joint ventures and co-investments taken deal by deal, alongside our own money in the same position.</p></div>
    <div><h3>Capital that can wait</h3><p>These assets pay their way over years. We work best with partners who are not counting on an exit date.</p></div>
    <div><h3>Clear governance</h3><p>Decision rights, reporting cadence and the reserve matters that need partner sign off are written down before anything closes.</p></div>
    <div><h3>One operator throughout</h3><p>The team that underwrites the building is the team that lets and runs it afterwards.</p></div>
  </div>
</div></section>

{band("Want to talk about a transaction?",
      "Ask for the investor overview, or go straight to a call with the people who make the decisions.",
      ("Request the investor overview","/contact/?ref=Investor%20overview"), ("See the portfolio","/portfolio/"))}
"""
    return shell("/investors/", f"Investors | {ORG['name']}",
      "Co-investment and joint venture partnerships in Interior Alaska real estate. Cost basis against appraised "
      "value, asset by asset case studies, and the development pipeline.", body,
      graph({"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Investors","item":SITE+"/investors/"}]}))

def about():
    cards = ""
    for t in TEAM:
        bio = ("<ul class='plist'>" + "".join(f"<li>{e(b)}</li>" for b in t["bio"]) + "</ul>") if t.get("bio") else ""
        cards += (f'<div class="person{" person--lead" if t.get("bio") else ""}">'
                  f'<div class="person__av" aria-hidden="true">{t["initials"]}</div>'
                  f'<div><h3>{e(t["name"])}</h3><p class="person__r">{e(t["role"])}</p>{bio}</div></div>')
    pillars = [
      ("Asset management", "Capital planning and performance review across every building we hold, not just the ones with a problem this month."),
      ("Property operations", "Leasing, tenant relations and maintenance coordination, run by our own staff rather than contracted out."),
      ("Financial governance", "Structured reporting, compliance oversight and controls on how capital gets committed."),
      ("Risk management", "Insurance, regulatory compliance and the operating discipline that keeps a building and the people in it safe."),
    ]
    pillars_h = "".join(f'<div><h3>{e(t)}</h3><p>{e(b)}</p></div>' for t, b in pillars)
    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>About</nav></div>
<section class="tight"><div class="wrap">
  <div class="shead"><p class="eyebrow">About</p><h1>We invest here because we live here</h1>
  <p class="lede">We are not a fund and we are not an agency. We put our own capital into buildings in Interior Alaska
    and on the North Slope, bring them back into good order, and stay to run them. Our office is in one of them.</p></div>
</div></section>

<section class="tight"><div class="wrap"><div class="split">
  <div>
    <h2>What we do</h2>
    <p>Fairbanks Commercial Properties is a privately held real estate operating company working across residential,
      commercial and mixed use property in Interior Alaska. We look after roughly 400,000 square feet: 201 homes,
      office suites and warehouses let to local businesses, two aircraft hangars, and 234 bedrooms of crew
      accommodation on the North Slope.</p>
    <p>Part of the Northward Building is income qualified, which means households the open market prices out of
      downtown can still live there. We think that matters, and we have no plans to convert those units.</p>
    <p>The mix across the portfolio is deliberate. Apartments in Fairbanks follow one set of economics, slope
      industrial and crew housing follow another, and the two rarely go soft at the same time. That stability is what
      lets us keep investing when other owners pull back.</p>
    <h2 style="margin-top:34px">How we are set up</h2>
    <p>Acquisition, renovation, leasing and day to day management all sit with the same team, working out of our own
      building at 300 Barnette Street. Nothing is handed to an outside manager once the deal closes, which is why a
      tenant with a problem reaches someone who can authorize the fix on the same call.</p>
    <p>The team's background runs through finance, engineering, construction and field operations, built up both here
      and overseas. We hire locally, we spend with Fairbanks trades and suppliers wherever we can, and the people
      making decisions about these buildings drive past them every day.</p>
  </div>
  <figure class="figure" style="margin:0">{pic('northward-exterior','The Northward Building on a Fairbanks street in autumn',sizes='(max-width:860px) 100vw, 520px')}
    <figcaption>The Northward Building, downtown Fairbanks.</figcaption></figure>
</div></div></section>

<section class="alt"><div class="wrap">
  <div class="split">
    <div>
      <p class="eyebrow">Our mission</p>
      <h2>Building so people stay</h2>
      <p class="lede">We want Interior Alaska to be a place people choose to stay in. That means homes families can
        settle into, workplaces that hold up through a Fairbanks winter, and buildings this town will still be glad
        of in fifty years.</p>
    </div>
    <div>
      <p class="eyebrow">Our philosophy</p>
      <h2>Value gets built, not bought</h2>
      <p class="lede">Nothing of value arrives at closing. It gets put in afterwards, by people rather than by the
        building itself. We decide quickly, we move quickly, and we give our attention to the unglamorous parts of
        the job, because that is where a building is won or lost.</p>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="shead"><p class="eyebrow">Our team</p><h2>The people who answer for these buildings</h2>
  <p>A small team, all of it in Fairbanks. Everyone here is reachable on the number below.</p></div>
  <div class="people">{cards}</div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="shead"><p class="eyebrow">How we operate</p><h2>Oversight on every building, every month</h2></div>
  <div class="steps">{pillars_h}</div>
</div></section>

<section><div class="wrap">
  <div class="shead"><h2>Reach us</h2></div>
  <div class="grid grid--2">
    <div class="panel"><ul class="clist">
      <li><div class="k">Office</div><div class="v">{e(ORG['street'])}<br>{ORG['city']}, {ORG['region']} {ORG['zip']}</div></li>
      <li><div class="k">Phone</div><div class="v"><a href="tel:{ORG['tel']}">{ORG['phone']}</a></div></li>
      <li><div class="k">Email</div><div class="v"><a href="mailto:{ORG['email']}">{ORG['email']}</a></div></li>
    </ul></div>
    <div class="panel">
      <h3 style="margin-bottom:10px">Who to contact</h3>
      <p style="font-size:15.5px;color:var(--ink-2)">Leasing inquiries, maintenance matters and investment questions all
        come through the same address and get routed internally. If it is urgent, call.</p>
      <p style="margin:16px 0 0"><a class="btn btn--primary btn--sm" href="/contact/">Send a message</a></p>
    </div>
  </div>
</div></section>
{band("Have a building you are thinking of selling?",
      "We buy in Fairbanks, North Pole and on the North Slope, and we can move without financing conditions on the right asset.",
      ("Talk to us","/contact/"), ("See what we look after","/portfolio/"))}
"""
    people_ld = [{"@type":"Person","name":t["name"],"jobTitle":t["role"],"worksFor":{"@id":SITE+"/#org"}} for t in TEAM]
    return shell("/about/", f"About and Leadership | {ORG['name']}",
      "Fairbanks Commercial Properties is a privately held real estate operating company in Interior Alaska. "
      "Our mission, how we operate, and the team behind the portfolio.", body,
      graph({"@type":"AboutPage","name":"About","url":SITE+"/about/"},
            *people_ld,
            {"@type":"BreadcrumbList","itemListElement":[
              {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
              {"@type":"ListItem","position":2,"name":"About","item":SITE+"/about/"}]}))

# ============================================================ page: contact
def contact():
    opts = "".join(f'<option value="{e(s["sku"])}">{e(s["name"])} ({e(s["prop"])})</option>' for s in SPACES)
    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Contact</nav></div>
<section class="tight"><div class="wrap">
  <div class="shead"><p class="eyebrow">Contact</p><h1>Get in touch</h1>
  <p class="lede">Leasing, maintenance, acquisitions or investment. Messages go to our office at 300 Barnette Street
    and we answer them ourselves.</p></div>
  <div class="dgrid">
    <div class="panel">
      <form action="{FORM}" method="POST" id="inquiry">
        <input type="hidden" name="_subject" value="Website inquiry from fairbankscp.com">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_next" value="{SITE}/thanks/">
        <div class="hp"><label for="_honey">Leave this field empty</label><input type="text" id="_honey" name="_honey" tabindex="-1" autocomplete="off"></div>
        <div class="two">
          <div class="field"><label for="fn">First name</label><input id="fn" name="First name" type="text" autocomplete="given-name" required></div>
          <div class="field"><label for="ln">Last name</label><input id="ln" name="Last name" type="text" autocomplete="family-name" required></div>
        </div>
        <div class="two">
          <div class="field"><label for="em">Email</label><input id="em" name="Email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="ph">Phone</label><input id="ph" name="Phone" type="tel" autocomplete="tel"></div>
        </div>
        <div class="field"><label for="rs">What is this about?</label>
          <select id="rs" name="Inquiry type">
            <option value="Leasing">Leasing or renting a space</option>
            <option value="Maintenance">Maintenance, I am a current tenant</option>
            <option value="Investment">Investment or partnership</option>
            <option value="Selling">I have a property to sell</option>
            <option value="Other">Something else</option>
          </select></div>
        <div class="field"><label for="sp">Space you are asking about (optional)</label>
          <select id="sp" name="Space"><option value="">Not about a specific space</option>{opts}</select></div>
        <div class="field"><label for="ms">Message</label>
          <textarea id="ms" name="Message" required placeholder="Tell us what you need and when you need it by."></textarea></div>
        <button class="btn btn--primary" type="submit" style="width:100%">Send message</button>
        <p class="form-note">We use your details to answer your inquiry and nothing else. See our
          <a href="/privacy/" style="color:var(--accent)">privacy policy</a>.</p>
      </form>
    </div>
    <aside><div class="panel panel--sticky">
      <h2 style="font-size:21px;margin-bottom:6px">Rather call?</h2>
      <ul class="clist">
        <li><div class="k">Phone</div><div class="v"><a href="tel:{ORG['tel']}">{ORG['phone']}</a></div></li>
        <li><div class="k">Email</div><div class="v"><a href="mailto:{ORG['email']}">{ORG['email']}</a></div></li>
        <li><div class="k">Office</div><div class="v" style="font-size:16px">{e(ORG['street'])}<br>{ORG['city']}, {ORG['region']} {ORG['zip']}</div></li>
      </ul>
      <p class="dim" style="font-size:14px;margin:16px 0 0">Our office is in the building we own at 300 Barnette Street,
        in downtown Fairbanks.</p>
    </div></aside>
  </div>
</div></section>
<script>
(function(){{
  try{{
    var r=new URL(location.href).searchParams.get("ref");
    if(!r)return;
    var s=document.getElementById("sp");
    if(s){{for(var i=0;i<s.options.length;i++){{if(s.options[i].value===r){{s.selectedIndex=i;break;}}}}}}
    var t=document.getElementById("ms");
    if(t&&!t.value)t.value="I would like to ask about "+r+".";
  }}catch(e){{}}
}})();
</script>
"""
    return shell("/contact/", f"Contact | {ORG['name']}",
      f"Contact Fairbanks Commercial Properties. Call {ORG['phone']}, email {ORG['email']}, or visit {ADDR_1L}.", body,
      graph({"@type":"ContactPage","name":"Contact","url":SITE+"/contact/"},
            {"@type":"BreadcrumbList","itemListElement":[
              {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
              {"@type":"ListItem","position":2,"name":"Contact","item":SITE+"/contact/"}]}))

def thanks():
    body = f"""
<section><div class="wrap narrow" style="text-align:center;padding:40px 0">
  <p class="eyebrow">Message sent</p>
  <h1>Thank you. We have it.</h1>
  <p class="lede" style="margin:20px auto 0;max-width:48ch">Someone from our office will come back to you. If it cannot
    wait, call us on <a href="tel:{ORG['tel']}" style="color:var(--accent)">{ORG['phone']}</a>.</p>
  <p style="margin-top:30px"><a class="btn btn--primary" href="/">Back to the home page</a>
     <a class="btn btn--ghost" href="/availability/">See available space</a></p>
</div></section>"""
    return shell("/thanks/", f"Thank you | {ORG['name']}", "Your message has been sent to Fairbanks Commercial Properties.", body)

# ============================================================ legal pages
EFFECTIVE = "October 2, 2026"
def legal(path, title, desc, inner):
    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>{e(title)}</nav></div>
<section class="tight"><div class="wrap"><div class="narrow">
  <h1 style="font-size:clamp(32px,5vw,50px)">{e(title)}</h1>
  <p class="dim" style="margin-top:14px">Effective {EFFECTIVE}. Applies to www.fairbankscp.com.</p>
  <div class="prose">{inner}</div>
</div></div></section>"""
    return shell(path, f"{title} | {ORG['name']}", desc, body)

def privacy():
    inner = f"""
<p>{e(ORG['name'])} operates this website. This policy explains what we collect, why we collect it, and what we do
   with it. If anything here is unclear, write to <a href="mailto:{ORG['email']}">{ORG['email']}</a>.</p>

<h2>Information we collect</h2>
<p>We collect what you give us. If you fill in a form on this site, that is your name, your email address, your phone
   number if you provide one, and whatever you write in the message. If you call or email us, we keep that
   correspondence so we can deal with your inquiry.</p>
<p>Our web host records standard server information such as the pages requested and the time of the request. We do not
   run advertising trackers on this site and we do not sell data to anyone.</p>

<h2>How we use it</h2>
<ul>
  <li>To answer your inquiry and arrange viewings or meetings.</li>
  <li>To administer tenancies, leases and maintenance where you are a tenant or applicant.</li>
  <li>To keep records we are required by law to keep.</li>
</ul>

<h2>How we disclose information</h2>
<p>We do not sell, rent or trade your personal information. We share it only where it is necessary: with service
   providers who process it on our behalf under contract, with professional advisers, and where the law or a court
   requires it.</p>

<h3>Mobile information and SMS consent</h3>
<p>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. Text
   messaging originator opt-in data and consent will not be shared with any third parties.</p>
<p>If you opt in to text messages from us, message frequency varies and message and data rates may apply. Reply STOP
   to end messages at any time, or HELP for help.</p>

<h2>How long we keep it</h2>
<p>Inquiries are kept for as long as we may reasonably need them to follow up, and tenancy records for as long as the
   law and our insurers require after a tenancy ends.</p>

<h2>Your choices</h2>
<p>You can ask us what we hold about you, ask us to correct it, or ask us to delete it where we are not required to
   keep it. Write to <a href="mailto:{ORG['email']}">{ORG['email']}</a> or to the office address below.</p>

<h2>Security</h2>
<p>This site is served over HTTPS. We take reasonable measures to protect the information we hold, though no method of
   transmission over the internet is completely secure.</p>

<h2>Children</h2>
<p>This site is not directed at children under 13 and we do not knowingly collect their information.</p>

<h2>Changes</h2>
<p>If we change this policy we will change the effective date at the top of this page.</p>

<h2>Contact</h2>
<p>{e(ORG['name'])}<br>{e(ORG['street'])}<br>{ORG['city']}, {ORG['region']} {ORG['zip']}<br>
   <a href="tel:{ORG['tel']}">{ORG['phone']}</a><br><a href="mailto:{ORG['email']}">{ORG['email']}</a></p>"""
    return legal("/privacy/", "Privacy Policy",
      "How Fairbanks Commercial Properties collects, uses and discloses personal information, including mobile "
      "information and SMS consent.", inner)

def terms():
    inner = f"""
<p>By using www.fairbankscp.com you accept these terms. If you do not accept them, please do not use the site.</p>
<h2>About the information here</h2>
<p>We publish details of property we own and space we have available, and we keep it as current as we can. Rents,
   availability and specifications can change without notice, and nothing on this site is an offer capable of
   acceptance. A tenancy or lease exists only once both parties have signed a written agreement.</p>
<h2>Investment information</h2>
<p>Nothing on this site is an offer to sell or a solicitation of an offer to buy any security or interest, and
   nothing here is investment advice.</p>
<h2>Fair housing</h2>
<p>We let residential property in accordance with federal and Alaska fair housing law. Income qualified units are let
   under the rules of the program that applies to them.</p>
<h2>Intellectual property</h2>
<p>The text, design, photographs and code of this site belong to {e(ORG['name'])} unless stated otherwise, and may not
   be copied or republished without our written permission.</p>
<h2>Links to other sites</h2>
<p>Where we link to a site we do not control, we are not responsible for its content.</p>
<h2>Liability</h2>
<p>We provide this site as it is. To the extent the law allows, we are not liable for loss arising from reliance on
   information published here.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the State of Alaska.</p>
<h2>Contact</h2>
<p>Questions about these terms go to <a href="mailto:{ORG['email']}">{ORG['email']}</a>.</p>"""
    return legal("/terms/", "Terms of Use", "Terms of use for the Fairbanks Commercial Properties website.", inner)


# ============================================================= page: insights
def insights_index():
    cards = "".join(
      f'<a class="post" href="/insights/{i["slug"]}/"><div class="post__b">'
      f'<p class="post__k">{e(i["kind"])}</p><h2>{e(i["title"])}</h2><p>{e(i["dek"])}</p>'
      f'<p class="post__m">{PUBHUMAN}</p></div></a>' for i in INSIGHTS)
    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Insights</nav></div>
<section class="tight"><div class="wrap">
  <div class="shead"><p class="eyebrow">Insights</p><h1>Notes from running buildings in Interior Alaska</h1>
  <p class="lede">What we are seeing in the Fairbanks market, what the capital work on our own buildings is
    producing, and how we think about owning property this far north.</p></div>
  <div class="grid grid--3">{cards}</div>
</div></section>
{band("Questions about any of this?",
      "If something here is relevant to a building you own or a space you need, we are easy to reach.",
      ("Get in touch","/contact/"), ("See the portfolio","/portfolio/"))}
"""
    items = [{"@type":"ListItem","position":n+1,"url":f"{SITE}/insights/{i['slug']}/","name":i["title"]} for n, i in enumerate(INSIGHTS)]
    return shell("/insights/", f"Insights | {ORG['name']}",
      "Market commentary, asset updates and investment perspective from Fairbanks Commercial Properties on "
      "property in Interior Alaska.", body,
      graph({"@type":"Blog","name":"FCP Insights","url":SITE+"/insights/"},
            {"@type":"ItemList","itemListElement":items},
            {"@type":"BreadcrumbList","itemListElement":[
              {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
              {"@type":"ListItem","position":2,"name":"Insights","item":SITE+"/insights/"}]}))

def insight_page(i):
    others = [x for x in INSIGHTS if x["slug"] != i["slug"]]
    rel = "".join(
      f'<a class="post" href="/insights/{o["slug"]}/"><div class="post__b">'
      f'<p class="post__k">{e(o["kind"])}</p><h3>{e(o["title"])}</h3><p>{e(o["dek"])}</p></div></a>' for o in others)
    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>
  <a href="/insights/">Insights</a><span>/</span>{e(i["kind"])}</nav></div>
<section class="tight article"><div class="wrap">
  <div class="article__head"><p class="eyebrow">{e(i["kind"])}</p><h1>{e(i["title"])}</h1>
    <p class="lede" style="margin-top:18px">{e(i["dek"])}</p>
    <p class="article__m">Published {PUBHUMAN} by {e(ORG["name"])}</p></div>
  <div class="prose">{i["body"]}</div>
  <div class="article__head" style="padding-top:34px">
    <p><a class="btn btn--ghost btn--sm" href="/insights/">&larr; All insights</a></p></div>
</div></section>
<section class="alt"><div class="wrap">
  <div class="shead"><h2 style="font-size:30px">See also</h2></div>
  <div class="grid grid--3">{rel}</div>
</div></section>
{band("Looking for space, or thinking about selling?",
      "We own and operate across Fairbanks, North Pole and the North Slope, and we answer our own phone.",
      ("Contact us","/contact/"), ("See available space","/availability/"))}
"""
    return shell(f"/insights/{i['slug']}/", f"{i['title']} | {ORG['name']}", i["dek"], body,
      graph({"@type":"BlogPosting","headline":i["title"],"description":i["dek"],
             "datePublished":PUBDATE,"dateModified":PUBDATE,
             "articleSection":i["kind"],
             "author":{"@id":SITE+"/#org"},"publisher":{"@id":SITE+"/#org"},
             "mainEntityOfPage":f"{SITE}/insights/{i['slug']}/"},
            {"@type":"BreadcrumbList","itemListElement":[
              {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
              {"@type":"ListItem","position":2,"name":"Insights","item":SITE+"/insights/"},
              {"@type":"ListItem","position":3,"name":i["title"],"item":f"{SITE}/insights/{i['slug']}/"}]}))

# =============================================================== 404 + misc
def notfound():
    body = f"""
<section><div class="wrap narrow" style="text-align:center;padding:40px 0">
  <p class="eyebrow">404</p><h1>That page has moved on.</h1>
  <p class="lede" style="margin:20px auto 0;max-width:46ch">We rebuilt this site, so a few old links no longer land
    where they used to. Everything is still here, just somewhere slightly different.</p>
  <p style="margin-top:30px"><a class="btn btn--primary" href="/availability/">Available space</a>
     <a class="btn btn--ghost" href="/portfolio/">The portfolio</a>
     <a class="btn btn--ghost" href="/">Home</a></p>
</div></section>"""
    h = shell("/404.html", f"Page not found | {ORG['name']}", "That page could not be found.", body)
    PAGES.pop()
    return h

def redirect(frm, to):
    """Keep URLs that search engines already know pointing at live content."""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Moved to {e(to)}</title>
<link rel="canonical" href="{SITE}{to}">
<meta name="robots" content="noindex,follow">
<meta http-equiv="refresh" content="0; url={to}">
<script>location.replace("{to}"+location.search+location.hash);</script>
</head><body style="font-family:system-ui,sans-serif;padding:3rem;max-width:40rem;margin:0 auto">
<p>This page has moved. <a href="{to}">Continue to its new home</a>.</p>
</body></html>"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="12" fill="#12171D"/>
<text x="32" y="43" font-family="Georgia,'Times New Roman',serif" font-size="27" fill="#C9752F"
 text-anchor="middle" letter-spacing="-.5">FCP</text></svg>"""

def main():
    write("/", home())
    write("/portfolio/", portfolio())
    write("/availability/", availability())
    for s in SPACES:
        write(f"/availability/{slug(s)}/", space_page(s))
    if PUBLISH_INVESTORS:
        write("/investors/", investors())
    else:
        d = os.path.join(OUT, "investors"); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(redirect("investors", "/about/"))
    write("/insights/", insights_index())
    for i in INSIGHTS:
        write(f"/insights/{i['slug']}/", insight_page(i))
    write("/about/", about())
    write("/contact/", contact())
    write("/thanks/", thanks())
    write("/privacy/", privacy())
    write("/terms/", terms())
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(notfound())

    # redirects from the previously indexed URL structure
    n = 0
    for old, sku in OLD_LISTINGS.items():
        p = os.path.join(OUT, "listings", old)
        os.makedirs(p, exist_ok=True)
        open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(redirect(old, f"/availability/{sku.lower()}/"))
        n += 1
    for old, to in OLD_PAGES.items():
        p = os.path.join(OUT, old)
        os.makedirs(p, exist_ok=True)
        open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(redirect(old, to))
        n += 1
    for old, new in OLD_POSTS.items():
        d = os.path.join(OUT, "tpost", old)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(redirect(old, f"/insights/{new}/"))
        n += 1
    p = os.path.join(OUT, "listings")
    open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(redirect("listings", "/availability/"))
    n += 1

    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
    open(os.path.join(OUT, "CNAME"), "w").write("www.fairbankscp.com\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    pri = {"/": "1.0", "/availability/": "0.9", "/portfolio/": "0.9", "/contact/": "0.7", "/about/": "0.7"}
    urls = "".join(
        f"<url><loc>{SITE}{u}</loc><changefreq>{'weekly' if u in ('/','/availability/') else 'monthly'}</changefreq>"
        f"<priority>{pri.get(u, '0.6' if u.startswith('/availability/') else '0.3')}</priority></url>"
        for u in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + urls + "</urlset>\n")

    open(os.path.join(OUT, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nDisallow: /thanks/\n\n"
        "User-agent: GPTBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\n"
        f"Sitemap: {SITE}/sitemap.xml\n")

    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(f"""# {ORG['name']}

> Privately held owner and operator investing in the homes, workplaces and industrial facilities Interior Alaska
> depends on. Roughly 400,000 sq ft across Fairbanks, North Pole and Prudhoe Bay: 201 homes (market rate and income
> qualified), office suites, eleven warehouses, two aircraft hangars and 234 bedrooms of crew accommodation.

Office: {ADDR_1L}
Phone: {ORG['phone']}
Email: {ORG['email']}
Markets: Fairbanks, North Pole, Prudhoe Bay and Deadhorse, Alaska

## Pages
- [Home]({SITE}/): overview, portfolio and how the company operates
- [Portfolio]({SITE}/portfolio/): the eight holdings in detail
- [Availability]({SITE}/availability/): {len(SPACES)} spaces available to let, with current rents
- [Insights]({SITE}/insights/): market commentary and asset updates\n- [About]({SITE}/about/): company background, mission and leadership
- [Contact]({SITE}/contact/): inquiry form
""")
    print(f"pages: {len(PAGES)}   redirects: {n}")

if __name__ == "__main__":
    main()
