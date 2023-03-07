const supertest = require("supertest");
const app = require("../src/app");
const pjson = require('../package.json');

describe('Default Endpoints', () => {
  it("GET /api", async () => {
    const response = await supertest(app).get("/api");

    expect(response.statusCode).toEqual(200);
    expect(response.body.message).toBe(`Authentication Gateway Service (V ${pjson.version}).`);
  });
});