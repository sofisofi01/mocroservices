import axios from "axios";
import type {Token, UserLogin, UserRegister} from "./types.ts";

const API_URL = 'http://localhost:9001/auth/';

class UserService {
    async registerUser(userRegister: UserRegister): Promise<Token> {
        const response = await axios.post(`${API_URL}register`, userRegister);
        return response.data;
    }

    async loginUser(userLogin: UserLogin): Promise<Token> {
        const response = await axios.post(`${API_URL}login`, userLogin);
        return response.data;
    }
}

export default new UserService();