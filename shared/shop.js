/* RELICTUM — магазинный слой (корзина + избранное + кабинет).
   Статический фронтенд-прототип на localStorage. Требует shared/catalog.js.
   Подключать ПОСЛЕ catalog.js. Сам встраивает бейджи корзины/избранного/кабинета в .nav-actions. */
(function(){
  var CART_KEY='relictum_cart', FAV_KEY='relictum_favs', USER_KEY='relictum_user';

  function read(k){ try{return JSON.parse(localStorage.getItem(k))||[]}catch(e){return []} }
  function write(k,v){ try{localStorage.setItem(k,JSON.stringify(v))}catch(e){} emit(); }
  function readObj(k){ try{return JSON.parse(localStorage.getItem(k))||null}catch(e){return null} }

  function catalog(){ return window.RELICTUM_CATALOG||[]; }
  function item(id){ return catalog().find(function(o){return o.id===id||o.slug===id})||null; }

  var Shop={
    getCart:function(){ return read(CART_KEY); },
    getFavs:function(){ return read(FAV_KEY); },
    inCart:function(id){ return this.getCart().indexOf(id)>=0; },
    inFav:function(id){ return this.getFavs().indexOf(id)>=0; },
    count:function(){ return this.getCart().length; },
    favCount:function(){ return this.getFavs().length; },
    item:item,
    cartItems:function(){ return this.getCart().map(item).filter(Boolean); },
    favItems:function(){ return this.getFavs().map(item).filter(Boolean); },
    addToCart:function(id){ var c=read(CART_KEY); if(c.indexOf(id)<0){c.push(id);write(CART_KEY,c);} },
    removeFromCart:function(id){ write(CART_KEY, read(CART_KEY).filter(function(x){return x!==id})); },
    clearCart:function(){ write(CART_KEY,[]); },
    toggleFav:function(id){ var f=read(FAV_KEY); var i=f.indexOf(id); if(i<0)f.push(id); else f.splice(i,1); write(FAV_KEY,f); return f.indexOf(id)>=0; },
    total:function(){ return this.cartItems().reduce(function(s,o){return s+(o.priceValue||0)},0); },
    hasRequestItems:function(){ return this.cartItems().some(function(o){return o.priceValue==null}); },
    /* пользователь (демо-кабинет) */
    user:function(){
      var u=readObj(USER_KEY);
      if(!u){
        u={ name:'Гость', email:'', phone:'', manager:'Ирина Вологдина', managerRole:'Персональный консультант дома',
            since:'2026', purchased:[], interests:[] };
        localStorage.setItem(USER_KEY,JSON.stringify(u));
      }
      return u;
    },
    saveUser:function(u){ localStorage.setItem(USER_KEY,JSON.stringify(u)); emit(); },
    /* оформленный заказ переносит товары в "коллекцию" */
    placeOrder:function(){
      var u=this.user(); var ids=this.getCart();
      u.purchased=(u.purchased||[]).concat(ids.filter(function(x){return u.purchased.indexOf(x)<0}));
      this.saveUser(u); this.clearCart();
      return ids;
    },
    /* ценовой статус/скидка по сумме коллекции */
    tier:function(){
      var spent=(this.user().purchased||[]).map(item).filter(Boolean).reduce(function(s,o){return s+(o.priceValue||0)},0);
      if(spent>=5000000) return {name:'Обсидиан',discount:12,spent:spent};
      if(spent>=2000000) return {name:'Бронза',discount:8,spent:spent};
      if(spent>=500000)  return {name:'Патрон',discount:5,spent:spent};
      return {name:'Гость дома',discount:0,spent:spent};
    },
    fmt:function(v){ return v==null?'Цена по запросу':(v.toLocaleString('ru-RU')+' ₽'); },
    /* экранирование пользовательского ввода перед вставкой в HTML/атрибуты (защита от self-XSS) */
    esc:function(s){ return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];}); }
  };
  window.RelictumShop=Shop;

  /* ---- бейджи в навигации ---- */
  function badge(href,label,icon,count){
    var extra=count>0?'<i class="rl-badge">'+count+'</i>':'';
    return '<a class="rl-navlink" href="'+href+'" aria-label="'+label+'">'+icon+extra+'</a>';
  }
  function paths(){
    // определяем префикс к 02_site_v1_gallery
    var p=location.pathname;
    if(p.indexOf('/02_site_v1_gallery/')>=0) return '';
    if(p.indexOf('/16_product_promos/')>=0) return '../02_site_v1_gallery/';
    return '02_site_v1_gallery/';
  }
  function render(){
    var pre=paths();
    var heart='<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 20s-7-4.35-9.5-8.5C1 8.5 2.5 5 6 5c2 0 3.2 1.2 4 2.3C10.8 6.2 12 5 14 5c3.5 0 5 3.5 3.5 6.5C19 15.65 12 20 12 20z"/></svg>';
    var bag='<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 8h12l-1 12H7L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>';
    var usr='<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="8" r="3.4"/><path d="M5 20c0-3.6 3-5.5 7-5.5s7 1.9 7 5.5"/></svg>';
    var html=
      badge(pre+'account.html#favorites','Избранное',heart,Shop.favCount())+
      badge(pre+'cart.html','Корзина',bag,Shop.count())+
      badge(pre+'account.html','Личный кабинет',usr,0);
    document.querySelectorAll('.nav-actions').forEach(function(na){
      var wrap=na.querySelector('.rl-shopnav');
      if(!wrap){ wrap=document.createElement('span'); wrap.className='rl-shopnav'; na.appendChild(wrap); }
      wrap.innerHTML=html;
    });
    // промо-страницы (.top бар)
    document.querySelectorAll('.top').forEach(function(t){
      if(t.querySelector('.rl-shopnav'))  t.querySelector('.rl-shopnav').innerHTML=html;
    });
  }
  function emit(){ try{render()}catch(e){} }

  /* стили бейджей + тост */
  var css='.rl-shopnav{display:inline-flex;gap:14px;align-items:center;margin-left:16px}'+
    '.rl-navlink{position:relative;color:inherit;display:inline-flex;opacity:.85;transition:opacity .3s}'+
    '.rl-navlink:hover{opacity:1}'+
    '.rl-badge{position:absolute;top:-7px;right:-9px;background:#B08A55;color:#0A0908;font-family:Inter,sans-serif;font-style:normal;font-size:9px;font-weight:600;min-width:15px;height:15px;line-height:15px;text-align:center;border-radius:8px;padding:0 3px}'+
    '.rl-toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);background:#14110E;color:#F4F0E8;padding:14px 24px;font-family:Inter,sans-serif;font-size:13px;letter-spacing:.04em;border:1px solid rgba(176,138,85,.4);opacity:0;transition:.4s cubic-bezier(.23,1,.32,1);z-index:9999;pointer-events:none}'+
    '.rl-toast.on{opacity:1;transform:translateX(-50%) translateY(0)}';
  var st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);

  var toastEl;
  Shop.toast=function(msg){
    if(!toastEl){ toastEl=document.createElement('div'); toastEl.className='rl-toast'; document.body.appendChild(toastEl); }
    toastEl.textContent=msg; toastEl.classList.add('on');
    clearTimeout(toastEl._t); toastEl._t=setTimeout(function(){toastEl.classList.remove('on')},2200);
  };

  if(document.readyState!=='loading') render();
  else document.addEventListener('DOMContentLoaded',render);
})();
