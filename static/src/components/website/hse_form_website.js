/** @odoo-module **/

import { Component , useState, useRef, onMounted, onWillUnmount, xml} from "@odoo/owl";
import { registry } from "@web/core/registry"
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { _t } from "@web/core/l10n/translation";
import { browser } from "@web/core/browser/browser";
import { useService } from "@web/core/utils/hooks";
import { usePopover } from "@web/core/popover/popover_hook";
import { Tooltip } from "@web/core/tooltip/tooltip";
import { rpc } from "@web/core/network/rpc";
import { session } from "@web/session";
    import {ReCaptcha} from "@google_recaptcha/js/recaptcha";


export class SdHseFormsWebsite extends Component {
    static template = "sd_hse_forms.website_form_template";
    static props = {};
    static components = { Dropdown, DropdownItem };
    setup(){
        this.state = useState({uu_id: 0})
        this.form = useRef('hse_form')
        this.sendButton = useRef('send_button')
        this.hse_checkboxes = useRef('hse_checkboxes')
        this.form_result = useRef('form_result')
        this._recaptcha = new ReCaptcha();
        console.log('this', session)
        onMounted( () => {
//            this.getGeoData()
            this.sendButtonListener = this.sendButton.el.addEventListener('click', async (e) => {
                e.preventDefault();
                this.form_result.el.innerHTML = ''
                const inputs = this.form.el.querySelectorAll('.website_form_input')
                const checkboxs = this.form.el.querySelectorAll('.website_form_checkbox')
                const data = {};
//                data[si] = session
                let notCompletedForm = false;
                let hseCheckbox = false;
                let requiredEmpty = []
                inputs.forEach(input => {
                    input.classList.remove('sd-border-danger')
                    if (input.required && input.value.length < 6){
                        input.classList.add('sd-border-danger')
                        notCompletedForm = true
                    }
                    data[input.name] = {value: input.value, required: input.required};

                });
                checkboxs.forEach(checkbox => {
                    checkbox.classList.remove('sd-border-danger')
                    if (checkbox.required && !checkbox.checked){
                        checkbox.classList.add('sd-border-danger')
                        notCompletedForm = true
                    }
                    checkbox.checked ? hseCheckbox = true : ''
                    data[checkbox.name] = {value: checkbox.checked, required: checkbox.required}
                });
                this.hse_checkboxes.el.classList.remove('sd-border-danger')
                if (!hseCheckbox){
                    this.hse_checkboxes.el.classList.add('sd-border-danger')
                    notCompletedForm = true

                }

                if(!notCompletedForm){
                    let res = await this.setRecord(data);
                    console.log('res:', res)
                    if (!res){
                         this.form_result.el.innerHTML = `<p class="text-danger" > Reload page</p>`

                    }else{
//                        this.form.el.reset()
//                        document.location.reload()
                        let submitButton = document.createElement('input')
                        submitButton.type = 'submit'
                        submitButton.classList = 'd-none'
//                        link.href = `/sdhseformsent/${data.uu_id.value}`
//                        this.form_result.el.innerHTML = `<p class="text-success" > Sent</p>`
                        this.form.el.appendChild(submitButton).click()
                    }


                }else{
                    this.form_result.el.innerHTML = `<p class="text-danger" > * Required</p>`

                }
            });
        })
        this.setRecord = this.setRecord.bind(this)
    }
    async setRecord(data){

        let res = await rpc('/sdhseformsdata', data)
        return res
    }
    getGeoData(){
                        console.log('location 1:' )

        navigator.geolocation.getCurrentPosition(
            ({coords: {latitude, longitude}}) => {
                    console.log('location 2:', coords )
            },
            err => {
                    console.log('location 3:', err )

            })
    }

    }

registry.category("public_components").add("sd_hse_forms.website_form_component", SdHseFormsWebsite);