import{J as o,r as i,b as e,d as t,p as s,n as a,s as n,y as c,E as d,$ as l}from"./index-91e6f5fe.js";import"./c.399eda54.js";import{c as p}from"./c.5ee2a770.js";let r=class extends n{constructor(){super(...arguments),this._showCopied=!1}render(){return c`
      <mwc-dialog
        open
        heading=${`API key for ${this.configuration}`}
        scrimClickAction
        @closed=${this._handleClose}
      >
        ${void 0===this._apiKey?"Loading…":null===this._apiKey?c`Unable to automatically extract API key. Open the configuration
              and look for <code>api:</code>.`:c`
              <div class="key" @click=${this._copyApiKey}>
                <code>${this._apiKey}</code>
                <mwc-button ?disabled=${this._showCopied}
                  >${this._showCopied?"Copied!":"Copy"}</mwc-button
                >
              </div>
            `}
        ${null===this._apiKey?c`
              <mwc-button
                @click=${this._editConfig}
                no-attention
                slot="secondaryAction"
                dialogAction="close"
                label="Open configuration"
              ></mwc-button>
            `:""}

        <mwc-button
          no-attention
          slot="primaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
      </mwc-dialog>
    `}firstUpdated(o){super.firstUpdated(o),d(this.configuration).then((o=>{this._apiKey=o}))}_copyApiKey(){p(this._apiKey),this._showCopied=!0,setTimeout((()=>this._showCopied=!1),2e3)}_editConfig(){l(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};r.styles=[o,i`
      .key {
        position: relative;
        display: flex;
        align-items: center;
      }
      code {
        word-break: break-all;
      }
      .key mwc-button {
        margin-left: 16px;
      }
      .copied {
        font-weight: bold;
        color: var(--alert-success-color);

        position: absolute;
        background-color: var(--mdc-theme-surface, #fff);
        padding: 10px;
        right: 0;
        font-size: 1.2em;
      }
    `],e([t()],r.prototype,"configuration",void 0),e([s()],r.prototype,"_apiKey",void 0),e([s()],r.prototype,"_showCopied",void 0),r=e([a("esphome-show-api-key-dialog")],r);
