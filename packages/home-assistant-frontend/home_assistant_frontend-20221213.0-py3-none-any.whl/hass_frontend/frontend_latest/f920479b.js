"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[28279],{54531:(e,t,i)=>{i.d(t,{zJ:()=>s,Xr:()=>l,Qc:()=>c});const r=["zone","persistent_notification"],n=(e,t)=>{var i,r,n,o,a,s,l,c;if(!("call-service"===t.action&&(null!==(i=t.target)&&void 0!==i&&i.entity_id||null!==(r=t.service_data)&&void 0!==r&&r.entity_id||null!==(n=t.data)&&void 0!==n&&n.entity_id)))return;let d=null!==(o=null!==(a=null===(s=t.service_data)||void 0===s?void 0:s.entity_id)&&void 0!==a?a:null===(l=t.data)||void 0===l?void 0:l.entity_id)&&void 0!==o?o:null===(c=t.target)||void 0===c?void 0:c.entity_id;Array.isArray(d)||(d=[d]);for(const t of d)e.add(t)},o=(e,t)=>{"string"!=typeof t?(t.entity&&e.add(t.entity),t.camera_image&&e.add(t.camera_image),t.tap_action&&n(e,t.tap_action),t.hold_action&&n(e,t.hold_action)):e.add(t)},a=(e,t)=>{t.entity&&o(e,t.entity),t.entities&&Array.isArray(t.entities)&&t.entities.forEach((t=>o(e,t))),t.card&&a(e,t.card),t.cards&&Array.isArray(t.cards)&&t.cards.forEach((t=>a(e,t))),t.elements&&Array.isArray(t.elements)&&t.elements.forEach((t=>a(e,t))),t.badges&&Array.isArray(t.badges)&&t.badges.forEach((t=>o(e,t)))},s=e=>{const t=new Set;return e.views.forEach((e=>a(t,e))),t},l=(e,t)=>{const i=new Set;for(const n of Object.keys(e.states))t.has(n)||r.includes(n.split(".",1)[0])||i.add(n);return i},c=(e,t)=>{const i=s(t);return l(e,i)}},4398:(e,t,i)=>{i.d(t,{i:()=>n});var r=i(47181);const n=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"hui-dialog-select-view",dialogImport:()=>Promise.all([i.e(29563),i.e(88278),i.e(85084),i.e(45507),i.e(66138)]).then(i.bind(i,66138)),dialogParams:t})}},28279:(e,t,i)=>{i.a(e,(async e=>{i.r(t),i.d(t,{HuiUnusedEntities:()=>A});var r=i(37500),n=i(33310),o=i(8636),a=i(58831),s=i(91741),l=i(87744),c=(i(36125),i(52039),i(54531)),d=i(59110),f=i(47512),h=i(4398),u=e([d]);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!y(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=k(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:b(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=b(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function v(e){var t,i=k(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function y(e){return e.decorators&&e.decorators.length}function g(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function b(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function k(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function E(){return E="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,t,i){var r=_(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(arguments.length<3?e:i):n.value}},E.apply(this,arguments)}function _(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=C(e)););return e}function C(e){return C=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},C(e)}d=(u.then?await u:u)[0];let A=function(e,t,i,r){var n=p();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(g(o.descriptor)||g(n.descriptor)){if(y(o)||y(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(y(o)){if(y(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}m(o,n)}else t.push(o)}return t}(a.d.map(v)),e);return n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("hui-unused-entities")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_unusedEntities",value:()=>[]},{kind:"field",decorators:[(0,n.SB)()],key:"_selectedEntities",value:()=>[]},{kind:"get",key:"_config",value:function(){return this.lovelace.config}},{kind:"method",key:"updated",value:function(e){E(C(i.prototype),"updated",this).call(this,e),e.has("lovelace")&&this._getUnusedEntities()}},{kind:"method",key:"render",value:function(){return this.hass&&this.lovelace?"storage"===this.lovelace.mode&&!1===this.lovelace.editMode?r.dy``:r.dy`
      <div class="container">
        ${this.narrow?"":r.dy`
              <ha-card
                header=${this.hass.localize("ui.panel.lovelace.unused_entities.title")}
              >
                <div class="card-content">
                  ${this.hass.localize("ui.panel.lovelace.unused_entities.available_entities")}
                  ${"storage"===this.lovelace.mode?r.dy`
                        <br />${this.hass.localize("ui.panel.lovelace.unused_entities.select_to_add")}
                      `:""}
                </div>
              </ha-card>
            `}
        <hui-entity-picker-table
          .hass=${this.hass}
          .narrow=${this.narrow}
          .entities=${this._unusedEntities.map((e=>{const t=this.hass.states[e];return{icon:"",entity_id:e,stateObj:t,name:t?(0,s.C)(t):"Unavailable",domain:(0,a.M)(e),last_changed:null==t?void 0:t.last_changed}}))}
          @selected-changed=${this._handleSelectedChanged}
        ></hui-entity-picker-table>
      </div>
      <div
        class="fab ${(0,o.$)({rtl:(0,l.HE)(this.hass),selected:this._selectedEntities.length})}"
      >
        <ha-fab
          .label=${this.hass.localize("ui.panel.lovelace.editor.edit_card.add")}
          extended
          @click=${this._addToLovelaceView}
        >
          <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </div>
    `:r.dy``}},{kind:"method",key:"_getUnusedEntities",value:function(){if(!this.hass||!this.lovelace)return;this._selectedEntities=[];const e=(0,c.Qc)(this.hass,this._config);this._unusedEntities=[...e].sort()}},{kind:"method",key:"_handleSelectedChanged",value:function(e){this._selectedEntities=e.detail.selectedEntities}},{kind:"method",key:"_addToLovelaceView",value:function(){1!==this.lovelace.config.views.length?(0,h.i)(this,{lovelaceConfig:this.lovelace.config,allowDashboardChange:!1,viewSelectedCallback:(e,t,i)=>{(0,f.f)(this,{lovelaceConfig:this.lovelace.config,saveConfig:this.lovelace.saveConfig,path:[i],entities:this._selectedEntities})}}):(0,f.f)(this,{lovelaceConfig:this.lovelace.config,saveConfig:this.lovelace.saveConfig,path:[0],entities:this._selectedEntities})}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        background: var(--lovelace-background);
        overflow: hidden;
      }
      .container {
        display: flex;
        flex-direction: column;
        height: 100%;
      }
      ha-card {
        --ha-card-box-shadow: none;
        --ha-card-border-radius: 0;
      }
      hui-entity-picker-table {
        flex-grow: 1;
      }
      .fab {
        position: sticky;
        float: right;
        right: calc(16px + env(safe-area-inset-right));
        bottom: calc(16px + env(safe-area-inset-bottom));
        z-index: 1;
      }
      .fab.rtl {
        right: initial;
        left: 0;
        bottom: 0;
        padding-right: 16px;
        padding-left: calc(16px + env(safe-area-inset-left));
      }
      ha-fab {
        position: relative;
        bottom: calc(-80px - env(safe-area-inset-bottom));
        transition: bottom 0.3s;
      }
      .fab.selected ha-fab {
        bottom: 0;
      }
    `}}]}}),r.oi)}))}}]);
//# sourceMappingURL=f920479b.js.map