import { useEffect, useState } from 'react';
import './App.css';
import { NextUIProvider, createTheme } from '@nextui-org/react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

import { getSlides, getStatus } from './utils/ScreenAPI';
import { ScreenStatus } from './utils/interfaces';
import { SetSlide } from './components/SetSlide';
// 2. Call `createTheme` and pass your custom values
const lightTheme = createTheme({
  type: 'light'

})

const darkTheme = createTheme({
  type: 'dark'

})
function App() {

  const [status, setStatus] = useState<ScreenStatus>();
  const [slides, setSlides] = useState<string[]>([]);

  async function updateStatus(){
      setStatus(await getStatus());
  }


  useEffect(() => {
    let updateSlides = async () => {
      setSlides(await getSlides());
    }

      updateStatus();
      updateSlides();
  }, []);

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
    <SetSlide allSlides={slides} currentSlide={status?.slide}/>
    </div>
  </NextUIProvider>
</NextThemesProvider>

  );
}

export default App;
 