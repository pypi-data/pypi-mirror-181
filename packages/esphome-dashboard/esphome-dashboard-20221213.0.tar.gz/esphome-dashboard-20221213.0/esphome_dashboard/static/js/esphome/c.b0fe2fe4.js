import{b as t,p as s,n as e,s as i,y as a,f as o,r}from"./index-91e6f5fe.js";import"./c.399eda54.js";let l=class extends i{async showDialog(t,s){this._params=t,this._resolve=s}render(){return this._params?a`
      <mwc-dialog
        .heading=${this._params.title||""}
        @closed=${this._handleClose}
        open
      >
        ${this._params.text?a`<div>${this._params.text}</div>`:""}
        <mwc-button
          slot="secondaryAction"
          no-attention
          .label=${this._params.dismissText||"Cancel"}
          dialogAction="dismiss"
        ></mwc-button>
        <mwc-button
          slot="primaryAction"
          .label=${this._params.confirmText||"Yes"}
          class=${o({destructive:this._params.destructive||!1})}
          dialogAction="confirm"
        ></mwc-button>
      </mwc-dialog>
    `:a``}_handleClose(t){this._resolve("confirm"===t.detail.action),this.parentNode.removeChild(this)}static get styles(){return r`
      .destructive {
        --mdc-theme-primary: var(--alert-error-color);
      }
    `}};t([s()],l.prototype,"_params",void 0),t([s()],l.prototype,"_resolve",void 0),l=t([e("esphome-confirmation-dialog")],l);
