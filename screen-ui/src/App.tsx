import { useEffect, useState } from "react";
import { NextUIProvider, createTheme } from "@nextui-org/react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import "./App.css";

import { getSlides, getStatus } from "./utils/ScreenAPI";
import { ScreenStatus } from "./utils/interfaces";
import { SetSlide } from "./components/SetSlide";

const theme = {
  fonts: {
    sans: "'Press Start 2P', cursive;",
    cursive: "'Press Start 2P', cursive;",
  },
};

const lightTheme = createTheme({
  type: "light",
  theme,
});

const darkTheme = createTheme({
  type: "dark",
  theme,
});
function App() {
  const [status, setStatus] = useState<ScreenStatus>();
  const [slides, setSlides] = useState<string[]>([]);

  async function init() {
    setStatus(await getStatus());
    setSlides(await getSlides());
  }

  const pollingID = setInterval(async () => {
    setStatus(await getStatus());
  }, 2000);

  useEffect(() => {
    init();

    return () => clearInterval(pollingID);
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
