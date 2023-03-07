const supertest = require("supertest");
const app = require("../src/app");

var token;

describe('Authentication /signin endpoints', () => {
  it("POST /signin = Valid username and password.", async () => {
    const obj = {
      username: "david-b",
      password: "12345678"
    }

    const response = await supertest(app).post("/api/auth/signin").send(obj);

    expect(response.statusCode).toEqual(200);
    expect(response.body.name).toBeDefined();
    expect(response.body.username).toBeDefined();
    expect(response.body.role).toBeDefined();
    expect(response.body.accessToken).toBeDefined();
  });

  it("POST /signin = Username does not exist.", async () => {
    const obj = {
      username: "unknown",
      password: "12345678"
    }

    const response = await supertest(app).post("/api/auth/signin").send(obj);

    expect(response.statusCode).toEqual(500);
    expect(response.body.message).toBe("No user found.");
  });

  it("POST /signin = Invalid password.", async () => {
    const obj = {
      username: "david-b",
      password: "1"
    }

    const response = await supertest(app).post("/api/auth/signin").send(obj);

    expect(response.statusCode).toEqual(500);
    expect(response.body.message).toBe("Wrong password.");
  });

  it("POST /signin = Neither username nor password is provided.", async () => {
    const response = await supertest(app).post("/api/auth/signin");

    expect(response.statusCode).toEqual(400);
    expect(response.body.errors).toBeDefined();
  });

  it("POST /signin = User is disabled.", async () => {
    const obj = {
      username: "bob-s",
      password: "12345678"
    }

    const response = await supertest(app).post("/api/auth/signin").send(obj);

    expect(response.statusCode).toEqual(500);
    expect(response.body.message).toBe("Disabled, contact admin.");
  });
});

describe('Authentication /signup endpoints', () => {
  beforeAll(async () => {
    const obj = {
      username: "david-b",
      password: "12345678"
    }

    const response = await supertest(app).post("/api/auth/signin").send(obj);
    token = response.body.accessToken;
  });

  it("POST /signup = Valid username, password and role.", async () => {
    const obj = {
      name: "John Carbon",
      username: "john-c",
      password: "12345678",
      role: "user"
    }

    const response = await supertest(app).post("/api/auth/signup").set('Authorization', `Bearer ${token}`).send(obj);

    expect(response.statusCode).toEqual(201);
  });

  it("POST /signup = No parameters are provided.", async () => {
    const response = await supertest(app).post("/api/auth/signup").set('Authorization', `Bearer ${token}`).send();

    expect(response.statusCode).toEqual(400);
    expect(response.body.errors).toBeDefined();
  });

  it("POST /signup = Duplicate username.", async () => {
    const obj = {
      name: "John Carbon",
      username: "john-c",
      password: "12345678",
      role: "user"
    }

    const response = await supertest(app).post("/api/auth/signup").set('Authorization', `Bearer ${token}`).send(obj);

    expect(response.statusCode).toEqual(500);
  });

  it("POST /signup = Provided role do not exist.", async () => {
    const obj = {
      name: "Adam Green",
      username: "adam-g",
      password: "12345678",
      role: "teacher"
    }

    const response = await supertest(app).post("/api/auth/signup").set('Authorization', `Bearer ${token}`).send(obj);

    expect(response.statusCode).toEqual(400);
    expect(response.body.errors).toBeDefined();
  });

  it("POST /signup = No token provided.", async () => {
    const obj = {
      name: "Adam Green",
      username: "adam-g",
      password: "12345678",
      role: "teacher"
    }

    const response = await supertest(app).post("/api/auth/signup").send(obj);

    expect(response.statusCode).toEqual(401);
    expect(response.body.message).toBe("No token provided.");
  });

  it("POST /signup = Invalid token.", async () => {
    const obj = {
      name: "Adam Green",
      username: "adam-g",
      password: "12345678",
      role: "teacher"
    }

    const response = await supertest(app).post("/api/auth/signup").set('Authorization', `Bearer jijiefeuhuafe`).send(obj);

    expect(response.statusCode).toEqual(401);
    expect(response.body.message).toBe("Unauthorized, invalid token.");
  });

  it("POST /signup = Role admin is required.", async () => {
    const signInUser = {
      username: "alice-m",
      password: "12345678"
    }

    const signInResponse = await supertest(app).post("/api/auth/signin").send(signInUser);
    const userToken = signInResponse.body.accessToken;

    const newUser = {
      name: "Adam Green",
      username: "adam-g",
      password: "12345678",
      role: "teacher"
    }

    const response = await supertest(app).post("/api/auth/signup").set('Authorization', `Bearer ${userToken}`).send(newUser);

    expect(response.statusCode).toEqual(403);
  });
});