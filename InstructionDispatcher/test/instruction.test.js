const supertest = require("supertest");
const app = require("../src/app");
const GLOBAL = require("../src/global.js");

describe('POST /instruction', () => {
  beforeAll(() => {
    GLOBAL.addValueToList(1, "pumping");
  });

  it("Invalid instruction.", async () => {
    const obj = {
        actuatorId: "3",
        instruction: "dancing",
    }

    const response = await supertest(app).post("/api/instruction").send(obj);

    expect(response.statusCode).toEqual(400);
  });

  it("Missing key from the body (actuatorId).", async () => {
    const obj = {
        instruction: "watering",
    }

    const response = await supertest(app).post("/api/instruction").send(obj);

    expect(response.statusCode).toEqual(400);
  });

  it("Client does not connected yet.", async () => {
    const obj = {
      actuatorId: "3",
      instruction: "watering",
    }

    const response = await supertest(app).post("/api/instruction").send(obj);

    expect(response.statusCode).toEqual(500);
  });

  it("Client connected.", async () => {
    const obj = {
      actuatorId: "1",
      instruction: "watering",
    }

    const response = await supertest(app).post("/api/instruction").send(obj);

    expect(response.statusCode).toEqual(200);
  });
});