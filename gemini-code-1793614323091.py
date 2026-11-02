import google.ds_python_interpreter

html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Atelier de la Rue — Galerie virtuelle</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<meta name="theme-color" content="#04060c">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600&display=swap" rel="stylesheet">
<link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js">

<!-- =====================================================================
     RÉGLAGES (c'est le seul endroit à modifier)
     ===================================================================== -->
<script>
window.GALLERY_CONFIG = {
  modelUrl: 'gallery.glb',
  binId: '6ac6a8dbffd5d16053572822',          // bin jsonbin (positions des tableaux)
  contactEmail: 'zonedel81@gmail.com',
  // EmailJS : à remplir avec les 3 valeurs de ton compte emailjs.com (elles sont faites pour être publiques)
  emailjs: { service: 'VOTRE_SERVICE_ID', template: 'VOTRE_TEMPLATE_ID', publicKey: 'VOTRE_CLE_PUBLIQUE' },
  rotationStepDeg: 5,     // pas de rotation des tableaux (admin : J / L)
  eyeHeight: 1.25,        // hauteur des yeux
  exposure: 1.0,          // luminosité globale (monte à 1.2 si c'est trop sombre)
  toneMapping: 'linear',  // 'linear' = couleurs fidèles des tableaux | 'aces' = rendu plus cinéma
  darken: 0.55,           // assombrissement des matériaux du modèle
  bloom: 0.55             // intensité du halo lumineux (0 = désactivé) — PC uniquement
};

/* Démarre les téléchargements TOUT DE SUITE (en parallèle du chargement de three.js) */
(function () {
  var C = window.GALLERY_CONFIG, E = window.__early = {};
  E.glb = fetch(C.modelUrl).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r; });
  E.glb.catch(function () {});
  E.remote = fetch('https://api.jsonbin.io/v3/b/' + C.binId + '/latest')
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(function (d) { return (d && d.record && d.record.paintings) || []; })
    .catch(function () { return null; });
})();
</script>

<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
} }
</script>

<style>
  :root {
    --c1: #00e5ff; --c2: #8a5cff; --c3: #ff3df2; --bg: #04060c;
    --glass: rgba(10, 14, 26, .55); --line: rgba(255, 255, 255, .14);
    --display: 'Orbitron', 'Segoe UI', system-ui, sans-serif;
    --body: 'Rajdhani', 'Segoe UI', system-ui, sans-serif;
  }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html, body { margin: 0; height: 100%; background: var(--bg); overflow: hidden; font-family: var(--body); color: #fff; }
  #stage { position: fixed; inset: 0; touch-action: none; }
  #stage canvas { display: block; touch-action: none; }

  /* ---------- Écran d'accueil / pause ---------- */
  #intro {
    position: fixed; inset: 0; z-index: 1010; display: flex; align-items: center; justify-content: center;
    background: var(--bg); overflow: hidden; transition: background .9s ease, opacity .7s ease, visibility .7s;
  }
  #intro.ready { background: radial-gradient(ellipse at center, rgba(4,6,12,.35) 0%, rgba(4,6,12,.82) 100%); backdrop-filter: blur(7px); -webkit-backdrop-filter: blur(7px); }
  #intro.out { opacity: 0; visibility: hidden; pointer-events: none; }
  .grid { position: absolute; left: -50%; right: -50%; bottom: -8%; height: 70%;
    background-image: linear-gradient(rgba(0,229,255,.35) 1px, transparent 1px), linear-gradient(90deg, rgba(0,229,255,.35) 1px, transparent 1px);
    background-size: 64px 64px; transform: perspective(520px) rotateX(62deg); animation: gridmove 3s linear infinite;
    -webkit-mask-image: linear-gradient(to top, #000 10%, transparent 85%); mask-image: linear-gradient(to top, #000 10%, transparent 85%); opacity: .55; transition: opacity .9s; }
  #intro.ready .grid { opacity: .18; }
  @keyframes gridmove { to { background-position: 0 64px; } }
  .aurora { position: absolute; width: 60vmax; height: 60vmax; border-radius: 50%; filter: blur(90px); opacity: .45; animation: drift 14s ease-in-out infinite alternate; }
  .aurora.a1 { background: var(--c2); left: -15vmax; top: -20vmax; }
  .aurora.a2 { background: var(--c3); right: -20vmax; bottom: -25vmax; animation-delay: -6s; opacity: .30; }
  .aurora.a3 { background: var(--c1); right: 10vmax; top: -30vmax; opacity: .22; animation-delay: -3s; }
  @keyframes drift { to { transform: translate(8vmax, 6vmax) scale(1.15); } }
  .card { position: relative; text-align: center; padding: 28px; max-width: 640px; width: 100%; }
  .eyebrow { font-family: var(--display); font-size: 12px; letter-spacing: .5em; color: var(--c1); text-shadow: 0 0 14px rgba(0,229,255,.8); margin-bottom: 18px; }
  .title { font-family: var(--display); font-weight: 900; margin: 0; line-height: 1.05; font-size: clamp(30px, 7.2vw, 66px); letter-spacing: .06em;
    background: linear-gradient(100deg, #fff 0%, var(--c1) 35%, var(--c2) 65%, var(--c3) 100%); background-size: 200% auto;
    -webkit-background-clip: text; background-clip: text; color: transparent; animation: shine 6s linear infinite; filter: drop-shadow(0 0 22px rgba(138,92,255,.55)); }
  @keyframes shine { to { background-position: 200% center; } }
  .sub { margin: 14px 0 34px; font-size: 18px; letter-spacing: .28em; text-transform: uppercase; color: rgba(255,255,255,.7); font-weight: 500; }
  .loadbox { width: min(360px, 82%); margin: 0 auto 26px; transition: opacity .5s, height .5s, margin .5s; }
  .loadbox.done { opacity: 0; height: 0; margin: 0 auto; overflow: hidden; }
  .track { height: 4px; border-radius: 4px; background: rgba(255,255,255,.12); overflow: hidden; position: relative; }
  #barfill { height: 100%; width: 0; border-radius: 4px; background: linear-gradient(90deg, var(--c1), var(--c2), var(--c3)); box-shadow: 0 0 16px var(--c1); transition: width .25s ease-out; }
  .loadtxt { display: flex; justify-content: space-between; margin-top: 10px; font-size: 13px; letter-spacing: .22em; text-transform: uppercase; color: rgba(255,255,255,.6); }
  #enter { position: relative; font-family: var(--display); font-weight: 700; font-size: 15px; letter-spacing: .38em; color: #fff; cursor: pointer;
    padding: 18px 46px 18px 52px; border-radius: 999px; border: 1px solid rgba(0,229,255,.7); background: rgba(0,229,255,.08);
    box-shadow: 0 0 0 0 rgba(0,229,255,.6), inset 0 0 22px rgba(0,229,255,.18); opacity: 0; transform: translateY(8px); pointer-events: none; transition: opacity .6s .1s, transform .6s .1s, background .25s; }
  #enter.show { opacity: 1; transform: none; pointer-events: auto; animation: pulse 2.2s ease-out infinite; }
  #enter:hover { background: rgba(0,229,255,.22); }
  @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0,229,255,.55), inset 0 0 22px rgba(0,229,255,.18); } 100% { box-shadow: 0 0 0 26px rgba(0,229,255,0), inset 0 0 22px rgba(0,229,255,.18); } }
  .hints { margin-top: 34px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; font-size: 15px; color: rgba(255,255,255,.75); }
  .hints span { padding: 6px 12px; border-radius: 8px; background: var(--glass); border: 1px solid var(--line); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
  .hints b { color: var(--c1); font-weight: 600; }

  /* ---------- HUD ---------- */
  #crosshair { position: fixed; top: 50%; left: 50%; width: 16px; height: 16px; margin: -8px 0 0 -8px; border-radius: 50%;
    border: 1px solid rgba(255,255,255,.55); pointer-events: none; z-index: 1005; display: none; transition: transform .2s, border-color .2s, box-shadow .2s; }
  #crosshair::after { content: ''; position: absolute; left: 50%; top: 50%; width: 3px; height: 3px; margin: -1.5px; border-radius: 50%; background: #fff; }
  #crosshair.hot { transform: scale(2); border-color: var(--c1); box-shadow: 0 0 16px var(--c1); }
  #tag { position: fixed; left: 50%; bottom: 9vh; transform: translate(-50%, 10px); z-index: 1005; opacity: 0; pointer-events: none;
    padding: 12px 22px; border-radius: 999px; background: var(--glass); border: 1px solid rgba(0,229,255,.5); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    font-size: 16px; letter-spacing: .18em; text-transform: uppercase; box-shadow: 0 0 24px rgba(0,229,255,.25); transition: opacity .25s, transform .25s; }
  #tag.show { opacity: 1; transform: translate(-50%, 0); }
  #tag b { color: var(--c1); }
  #paint-hud { position: fixed; bottom: 14px; left: 14px; z-index: 1005; pointer-events: none; user-select: none; display: none;
    background: var(--glass); border: 1px solid var(--line); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); padding: 10px 14px; border-radius: 10px; font-size: 14px; line-height: 1.55; }
  .glassbtn { position: fixed; z-index: 1050; cursor: pointer; color: #fff; font-family: var(--display); font-size: 13px; letter-spacing: .2em; text-transform: uppercase;
    background: var(--glass); border: 1px solid var(--line); border-radius: 12px; padding: 14px 20px; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); transition: border-color .2s, box-shadow .2s; }
  .glassbtn:hover { border-color: var(--c1); box-shadow: 0 0 18px rgba(0,229,255,.35); }
  #contact-btn { top: max(16px, env(safe-area-inset-top)); right: 16px; }

  /* ---------- Croix tactile ---------- */
  #dpad { position: fixed; bottom: max(22px, env(safe-area-inset-bottom)); left: 22px; z-index: 1040; display: none;
    grid-template-columns: repeat(3, 76px); grid-template-rows: repeat(3, 76px); gap: 6px; }
  #dpad button { width: 76px; height: 76px; border-radius: 16px; padding: 0; color: #fff; font-size: 28px; display: flex; align-items: center; justify-content: center;
    background: rgba(10,14,26,.5); border: 1px solid rgba(255,255,255,.35); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); touch-action: none; user-select: none; -webkit-user-select: none; }
  #dpad button.active { background: rgba(0,229,255,.35); border-color: var(--c1); box-shadow: 0 0 18px rgba(0,229,255,.6); }
  #dp-up { grid-column: 2; grid-row: 1; } #dp-left { grid-column: 1; grid-row: 2; } #dp-right { grid-column: 3; grid-row: 2; } #dp-down { grid-column: 2; grid-row: 3; }

  /* ---------- Visionneuse plein écran ---------- */
  #viewer { position: fixed; inset: 0; z-index: 3000; display: none; align-items: center; justify-content: center; background: rgba(2,3,8,.92); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); opacity: 0; transition: opacity .35s; }
  #viewer.show { opacity: 1; }
  #v-img { max-width: 92vw; max-height: 82vh; border-radius: 4px; box-shadow: 0 0 0 1px rgba(255,255,255,.12), 0 0 60px rgba(138,92,255,.35), 0 30px 80px rgba(0,0,0,.7); transition: filter .5s; }
  #v-img.blur { filter: blur(10px); }
  #v-bar { position: absolute; left: 0; right: 0; bottom: max(18px, env(safe-area-inset-bottom)); display: flex; justify-content: center; align-items: center; gap: 14px; font-family: var(--display); font-size: 12px; letter-spacing: .25em; }
  #v-bar button { font: inherit; color: #fff; cursor: pointer; padding: 11px 18px; border-radius: 10px; background: var(--glass); border: 1px solid var(--line); }
  #v-bar button:hover { border-color: var(--c1); }
  #v-count { color: rgba(255,255,255,.65); min-width: 80px; text-align: center; }

  /* ---------- Contact ---------- */
  #contact-modal { position: fixed; inset: 0; z-index: 2000; background: rgba(2,3,8,.75); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); display: none; align-items: center; justify-content: center; }
  #contact-box { width: 90%; max-width: 400px; padding: 26px; border-radius: 16px; background: rgba(14,18,32,.85); border: 1px solid var(--line); box-shadow: 0 0 60px rgba(138,92,255,.3); font-family: var(--body); }
  #contact-box h2 { margin: 0 0 16px; font-family: var(--display); font-size: 17px; letter-spacing: .18em; text-transform: uppercase; }
  #contact-box input, #contact-box textarea { width: 100%; margin-bottom: 10px; padding: 11px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,.2); background: rgba(255,255,255,.06); color: #fff; font: 500 16px var(--body); }
  #contact-box input:focus, #contact-box textarea:focus { outline: none; border-color: var(--c1); box-shadow: 0 0 12px rgba(0,229,255,.3); }
  #contact-box textarea { min-height: 96px; resize: vertical; }
  .c-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 6px; }
  .c-actions button { padding: 10px 16px; border-radius: 8px; border: none; cursor: pointer; font: 600 15px var(--body); letter-spacing: .06em; }
  #c-cancel { background: rgba(255,255,255,.14); color: #fff; }
  #c-send { background: linear-gradient(90deg, var(--c1), var(--c2)); color: #05060c; }
  #c-send:disabled { opacity: .6; cursor: default; }
  #c-error { color: #ff8686; font-size: 14px; margin: -4px 0 10px; display: none; }
  #c-status { font-size: 14px; margin: -4px 0 10px; display: none; }
</style>
</head>
<body>

<div id="stage"></div>

<div id="intro">
  <div class="grid"></div><div class="aurora a1"></div><div class="aurora a2"></div><div class="aurora a3"></div>
  <div class="card">
    <div class="eyebrow">GALERIE VIRTUELLE</div>
    <h1 class="title">ATELIER<br>DE LA RUE</h1>
    <div class="sub" id="mode-title"><span id="count"></span> œuvres</div>
    <div class="loadbox" id="loadbox">
      <div class="track"><div id="barfill"></div></div>
      <div class="loadtxt"><span id="load-label">Initialisation</span><span id="load-pct">0%</span></div>
    </div>
    <button id="enter">ENTRER</button>
    <div class="hints" id="hints"></div>
  </div>
</div>

<div id="crosshair"></div>
<div id="tag"><b>◈</b>&nbsp; Clic · voir l'œuvre en grand</div>
<div id="paint-hud"></div>
<div id="dpad">
  <button id="dp-up">▲</button><button id="dp-left">◀</button><button id="dp-right">▶</button><button id="dp-down">▼</button>
</div>

<button id="contact-btn" class="glassbtn">✉ Contact</button>

<div id="viewer">
  <img id="v-img" alt="Tableau">
  <div id="v-bar"><button id="v-prev">◀</button><span id="v-count"></span><button id="v-next">▶</button><button id="v-close">FERMER ✕</button></div>
</div>

<div id="contact-modal">
  <div id="contact-box">
    <h2>Contactez-nous</h2>
    <input id="c-name" placeholder="Votre nom" />
    <input id="c-email" placeholder="Votre email" type="email" />
    <textarea id="c-message" placeholder="Votre message"></textarea>
    <div id="c-error">Merci de remplir tous les champs (email valide).</div>
    <div id="c-status"></div>
    <div class="c-actions"><button id="c-cancel">Annuler</button><button id="c-send">Envoyer</button></div>
  </div>
</div>

<!-- Liste des tableaux -->
<script type="application