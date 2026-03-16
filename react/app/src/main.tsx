import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from '@emotion/react'
import { createTheme, CssBaseline } from '@mui/material'
import {RouterProvider} from "react-router-dom";
import {router} from "./routes/router.tsx";


const theme = createTheme()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline/>
    <RouterProvider router={router}/>
    </ThemeProvider>
  </StrictMode>,
)
