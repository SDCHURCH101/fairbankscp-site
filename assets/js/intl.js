/* Fairbanks Commercial Properties — language and currency selector.
   Original work for this site, 2026. Language switching uses Google Translate;
   currency figures are indicative only and USD is the contract currency. */
(function () {
  "use strict";
  if (window.__fcpIntl) return; window.__fcpIntl = true;

  var LANGS =
[
["en","English","English"],["es","Spanish","Español"],["zh-CN","Chinese (Simplified)","简体中文"],
["zh-TW","Chinese (Traditional)","繁體中文"],["hi","Hindi","हिन्दी"],["ar","Arabic","العربية"],
["pt","Portuguese","Português"],["bn","Bengali","বাংলা"],["ru","Russian","Русский"],
["ja","Japanese","日本語"],["pa","Punjabi","ਪੰਜਾਬੀ"],["de","German","Deutsch"],
["ko","Korean","한국어"],["fr","French","Français"],["tr","Turkish","Türkçe"],
["vi","Vietnamese","Tiếng Việt"],["it","Italian","Italiano"],["ta","Tamil","தமிழ்"],
["ur","Urdu","اردو"],["fa","Persian","فارسی"],["pl","Polish","Polski"],
["uk","Ukrainian","Українська"],["ro","Romanian","Română"],["nl","Dutch","Nederlands"],
["th","Thai","ไทย"],["id","Indonesian","Bahasa Indonesia"],["ms","Malay","Bahasa Melayu"],
["tl","Filipino","Filipino"],["sw","Swahili","Kiswahili"],["he","Hebrew","עברית"],
["el","Greek","Ελληνικά"],["cs","Czech","Čeština"],["sv","Swedish","Svenska"],
["hu","Hungarian","Magyar"],["fi","Finnish","Suomi"],["da","Danish","Dansk"],
["no","Norwegian","Norsk"],["sk","Slovak","Slovenčina"],["bg","Bulgarian","Български"],
["hr","Croatian","Hrvatski"],["sr","Serbian","Српски"],["sl","Slovenian","Slovenščina"],
["lt","Lithuanian","Lietuvių"],["lv","Latvian","Latviešu"],["et","Estonian","Eesti"],
["te","Telugu","తెలుగు"],["mr","Marathi","मराठी"],["gu","Gujarati","ગુજરાતી"],
["kn","Kannada","ಕನ್ನಡ"],["ml","Malayalam","മലയാളം"],["si","Sinhala","සිංහල"],
["ne","Nepali","नेपाली"],["my","Burmese","မြန်မာ"],["km","Khmer","ខ្មែរ"],
["lo","Lao","ລາວ"],["am","Amharic","አማርኛ"],["ha","Hausa","Hausa"],
["yo","Yoruba","Yorùbá"],["ig","Igbo","Igbo"],["zu","Zulu","isiZulu"],
["xh","Xhosa","isiXhosa"],["af","Afrikaans","Afrikaans"],["so","Somali","Soomaali"],
["rw","Kinyarwanda","Kinyarwanda"],["ny","Chichewa","Chichewa"],["st","Sesotho","Sesotho"],
["sn","Shona","chiShona"],["az","Azerbaijani","Azərbaycan"],["kk","Kazakh","Қазақ"],
["uz","Uzbek","Oʻzbek"],["ky","Kyrgyz","Кыргызча"],["tg","Tajik","Тоҷикӣ"],
["tk","Turkmen","Türkmen"],["mn","Mongolian","Монгол"],["ka","Georgian","ქართული"],
["hy","Armenian","Հայերեն"],["sq","Albanian","Shqip"],["mk","Macedonian","Македонски"],
["bs","Bosnian","Bosanski"],["is","Icelandic","Íslenska"],["ga","Irish","Gaeilge"],
["cy","Welsh","Cymraeg"],["gl","Galician","Galego"],["ca","Catalan","Català"],
["eu","Basque","Euskara"],["mt","Maltese","Malti"],["lb","Luxembourgish","Lëtzebuergesch"],
["be","Belarusian","Беларуская"],["ps","Pashto","پښتو"],["sd","Sindhi","سنڌي"],
["ku","Kurdish","Kurdî"],["yi","Yiddish","ייִדיש"],["haw","Hawaiian","ʻŌlelo Hawaiʻi"],
["mi","Maori","Te Reo Māori"],["sm","Samoan","Gagana Samoa"],["jv","Javanese","Basa Jawa"],
["su","Sundanese","Basa Sunda"],["ceb","Cebuano","Cebuano"],["la","Latin","Latina"],
["eo","Esperanto","Esperanto"]
  ];
  var CURR =
[
["USD","US Dollar","$",1],["EUR","Euro","€",0.92],["GBP","British Pound","£",0.78],
["CAD","Canadian Dollar","C$",1.36],["AUD","Australian Dollar","A$",1.50],
["JPY","Japanese Yen","¥",147],["CNY","Chinese Yuan","¥",7.12],["CHF","Swiss Franc","CHF",0.86],
["HKD","Hong Kong Dollar","HK$",7.80],["SGD","Singapore Dollar","S$",1.29],
["NZD","New Zealand Dollar","NZ$",1.63],["INR","Indian Rupee","₹",83.5],
["KRW","South Korean Won","₩",1340],["MXN","Mexican Peso","MX$",18.6],
["BRL","Brazilian Real","R$",5.45],["ZAR","South African Rand","R",18.2],
["SEK","Swedish Krona","kr",10.5],["NOK","Norwegian Krone","kr",10.7],
["DKK","Danish Krone","kr",6.85],["PLN","Polish Zloty","zł",3.95],
["CZK","Czech Koruna","Kč",23.2],["HUF","Hungarian Forint","Ft",360],
["RON","Romanian Leu","lei",4.58],["TRY","Turkish Lira","₺",34.0],
["RUB","Russian Ruble","₽",92],["UAH","Ukrainian Hryvnia","₴",41],
["ILS","Israeli Shekel","₪",3.72],["AED","UAE Dirham","AED",3.67],
["SAR","Saudi Riyal","SAR",3.75],["QAR","Qatari Riyal","QAR",3.64],
["KWD","Kuwaiti Dinar","KD",0.31],["BHD","Bahraini Dinar","BD",0.38],
["OMR","Omani Rial","OMR",0.38],["JOD","Jordanian Dinar","JD",0.71],
["EGP","Egyptian Pound","E£",48],["NGN","Nigerian Naira","₦",1580],
["KES","Kenyan Shilling","KSh",129],["GHS","Ghanaian Cedi","₵",15.6],
["MAD","Moroccan Dirham","MAD",9.85],["TND","Tunisian Dinar","DT",3.05],
["THB","Thai Baht","฿",33.5],["VND","Vietnamese Dong","₫",24800],
["IDR","Indonesian Rupiah","Rp",15600],["MYR","Malaysian Ringgit","RM",4.35],
["PHP","Philippine Peso","₱",56.5],["PKR","Pakistani Rupee","₨",278],
["BDT","Bangladeshi Taka","৳",119],["LKR","Sri Lankan Rupee","Rs",296],
["NPR","Nepalese Rupee","NRs",133],["TWD","Taiwan Dollar","NT$",32.0],
["CLP","Chilean Peso","CLP$",945],["COP","Colombian Peso","COL$",4100],
["ARS","Argentine Peso","AR$",960],["PEN","Peruvian Sol","S/",3.75],
["UYU","Uruguayan Peso","$U",40.5],["ISK","Icelandic Krona","kr",137],
["KZT","Kazakhstani Tenge","₸",478],["GEL","Georgian Lari","₾",2.70],
["RSD","Serbian Dinar","RSD",108],["BGN","Bulgarian Lev","лв",1.80],
["HRK","Croatian Kuna","kn",6.93],["ETB","Ethiopian Birr","Br",116]
  ];

  var LS_L = "fcp.lang", LS_C = "fcp.curr";
  var host = document.getElementById("intl");
  if (!host) return;

  function get(k){ try { return localStorage.getItem(k); } catch(e){ return null; } }
  function set(k,v){ try { localStorage.setItem(k,v); } catch(e){} }

  /* ---------- build the two selects ---------- */
  function opts(list, cur){
    var h = "";
    for (var i = 0; i < list.length; i++) {
      var r = list[i], code = r[0];
      var label = (list === LANGS) ? (r[2] + (r[2] !== r[1] ? " · " + r[1] : ""))
                                   : (code + " · " + r[1]);
      h += '<option value="' + code + '"' + (code === cur ? ' selected' : '') + '>' + label + '</option>';
    }
    return h;
  }
  var curLang = get(LS_L) || "en", curCurr = get(LS_C) || "USD";
  host.innerHTML =
    '<div class="intl">' +
      '<label class="intl__f"><span class="intl__lb">Language</span>' +
        '<select id="intl-lang" aria-label="Choose a language">' + opts(LANGS, curLang) + '</select></label>' +
      '<label class="intl__f"><span class="intl__lb">Currency</span>' +
        '<select id="intl-curr" aria-label="Choose a currency">' + opts(CURR, curCurr) + '</select></label>' +
      '<span class="intl__note" id="intl-note"></span>' +
    '</div>';

  var selL = document.getElementById("intl-lang"),
      selC = document.getElementById("intl-curr"),
      note = document.getElementById("intl-note");

  /* ---------- language via Google Translate ---------- */
  function loadGT(){
    if (window.__fcpGT) return; window.__fcpGT = true;
    var holder = document.createElement("div");
    holder.id = "google_translate_element";
    holder.style.cssText = "position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden";
    document.body.appendChild(holder);
    window.googleTranslateElementInit = function(){
      new google.translate.TranslateElement(
        { pageLanguage: "en", autoDisplay: false }, "google_translate_element");
      setTimeout(function(){ applyLang(curLang, 0); }, 400);
    };
    var sc = document.createElement("script");
    sc.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    sc.async = true;
    document.body.appendChild(sc);
  }
  function applyLang(code, tries){
    var combo = document.querySelector("select.goog-te-combo");
    if (!combo) {
      if ((tries || 0) < 40) return setTimeout(function(){ applyLang(code, (tries||0)+1); }, 250);
      return;
    }
    combo.value = (code === "en") ? "" : code;
    combo.dispatchEvent(new Event("change", { bubbles: true }));
  }
  selL.addEventListener("change", function(){
    curLang = selL.value; set(LS_L, curLang);
    document.documentElement.lang = curLang.split("-")[0];
    if (curLang === "en" && !window.__fcpGT) return;
    loadGT(); applyLang(curLang, 0);
  });
  if (curLang && curLang !== "en") { loadGT(); }

  /* ---------- currency ---------- */
  var RATE = {}, SYM = {}, NAME = {};
  CURR.forEach(function(r){ RATE[r[0]] = r[3]; SYM[r[0]] = r[2]; NAME[r[0]] = r[1]; });
  var origins = (typeof WeakMap !== "undefined") ? new WeakMap() : null;
  var tracked = [];
  var MONEY = /\$\s?([0-9][0-9,]*(?:\.[0-9]{1,2})?)/g;

  function skip(node){
    var p = node.parentNode;
    while (p && p !== document.body) {
      var t = p.nodeName;
      if (t === "SCRIPT" || t === "STYLE" || t === "SELECT" || t === "OPTION" || t === "TEXTAREA") return true;
      if (p.id === "intl") return true;
      p = p.parentNode;
    }
    return false;
  }
  /* Collect any *new* text nodes that still carry a USD figure. Nodes already
     converted no longer contain "$", which is why we keep our own list. */
  function collect(){
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function(n){
        if (!n.nodeValue || n.nodeValue.indexOf("$") === -1) return NodeFilter.FILTER_REJECT;
        if (origins && origins.has(n)) return NodeFilter.FILTER_REJECT;
        return skip(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = w.nextNode())) {
      if (origins) origins.set(n, n.nodeValue);
      tracked.push(n);
    }
  }
  function fmt(amount, code){
    try { return SYM[code] + Math.round(amount).toLocaleString("en-US"); }
    catch (e) { return SYM[code] + Math.round(amount); }
  }
  function applyCurr(code){
    collect();
    var rate = RATE[code] || 1;
    for (var i = 0; i < tracked.length; i++) {
      var n = tracked[i];
      if (!n.isConnected) continue;
      var src = (origins && origins.get(n)) || n.nodeValue;
      if (code === "USD") { n.nodeValue = src; continue; }
      n.nodeValue = src.replace(MONEY, function(whole, num){
        var v = parseFloat(num.replace(/,/g, ""));
        return isFinite(v) ? fmt(v * rate, code) : whole;
      });
    }
    note.textContent = (code === "USD") ? "" : "Indicative " + code + ". All agreements are in USD.";
  }
  selC.addEventListener("change", function(){
    curCurr = selC.value; set(LS_C, curCurr); applyCurr(curCurr);
  });
  if (curCurr && curCurr !== "USD") applyCurr(curCurr);
})();
