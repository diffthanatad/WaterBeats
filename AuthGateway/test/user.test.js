const supertest = require("supertest");
const app = require("../src/app");

var token;

describe('User GET /user/single/:username endpoint', () => {
    beforeAll(async () => {
        const obj = {
            username: "alice-m",
            password: "12345678"
        }

        const response = await supertest(app).post("/api/auth/signin").send(obj);
        token = response.body.accessToken;
    });

    it("User exist.", async () => {
        const username = "alice-m";

        const response = await supertest(app).get(`/api/user/single/${username}`).set('Authorization', `Bearer ${token}`).send();

        expect(response.statusCode).toEqual(200);
        expect(response.body.name).toBeDefined();
        expect(response.body.username).toBeDefined();
        expect(response.body.role).toBeDefined();
    });

    it("User does not exist.", async () => {
        const username = "unknown-u";

        const response = await supertest(app).get(`/api/user/single/${username}`).set('Authorization', `Bearer ${token}`).send();

        expect(response.statusCode).toEqual(204);
    });
});

describe('User GET /user/pagination endpoint', () => {
    beforeAll(async () => {
        const obj = {
            username: "david-b",
            password: "12345678"
        }

        const response = await supertest(app).post("/api/auth/signin").send(obj);
        token = response.body.accessToken;
    });

    it("User exist.", async () => {
        let page = 0;
        let size = 10;
        let username = "d";

        const response = await supertest(app).get(`/api/user/pagination?page=${page}&size=${size}&username=${username}`).set('Authorization', `Bearer ${token}`).send();

        expect(response.statusCode).toEqual(200);
        expect(response.body.totalItems).toBeDefined();
        expect(response.body.users).toBeDefined();
        expect(response.body.totalPages).toBeDefined();
        expect(response.body.currentPage).toBeDefined();
    });

    it("User does not exist.", async () => {
        let page = 0;
        let size = 10;
        let username = "z";

        const response = await supertest(app).get(`/api/user/pagination?page=${page}&size=${size}&username=${username}`).set('Authorization', `Bearer ${token}`).send();

        expect(response.statusCode).toEqual(204);
    });
});

describe('User PUT /user/info endpoint', () => {
    beforeAll(async () => {
        const obj = {
            username: "david-b",
            password: "12345678"
        }

        const response = await supertest(app).post("/api/auth/signin").send(obj);
        token = response.body.accessToken;
    });

    it("User exist.", async () => {
        const obj = {
            id: "2",
            name: "Daniel Smith",
            username: "daniel-s",
            role: "user",
            disable: "0",
        }

        const response = await supertest(app).put("/api/user/info").set('Authorization', `Bearer ${token}`).send(obj);

        expect(response.statusCode).toEqual(200);
    });

    it("No parameter provided.", async () => {
        const response = await supertest(app).put("/api/user/info").set('Authorization', `Bearer ${token}`).send();

        expect(response.statusCode).toEqual(400);
        expect(response.body.errors).toBeDefined();
    });
});

describe('User PUT /user/personal endpoint', () => {
    beforeAll(async () => {
        const obj = {
            username: "david-b",
            password: "12345678"
        }

        const response = await supertest(app).post("/api/auth/signin").send(obj);
        token = response.body.accessToken;
    });

    it("User exist.", async () => {
        const obj = {
            id: "2",
            name: "Daniel Smith",
            username: "daniel-s3",
        }

        const response = await supertest(app).put("/api/user/personal").set('Authorization', `Bearer ${token}`).send(obj);

        expect(response.statusCode).toEqual(200);
    });

    it("No parameter provided.", async () => {
        const response = await supertest(app).put("/api/user/personal").set('Authorization', `Bearer ${token}`).send();

        expect(response.statusCode).toEqual(400);
        expect(response.body.errors).toBeDefined();
    });
});

describe('User PUT /user/password endpoint', () => {
    beforeAll(async () => {
        const obj = {
            username: "david-b",
            password: "12345678"
        }

        const response = await supertest(app).post("/api/auth/signin").send(obj);
        token = response.body.accessToken;
    });

    it("Old password match.", async () => {
        const obj = {
            id: "2",
            oldPassword: "12345678",
            newPassword: "1",
        }

        const response = await supertest(app).put("/api/user/password").set('Authorization', `Bearer ${token}`).send(obj);

        expect(response.statusCode).toEqual(200);
    });

    it("Old password does not match.", async () => {
        const obj = {
            id: "2",
            oldPassword: "87654321",
            newPassword: "1",
        }

        const response = await supertest(app).put("/api/user/password").set('Authorization', `Bearer ${token}`).send(obj);

        expect(response.statusCode).toEqual(500);
        expect(response.body.message).toBe("Wrong password.");
    });

    it("No parameter provided.", async () => {
        const response = await supertest(app).put("/api/user/password").set('Authorization', `Bearer ${token}`).send();

        expect(response.statusCode).toEqual(400);
        expect(response.body.errors).toBeDefined();
    });

    it("User does not exist.", async () => {
        const obj = {
            id: "99",
            oldPassword: "87654321",
            newPassword: "1",
        }

        const response = await supertest(app).put("/api/user/password").set('Authorization', `Bearer ${token}`).send(obj);

        expect(response.statusCode).toEqual(500);
        expect(response.body.message).toBe("No user found.");
    });
});

describe('User DEL /user/:id endpoint', () => {
    beforeAll(async () => {
        const obj = {
            username: "david-b",
            password: "12345678"
        }

        const response = await supertest(app).post("/api/auth/signin").send(obj);
        token = response.body.accessToken;
    });

    it("User exist.", async () => {
        let id = 4

        const response = await supertest(app).del(`/api/user/${id}`).set('Authorization', `Bearer ${token}`).send();

        expect(response.statusCode).toEqual(200);
    });
});