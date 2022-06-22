import { useEffect, useState } from "react";
import { NextUIProvider, createTheme } from "@nextui-org/react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import "./App.css";

import { getSlides, getStatus } from "./utils/ScreenAPI";
import { ScreenStatus } from "./utils/interfaces";
import { SetSlide } from "./components/SetSlide";
// 2. Call `createTheme` and pass your custom values
const lightTheme = createTheme({
  type: "light",
});

const darkTheme = createTheme({
  type: "dark",
  theme: {
    fonts: {
      sans: "'Press Start 2P', cursive;",
      cursive: "'Press Start 2P', cursive;",
    },
  },
});
function App() {
  const [status, setStatus] = useState<ScreenStatus>();
  const [slides, setSlides] = useState<string[]>([]);

  async function init() {
    setStatus(await getStatus());
    setSlides(await getSlides());
  }

  useEffect(() => {
    init();
  }, []);

  return (
    <NextThemesProvider
      defaultTheme="dark"
      attribute="class"
      value={{
        light: lightTheme.className,
        dark: darkTheme.className,
      }}
    >
      <NextUIProvider>
        <div className="h-screen flex items-center flex-col">
          <div id="app-wrapper" className="mt-5">
            <SetSlide
              getStatus={async () => setStatus(await getStatus())}
              allSlides={slides}
              currentSlide={status?.slide}
            />
          </div>
        </div>
      </NextUIProvider>
    </NextThemesProvider>
  );
}

export default App;
