(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[28173],{20122:(e,a,i)=>{e.exports=i(52461)},22311:(e,a,i)=>{"use strict";i.d(a,{N:()=>r});var t=i(58831);const r=e=>(0,t.M)(e.entity_id)},51114:(e,a,i)=>{"use strict";i.r(a);i(51187);var t=i(37500),r=i(33310),n=i(14516),o=i(47181),s=i(85415);const c=["AED","AFN","ALL","AMD","ANG","AOA","ARS","AUD","AWG","AZN","BAM","BBD","BDT","BGN","BHD","BIF","BMD","BND","BOB","BRL","BSD","BTN","BWP","BYN","BYR","BZD","CAD","CDF","CHF","CLP","CNY","COP","CRC","CUP","CVE","CZK","DJF","DKK","DOP","DZD","EGP","ERN","ETB","EUR","FJD","FKP","GBP","GEL","GHS","GIP","GMD","GNF","GTQ","GYD","HKD","HNL","HRK","HTG","HUF","IDR","ILS","INR","IQD","IRR","ISK","JMD","JOD","JPY","KES","KGS","KHR","KMF","KPW","KRW","KWD","KYD","KZT","LAK","LBP","LKR","LRD","LSL","LTL","LYD","MAD","MDL","MGA","MKD","MMK","MNT","MOP","MRO","MUR","MVR","MWK","MXN","MYR","MZN","NAD","NGN","NIO","NOK","NPR","NZD","OMR","PAB","PEN","PGK","PHP","PKR","PLN","PYG","QAR","RON","RSD","RUB","RWF","SAR","SBD","SCR","SDG","SEK","SGD","SHP","SLL","SOS","SRD","SSP","STD","SYP","SZL","THB","TJS","TMT","TND","TOP","TRY","TTD","TWD","TZS","UAH","UGX","USD","UYU","UZS","VEF","VND","VUV","WST","XAF","XCD","XOF","XPF","YER","ZAR","ZMK","ZWL"],l=(0,n.Z)((e=>{const a=Intl&&"DisplayNames"in Intl?new Intl.DisplayNames(e,{type:"currency",fallback:"code"}):void 0,i=c.map((e=>({value:e,label:a?a.of(e):e})));return i.sort(((e,a)=>(0,s.f)(e.label,a.label))),i}));i(48456);var u=i(20122);const d={$:"USD","€":"EUR","¥":"JPY","£":"GBP","₽":"RUB","₹":"INR"};var m=i(76307),h=(i(33220),i(83927),i(3555),i(69906));const M=["AD","AE","AF","AG","AI","AL","AM","AO","AQ","AR","AS","AT","AU","AW","AX","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN","BO","BQ","BR","BS","BT","BV","BW","BY","BZ","CA","CC","CD","CF","CG","CH","CI","CK","CL","CM","CN","CO","CR","CU","CV","CW","CX","CY","CZ","DE","DJ","DK","DM","DO","DZ","EC","EE","EG","EH","ER","ES","ET","FI","FJ","FK","FM","FO","FR","GA","GB","GD","GE","GF","GG","GH","GI","GL","GM","GN","GP","GQ","GR","GS","GT","GU","GW","GY","HK","HM","HN","HR","HT","HU","ID","IE","IL","IM","IN","IO","IQ","IR","IS","IT","JE","JM","JO","JP","KE","KG","KH","KI","KM","KN","KP","KR","KW","KY","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MF","MG","MH","MK","ML","MM","MN","MO","MP","MQ","MR","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NC","NE","NF","NG","NI","NL","NO","NP","NR","NU","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PM","PN","PR","PS","PT","PW","PY","QA","RE","RO","RS","RU","RW","SA","SB","SC","SD","SE","SG","SH","SI","SJ","SK","SL","SM","SN","SO","SR","SS","ST","SV","SX","SY","SZ","TC","TD","TF","TG","TH","TJ","TK","TL","TM","TN","TO","TR","TT","TV","TW","TZ","UA","UG","UM","US","UY","UZ","VA","VC","VE","VG","VI","VN","VU","WF","WS","YE","YT","ZA","ZM","ZW"],f=(0,n.Z)((e=>{const a=Intl&&"DisplayNames"in Intl?new Intl.DisplayNames(e,{type:"region",fallback:"code"}):void 0,i=M.map((e=>({value:e,label:a?a.of(e):e})));return i.sort(((e,a)=>(0,s.f)(e.label,a.label))),i}));function T(){T=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,a){["method","field"].forEach((function(i){a.forEach((function(a){a.kind===i&&"own"===a.placement&&this.defineClassElement(e,a)}),this)}),this)},initializeClassElements:function(e,a){var i=e.prototype;["method","field"].forEach((function(t){a.forEach((function(a){var r=a.placement;if(a.kind===t&&("static"===r||"prototype"===r)){var n="static"===r?e:i;this.defineClassElement(n,a)}}),this)}),this)},defineClassElement:function(e,a){var i=a.descriptor;if("field"===a.kind){var t=a.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===t?void 0:t.call(e)}}Object.defineProperty(e,a.key,i)},decorateClass:function(e,a){var i=[],t=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!A(e))return i.push(e);var a=this.decorateElement(e,r);i.push(a.element),i.push.apply(i,a.extras),t.push.apply(t,a.finishers)}),this),!a)return{elements:i,finishers:t};var n=this.decorateConstructor(i,a);return t.push.apply(t,n.finishers),n.finishers=t,n},addElementPlacement:function(e,a,i){var t=a[e.placement];if(!i&&-1!==t.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");t.push(e.key)},decorateElement:function(e,a){for(var i=[],t=[],r=e.decorators,n=r.length-1;n>=0;n--){var o=a[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,r[n])(s)||s);e=c.element,this.addElementPlacement(e,a),c.finisher&&t.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],a);i.push.apply(i,l)}}return{element:e,finishers:t,extras:i}},decorateConstructor:function(e,a){for(var i=[],t=a.length-1;t>=0;t--){var r=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,a[t])(r)||r);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var a={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(a,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(a.initializer=e.initializer),a},toElementDescriptors:function(e){var a;if(void 0!==e)return(a=e,function(e){if(Array.isArray(e))return e}(a)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(a)||function(e,a){if(e){if("string"==typeof e)return k(e,a);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?k(e,a):void 0}}(a)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var a=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),a}),this)},toElementDescriptor:function(e){var a=String(e.kind);if("method"!==a&&"field"!==a)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+a+'"');var i=v(e.key),t=String(e.placement);if("static"!==t&&"prototype"!==t&&"own"!==t)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+t+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:a,key:i,placement:t,descriptor:Object.assign({},r)};return"field"!==a?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var a={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(a,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),a},toClassDescriptor:function(e){var a=String(e.kind);if("class"!==a)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+a+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,a){for(var i=0;i<a.length;i++){var t=(0,a[i])(e);if(void 0!==t){if("function"!=typeof t)throw new TypeError("Finishers must return a constructor.");e=t}}return e},disallowProperty:function(e,a,i){if(void 0!==e[a])throw new TypeError(i+" can't have a ."+a+" property.")}};return e}function p(e){var a,i=v(e.key);"method"===e.kind?a={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?a={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?a={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(a={configurable:!0,writable:!0,enumerable:!0});var t={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:a};return e.decorators&&(t.decorators=e.decorators),"field"===e.kind&&(t.initializer=e.value),t}function G(e,a){void 0!==e.descriptor.get?a.descriptor.get=e.descriptor.get:a.descriptor.set=e.descriptor.set}function A(e){return e.decorators&&e.decorators.length}function g(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,a){var i=e[a];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+a+"' to be a function");return i}function v(e){var a=function(e,a){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var t=i.call(e,a||"default");if("object"!=typeof t)return t;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===a?String:Number)(e)}(e,"string");return"symbol"==typeof a?a:String(a)}function k(e,a){(null==a||a>e.length)&&(a=e.length);for(var i=0,t=new Array(a);i<a;i++)t[i]=e[i];return t}function b(){return b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,a,i){var t=_(e,a);if(t){var r=Object.getOwnPropertyDescriptor(t,a);return r.get?r.get.call(arguments.length<3?e:i):r.value}},b.apply(this,arguments)}function _(e,a){for(;!Object.prototype.hasOwnProperty.call(e,a)&&null!==(e=E(e)););return e}function E(e){return E=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},E(e)}const P=[52.3731339,4.8903147],C=matchMedia("(prefers-color-scheme: dark)"),S="location";!function(e,a,i,t){var r=T();if(t)for(var n=0;n<t.length;n++)r=t[n](r);var o=a((function(e){r.initializeInstanceElements(e,s.elements)}),i),s=r.decorateClass(function(e){for(var a=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},t=0;t<e.length;t++){var r,n=e[t];if("method"===n.kind&&(r=a.find(i)))if(g(n.descriptor)||g(r.descriptor)){if(A(n)||A(r))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");r.descriptor=n.descriptor}else{if(A(n)){if(A(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");r.decorators=n.decorators}G(n,r)}else a.push(n)}return a}(o.d.map(p)),e);r.initializeClassElements(o.F,s.elements),r.runClassFinishers(o.F,s.finishers)}([(0,r.Mo)("onboarding-core-config")],(function(e,a){class i extends a{constructor(...a){super(...a),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"onboardingLocalize",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_working",value:()=>!1},{kind:"field",decorators:[(0,r.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_location",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_elevation",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_unitSystem",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_currency",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_timeZone",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_language",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_country",value:void 0},{kind:"field",decorators:[(0,r.IO)("ha-locations-editor",!0)],key:"map",value:void 0},{kind:"method",key:"render",value:function(){return t.dy`
      <p>
        ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.intro","name",this.hass.user.name)}
      </p>

      <ha-textfield
        .label=${this.onboardingLocalize("ui.panel.page-onboarding.core-config.location_name")}
        name="name"
        .disabled=${this._working}
        .value=${this._nameValue}
        @change=${this._handleChange}
      ></ha-textfield>

      <div class="middle-text">
        <p>
          ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.intro_location")}
        </p>

        <div class="row">
          <div>
            ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.intro_location_detect")}
          </div>
          <mwc-button @click=${this._detect}>
            ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.button_detect")}
          </mwc-button>
        </div>
      </div>

      <div class="row">
        <ha-locations-editor
          class="flex"
          .hass=${this.hass}
          .locations=${this._markerLocation(this._locationValue)}
          zoom="14"
          .darkMode=${C.matches}
          @location-updated=${this._locationChanged}
        ></ha-locations-editor>
      </div>

      <div class="row">
        <ha-textfield
          class="flex"
          .label=${this.hass.localize("ui.panel.config.core.section.core.core_config.country")}
          name="country"
          .disabled=${this._working}
          .value=${this._countryValue}
          @change=${this._handleChange}
        ></ha-textfield>

        <ha-textfield
          class="flex"
          .label=${this.hass.localize("ui.panel.config.core.section.core.core_config.language")}
          name="language"
          .disabled=${this._working}
          .value=${this._languageValue}
          @change=${this._handleChange}
        ></ha-textfield>
      </div>

      <div class="row">
        <ha-textfield
          class="flex"
          .label=${this.hass.localize("ui.panel.config.core.section.core.core_config.time_zone")}
          name="timeZone"
          .disabled=${this._working}
          .value=${this._timeZoneValue}
          @change=${this._handleChange}
        ></ha-textfield>

        <ha-textfield
          class="flex"
          .label=${this.hass.localize("ui.panel.config.core.section.core.core_config.elevation")}
          name="elevation"
          type="number"
          .disabled=${this._working}
          .value=${this._elevationValue}
          @change=${this._handleChange}
        >
          <span slot="suffix">
            ${this.hass.localize("ui.panel.config.core.section.core.core_config.elevation_meters")}
          </span>
        </ha-textfield>
      </div>

      <div class="row">
        <div class="flex">
          ${this.hass.localize("ui.panel.config.core.section.core.core_config.unit_system")}
        </div>
        <div class="radio-group">
          <ha-formfield
            .label=${t.dy`${this.hass.localize("ui.panel.config.core.section.core.core_config.unit_system_metric")}
              <div class="secondary">
                ${this.hass.localize("ui.panel.config.core.section.core.core_config.metric_example")}
              </div>`}
          >
            <ha-radio
              name="unit_system"
              value="metric"
              .checked=${"metric"===this._unitSystemValue}
              @change=${this._unitSystemChanged}
              .disabled=${this._working}
            ></ha-radio>
          </ha-formfield>
          <ha-formfield
            .label=${t.dy`${this.hass.localize("ui.panel.config.core.section.core.core_config.unit_system_us_customary")}
              <div class="secondary">
                ${this.hass.localize("ui.panel.config.core.section.core.core_config.us_customary_example")}
              </div>`}
          >
            <ha-radio
              name="unit_system"
              value="us_customary"
              .checked=${"us_customary"===this._unitSystemValue}
              @change=${this._unitSystemChanged}
              .disabled=${this._working}
            ></ha-radio>
          </ha-formfield>
        </div>
      </div>

      <div class="row">
            <div class="flex">
              ${this.hass.localize("ui.panel.config.core.section.core.core_config.currency")}<br />
              <a
                href="https://en.wikipedia.org/wiki/ISO_4217#Active_codes"
                target="_blank"
                rel="noopener noreferrer"
                >${this.hass.localize("ui.panel.config.core.section.core.core_config.find_currency_value")}</a
              >
            </div>

            <ha-textfield
              class="flex"
              .label=${this.hass.localize("ui.panel.config.core.section.core.core_config.currency")}
              name="currency"
              .disabled=${this._working}
              .value=${this._currencyValue}
              @change=${this._handleChange}
            ></ha-textfield>
          </div>
        </div>

      <div class="footer">
        <mwc-button @click=${this._save} .disabled=${this._working}>
          ${this.onboardingLocalize("ui.panel.page-onboarding.core-config.finish")}
        </mwc-button>
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(e){b(E(i.prototype),"firstUpdated",this).call(this,e),setTimeout((()=>this.shadowRoot.querySelector("ha-textfield").focus()),100),this.addEventListener("keypress",(e=>{13===e.keyCode&&this._save(e)}));const a=this.shadowRoot.querySelector("[name=timeZone]");a.updateComplete.then((()=>{a.shadowRoot.appendChild((()=>{const e=document.createElement("datalist");return e.id="timezones",Object.keys(u).forEach((a=>{const i=document.createElement("option");i.value=a,i.innerText=u[a],e.appendChild(i)})),e})()),a.formElement.setAttribute("list","timezones")}));const t=this.shadowRoot.querySelector("[name=currency]");t.updateComplete.then((()=>{t.shadowRoot.appendChild((()=>{const e=document.createElement("datalist");e.id="currencies";for(const a of l()){const i=document.createElement("option");i.value=a.value,i.innerText=a.label,e.appendChild(i)}return e})()),t.formElement.setAttribute("list","currencies")}));const r=this.shadowRoot.querySelector("[name=country]");r.updateComplete.then((()=>{r.shadowRoot.appendChild((()=>{const e=document.createElement("datalist");e.id="countries";const a=f();for(const i of a){const a=document.createElement("option");a.value=i.value,a.innerText=i.label,e.appendChild(a)}return e})()),r.formElement.setAttribute("list","countries")}));const n=this.shadowRoot.querySelector("[name=language]");n.updateComplete.then((()=>{n.shadowRoot.appendChild((e=>{const a=document.createElement("datalist");a.id="languages";for(const[i,t]of Object.entries(e.translationMetadata.translations)){const e=document.createElement("option");e.value=i,e.innerText=t.nativeName,a.appendChild(e)}return a})(this.hass)),n.formElement.setAttribute("list","languages")}))}},{kind:"get",key:"_nameValue",value:function(){return void 0!==this._name?this._name:this.onboardingLocalize("ui.panel.page-onboarding.core-config.location_name_default")}},{kind:"get",key:"_locationValue",value:function(){return this._location||P}},{kind:"get",key:"_elevationValue",value:function(){return void 0!==this._elevation?this._elevation:0}},{kind:"get",key:"_timeZoneValue",value:function(){return this._timeZone||""}},{kind:"get",key:"_languageValue",value:function(){return this._language||""}},{kind:"get",key:"_countryValue",value:function(){return this._country||""}},{kind:"get",key:"_unitSystemValue",value:function(){return void 0!==this._unitSystem?this._unitSystem:"metric"}},{kind:"get",key:"_currencyValue",value:function(){return void 0!==this._currency?this._currency:""}},{kind:"field",key:"_markerLocation",value:()=>(0,n.Z)((e=>[{id:S,latitude:e[0],longitude:e[1],location_editable:!0}]))},{kind:"method",key:"_handleChange",value:function(e){const a=e.currentTarget;let i=a.value;"currency"===a.name&&i&&i in d&&(i=d[i]),this[`_${a.name}`]=i}},{kind:"method",key:"_locationChanged",value:function(e){this._location=e.detail.location}},{kind:"method",key:"_unitSystemChanged",value:function(e){this._unitSystem=e.target.value}},{kind:"method",key:"_detect",value:async function(){this._working=!0;try{const a=await(e=this.hass,e.callWS({type:"config/core/detect"}));a.latitude&&a.longitude&&(this.map.addEventListener("markers-updated",(()=>{this.map.fitMarker(S)}),{once:!0}),this._location=[Number(a.latitude),Number(a.longitude)]),a.elevation&&(this._elevation=String(a.elevation)),a.unit_system&&(this._unitSystem=a.unit_system),a.time_zone&&(this._timeZone=a.time_zone),a.currency&&(this._currency=a.currency),a.country&&(this._country=a.country),this._language=(0,h.sS)()}catch(e){alert(`Failed to detect location information: ${e.message}`)}finally{this._working=!1}var e}},{kind:"method",key:"_save",value:async function(e){e.preventDefault(),this._working=!0;try{const e=this._locationValue;await(a=this.hass,i={location_name:this._nameValue,latitude:e[0],longitude:e[1],elevation:Number(this._elevationValue),unit_system:this._unitSystemValue,time_zone:this._timeZoneValue||"UTC",currency:this._currencyValue||"EUR",country:this._countryValue,language:this._languageValue},a.callWS({type:"config/core/update",...i}));const t=await(0,m.Rj)(this.hass);(0,o.B)(this,"onboarding-step",{type:"core_config",result:t})}catch(e){this._working=!1,alert(`Failed to save: ${e.message}`)}var a,i}},{kind:"get",static:!0,key:"styles",value:function(){return t.iv`
      .row {
        display: flex;
        flex-direction: row;
        margin: 0 -8px;
        align-items: center;
      }

      .secondary {
        color: var(--secondary-text-color);
      }

      ha-textfield {
        display: block;
      }

      ha-locations-editor {
        height: 200px;
      }

      .flex {
        flex: 1;
      }

      .middle-text {
        margin: 16px 0;
      }

      .row {
        margin-top: 16px;
      }

      .row > * {
        margin: 0 8px;
      }

      .radio-group {
        display: flex;
        flex-direction: column;
        flex: 1;
      }

      .footer {
        margin-top: 16px;
        text-align: right;
      }
      a {
        color: var(--primary-color);
      }
    `}}]}}),t.oi)},52461:e=>{"use strict";e.exports=JSON.parse('{"Pacific/Niue":"(GMT-11:00) Niue","Pacific/Pago_Pago":"(GMT-11:00) Pago Pago","Pacific/Honolulu":"(GMT-10:00) Hawaii Time","Pacific/Rarotonga":"(GMT-10:00) Rarotonga","Pacific/Tahiti":"(GMT-10:00) Tahiti","Pacific/Marquesas":"(GMT-09:30) Marquesas","America/Anchorage":"(GMT-09:00) Alaska Time","Pacific/Gambier":"(GMT-09:00) Gambier","America/Los_Angeles":"(GMT-08:00) Pacific Time","America/Tijuana":"(GMT-08:00) Pacific Time - Tijuana","America/Vancouver":"(GMT-08:00) Pacific Time - Vancouver","America/Whitehorse":"(GMT-08:00) Pacific Time - Whitehorse","Pacific/Pitcairn":"(GMT-08:00) Pitcairn","America/Dawson_Creek":"(GMT-07:00) Mountain Time - Dawson Creek","America/Denver":"(GMT-07:00) Mountain Time","America/Edmonton":"(GMT-07:00) Mountain Time - Edmonton","America/Hermosillo":"(GMT-07:00) Mountain Time - Hermosillo","America/Mazatlan":"(GMT-07:00) Mountain Time - Chihuahua, Mazatlan","America/Phoenix":"(GMT-07:00) Mountain Time - Arizona","America/Yellowknife":"(GMT-07:00) Mountain Time - Yellowknife","America/Belize":"(GMT-06:00) Belize","America/Chicago":"(GMT-06:00) Central Time","America/Costa_Rica":"(GMT-06:00) Costa Rica","America/El_Salvador":"(GMT-06:00) El Salvador","America/Guatemala":"(GMT-06:00) Guatemala","America/Managua":"(GMT-06:00) Managua","America/Mexico_City":"(GMT-06:00) Central Time - Mexico City","America/Regina":"(GMT-06:00) Central Time - Regina","America/Tegucigalpa":"(GMT-06:00) Central Time - Tegucigalpa","America/Winnipeg":"(GMT-06:00) Central Time - Winnipeg","Pacific/Galapagos":"(GMT-06:00) Galapagos","America/Bogota":"(GMT-05:00) Bogota","America/Cancun":"(GMT-05:00) America Cancun","America/Cayman":"(GMT-05:00) Cayman","America/Guayaquil":"(GMT-05:00) Guayaquil","America/Havana":"(GMT-05:00) Havana","America/Iqaluit":"(GMT-05:00) Eastern Time - Iqaluit","America/Jamaica":"(GMT-05:00) Jamaica","America/Lima":"(GMT-05:00) Lima","America/Nassau":"(GMT-05:00) Nassau","America/New_York":"(GMT-05:00) Eastern Time","America/Panama":"(GMT-05:00) Panama","America/Port-au-Prince":"(GMT-05:00) Port-au-Prince","America/Rio_Branco":"(GMT-05:00) Rio Branco","America/Toronto":"(GMT-05:00) Eastern Time - Toronto","Pacific/Easter":"(GMT-05:00) Easter Island","America/Caracas":"(GMT-04:30) Caracas","America/Asuncion":"(GMT-03:00) Asuncion","America/Barbados":"(GMT-04:00) Barbados","America/Boa_Vista":"(GMT-04:00) Boa Vista","America/Campo_Grande":"(GMT-03:00) Campo Grande","America/Cuiaba":"(GMT-03:00) Cuiaba","America/Curacao":"(GMT-04:00) Curacao","America/Grand_Turk":"(GMT-04:00) Grand Turk","America/Guyana":"(GMT-04:00) Guyana","America/Halifax":"(GMT-04:00) Atlantic Time - Halifax","America/La_Paz":"(GMT-04:00) La Paz","America/Manaus":"(GMT-04:00) Manaus","America/Martinique":"(GMT-04:00) Martinique","America/Port_of_Spain":"(GMT-04:00) Port of Spain","America/Porto_Velho":"(GMT-04:00) Porto Velho","America/Puerto_Rico":"(GMT-04:00) Puerto Rico","America/Santo_Domingo":"(GMT-04:00) Santo Domingo","America/Thule":"(GMT-04:00) Thule","Atlantic/Bermuda":"(GMT-04:00) Bermuda","America/St_Johns":"(GMT-03:30) Newfoundland Time - St. Johns","America/Araguaina":"(GMT-03:00) Araguaina","America/Argentina/Buenos_Aires":"(GMT-03:00) Buenos Aires","America/Bahia":"(GMT-03:00) Salvador","America/Belem":"(GMT-03:00) Belem","America/Cayenne":"(GMT-03:00) Cayenne","America/Fortaleza":"(GMT-03:00) Fortaleza","America/Godthab":"(GMT-03:00) Godthab","America/Maceio":"(GMT-03:00) Maceio","America/Miquelon":"(GMT-03:00) Miquelon","America/Montevideo":"(GMT-03:00) Montevideo","America/Paramaribo":"(GMT-03:00) Paramaribo","America/Recife":"(GMT-03:00) Recife","America/Santiago":"(GMT-03:00) Santiago","America/Sao_Paulo":"(GMT-02:00) Sao Paulo","Antarctica/Palmer":"(GMT-03:00) Palmer","Antarctica/Rothera":"(GMT-03:00) Rothera","Atlantic/Stanley":"(GMT-03:00) Stanley","America/Noronha":"(GMT-02:00) Noronha","Atlantic/South_Georgia":"(GMT-02:00) South Georgia","America/Scoresbysund":"(GMT-01:00) Scoresbysund","Atlantic/Azores":"(GMT-01:00) Azores","Atlantic/Cape_Verde":"(GMT-01:00) Cape Verde","Africa/Abidjan":"(GMT+00:00) Abidjan","Africa/Accra":"(GMT+00:00) Accra","Africa/Bissau":"(GMT+00:00) Bissau","Africa/Casablanca":"(GMT+00:00) Casablanca","Africa/El_Aaiun":"(GMT+00:00) El Aaiun","Africa/Monrovia":"(GMT+00:00) Monrovia","America/Danmarkshavn":"(GMT+00:00) Danmarkshavn","Atlantic/Canary":"(GMT+00:00) Canary Islands","Atlantic/Faroe":"(GMT+00:00) Faeroe","Atlantic/Reykjavik":"(GMT+00:00) Reykjavik","Etc/GMT":"(GMT+00:00) GMT (no daylight saving)","Europe/Dublin":"(GMT+00:00) Dublin","Europe/Lisbon":"(GMT+00:00) Lisbon","Europe/London":"(GMT+00:00) London","Africa/Algiers":"(GMT+01:00) Algiers","Africa/Ceuta":"(GMT+01:00) Ceuta","Africa/Lagos":"(GMT+01:00) Lagos","Africa/Ndjamena":"(GMT+01:00) Ndjamena","Africa/Tunis":"(GMT+01:00) Tunis","Africa/Windhoek":"(GMT+02:00) Windhoek","Europe/Amsterdam":"(GMT+01:00) Amsterdam","Europe/Andorra":"(GMT+01:00) Andorra","Europe/Belgrade":"(GMT+01:00) Central European Time - Belgrade","Europe/Berlin":"(GMT+01:00) Berlin","Europe/Brussels":"(GMT+01:00) Brussels","Europe/Budapest":"(GMT+01:00) Budapest","Europe/Copenhagen":"(GMT+01:00) Copenhagen","Europe/Gibraltar":"(GMT+01:00) Gibraltar","Europe/Luxembourg":"(GMT+01:00) Luxembourg","Europe/Madrid":"(GMT+01:00) Madrid","Europe/Malta":"(GMT+01:00) Malta","Europe/Monaco":"(GMT+01:00) Monaco","Europe/Oslo":"(GMT+01:00) Oslo","Europe/Paris":"(GMT+01:00) Paris","Europe/Prague":"(GMT+01:00) Central European Time - Prague","Europe/Rome":"(GMT+01:00) Rome","Europe/Stockholm":"(GMT+01:00) Stockholm","Europe/Tirane":"(GMT+01:00) Tirane","Europe/Vienna":"(GMT+01:00) Vienna","Europe/Warsaw":"(GMT+01:00) Warsaw","Europe/Zurich":"(GMT+01:00) Zurich","Africa/Cairo":"(GMT+02:00) Cairo","Africa/Johannesburg":"(GMT+02:00) Johannesburg","Africa/Maputo":"(GMT+02:00) Maputo","Africa/Tripoli":"(GMT+02:00) Tripoli","Asia/Amman":"(GMT+02:00) Amman","Asia/Beirut":"(GMT+02:00) Beirut","Asia/Damascus":"(GMT+02:00) Damascus","Asia/Gaza":"(GMT+02:00) Gaza","Asia/Jerusalem":"(GMT+02:00) Jerusalem","Asia/Nicosia":"(GMT+02:00) Nicosia","Europe/Athens":"(GMT+02:00) Athens","Europe/Bucharest":"(GMT+02:00) Bucharest","Europe/Chisinau":"(GMT+02:00) Chisinau","Europe/Helsinki":"(GMT+02:00) Helsinki","Europe/Istanbul":"(GMT+02:00) Istanbul","Europe/Kaliningrad":"(GMT+02:00) Moscow-01 - Kaliningrad","Europe/Kiev":"(GMT+02:00) Kiev","Europe/Riga":"(GMT+02:00) Riga","Europe/Sofia":"(GMT+02:00) Sofia","Europe/Tallinn":"(GMT+02:00) Tallinn","Europe/Vilnius":"(GMT+02:00) Vilnius","Africa/Khartoum":"(GMT+03:00) Khartoum","Africa/Nairobi":"(GMT+03:00) Nairobi","Antarctica/Syowa":"(GMT+03:00) Syowa","Asia/Baghdad":"(GMT+03:00) Baghdad","Asia/Qatar":"(GMT+03:00) Qatar","Asia/Riyadh":"(GMT+03:00) Riyadh","Europe/Minsk":"(GMT+03:00) Minsk","Europe/Moscow":"(GMT+03:00) Moscow+00 - Moscow","Asia/Tehran":"(GMT+03:30) Tehran","Asia/Baku":"(GMT+04:00) Baku","Asia/Dubai":"(GMT+04:00) Dubai","Asia/Tbilisi":"(GMT+04:00) Tbilisi","Asia/Yerevan":"(GMT+04:00) Yerevan","Europe/Samara":"(GMT+04:00) Moscow+01 - Samara","Indian/Mahe":"(GMT+04:00) Mahe","Indian/Mauritius":"(GMT+04:00) Mauritius","Indian/Reunion":"(GMT+04:00) Reunion","Asia/Kabul":"(GMT+04:30) Kabul","Antarctica/Mawson":"(GMT+05:00) Mawson","Asia/Aqtau":"(GMT+05:00) Aqtau","Asia/Aqtobe":"(GMT+05:00) Aqtobe","Asia/Ashgabat":"(GMT+05:00) Ashgabat","Asia/Dushanbe":"(GMT+05:00) Dushanbe","Asia/Karachi":"(GMT+05:00) Karachi","Asia/Tashkent":"(GMT+05:00) Tashkent","Asia/Yekaterinburg":"(GMT+05:00) Moscow+02 - Yekaterinburg","Indian/Kerguelen":"(GMT+05:00) Kerguelen","Indian/Maldives":"(GMT+05:00) Maldives","Asia/Calcutta":"(GMT+05:30) India Standard Time","Asia/Colombo":"(GMT+05:30) Colombo","Asia/Katmandu":"(GMT+05:45) Katmandu","Antarctica/Vostok":"(GMT+06:00) Vostok","Asia/Almaty":"(GMT+06:00) Almaty","Asia/Bishkek":"(GMT+06:00) Bishkek","Asia/Dhaka":"(GMT+06:00) Dhaka","Asia/Omsk":"(GMT+06:00) Moscow+03 - Omsk, Novosibirsk","Asia/Thimphu":"(GMT+06:00) Thimphu","Indian/Chagos":"(GMT+06:00) Chagos","Asia/Rangoon":"(GMT+06:30) Rangoon","Indian/Cocos":"(GMT+06:30) Cocos","Antarctica/Davis":"(GMT+07:00) Davis","Asia/Bangkok":"(GMT+07:00) Bangkok","Asia/Hovd":"(GMT+07:00) Hovd","Asia/Jakarta":"(GMT+07:00) Jakarta","Asia/Krasnoyarsk":"(GMT+07:00) Moscow+04 - Krasnoyarsk","Asia/Saigon":"(GMT+07:00) Hanoi","Asia/Ho_Chi_Minh":"(GMT+07:00) Ho Chi Minh","Indian/Christmas":"(GMT+07:00) Christmas","Antarctica/Casey":"(GMT+08:00) Casey","Asia/Brunei":"(GMT+08:00) Brunei","Asia/Choibalsan":"(GMT+08:00) Choibalsan","Asia/Hong_Kong":"(GMT+08:00) Hong Kong","Asia/Irkutsk":"(GMT+08:00) Moscow+05 - Irkutsk","Asia/Kuala_Lumpur":"(GMT+08:00) Kuala Lumpur","Asia/Macau":"(GMT+08:00) Macau","Asia/Makassar":"(GMT+08:00) Makassar","Asia/Manila":"(GMT+08:00) Manila","Asia/Shanghai":"(GMT+08:00) China Time - Beijing","Asia/Singapore":"(GMT+08:00) Singapore","Asia/Taipei":"(GMT+08:00) Taipei","Asia/Ulaanbaatar":"(GMT+08:00) Ulaanbaatar","Australia/Perth":"(GMT+08:00) Western Time - Perth","Asia/Pyongyang":"(GMT+08:30) Pyongyang","Asia/Dili":"(GMT+09:00) Dili","Asia/Jayapura":"(GMT+09:00) Jayapura","Asia/Seoul":"(GMT+09:00) Seoul","Asia/Tokyo":"(GMT+09:00) Tokyo","Asia/Yakutsk":"(GMT+09:00) Moscow+06 - Yakutsk","Pacific/Palau":"(GMT+09:00) Palau","Australia/Adelaide":"(GMT+10:30) Central Time - Adelaide","Australia/Darwin":"(GMT+09:30) Central Time - Darwin","Antarctica/DumontDUrville":"(GMT+10:00) Dumont D\'Urville","Asia/Magadan":"(GMT+10:00) Moscow+07 - Magadan","Asia/Vladivostok":"(GMT+10:00) Moscow+07 - Yuzhno-Sakhalinsk","Australia/Brisbane":"(GMT+10:00) Eastern Time - Brisbane","Australia/Hobart":"(GMT+11:00) Eastern Time - Hobart","Australia/Sydney":"(GMT+11:00) Eastern Time - Melbourne, Sydney","Pacific/Chuuk":"(GMT+10:00) Truk","Pacific/Guam":"(GMT+10:00) Guam","Pacific/Port_Moresby":"(GMT+10:00) Port Moresby","Pacific/Efate":"(GMT+11:00) Efate","Pacific/Guadalcanal":"(GMT+11:00) Guadalcanal","Pacific/Kosrae":"(GMT+11:00) Kosrae","Pacific/Norfolk":"(GMT+11:00) Norfolk","Pacific/Noumea":"(GMT+11:00) Noumea","Pacific/Pohnpei":"(GMT+11:00) Ponape","Asia/Kamchatka":"(GMT+12:00) Moscow+09 - Petropavlovsk-Kamchatskiy","Pacific/Auckland":"(GMT+13:00) Auckland","Pacific/Fiji":"(GMT+13:00) Fiji","Pacific/Funafuti":"(GMT+12:00) Funafuti","Pacific/Kwajalein":"(GMT+12:00) Kwajalein","Pacific/Majuro":"(GMT+12:00) Majuro","Pacific/Nauru":"(GMT+12:00) Nauru","Pacific/Tarawa":"(GMT+12:00) Tarawa","Pacific/Wake":"(GMT+12:00) Wake","Pacific/Wallis":"(GMT+12:00) Wallis","Pacific/Apia":"(GMT+14:00) Apia","Pacific/Enderbury":"(GMT+13:00) Enderbury","Pacific/Fakaofo":"(GMT+13:00) Fakaofo","Pacific/Tongatapu":"(GMT+13:00) Tongatapu","Pacific/Kiritimati":"(GMT+14:00) Kiritimati"}')}}]);
//# sourceMappingURL=cd6b1ea4.js.map