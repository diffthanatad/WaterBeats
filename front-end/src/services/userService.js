import httpClient from './httpClient';

const END_POINT = '/user';

const logIn = (obj) => httpClient.post(`${END_POINT}/login`, obj);

const deleteUser = (id) => httpClient.delete(`${END_POINT}?id=${id}`);

const updateUser = (obj) => httpClient.put(`${END_POINT}`, obj);

const getAllUsersWithPagination = (username="", page=0) => httpClient.get(END_POINT + `?username=${username}&page=${page}`);

const createUser = (obj) => httpClient.post(`${END_POINT}`, obj);

export {
    logIn,
    deleteUser,
    updateUser,
    getAllUsersWithPagination,
    createUser,
}