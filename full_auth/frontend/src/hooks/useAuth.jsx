import { useState, createContext } from "react";

const AuthContext = createContext()

function useAuth() {
    const [user, setUser] = useState("");

    return (
        <AuthContext.Provider value={user}>
        </AuthContext.Provider>
    )
}