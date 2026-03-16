export const startSession = (token: string) => {
    localStorage.setItem('token', token);
}

export const stopSession = () => {
    localStorage.removeItem('token');
}

export const hasSession = () => {
    return localStorage.getItem('token') !== null;
}