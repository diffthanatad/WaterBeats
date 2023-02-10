const GLOBAL = require("../src/global.js");
var CLIENTS = GLOBAL.clients;

describe('addValueToList(key, value)', () => {
    it("No key provided.", () => {
        GLOBAL.addValueToList(null, "pumping");
        
        expect(Object.keys(CLIENTS).length === 0).toBe(true);
    });

    it("No value provided.", () => {
        const key = 1;

        GLOBAL.addValueToList(key, null);
        
        expect(Object.keys(CLIENTS).length === 1).toBe(true);
        expect(CLIENTS[key].length).toEqual(0);
    });

    it("Valid parameters.", () => {
        const key = 1;

        GLOBAL.addValueToList(1, "watering");
        
        expect(Object.keys(CLIENTS).length === 1).toBe(true);
        expect(CLIENTS[key][0]).toEqual("watering");
    });

    afterAll(() => {
        GLOBAL.resetClients();
    });
});

describe('connectionExist(key)', () => {
    beforeAll(() => {
        GLOBAL.addValueToList(1, "pumping");
    });

    it("No key provided.", () => {
        const response = GLOBAL.connectionExist(null);
        
        expect(response).toBe(false);
    });

    it("Key provided, but does not exist.", () => {
        const response = GLOBAL.connectionExist(2);
        
        expect(response).toBe(false);
    });

    it("Key provided and existed.", () => {
        const response = GLOBAL.connectionExist(1);
        
        expect(response).toBe(true);
    });

    afterAll(() => {
        GLOBAL.resetClients();
    });
});

describe('getFirstValue(key)', () => {
    beforeAll(() => {
        GLOBAL.addValueToList(1, "pumping");
    });

    it("No key provided.", () => {
        const response = GLOBAL.getFirstValue(null);
        
        expect(response).toEqual(null);
    });

    it("Key provided, but does not exist.", () => {
        const response = GLOBAL.getFirstValue(2);
        
        expect(response).toEqual(null);
    });

    it("Key provided and existed.", () => {
        const response = GLOBAL.getFirstValue(1);
        
        expect(response).toEqual("pumping");
    });

    afterAll(() => {
        GLOBAL.resetClients();
    });
});

describe('connectionExist(key)', () => {
    beforeAll(() => {
        GLOBAL.addValueToList(1, "pumping");
    });

    it("No key provided.", () => {
        const response = GLOBAL.connectionExist(null);
        
        expect(response).toBe(false);
    });

    it("Key provided, but does not exist.", () => {
        const response = GLOBAL.connectionExist(2);
        
        expect(response).toBe(false);
    });

    it("Key provided and existed.", () => {
        const response = GLOBAL.connectionExist(1);
        
        expect(response).toBe(true);
    });

    afterAll(() => {
        GLOBAL.resetClients();
    });
});

describe('removeAndReturnFirstValue(key)', () => {
    beforeAll(() => {
        GLOBAL.addValueToList(1, "pumping");
    });

    it("No key provided.", () => {
        const response = GLOBAL.removeAndReturnFirstValue(null);
        
        expect(response).toEqual(null);
    });

    it("Key provided, but does not exist.", () => {
        const response = GLOBAL.removeAndReturnFirstValue(2);
        
        expect(response).toEqual(null);
    });

    it("Key provided and existed.", () => {
        const response = GLOBAL.removeAndReturnFirstValue(1);
        
        expect(response).toEqual("pumping");
    });

    afterAll(() => {
        GLOBAL.resetClients();
    });
});

describe('removeKey(key)', () => {
    beforeAll(() => {
        GLOBAL.addValueToList(1, "pumping");
    });

    it("No key provided.", () => {
        GLOBAL.removeKey(null);
        
        expect(Object.keys(CLIENTS).length === 1).toBe(true);
    });

    it("Key provided, but does not exist.", () => {
        GLOBAL.removeKey(2);
        
        expect(Object.keys(CLIENTS).length === 1).toBe(true);
    });

    it("Key provided and existed.", () => {
        GLOBAL.removeKey(1);
        
        expect(Object.keys(CLIENTS).length === 0).toBe(true);
    });

    afterAll(() => {
        GLOBAL.resetClients();
    });
});