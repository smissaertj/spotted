import {
  Form as VeeForm,
  Field as VeeField,
  defineRule,
  ErrorMessage,
  configure,
} from "vee-validate";

import { required, email, confirmed, min } from "@vee-validate/rules";

export default {
  install(app) {
    app.component("VeeForm", VeeForm);
    app.component("VeeField", VeeField);
    app.component("ErrorMessage", ErrorMessage);

    defineRule("required", required);
    defineRule("email", email);
    defineRule("confirmed", confirmed);
    defineRule("min", min);

    configure({
      generateMessage: (ctx) => {
        const messages = {
          required: `This field is required.`,
          email: `Must be a valid ${ctx.field}.`,
          confirmed: "Passwords do not match.",
          min: "Passwords should be at least 6 characters.",
        };

        const message = messages[ctx.rule.name]
          ? messages[ctx.rule.name]
          : `The field is invalid.`;

        return message;
      },
      validateOnBlur: true,
      validateOnChange: true,
      validateOnInput: false,
      validateOnModelUpdate: true,
    });
  },
};
