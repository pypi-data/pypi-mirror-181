/*! For license information please see ad967dfa.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[79042],{89833:(e,t,i)=>{i.d(t,{O:()=>h});var r=i(87480),n=i(86251),a=i(37500),o=i(33310),s=i(8636),l=i(51346),d=i(71260);const c={fromAttribute:e=>null!==e&&(""===e||e),toAttribute:e=>"boolean"==typeof e?e?"":null:e};class h extends n.P{constructor(){super(...arguments),this.rows=2,this.cols=20,this.charCounter=!1}render(){const e=this.charCounter&&-1!==this.maxLength,t=e&&"internal"===this.charCounter,i=e&&!t,r=!!this.helper||!!this.validationMessage||i,n={"mdc-text-field--disabled":this.disabled,"mdc-text-field--no-label":!this.label,"mdc-text-field--filled":!this.outlined,"mdc-text-field--outlined":this.outlined,"mdc-text-field--end-aligned":this.endAligned,"mdc-text-field--with-internal-counter":t};return a.dy`
      <label class="mdc-text-field mdc-text-field--textarea ${(0,s.$)(n)}">
        ${this.renderRipple()}
        ${this.outlined?this.renderOutline():this.renderLabel()}
        ${this.renderInput()}
        ${this.renderCharCounter(t)}
        ${this.renderLineRipple()}
      </label>
      ${this.renderHelperText(r,i)}
    `}renderInput(){const e=this.label?"label":void 0,t=-1===this.minLength?void 0:this.minLength,i=-1===this.maxLength?void 0:this.maxLength,r=this.autocapitalize?this.autocapitalize:void 0;return a.dy`
      <textarea
          aria-labelledby=${(0,l.o)(e)}
          class="mdc-text-field__input"
          .value="${(0,d.a)(this.value)}"
          rows="${this.rows}"
          cols="${this.cols}"
          ?disabled="${this.disabled}"
          placeholder="${this.placeholder}"
          ?required="${this.required}"
          ?readonly="${this.readOnly}"
          minlength="${(0,l.o)(t)}"
          maxlength="${(0,l.o)(i)}"
          name="${(0,l.o)(""===this.name?void 0:this.name)}"
          inputmode="${(0,l.o)(this.inputMode)}"
          autocapitalize="${(0,l.o)(r)}"
          @input="${this.handleInputChange}"
          @blur="${this.onInputBlur}">
      </textarea>`}}(0,r.__decorate)([(0,o.IO)("textarea")],h.prototype,"formElement",void 0),(0,r.__decorate)([(0,o.Cb)({type:Number})],h.prototype,"rows",void 0),(0,r.__decorate)([(0,o.Cb)({type:Number})],h.prototype,"cols",void 0),(0,r.__decorate)([(0,o.Cb)({converter:c})],h.prototype,"charCounter",void 0)},96791:(e,t,i)=>{i.d(t,{W:()=>r});const r=i(37500).iv`.mdc-text-field{height:100%}.mdc-text-field__input{resize:none}`},59699:(e,t,i)=>{i.d(t,{Z:()=>s});var r=i(90394),n=i(39244),a=i(23682),o=36e5;function s(e,t){(0,a.Z)(2,arguments);var i=(0,r.Z)(t);return(0,n.Z)(e,i*o)}},39244:(e,t,i)=>{i.d(t,{Z:()=>o});var r=i(90394),n=i(34327),a=i(23682);function o(e,t){(0,a.Z)(2,arguments);var i=(0,n.Z)(e).getTime(),o=(0,r.Z)(t);return new Date(i+o)}},99307:(e,t,i)=>{i.d(t,{Z:()=>a});var r=i(34327),n=i(23682);function a(e,t){(0,n.Z)(2,arguments);var i=(0,r.Z)(e),a=(0,r.Z)(t);return i.getTime()-a.getTime()}},72949:(e,t,i)=>{i.d(t,{Z:()=>a});var r=i(34327),n=i(23682);function a(e){(0,n.Z)(1,arguments);var t=(0,r.Z)(e);return t.setMinutes(0,0,0),t}},53297:(e,t,i)=>{var r=i(89833),n=i(31338),a=i(96791),o=i(37500),s=i(33310);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var a="static"===n?e:i;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var a=this.decorateConstructor(i,t);return r.push.apply(r,a.finishers),a.finishers=r,a},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function v(){return v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,t,i){var r=y(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(arguments.length<3?e:i):n.value}},v.apply(this,arguments)}function y(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}function g(e){return g=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},g(e)}!function(e,t,i,r){var n=l();if(r)for(var a=0;a<r.length;a++)n=r[a](n);var o=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},r=0;r<e.length;r++){var n,a=e[r];if("method"===a.kind&&(n=t.find(i)))if(u(a.descriptor)||u(n.descriptor)){if(h(a)||h(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(h(a)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}c(a,n)}else t.push(a)}return t}(o.d.map(d)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([(0,s.Mo)("ha-textarea")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({type:Boolean,reflect:!0})],key:"autogrow",value:()=>!1},{kind:"method",key:"updated",value:function(e){v(g(i.prototype),"updated",this).call(this,e),this.autogrow&&e.has("value")&&(this.mdcRoot.dataset.value=this.value+'=​"')}},{kind:"field",static:!0,key:"styles",value:()=>[n.W,a.W,o.iv`
      :host([autogrow]) .mdc-text-field {
        position: relative;
        min-height: 74px;
        min-width: 178px;
        max-height: 200px;
      }
      :host([autogrow]) .mdc-text-field:after {
        content: attr(data-value);
        margin-top: 23px;
        margin-bottom: 9px;
        line-height: 1.5rem;
        min-height: 42px;
        padding: 0px 32px 0 16px;
        letter-spacing: var(
          --mdc-typography-subtitle1-letter-spacing,
          0.009375em
        );
        visibility: hidden;
        white-space: pre-wrap;
      }
      :host([autogrow]) .mdc-text-field__input {
        position: absolute;
        height: calc(100% - 32px);
      }
      :host([autogrow]) .mdc-text-field.mdc-text-field--no-label:after {
        margin-top: 16px;
        margin-bottom: 16px;
      }
    `]}]}}),r.O)},79042:(e,t,i)=>{i.a(e,(async e=>{i.r(t);i(51187);var r=i(79021),n=i(72949),a=i(59699),o=i(99307),s=i(39244),l=i(37500),d=i(33310),c=i(14516),h=i(47181),u=i(99137),p=i(94653),m=(i(53297),i(85066),i(51144)),f=i(11654),v=i(91476),y=i(29152),g=i(89207),_=e([y,v,p]);function b(){b=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var a="static"===n?e:i;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!E(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var a=this.decorateConstructor(i,t);return r.push.apply(r,a.finishers),a.finishers=r,a},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,a=n.length-1;a>=0;a--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return C(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?C(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=$(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:x(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=x(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function k(e){var t,i=$(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function w(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function E(e){return e.decorators&&e.decorators.length}function D(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function x(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function $(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function C(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}[y,v,p]=_.then?await _:_;const z=e=>l.dy`<mwc-list-item>
  <span>${e.name}</span>
</mwc-list-item>`;!function(e,t,i,r){var n=b();if(r)for(var a=0;a<r.length;a++)n=r[a](n);var o=t((function(e){n.initializeInstanceElements(e,s.elements)}),i),s=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},r=0;r<e.length;r++){var n,a=e[r];if("method"===a.kind&&(n=t.find(i)))if(D(a.descriptor)||D(n.descriptor)){if(E(a)||E(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(E(a)){if(E(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}w(a,n)}else t.push(a)}return t}(o.d.map(k)),e);n.initializeClassElements(o.F,s.elements),n.runClassFinishers(o.F,s.finishers)}([(0,d.Mo)("dialog-calendar-event-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_info",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_calendars",value:()=>[]},{kind:"field",decorators:[(0,d.SB)()],key:"_calendarId",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_summary",value:()=>""},{kind:"field",decorators:[(0,d.SB)()],key:"_description",value:()=>""},{kind:"field",decorators:[(0,d.SB)()],key:"_rrule",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_allDay",value:()=>!1},{kind:"field",decorators:[(0,d.SB)()],key:"_dtstart",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_dtend",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_submitting",value:()=>!1},{kind:"method",key:"showDialog",value:function(e){if(this._error=void 0,this._info=void 0,this._params=e,this._calendars=e.calendars,this._calendarId=e.calendarId||this._calendars[0].entity_id,e.entry){const t=e.entry;this._allDay=(0,u.J)(t.dtstart),this._summary=t.summary,this._rrule=t.rrule,this._allDay?(this._dtstart=new Date(t.dtstart),this._dtend=(0,r.Z)(new Date(t.dtend),-1)):(this._dtstart=new Date(t.dtstart),this._dtend=new Date(t.dtend))}else this._allDay=!1,this._dtstart=(0,n.Z)(e.selectedDate?e.selectedDate:new Date),this._dtend=(0,a.Z)(this._dtstart,1)}},{kind:"method",key:"closeDialog",value:function(){this._params&&(this._calendars=[],this._calendarId=void 0,this._params=void 0,this._dtstart=void 0,this._dtend=void 0,this._summary="",this._description="",this._rrule=void 0,(0,h.B)(this,"dialog-closed",{dialog:this.localName}))}},{kind:"method",key:"render",value:function(){if(!this._params)return l.dy``;const e=void 0===this._params.entry,{startDate:t,startTime:i,endDate:r,endTime:n}=this._getLocaleStrings(this._dtstart,this._dtend);return l.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        .heading=${l.dy`
          <div class="header_title">
            ${e?this.hass.localize("ui.components.calendar.event.add"):this._summary}
          </div>
          <ha-icon-button
            .label=${this.hass.localize("ui.dialogs.generic.close")}
            .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
            dialogAction="close"
            class="header_button"
          ></ha-icon-button>
        `}
      >
        <div class="content">
          ${this._error?l.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
          ${this._info?l.dy`<ha-alert
                alert-type="info"
                dismissable
                @alert-dismissed-clicked=${this._clearInfo}
                >${this._info}</ha-alert
              >`:""}

          <ha-textfield
            class="summary"
            name="summary"
            .label=${this.hass.localize("ui.components.calendar.event.summary")}
            required
            @change=${this._handleSummaryChanged}
            error-message=${this.hass.localize("ui.common.error_required")}
            dialogInitialFocus
          ></ha-textfield>
          <ha-textarea
            class="description"
            name="description"
            .label=${this.hass.localize("ui.components.calendar.event.description")}
            @change=${this._handleDescriptionChanged}
            autogrow
          ></ha-textarea>
          <ha-combo-box
            name="calendar"
            .hass=${this.hass}
            .label=${this.hass.localize("ui.components.calendar.label")}
            .value=${this._calendarId}
            .renderer=${z}
            .items=${this._calendars}
            item-id-path="entity_id"
            item-value-path="entity_id"
            item-label-path="name"
            required
            @value-changed=${this._handleCalendarChanged}
          ></ha-combo-box>
          <ha-formfield
            .label=${this.hass.localize("ui.components.calendar.event.all_day")}
          >
            <ha-switch
              id="all_day"
              .checked=${this._allDay}
              @change=${this._allDayToggleChanged}
            ></ha-switch>
          </ha-formfield>

          <div>
            <span class="label"
              >${this.hass.localize("ui.components.calendar.event.start")}:</span
            >
            <div class="flex">
              <ha-date-input
                .value=${t}
                .locale=${this.hass.locale}
                @value-changed=${this._startDateChanged}
              ></ha-date-input>
              ${this._allDay?"":l.dy`<ha-time-input
                    .value=${i}
                    .locale=${this.hass.locale}
                    @value-changed=${this._startTimeChanged}
                  ></ha-time-input>`}
            </div>
          </div>
          <div>
            <span class="label"
              >${this.hass.localize("ui.components.calendar.event.end")}:</span
            >
            <div class="flex">
              <ha-date-input
                .value=${r}
                .min=${t}
                .locale=${this.hass.locale}
                @value-changed=${this._endDateChanged}
              ></ha-date-input>
              ${this._allDay?"":l.dy`<ha-time-input
                    .value=${n}
                    .locale=${this.hass.locale}
                    @value-changed=${this._endTimeChanged}
                  ></ha-time-input>`}
            </div>
          </div>
          <ha-recurrence-rule-editor
            .locale=${this.hass.locale}
            .timezone=${this.hass.config.time_zone}
            .value=${this._rrule||""}
            @value-changed=${this._handleRRuleChanged}
          >
          </ha-recurrence-rule-editor>
        </div>
        ${e?l.dy`
              <mwc-button
                slot="primaryAction"
                @click=${this._createEvent}
                .disabled=${this._submitting}
              >
                ${this.hass.localize("ui.components.calendar.event.add")}
              </mwc-button>
            `:l.dy`
              <mwc-button
                slot="primaryAction"
                @click=${this._saveEvent}
                .disabled=${this._submitting}
              >
                ${this.hass.localize("ui.components.calendar.event.save")}
              </mwc-button>
              ${this._params.canDelete?l.dy`
                    <mwc-button
                      slot="secondaryAction"
                      class="warning"
                      @click=${this._deleteEvent}
                      .disabled=${this._submitting}
                    >
                      ${this.hass.localize("ui.components.calendar.event.delete")}
                    </mwc-button>
                  `:""}
            `}
      </ha-dialog>
    `}},{kind:"field",key:"_getLocaleStrings",value(){return(0,c.Z)(((e,t)=>{const i=this.hass.config.time_zone;return{startDate:null==e?void 0:e.toLocaleDateString("en-CA",{timeZone:i}),startTime:null==e?void 0:e.toLocaleTimeString("en-GB",{timeZone:i}),endDate:null==t?void 0:t.toLocaleDateString("en-CA",{timeZone:i}),endTime:null==t?void 0:t.toLocaleTimeString("en-GB",{timeZone:i})}}))}},{kind:"method",key:"_clearInfo",value:function(){this._info=void 0}},{kind:"method",key:"_handleSummaryChanged",value:function(e){this._summary=e.target.value}},{kind:"method",key:"_handleDescriptionChanged",value:function(e){this._description=e.target.value}},{kind:"method",key:"_handleRRuleChanged",value:function(e){this._rrule=e.detail.value}},{kind:"method",key:"_allDayToggleChanged",value:function(e){this._allDay=e.target.checked}},{kind:"method",key:"_startDateChanged",value:function(e){const t=(0,o.Z)(this._dtend,this._dtstart);if(this._dtstart=new Date(e.detail.value+"T"+this._dtstart.toLocaleTimeString("en-GB",{timeZone:this.hass.config.time_zone})),this._dtend<=this._dtstart){const e=(0,s.Z)(this._dtstart,t);this._dtend=new Date(`${e.toLocaleDateString("en-CA",{timeZone:this.hass.config.time_zone})}T${e.toLocaleTimeString("en-GB",{timeZone:this.hass.config.time_zone})}`),this._info=this.hass.localize("ui.components.calendar.event.end_auto_adjusted")}}},{kind:"method",key:"_endDateChanged",value:function(e){this._dtend=new Date(e.detail.value+"T"+this._dtend.toLocaleTimeString("en-GB",{timeZone:this.hass.config.time_zone}))}},{kind:"method",key:"_startTimeChanged",value:function(e){const t=(0,o.Z)(this._dtend,this._dtstart);if(this._dtstart=new Date(this._dtstart.toLocaleDateString("en-CA",{timeZone:this.hass.config.time_zone})+"T"+e.detail.value),this._dtend<=this._dtstart){const e=(0,s.Z)(new Date(this._dtstart),t);this._dtend=new Date(`${e.toLocaleDateString("en-CA",{timeZone:this.hass.config.time_zone})}T${e.toLocaleTimeString("en-GB",{timeZone:this.hass.config.time_zone})}`),this._info=this.hass.localize("ui.components.calendar.event.end_auto_adjusted")}}},{kind:"method",key:"_endTimeChanged",value:function(e){this._dtend=new Date(this._dtend.toLocaleDateString("en-CA",{timeZone:this.hass.config.time_zone})+"T"+e.detail.value)}},{kind:"method",key:"_calculateData",value:function(){const{startDate:e,startTime:t,endDate:i,endTime:n}=this._getLocaleStrings(this._dtstart,this._dtend),a={summary:this._summary,description:this._description,rrule:this._rrule,dtstart:"",dtend:""};return this._allDay?(a.dtstart=e,a.dtend=(0,r.Z)(new Date(this._dtend),1).toLocaleDateString("en-CA")):(a.dtstart=`${e}T${t}`,a.dtend=`${i}T${n}`),a}},{kind:"method",key:"_handleCalendarChanged",value:function(e){this._calendarId=e.detail.value}},{kind:"method",key:"_createEvent",value:async function(){if(this._summary&&this._calendarId)if(this._dtend<=this._dtstart)this._error=this.hass.localize("ui.components.calendar.event.invalid_duration");else{this._submitting=!0;try{await(0,m.fE)(this.hass,this._calendarId,this._calculateData())}catch(e){return void(this._error=e?e.message:"Unknown error")}finally{this._submitting=!1}await this._params.updated(),this.closeDialog()}else this._error=this.hass.localize("ui.components.calendar.event.not_all_required_fields")}},{kind:"method",key:"_saveEvent",value:async function(){}},{kind:"method",key:"_deleteEvent",value:async function(){this._submitting=!0;const e=this._params.entry,t=await(0,g.Y)(this,{title:this.hass.localize("ui.components.calendar.event.confirm_delete.delete"),text:e.recurrence_id?this.hass.localize("ui.components.calendar.event.confirm_delete.recurring_prompt"):this.hass.localize("ui.components.calendar.event.confirm_delete.prompt"),confirmText:e.recurrence_id?this.hass.localize("ui.components.calendar.event.confirm_delete.delete_this"):this.hass.localize("ui.components.calendar.event.confirm_delete.delete"),confirmFutureText:e.recurrence_id?this.hass.localize("ui.components.calendar.event.confirm_delete.delete_future"):void 0});if(void 0!==t){try{await(0,m.d1)(this.hass,this._calendarId,e.uid,e.recurrence_id||"",t)}catch(e){return void(this._error=e?e.message:"Unknown error")}finally{this._submitting=!1}await this._params.updated(),this.closeDialog()}else this._submitting=!1}},{kind:"get",static:!0,key:"styles",value:function(){return[f.yu,l.iv`
        state-info {
          line-height: 40px;
        }
        ha-alert {
          display: block;
          margin-bottom: 16px;
        }
        ha-textfield,
        ha-textarea {
          display: block;
        }
        ha-textarea {
          margin-bottom: 16px;
        }
        ha-formfield {
          display: block;
          padding: 16px 0;
        }
        ha-date-input {
          flex-grow: 1;
        }
        ha-time-input {
          margin-left: 16px;
        }
        ha-recurrence-rule-editor {
          display: block;
          margin-top: 16px;
        }
        .flex {
          display: flex;
          justify-content: space-between;
        }
        .label {
          font-size: 12px;
          font-weight: 500;
          color: var(--input-label-ink-color);
        }
        .date-range-details-content {
          display: inline-block;
        }
        ha-rrule {
          display: block;
        }
        ha-combo-box {
          display: block;
        }
        ha-svg-icon {
          width: 40px;
          margin-right: 8px;
          margin-inline-end: 16px;
          margin-inline-start: initial;
          direction: var(--direction);
          vertical-align: top;
        }
        ha-rrule {
          display: inline-block;
        }
        .key {
          display: inline-block;
          vertical-align: top;
        }
        .value {
          display: inline-block;
          vertical-align: top;
        }
      `]}}]}}),l.oi)}))}}]);
//# sourceMappingURL=ad967dfa.js.map