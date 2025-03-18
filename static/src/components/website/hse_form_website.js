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

export class SdHseFormsWebsite extends Component {
    static template = "sd_hse_forms.website_form_template";
    static props = {};
    static components = { Dropdown, DropdownItem };
    setup(){
        this.form = useRef('hse_form')
        this.form
    }

    }

registry.category("public_components").add("sd_hse_forms.website_form_component", SdHseFormsWebsite);