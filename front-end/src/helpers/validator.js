import { defineRule } from "vee-validate";
// import { required, double, integer } from "vee-validate/dist/rules";

defineRule("required", (value) => {
  if (!value || !value.length) {
    return "This field is required";
  }
  return true;
});
defineRule("minLength", (value, [limit]) => {
  if (!value || !value.length) {
    return true;
  }
  if (value.length < limit) {
    return `This field must be at least ${limit} characters`;
  }
  return true;
});

// extend('required', {
//   ...required,
//   message: 'This field is required.'
// });

// extend('double', {
//   ...double,
//   message: 'This field must be a decimal number.'
// });

// extend('integer', {
//   ...integer,
//   message: 'This field must be an integer number.'
// })

// extend("stringMinAndMaxLength", {
//   params: ["min", "max"],
//   validate: (name, { min, max }) => {
//     var obj = String(name);
//     var n = obj.length;

//     if (n <= max && n >= min) {
//       return true;
//     } else {
//       return false;
//     }
//   },
//   message: 'This field must be be between {min} to {max} in length.'
// });