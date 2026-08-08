"""Page shell, typography and navigation for the book."""

CSS = """
:root{
  --paper:#F7F7F5; --sunk:#EFEFEC; --edge:#E2E2DD; --rule:#CFCFC8;
  --ink:#1A1A18; --body:#33332F; --soft:#6B6B64; --faint:#94948C;
  --sig:#8C2F39; --sig-tint:#8C2F3914;
  --bench:#2F6D7A; --bench-tint:#2F6D7A14;
  --measure:33.5rem;
  --book:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Charter,
         "Sitka Text",Cambria,Georgia,"Times New Roman",serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono","Cascadia Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#14140F; --sunk:#1C1C17; --edge:#2A2A24; --rule:#3A3A32;
    --ink:#F0EFE8; --body:#CDCCC2; --soft:#918F85; --faint:#6E6C63;
    --sig:#DE8A92; --sig-tint:#DE8A9218;
    --bench:#74C0CC; --bench-tint:#74C0CC18;
  }
}
:root[data-theme="dark"]{
  --paper:#14140F; --sunk:#1C1C17; --edge:#2A2A24; --rule:#3A3A32;
  --ink:#F0EFE8; --body:#CDCCC2; --soft:#918F85; --faint:#6E6C63;
  --sig:#DE8A92; --sig-tint:#DE8A9218;
  --bench:#74C0CC; --bench-tint:#74C0CC18;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--body);
  font-family:var(--book);font-size:19px;line-height:1.72;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
  font-kerning:normal;font-variant-ligatures:common-ligatures}
.page{max-width:64rem;margin:0 auto;padding:0 1.6rem 7rem}
.col{max-width:var(--measure);margin:0 auto}
p{margin:0 0 1.15em;hyphens:auto}
a{color:inherit;text-decoration:none;border-bottom:1px solid var(--rule)}
a:hover{border-bottom-color:var(--sig)}
a:focus-visible{outline:2px solid var(--bench);outline-offset:3px;border-radius:2px}
strong{color:var(--ink);font-weight:600}
code,.mono{font-family:var(--mono);font-size:.82em;color:var(--ink)}
code{background:var(--sunk);padding:.06em .3em;border-radius:2px}

/* running head */
.rh{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;
  padding:1.6rem 0 0;font-family:var(--mono);font-size:.68rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--faint)}
.rh a{border:none;color:var(--faint)}
.rh a:hover{color:var(--sig)}

/* chapter opener */
.opener{padding:4.5rem 0 2.2rem;border-bottom:1px solid var(--rule);margin-bottom:2.6rem}
/* interludes are asides about method, set apart from the running argument */
.inter-open{border-left:3px solid var(--sig);padding-left:1.4rem;border-bottom-style:dotted}
.inter-open h1{font-style:italic;font-weight:500}
.chno .kind{font-family:var(--book);font-style:italic;text-transform:none;letter-spacing:0;
  color:var(--soft);font-size:.98rem;margin-left:.9rem}
.chno{font-family:var(--mono);font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;
  color:var(--sig);margin:0 0 1.1rem}
h1{font-family:var(--book);font-weight:600;font-size:clamp(2.1rem,5.4vw,3.2rem);
  line-height:1.08;letter-spacing:-.018em;color:var(--ink);margin:0 0 .8rem;
  text-wrap:balance;max-width:20ch}
.q{font-style:italic;color:var(--soft);font-size:1.08rem;max-width:40ch;margin:0;line-height:1.5}

/* drop cap on the first paragraph of a chapter */
.first::first-letter{float:left;font-size:3.45em;line-height:.84;padding:.06em .09em 0 0;
  color:var(--ink);font-weight:600}
.first::first-line{font-variant-caps:small-caps;letter-spacing:.02em}

h2{font-family:var(--book);font-weight:600;font-size:1.42rem;line-height:1.25;color:var(--ink);
  margin:2.9rem 0 .8rem;letter-spacing:-.008em;text-wrap:balance}
h3{font-family:var(--mono);font-weight:600;font-size:.72rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--soft);margin:2.4rem 0 .7rem}

/* devices */
.lead{font-size:1.13rem;line-height:1.55;color:var(--ink)}
.pull{font-family:var(--book);font-style:italic;font-size:1.32rem;line-height:1.4;
  color:var(--ink);margin:2.4rem 0;padding-left:1.2rem;border-left:2px solid var(--sig);
  text-wrap:balance}
.aside{background:var(--sunk);border-radius:3px;padding:1.1rem 1.3rem;margin:2rem 0;
  font-size:.94rem;line-height:1.6}
.aside h4{margin:0 0 .4rem;font-family:var(--mono);font-size:.68rem;letter-spacing:.13em;
  text-transform:uppercase;color:var(--sig);font-weight:600}
.aside p:last-child{margin-bottom:0}
.warn{border-left:3px solid var(--sig);background:var(--sig-tint);border-radius:0 3px 3px 0;
  padding:1.1rem 1.3rem;margin:2rem 0;font-size:.96rem;line-height:1.6}
.warn p:last-child{margin-bottom:0}
.scene{border-left:2px solid var(--rule);padding-left:1.2rem;margin:2rem 0;color:var(--soft);
  font-size:.97rem}
.scene .when{font-family:var(--mono);font-size:.7rem;letter-spacing:.1em;color:var(--sig);
  display:block;margin-bottom:.3rem;text-transform:uppercase}
blockquote{margin:1.8rem 0;padding-left:1.2rem;border-left:2px solid var(--bench);
  font-style:italic;color:var(--ink)}
blockquote p{margin-bottom:.4rem}
blockquote cite{font-style:normal;font-family:var(--mono);font-size:.72rem;color:var(--faint);
  letter-spacing:.06em}
ul,ol{padding-left:1.3rem;margin:0 0 1.15em}
li{margin-bottom:.45rem}
hr.sep{border:none;text-align:center;margin:2.6rem 0}
hr.sep::before{content:"§";color:var(--faint);font-size:1rem}

/* figures */
figure{margin:2.6rem auto;max-width:54rem}
figure svg{width:100%;height:auto;display:block;background:var(--paper);
  border:1px solid var(--edge);border-radius:2px;padding:.5rem}
figcaption{font-family:var(--mono);font-size:.73rem;line-height:1.62;color:var(--soft);
  margin-top:.7rem;max-width:44rem;letter-spacing:.01em}
figcaption b{color:var(--ink);letter-spacing:.1em;text-transform:uppercase;font-size:.67rem;
  display:block;margin-bottom:.3rem}
.grid{stroke:var(--edge);stroke-width:1}
.ref{stroke:var(--rule);stroke-width:1}.ref.dash{stroke-dasharray:3 3}
.ln{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.ln.sig{stroke:var(--sig)}.ln.bench{stroke:var(--bench)}.ln.ink{stroke:var(--ink)}
.ln.ink2{stroke:var(--ink);stroke-dasharray:5 3}
.dot{stroke:none}.dot.sig{fill:var(--sig)}.dot.bench{fill:var(--bench)}
.dot.ink,.dot.ink2{fill:var(--ink)}
.bar.sig{fill:var(--rule)}.bar.bench{fill:var(--bench)}
.band.disc{fill:var(--rule);opacity:.5}
.band.redd{fill:var(--bench-tint);stroke:var(--bench)}
.band.twit{fill:var(--sig-tint);stroke:var(--sig)}
.band.gap{fill:var(--edge);opacity:.6;stroke:none}
.conn{stroke:var(--rule);stroke-width:2}
.cell{fill:var(--bench)}.cellv{font-size:9.5px;fill:var(--paper);font-weight:600}
.reg.r1{fill:var(--rule)}.reg.r2{fill:var(--soft)}.reg.r3{fill:var(--bench)}.reg.r4{fill:var(--sig)}
.regname{font-size:10.5px;font-weight:600;fill:var(--paper);text-anchor:middle}
text{font-family:var(--mono);fill:var(--soft)}
.tick{font-size:10.5px}.tick.tiny{font-size:9px}
.axlab{font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;fill:var(--faint)}
/* series labels sit inside the plot, so knock a halo of page colour out
   behind them — otherwise a steeply descending line runs through the text */
.serlab{font-size:11px;font-weight:600;stroke:var(--paper);stroke-width:3.5px;
  stroke-linejoin:round;paint-order:stroke fill}
.serlab.sig{fill:var(--sig)}.serlab.bench{fill:var(--bench)}
.serlab.ink,.serlab.ink2{fill:var(--ink)}
.rowlab{font-size:12px;fill:var(--ink)}
.gaplab{font-size:10px;fill:var(--faint);letter-spacing:.06em;text-transform:uppercase}
.ptlab{font-size:10.5px;fill:var(--ink)}
.bandlab{font-size:11px;font-weight:600;fill:var(--ink)}

/* tables */
.tw{overflow-x:auto;margin:2rem auto;max-width:54rem}
table{border-collapse:collapse;width:100%;font-family:var(--mono);font-size:.77rem;
  font-variant-numeric:tabular-nums}
th{text-align:left;font-weight:600;color:var(--ink);letter-spacing:.06em;text-transform:uppercase;
  font-size:.65rem;padding:.6rem .7rem;border-bottom:1px solid var(--rule);white-space:nowrap}
td{padding:.5rem .7rem;border-bottom:1px solid var(--edge);color:var(--body)}
tr:last-child td{border-bottom:none}
td.n,th.n{text-align:right;white-space:nowrap}
caption{caption-side:top;text-align:left;font-family:var(--mono);font-size:.67rem;
  letter-spacing:.1em;text-transform:uppercase;color:var(--faint);padding:0 .7rem .6rem}
.hi{color:var(--sig);font-weight:600}.hib{color:var(--bench);font-weight:600}

/* chapter footer nav */
.nav{display:flex;justify-content:space-between;gap:1.5rem;margin-top:5rem;padding-top:1.6rem;
  border-top:1px solid var(--rule)}
.nav a{border:none;display:block;max-width:20rem}
.nav .dir{font-family:var(--mono);font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--faint);display:block;margin-bottom:.25rem}
.nav .t{color:var(--ink);font-size:1rem;line-height:1.3}
.nav a:hover .t{color:var(--sig)}
.nav .next{text-align:right;margin-left:auto}

/* contents page */
.front{max-width:44rem;margin:0 auto}
.front .col{max-width:none}
.title-page{padding:5rem 0 3rem;border-bottom:1px solid var(--rule);margin-bottom:3rem}
.title-page h1{font-size:clamp(2.6rem,7vw,4.4rem);max-width:14ch;margin-bottom:1.1rem}
.title-page .sub{font-style:italic;color:var(--soft);font-size:1.2rem;max-width:38ch;
  line-height:1.45;margin:0 0 2.2rem}
.stats{display:flex;flex-wrap:wrap;gap:.4rem 2rem;font-family:var(--mono);font-size:.7rem;
  letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
.stats b{color:var(--ink);font-weight:600}
.part-head{font-family:var(--mono);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;
  color:var(--sig);margin:2.8rem 0 .2rem;padding-bottom:.5rem;border-bottom:1px solid var(--rule)}
.toc{list-style:none;padding:0;margin:0}
.toc li{margin:0;border-bottom:1px solid var(--edge)}
.toc a{display:grid;grid-template-columns:2.6rem 1fr;gap:1rem;padding:.85rem .4rem;border:none;
  align-items:baseline}
.toc a:hover{background:var(--sunk)}
.toc .n{font-family:var(--mono);font-size:.72rem;color:var(--faint);letter-spacing:.06em}
.toc .tx{display:block}
.toc .t{color:var(--ink);font-size:1.06rem;line-height:1.32}
.toc .d{display:block;color:var(--soft);font-size:.9rem;font-style:italic;margin-top:.15rem}
.toc li.inter a{background:var(--sig-tint)}
.toc li.inter .t{color:var(--sig)}
.toc li.todo .t,.toc li.todo .d,.toc li.todo .n{color:var(--faint)}
.toc li.todo a{pointer-events:none}
.toc li.todo .t::after{content:" in draft";font-family:var(--mono);font-size:.58rem;
  letter-spacing:.12em;text-transform:uppercase;color:var(--faint);font-style:normal;
  border:1px solid var(--edge);border-radius:2px;padding:.12em .4em;margin-left:.5em;
  white-space:nowrap;vertical-align:.14em}

@media (max-width:640px){
  body{font-size:18px}
  .page{padding:0 1.15rem 4rem}
  .nav{flex-direction:column;gap:1.6rem}
  .nav .next{text-align:left;margin-left:0}
  .first::first-letter{font-size:3em}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<meta property="og:type" content="book">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,{favicon}">
<style>{css}</style>
</head>
<body>
<div class="page">
{runhead}
{body}
</div>
</body>
</html>
"""
