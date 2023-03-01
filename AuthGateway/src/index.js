const app = require("./app.js");

const PORT = process.env.PORT || 9091;
app.listen(PORT, () => {
  console.log(`Authentication Gateway is running on port ${PORT}.`);
});