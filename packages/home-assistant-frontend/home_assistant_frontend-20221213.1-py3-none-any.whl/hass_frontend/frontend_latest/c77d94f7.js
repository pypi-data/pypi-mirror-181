"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[55934],{44583:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{o0:()=>o,yD:()=>l,E8:()=>d});var i=r(14516),n=r(54121),a=r(65810);n.Xp&&await n.Xp;const o=(e,t)=>s(t).format(e),s=(0,i.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,a.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"long",day:"numeric",hour:(0,a.y)(e)?"numeric":"2-digit",minute:"2-digit",hour12:(0,a.y)(e)}))),l=(e,t)=>c(t).format(e),c=(0,i.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,a.y)(e)?e.language:"en-u-hc-h23",{month:"short",day:"numeric",hour:(0,a.y)(e)?"numeric":"2-digit",minute:"2-digit",hour12:(0,a.y)(e)}))),d=(e,t)=>h(t).format(e),h=(0,i.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,a.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"long",day:"numeric",hour:(0,a.y)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,a.y)(e)})));(0,i.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,a.y)(e)?e.language:"en-u-hc-h23",{year:"numeric",month:"numeric",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,a.y)(e)})));e()}),1)},49684:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{mr:()=>o,Vu:()=>l,xO:()=>d,Zs:()=>u});var i=r(14516),n=r(54121),a=r(65810);n.Xp&&await n.Xp;const o=(e,t)=>s(t).format(e),s=(0,i.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,a.y)(e)?e.language:"en-u-hc-h23",{hour:"numeric",minute:"2-digit",hour12:(0,a.y)(e)}))),l=(e,t)=>c(t).format(e),c=(0,i.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,a.y)(e)?e.language:"en-u-hc-h23",{hour:(0,a.y)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hour12:(0,a.y)(e)}))),d=(e,t)=>h(t).format(e),h=(0,i.Z)((e=>new Intl.DateTimeFormat("en"!==e.language||(0,a.y)(e)?e.language:"en-u-hc-h23",{weekday:"long",hour:(0,a.y)(e)?"numeric":"2-digit",minute:"2-digit",hour12:(0,a.y)(e)}))),u=e=>f().format(e),f=(0,i.Z)((()=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1})));e()}),1)},92115:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{$:()=>l});var i=r(79021),n=r(59401),a=r(14516),o=r(12198),s=e([o]);o=(s.then?await s:s)[0];const l=(0,a.Z)((e=>Array.from({length:7},((t,r)=>(0,o.D_)((0,i.Z)((0,n.Z)(new Date),r),e)))))}))},62822:(e,t,r)=>{r.a(e,(async e=>{r.d(t,{l:()=>l});var i=r(32182),n=r(69388),a=r(14516),o=r(12198),s=e([o]);o=(s.then?await s:s)[0];const l=(0,a.Z)((e=>Array.from({length:12},((t,r)=>(0,o.Nh)((0,i.Z)((0,n.Z)(new Date),r),e)))))}))},65992:(e,t,r)=>{r.a(e,(async e=>{r(54444);var t=r(37500),i=r(33310),n=r(91741),a=r(87744),o=r(42952),s=(r(3143),e([o]));function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var a="static"===n?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function y(){return y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,t,r){var i=v(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(arguments.length<3?e:r):n.value}},y.apply(this,arguments)}function v(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}function g(e){return g=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},g(e)}o=(s.then?await s:s)[0];!function(e,t,r,i){var n=l();if(i)for(var a=0;a<i.length;a++)n=i[a](n);var o=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var n,a=e[i];if("method"===a.kind&&(n=t.find(r)))if(u(a.descriptor)||u(n.descriptor)){if(h(a)||h(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(h(a)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}d(a,n)}else t.push(a)}return t}(o.d.map(c)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([(0,i.Mo)("state-info")],(function(e,r){class o extends r{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"inDialog",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"rtl",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.hass||!this.stateObj)return t.dy``;const e=(0,n.C)(this.stateObj);return t.dy`<state-badge
        .stateObj=${this.stateObj}
        .stateColor=${!0}
      ></state-badge>
      <div class="info">
        <div class="name" .title=${e} .inDialog=${this.inDialog}>
          ${e}
        </div>
        ${this.inDialog?t.dy`<div class="time-ago">
              <ha-relative-time
                id="last_changed"
                .hass=${this.hass}
                .datetime=${this.stateObj.last_changed}
                capitalize
              ></ha-relative-time>
              <paper-tooltip animation-delay="0" for="last_changed">
                <div>
                  <div class="row">
                    <span class="column-name">
                      ${this.hass.localize("ui.dialogs.more_info_control.last_changed")}:
                    </span>
                    <ha-relative-time
                      .hass=${this.hass}
                      .datetime=${this.stateObj.last_changed}
                      capitalize
                    ></ha-relative-time>
                  </div>
                  <div class="row">
                    <span>
                      ${this.hass.localize("ui.dialogs.more_info_control.last_updated")}:
                    </span>
                    <ha-relative-time
                      .hass=${this.hass}
                      .datetime=${this.stateObj.last_updated}
                      capitalize
                    ></ha-relative-time>
                  </div>
                </div>
              </paper-tooltip>
            </div>`:t.dy`<div class="extra-info"><slot></slot></div>`}
      </div>`}},{kind:"method",key:"updated",value:function(e){if(y(g(o.prototype),"updated",this).call(this,e),!e.has("hass"))return;const t=e.get("hass");t&&t.locale===this.hass.locale||(this.rtl=(0,a.HE)(this.hass))}},{kind:"get",static:!0,key:"styles",value:function(){return t.iv`
      :host {
        min-width: 120px;
        white-space: nowrap;
      }

      state-badge {
        float: left;
      }
      :host([rtl]) state-badge {
        float: right;
      }

      .info {
        margin-left: 56px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
      }

      :host([rtl]) .info {
        margin-right: 56px;
        margin-left: 0;
        text-align: right;
      }

      .name {
        color: var(--primary-text-color);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .name[in-dialog],
      :host([secondary-line]) .name {
        line-height: 20px;
      }

      .time-ago,
      .extra-info,
      .extra-info > * {
        color: var(--secondary-text-color);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .row {
        display: flex;
        flex-direction: row;
        flex-wrap: no-wrap;
        width: 100%;
        justify-content: space-between;
        margin: 0 2px 4px 0;
      }

      .row:last-child {
        margin-bottom: 0px;
      }
    `}}]}}),t.oi)}))},55934:(e,t,r)=>{r.a(e,(async e=>{r.r(t);r(51187);var i=r(79021),n=r(30443),a=r(37500),o=r(33310),s=r(70278),l=r(12198),c=r(44583),d=r(49684),h=r(47181),u=r(21780),f=r(99137),p=r(92115),m=r(62822),y=r(65992),v=r(94653),g=(r(85066),r(51144)),w=r(11654),b=r(91476),k=r(29152),E=r(89207),_=r(28940),D=e([c,l,d,m,p,k,b,v,y]);function x(){x=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var a="static"===n?e:r;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!P(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var a=this.decorateConstructor(r,t);return i.push.apply(i,a.finishers),a.finishers=i,a},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==a.finisher&&r.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return O(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?O(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=z(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:T(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=T(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function C(e){var t,r=z(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function A(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function P(e){return e.decorators&&e.decorators.length}function $(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function T(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function z(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function O(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}[c,l,d,m,p,k,b,v,y]=D.then?await D:D;let S=function(e,t,r,i){var n=x();if(i)for(var a=0;a<i.length;a++)n=i[a](n);var o=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},i=0;i<e.length;i++){var n,a=e[i];if("method"===a.kind&&(n=t.find(r)))if($(a.descriptor)||$(n.descriptor)){if(P(a)||P(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(P(a)){if(P(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}A(a,n)}else t.push(a)}return t}(o.d.map(C)),e);return n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_calendarId",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_submitting",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_data",value:void 0},{kind:"method",key:"showDialog",value:async function(e){if(this._params=e,e.entry){const t=e.entry;this._data=t,this._calendarId=e.calendarId||e.calendars[0].entity_id}}},{kind:"method",key:"closeDialog",value:function(){this._calendarId=void 0,this._params=void 0,(0,h.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return a.dy``;const e=this.hass.states[this._calendarId];return a.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        .heading=${a.dy`
          <div class="header_title">${this._data.summary}</div>
          <ha-icon-button
            .label=${this.hass.localize("ui.dialogs.generic.close")}
            .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
            dialogAction="close"
            class="header_button"
          ></ha-icon-button>
        `}
      >
        <div class="content">
          ${this._error?a.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
          <div class="field">
            <ha-svg-icon .path=${"M15,13H16.5V15.82L18.94,17.23L18.19,18.53L15,16.69V13M19,8H5V19H9.67C9.24,18.09 9,17.07 9,16A7,7 0 0,1 16,9C17.07,9 18.09,9.24 19,9.67V8M5,21C3.89,21 3,20.1 3,19V5C3,3.89 3.89,3 5,3H6V1H8V3H16V1H18V3H19A2,2 0 0,1 21,5V11.1C22.24,12.36 23,14.09 23,16A7,7 0 0,1 16,23C14.09,23 12.36,22.24 11.1,21H5M16,11.15A4.85,4.85 0 0,0 11.15,16C11.15,18.68 13.32,20.85 16,20.85A4.85,4.85 0 0,0 20.85,16C20.85,13.32 18.68,11.15 16,11.15Z"}></ha-svg-icon>
            <div class="value">
              ${this._formatDateRange()}<br />
              ${this._data.rrule?this._renderRRuleAsText(this._data.rrule):""}
              ${this._data.description?a.dy`<br />
                    <div class="description">${this._data.description}</div>
                    <br />`:a.dy``}
            </div>
          </div>

          <div class="attribute">
            <state-info
              .hass=${this.hass}
              .stateObj=${e}
              inDialog
            ></state-info>
          </div>
        </div>
        ${this._params.canDelete?a.dy`
              <mwc-button
                slot="secondaryAction"
                class="warning"
                @click=${this._deleteEvent}
                .disabled=${this._submitting}
              >
                ${this.hass.localize("ui.components.calendar.event.delete")}
              </mwc-button>
            `:""}
        ${this._params.canEdit?a.dy`<mwc-button
              slot="primaryAction"
              @click=${this._editEvent}
              .disabled=${this._submitting}
            >
              ${this.hass.localize("ui.components.calendar.event.edit")}
            </mwc-button>`:""}
      </ha-dialog>
    `}},{kind:"method",key:"_renderRRuleAsText",value:function(e){if(!e)return"";try{const t=s.Ci.fromString(`RRULE:${e}`);return t.isFullyConvertibleToText()?a.dy`<div id="text">
          ${(0,u.f)(t.toText(this._translateRRuleElement,{dayNames:(0,p.$)(this.hass.locale),monthNames:(0,m.l)(this.hass.locale),tokens:{}},this._formatDate))}
        </div>`:a.dy`<div id="text">Cannot convert recurrence rule</div>`}catch(e){return"Error while processing the rule"}}},{kind:"field",key:"_translateRRuleElement",value(){return e=>"string"==typeof e?this.hass.localize(`ui.components.calendar.event.rrule.${e}`):""}},{kind:"field",key:"_formatDate",value(){return(e,t,r)=>{if(!e||!t||!r)return"";const i=new Date;return i.setFullYear(e),i.setMonth((0,m.l)(this.hass.locale).indexOf(t)),i.setDate(r),(0,l.p6)(i,this.hass.locale)}}},{kind:"method",key:"_formatDateRange",value:function(){const e=new Date(this._data.dtstart),t=(0,f.J)(this._data.dtend)?(0,i.Z)(new Date(this._data.dtend),-1):new Date(this._data.dtend);return(0,n.Z)(e,t)?(0,f.J)(this._data.dtstart)?(0,l.p6)(e,this.hass.locale):`${(0,l.p6)(e,this.hass.locale)} ${(0,d.mr)(e,this.hass.locale)} - ${(0,d.mr)(t,this.hass.locale)}`:`${(0,f.J)(this._data.dtstart)?(0,l.p6)(e,this.hass.locale):(0,c.o0)(e,this.hass.locale)} - ${(0,f.J)(this._data.dtend)?(0,l.p6)(t,this.hass.locale):(0,c.o0)(t,this.hass.locale)}`}},{kind:"method",key:"_editEvent",value:async function(){(0,_.R)(this,this._params),this.closeDialog()}},{kind:"method",key:"_deleteEvent",value:async function(){this._submitting=!0;const e=this._params.entry,t=await(0,E.Y)(this,{title:this.hass.localize("ui.components.calendar.event.confirm_delete.delete"),text:e.recurrence_id?this.hass.localize("ui.components.calendar.event.confirm_delete.recurring_prompt"):this.hass.localize("ui.components.calendar.event.confirm_delete.prompt"),confirmText:e.recurrence_id?this.hass.localize("ui.components.calendar.event.confirm_delete.delete_this"):this.hass.localize("ui.components.calendar.event.confirm_delete.delete"),confirmFutureText:e.recurrence_id?this.hass.localize("ui.components.calendar.event.confirm_delete.delete_future"):void 0});if(void 0!==t){try{await(0,g.d1)(this.hass,this._calendarId,e.uid,e.recurrence_id||"",t)}catch(e){return void(this._error=e?e.message:"Unknown error")}finally{this._submitting=!1}await this._params.updated(),this.closeDialog()}else this._submitting=!1}},{kind:"get",static:!0,key:"styles",value:function(){return[w.yu,a.iv`
        state-info {
          line-height: 40px;
        }
        ha-svg-icon {
          width: 40px;
          margin-right: 8px;
          margin-inline-end: 16px;
          margin-inline-start: initial;
          direction: var(--direction);
          vertical-align: top;
        }
        .field {
          display: flex;
        }
        .description {
          color: var(--secondary-text-color);
          max-width: 300px;
          overflow-wrap: break-word;
        }
      `]}}]}}),a.oi);customElements.define("dialog-calendar-event-detail",S)}))}}]);
//# sourceMappingURL=c77d94f7.js.map