import{b as o,d as t,p as e,n as s,s as i,y as r,$ as a}from"./index-91e6f5fe.js";import"./c.29b5e666.js";import{o as c}from"./c.284caccc.js";import"./c.399eda54.js";import"./c.25060a53.js";import"./c.dcb63c24.js";let n=class extends i{render(){return r`
      <esphome-process-dialog
        always-show-close
        .heading=${`Logs ${this.configuration}`}
        .type=${"logs"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":r`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){c(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],n.prototype,"configuration",void 0),o([t()],n.prototype,"target",void 0),o([e()],n.prototype,"_result",void 0),n=o([s("esphome-logs-dialog")],n);
