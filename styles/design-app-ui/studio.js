// studio.js：整部作品共用一個時鐘（第 4 招）。
// 在 GSAP 之後、場景腳本之前載入。
// 場景呼叫 STUDIO.play(render)。render(t) 必須只憑 t 畫出整幀。
// 同一個 t 進，同一張畫面出。這樣渲染才精確、可跳轉、可循環。
(function () {
  // 放在 <head> 或 <body> 裡都行：根元素在第一次需要時才查詢
  const R = () => document.querySelector('[data-composition-id]');
  const num = (k) => +R().dataset[k];
  const cache = {};
  const S = {
    get root() { return R(); },
    get D() { return num('duration'); },
    get W() { return num('width'); },
    get H() { return num('height'); },
    get V() { return S.H > S.W; },               // 9:16 時為 true
    get u() { return Math.min(S.W, S.H) / 1080; }, // 短邊為 1080 時，1 單位 = 1 px
    ease(name) { return cache[name] || (cache[name] = name === 'none' ? (p) => p : gsap.parseEase(name)); },
    // 一個從 `start` 開始、持續 `dur` 的動作，經緩動後的 0..1 進度
    seg(t, start, dur, ease) {
      const p = Math.min(1, Math.max(0, (t - start) / dur));
      return S.ease(ease || 'power3.out')(p);
    },
    mix(a, b, p) { return a + (b - a) * p; },
    // 總能循環的波：週期數用整數
    wave(t, cycles, offset) { return Math.sin(2 * Math.PI * ((cycles || 1) * t / S.D + (offset || 0))); },
    // 帶種子的隨機數（渲染裡絕不用 Math.random）
    rng(seed) {
      let a = seed >>> 0;
      return function () {
        a = (a + 0x6d2b79f5) | 0;
        let t = Math.imul(a ^ (a >>> 15), 1 | a);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
    },
    // 一個時鐘驅動一切；loop:true 會讓 t 迴繞，所以 t = D 畫出的幀和 t = 0 相同
    play(render, opts) {
      const loop = !opts || opts.loop !== false;
      const D = S.D, root = S.root;
      const clock = { t: 0 };
      const tl = gsap.timeline({ paused: true });
      // loop_check.py 會設定 STUDIO_NO_WRAP，以證明 render(結尾) 真的等於 render(0)
      const wrap = loop && !window.STUDIO_NO_WRAP;
      const draw = () => render(wrap ? clock.t % D : clock.t);
      tl.to(clock, { t: D, duration: D, ease: 'none', onUpdate: draw }, 0);
      draw();
      // 字型可能在第一次繪製之後才到；再畫一次，讓依賴字型測量的文字也正確，
      // 第 0 幀也一樣（跳到當前所在的時間點不會觸發重繪）
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
      window.addEventListener('load', draw);
      window.__timelines = window.__timelines || {};
      window.__timelines[root.dataset.compositionId] = tl;
      return tl;
    },
  };
  window.STUDIO = S;
})();
