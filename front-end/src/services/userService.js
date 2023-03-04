import httpClient from './httpClient';

const END_POINT = '/api/user';

const signIn = (obj) => httpClient.post('/api/auth/signin', obj);

const signUp = (obj) => httpClient.post('/api/auth/signup', obj);

const deleteUser = (id) => httpClient.delete(`${END_POINT}/${id}`);

const updateUserByAdmin = (obj) => httpClient.put(`${END_POINT}/info`, obj);

const updateUserByUser = (obj) => httpClient.put(`${END_POINT}/personal`, obj);

const changePassword = (obj) => httpClient.put(`${END_POINT}/password`, obj);

const getAllUsersWithPagination = (username="", page=0, size=10) => httpClient.get(END_POINT + `/pagination?username=${username}&page=${page}&size=${size}`);

const getSingleUser = (username="") => httpClient.get(END_POINT + `/single/${username}`);

export {
    signIn,
    signUp,
    deleteUser,
    updateUserByAdmin,
    updateUserByUser,
    changePassword,
    getAllUsersWithPagination,
    getSingleUser,
}