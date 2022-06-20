import { useState } from 'react';
import './App.css';
import { Button, NextUIProvider, createTheme, Card, Text } from '@nextui-org/react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

import { getStatus } from './utils/ScreenAPI';
import { ScreenStatus } from './utils/interfaces';
// 2. Call `createTheme` and pass your custom values
const lightTheme = createTheme({
  type: 'light'

})

const darkTheme = createTheme({
  type: 'dark'

})
function App() {

  const [status, setStatus] = useState<ScreenStatus>();

  async function updateStatus(){
    setStatus(await getStatus());
  }
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
    <div className="h-screen flex items-center justify-center flex-col">
    <Button onPress={updateStatus}>Status</Button>
    <Card>
      <Card.Body>
        <Text>{JSON.stringify(status)}</Text>
      </Card.Body>
    </Card>
    </div>
  </NextUIProvider>
</NextThemesProvider>

  );
}

export default App;
 