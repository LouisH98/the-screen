import { useState } from 'react';
import './App.css';
import { Button, NextUIProvider, createTheme } from '@nextui-org/react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

import { getStatus } from './utils/ScreenAPI';
// 2. Call `createTheme` and pass your custom values
const lightTheme = createTheme({
  type: 'light'

})

const darkTheme = createTheme({
  type: 'dark'

})
function App() {
  const [count, setCount] = useState(0);
  return (
    <NextThemesProvider
    defaultTheme="dark"
    attribute="class"
    value={{
      light: lightTheme.className,
      dark: darkTheme.className
    }}
  >
  <NextUIProvider>
    <div className="h-screen">
    <Button onClick={getStatus}>Status</Button>

    </div>
  </NextUIProvider>
</NextThemesProvider>

  );
}

export default App;
 