import{b as e,d as t,n as o,s as a,y as i,I as n,h as l,r as s}from"./index-91e6f5fe.js";import"./c.399eda54.js";let r=class extends a{render(){return i`
      <mwc-dialog
        .heading=${`Delete ${this.name}`}
        @closed=${this._handleClose}
        open
      >
        <div>Are you sure you want to delete ${this.name}?</div>
        <mwc-button
          slot="primaryAction"
          class="warning"
          label="Delete"
          dialogAction="close"
          @click=${this._handleDelete}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          no-attention
          label="Cancel"
          dialogAction="cancel"
        ></mwc-button>
      </mwc-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}async _handleDelete(){await n(this.configuration),l(this,"deleted")}static get styles(){return s`
      .warning {
        --mdc-theme-primary: var(--alert-error-color);
      }
    `}};e([t()],r.prototype,"name",void 0),e([t()],r.prototype,"configuration",void 0),r=e([o("esphome-delete-device-dialog")],r);
