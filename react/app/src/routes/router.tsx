import {createBrowserRouter} from "react-router-dom";
import App from "../App.tsx";
import {Expenses} from "../containers/Expenses/Expenses.tsx";
import {ExpensesForm} from "../containers/ExpensesForm/ExpensesForm.tsx";
import {AuthForm} from "../containers/AuthForm/AuthForm.tsx";


export const router = createBrowserRouter([
    {
        path: '/',
        element: <App/>,
        children: [
            {
                index: true,
                element: <AuthForm/>
            },
            {
                path: 'register',
                element: <AuthForm />
            },
            {
                path: 'expenseslist',
                children: [
                    {
                       index: true,
                       element: <Expenses/>
                    },
                    {
                        path: 'create',
                        element: <ExpensesForm/>
                    },
                    {
                        path: ':id/change',
                        element: <ExpensesForm/>
                    }
                ]

            }
        ]
    }
])